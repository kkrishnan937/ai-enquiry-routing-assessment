"""HTTP acceptance checks against an isolated running application, not file declarations."""
import datetime as dt
import hashlib
import http.cookiejar
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request

APP = Path(__file__).with_name("app.py")


class Client:
    def __init__(self, port):
        self.base = f"http://127.0.0.1:{port}"
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
        self.csrf = ""

    def request(self, path, data=None, method=None):
        request = urllib.request.Request(self.base + path,
                                        data=None if data is None else json.dumps(data).encode(),
                                        method=method or ("GET" if data is None else "POST"),
                                        headers={"Content-Type": "application/json", "X-CSRF-Token": self.csrf})
        try:
            response = self.opener.open(request, timeout=5)
        except urllib.error.HTTPError as exc:
            response = exc
        raw = response.read().decode()
        try:
            body = json.loads(raw)
        except ValueError:
            body = raw
        return response.code, body

    def login(self, name, password):
        code, result = self.request("/api/login", {"username": name, "password": password})
        if code != 200:
            raise AssertionError(f"Login failed: {code}")
        self.csrf = result["csrf"]
        return self


class Acceptance(unittest.TestCase):
    observations = []

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="enquiry-acceptance-")
        self.db = Path(self.temp.name) / "test.sqlite"
        subprocess.run([sys.executable, str(APP), "--db", str(self.db), "--init"], check=True, capture_output=True)
        self.passwords = json.loads((self.db.parent / "credentials.json").read_text())
        self.process = None
        self.addCleanup(self.cleanup)
        self.start()
        self.clients = {name: Client(self.port).login(name, password) for name, password in self.passwords.items()}

    def start(self, today="2026-11-11"):
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            self.port = sock.getsockname()[1]
        flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        self.process = subprocess.Popen([sys.executable, str(APP), "--db", str(self.db), "--port", str(self.port), "--test-today", today],
                                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=flags)
        for _ in range(100):
            try:
                urllib.request.build_opener(urllib.request.ProxyHandler({})).open(f"http://127.0.0.1:{self.port}/login", timeout=1).close()
                return
            except OSError:
                if self.process.poll() is not None:
                    raise RuntimeError("Application exited during startup")
                time.sleep(.05)
        raise RuntimeError("Application did not start")

    def restart(self, today="2026-11-11"):
        self.process.terminate()
        self.process.wait(timeout=5)
        self.start(today)
        self.clients = {name: Client(self.port).login(name, password) for name, password in self.passwords.items()}

    def cleanup(self):
        if self.process:
            self.process.terminate()
            self.process.wait(timeout=5)
        self.temp.cleanup()

    def call(self, who, path, data=None, method=None, expected=200):
        code, result = self.clients[who].request(path, data, method)
        self.assertEqual(code, expected, (path, result))
        return result

    def create(self, **changes):
        data = dict(received="2026-11-11T09:00:00-06:00", message="My garbage cart was not emptied.",
                    responsible="rep-a", missing="Collection address; missed collection date", last_action="Requested details",
                    next_action="Review resident reply", follow_up="2026-11-12")
        data.update(changes)
        return self.call("rep-a", "/api/enquiries", data, expected=201)

    def read(self, ref, who="rep-a"):
        return self.call(who, f"/api/enquiries/{ref}")

    def act(self, ref, action, data, who="rep-a", expected=200):
        return self.call(who, f"/api/enquiries/{ref}/{action}", data, expected=expected)

    def note(self, case, details):
        self.observations.append({"case": case, "observed": details})

    def test_F01_received_timestamp(self):
        value = '2026-11-12T10:00:00-06:00'
        record = self.create(received='\t  ' + value + '  \n')
        self.assertEqual(self.read(record['id'])['received'], value)
        base = dict(message='Timestamp negative check', responsible='rep-a', follow_up='2026-11-13')
        for received, expected_error in (('', 'Received time is required'),
                                         ('not-a-date', 'Received time must be a valid date and time'),
                                         ('2026-02-30T09:00:00-06:00', 'Received time must be a valid date and time'),
                                         ('2026-11-12T09:00:00', 'Received time must include its time zone'),
                                         (None, 'Received time is required')):
            before = self.call('rep-a', '/api/enquiries')
            response = self.call('rep-a', '/api/enquiries', base | {'received': received}, expected=400)
            self.assertTrue(response['error'].startswith(expected_error), response)
            self.assertEqual(before, self.call('rep-a', '/api/enquiries'))
        self.restart()
        self.assertEqual(self.read(record['id'])['received'], value)
        self.note('F-01', 'Leading/trailing whitespace accepted and trimmed; normalised timestamp persists across restart. Blank/non-text, malformed/impossible and offset-free values rejected with differentiated errors and no record creation.')

    def test_TC01(self):
        a = self.create()
        b = self.create(message="My recycling cart was not emptied.", received="2026-11-11T09:15:00-06:00",
                        missing="Missed collection date", follow_up="2026-11-13")
        self.assertNotEqual(a["id"], b["id"])
        for record, text in ((a, "Please provide the collection address for your garbage enquiry."),
                             (b, "Please confirm the missed collection date for your recycling enquiry.")):
            self.act(record["id"], "message", {"direction": "outgoing", "text": text})
        before = [self.read(r["id"]) for r in (a, b)]
        self.restart()
        for record, original in zip((a, b), before):
            matches = self.call("rep-a", "/api/enquiries?ref=" + record["id"])
            self.assertEqual([r["id"] for r in matches], [record["id"]])
            after = self.read(record["id"])
            for key in ("id", "received", "message", "messages"):
                self.assertEqual(original[key], after[key])
            self.assertEqual(len(after["messages"]), 2)
        self.assertNotEqual(before[0]["messages"], before[1]["messages"])
        code, screen = self.clients["rep-a"].request("/enquiries/" + a["id"])
        self.assertEqual(code, 200)
        self.assertIn("Correspondence", screen)
        self.note("TC-01", "Two references searched and retrieved after process restart using unchanged database; timestamps and both messages unchanged and separate. No email integration exists. Detail page returns HTML.")

    def test_TC02(self):
        ref = self.create()["id"]
        self.act(ref, "message", {"direction": "outgoing", "text": "Please provide the collection address and missed collection date."})
        self.act(ref, "message", {"direction": "incoming", "text": "The collection address is Test Property A."})
        self.act(ref, "update", dict(address="Test Property A", missing="Missed collection date", last_action="Recorded collection address", next_action="Request missed collection date"))
        r = self.read(ref)
        self.assertEqual((r["address"], r["missing"], r["responsible"], r["state"]), ("Test Property A", "Missed collection date", "rep-a", "Open"))
        self.assertEqual(r["last_action"], "Recorded collection address")
        self.assertEqual(r["next_action"], "Request missed collection date")
        self.assertEqual(len(r["messages"]), 3)
        event = next(e for e in r["history"] if e["field"] == "missing")
        self.assertEqual(event["actor"], "rep-a")
        self.assertTrue(event["timestamp"])
        self.assertEqual(json.loads(event["new_value"]), "Missed collection date")
        self.note("TC-02", "Address received; other missing detail retained; three messages preserved; actor/time history available; responsible rep unchanged and state remains Open. No referral integration exists.")

    def test_TC03(self):
        before = self.call("rep-a", "/api/enquiries")
        self.call("rep-a", "/api/enquiries", dict(message="Test", received="2026-11-11T09:00:00-06:00", follow_up="2026-11-12"), expected=400)
        self.assertEqual(before, self.call("rep-a", "/api/enquiries"))
        ref = self.create()["id"]
        self.act(ref, "message", {"direction": "outgoing", "text": "Please provide the address."})
        self.act(ref, "message", {"direction": "incoming", "text": "Test Property A"})
        self.act(ref, "update", {"address": "Test Property A", "missing": "Missed collection date"})
        self.act(ref, "cover", {"representative": "rep-b"}, "supervisor-a")
        r = self.read(ref)
        self.assertEqual((r["responsible"], r["cover"]), ("rep-a", "rep-b"))
        self.note("TC-03", "Ownerless creation rejected without persistence; requests, resident reply and cover preserve rep-a; rep-b stored separately as cover.")

    def test_TC04(self):
        for value in ("", "2026-02-30"):
            self.call("rep-a", "/api/enquiries", dict(message="Test", received="2026-11-11T09:00:00-06:00", responsible="rep-a", follow_up=value), expected=400)
        self.assertEqual(self.call("rep-a", "/api/enquiries"), [])
        ref = self.create()["id"]
        for value in ("", "2026-02-30"):
            self.act(ref, "update", {"follow_up": value}, expected=400)
            self.assertEqual(self.read(ref)["follow_up"], "2026-11-12")
        self.act(ref, "update", {"follow_up": "2026-11-13"})
        self.assertTrue(any(e["field"] == "follow_up" for e in self.read(ref)["history"]))
        self.restart("2026-11-14")
        r = self.read(ref)
        self.assertEqual((r["follow_up"], r["responsible"], r["state"], r["overdue"]), ("2026-11-13", "rep-a", "Open", True))
        self.note("TC-04", "Blank/impossible dates rejected on create and update; valid changed date persisted. Isolated clock advanced Nov11 to Nov14 through process restart; record remains Open, rep-a responsible, overdue true. No scheduler or timed jobs implemented; no indefinite behaviour guarantee.")

    def test_TC05(self):
        ref = self.create()["id"]
        self.act(ref, "cover", {"representative": "rep-b"}, "rep-b", expected=403)
        self.assertIsNone(self.read(ref)["cover"])
        self.act(ref, "cover", {"representative": "rep-b"}, "supervisor-a")
        self.assertEqual(len(self.read(ref, "rep-b")["messages"]), 1)
        self.act(ref, "update", {"next_action": "Follow up for collection address"}, "rep-b")
        self.assertEqual(self.read(ref, "rep-b")["next_action"], "Follow up for collection address")
        self.act(ref, "cover", {"representative": ""}, "supervisor-a")
        self.call("rep-b", f"/api/enquiries/{ref}", expected=403)
        self.call("rep-b", f"/enquiries/{ref}", expected=403)
        self.act(ref, "update", {"next_action": "UNAUTHORISED CHANGE"}, "rep-b", expected=403)
        r = self.read(ref)
        self.assertEqual(r["responsible"], "rep-a")
        self.assertEqual(r["next_action"], "Follow up for collection address")
        events = [e for e in r["history"] if e["field"] == "cover"]
        self.assertEqual(len(events), 2)
        self.assertTrue(all(e["actor"] == "supervisor-a" for e in events))
        self.note("TC-05", "Self-assignment denied; supervisor cover grants read/update; removal revokes same-session API and page access; stale update rejected; original responsibility retained and both cover events stored.")

    def test_TC06(self):
        ref = self.create()["id"]
        self.act(ref, "cover", {"representative": "rep-b"}, "supervisor-a")
        for who in ("rep-a", "rep-b", "supervisor-a"):
            self.read(ref, who)
            self.act(ref, "update", {"next_action": "Updated by " + who}, who)
        self.assertEqual(self.call("rep-c", "/api/enquiries"), [])
        self.assertEqual(self.call("rep-c", "/api/enquiries?ref=" + ref), [])
        for suffix in ("", "/messages", "/history"):
            self.call("rep-c", f"/api/enquiries/{ref}{suffix}", expected=403)
        self.act(ref, "update", {"next_action": "UNAUTHORISED CHANGE"}, "rep-c", expected=403)
        self.call("rep-c", "/api/logout", {})
        self.call("rep-c", f"/api/enquiries/{ref}", expected=401)
        self.act(ref, "update", {"next_action": "UNAUTHORISED CHANGE"}, "rep-c", expected=401)
        r = self.read(ref)
        self.assertEqual(r["next_action"], "Updated by supervisor-a")
        self.assertEqual({e["actor"] for e in r["history"] if e["field"] == "next_action"}, {"rep-a", "rep-b", "supervisor-a"})
        self.note("TC-06", "Responsible rep, named cover and supervisor can read/update. Unrelated rep cannot list/search/read messages/history or write; signed-out direct reads/writes return 401. Denied changes not persisted.")

    def test_TC07(self):
        start = dt.datetime.now(dt.timezone.utc)
        ref = self.create()["id"]
        self.act(ref, "update", {"missing": "", "address": "Test Property A", "follow_up": "2026-11-13"})
        self.act(ref, "cover", {"representative": "rep-b"}, "supervisor-a")
        for who in ("rep-a", "rep-b"):
            before = self.read(ref, who)["history"]
            for method in ("PATCH", "DELETE"):
                self.call(who, f"/api/enquiries/{ref}/history", {"actor": "altered"}, method, expected=405)
            self.act(ref, "history", {"actor": "altered"}, who, expected=405)
            self.assertEqual(before, self.read(ref, who)["history"])
        self.act(ref, "cover", {"representative": ""}, "supervisor-a")
        before_restart = self.read(ref)["history"]
        self.restart()
        self.assertEqual(before_restart, self.read(ref)["history"])
        self.act(ref, "transfer", {"representative": "rep-c", "reason": "Workload redistribution", "confirmed": True}, expected=403)
        for data in ({"representative": "rep-c", "confirmed": True}, {"representative": "rep-c", "reason": "Workload redistribution"}):
            self.act(ref, "transfer", data, "supervisor-a", expected=400)
            self.assertEqual(self.read(ref)["responsible"], "rep-a")
        self.act(ref, "transfer", {"representative": "rep-c", "reason": "Workload redistribution", "confirmed": True}, "supervisor-a")
        r = self.read(ref, "supervisor-a")
        transfer = next(e for e in r["history"] if e["field"] == "responsible")
        self.assertEqual((json.loads(transfer["old_value"]), json.loads(transfer["new_value"]), transfer["actor"], transfer["reason"]),
                         ("rep-a", "rep-c", "supervisor-a", "Workload redistribution"))
        for event in r["history"]:
            self.assertGreaterEqual(dt.datetime.fromisoformat(event["timestamp"]), start)
            self.assertLessEqual(dt.datetime.fromisoformat(event["timestamp"]), dt.datetime.now(dt.timezone.utc))
        self.assertEqual([json.loads(e["new_value"]) for e in r["history"] if e["field"] == "cover"], ["rep-b", None])
        self.assertTrue(any(e["field"] == "missing" and json.loads(e["new_value"]) == "" and e["actor"] == "rep-a" for e in r["history"]))
        self.restart()
        self.assertEqual(r["history"], self.read(ref, "supervisor-a")["history"])
        self.assertEqual(self.read(ref, "rep-c")["responsible"], "rep-c")
        self.call("rep-a", f"/api/enquiries/{ref}", expected=403)
        self.note("TC-07", "Field/cover events retain actor, old/new values and UTC timestamps. Ordinary-user history POST/PATCH/DELETE denied. History persists through two process restarts. Non-supervisor/incomplete transfers denied; complete supervisor transfer and reason retained; receiving rep gains access and former rep loses it.")


class Result(unittest.TextTestResult):
    outcomes = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.outcomes.append({"test": test.id().split(".")[-1], "outcome": "PASS"})

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.outcomes.append({"test": test.id().split(".")[-1], "outcome": "FAIL", "detail": self._exc_info_to_string(err, test)})

    def addError(self, test, err):
        super().addError(test, err)
        self.outcomes.append({"test": test.id().split(".")[-1], "outcome": "ERROR", "detail": self._exc_info_to_string(err, test)})


if __name__ == "__main__":
    stamp = dt.datetime.now(dt.timezone.utc)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Acceptance)
    result = unittest.TextTestRunner(verbosity=2, resultclass=Result).run(suite)
    directory = APP.parents[2] / "results" / "tracking-prototype" / stamp.strftime("%Y%m%dT%H%M%S%fZ")
    directory.mkdir(parents=True)
    report = {"run_id": directory.name, "executed_utc": stamp.isoformat(), "python": sys.version.split()[0],
              "application_sha256": hashlib.sha256(APP.read_bytes()).hexdigest(), "test_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "environment": "local subprocess HTTP server, isolated temporary SQLite database per case; authenticated sessions; controlled test date",
              "outcomes": Result.outcomes, "observations": Acceptance.observations,
              "limitations": ["HTTP automation; browser interaction and visual layout not assessed", "Synthetic data only; no municipal system or operational approval",
                              "No Azure Pipeline executed; tests ran locally", "No timed jobs implemented; overdue observation covers controlled date-boundary checks only"]}
    (directory / "results.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    rows = "\n".join(f'| {r["test"].replace("test_TC", "TC-")} | {r["outcome"]} |' for r in Result.outcomes)
    notes = "\n\n".join(f'### {o["case"]}\n\n{o["observed"]}' for o in Acceptance.observations)
    (directory / "report.md").write_text(f'# Tracking prototype — automated acceptance results\n\nRun: {directory.name}\nExecuted UTC: {stamp.isoformat()}\nPython: {report["python"]}\nApplication SHA-256: `{report["application_sha256"]}`\nTest SHA-256: `{report["test_sha256"]}`\n\nEnvironment: {report["environment"]}.\n\n| Case | Automated outcome |\n|---|---|\n{rows}\n\n{notes}\n\n## Limits\n\n' + "\n".join("- " + x for x in report["limitations"]) + '\n\nThese results cover implemented HTTP assertions, not completed manual sign-off of every test-case step. Temporary test databases and passwords were removed after execution. Failed-run details, if any, are retained in results.json.\n', encoding="utf-8")
    print(f"Evidence saved: {directory}")
    sys.exit(0 if result.wasSuccessful() else 1)
