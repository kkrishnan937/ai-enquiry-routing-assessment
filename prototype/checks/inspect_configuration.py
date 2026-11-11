"""Inspect the local practice configuration; does not test a running system."""
import json
from pathlib import Path
from datetime import datetime, timezone
import hashlib

root = Path(__file__).resolve().parents[2]
source = root / "prototype/config/enquiry-statuses.json"
raw = source.read_bytes()
config = json.loads(raw.decode("utf-8-sig"))
checks = {
    "awaiting status declared": "Awaiting Information" in config["statuses"],
    "all transition endpoints declared": all(s in config["statuses"] and all(t in config["statuses"] for t in targets) for s, targets in config["transitions"].items()),
    "open can enter awaiting": "Awaiting Information" in config["transitions"]["Open"],
    "awaiting can return to open": "Open" in config["transitions"]["Awaiting Information"],
    "awaiting cannot directly close": "Closed" not in config["transitions"]["Awaiting Information"],
    "named representative retained": config["awaiting_information"]["retain_named_representative"] is True,
    "follow-up date required": config["awaiting_information"]["follow_up_date_required"] is True,
    "automatic closure disabled": config["awaiting_information"]["automatic_closure"] is False,
    "automatic reassignment disabled": config["awaiting_information"]["automatic_reassignment"] is False,
    "automatic timer disabled": config["awaiting_information"]["automatic_timer"] is False,
}
report = ["# Local configuration inspection", "", "Scope: authored practice configuration only. No running application, database, scheduler, or municipal system was tested.", "", f"Execution time (UTC): {datetime.now(timezone.utc).isoformat()}", f"Configuration SHA-256: {hashlib.sha256(raw).hexdigest()}", "", "| Check | Result |", "|---|---|"]
report += [f"| {name} | {'PASS' if passed else 'FAIL'} |" for name, passed in checks.items()]
report += ["", "These checks establish what the file declares and its consistency with the selected practice expectations. They do not prove that an application enforces these rules or that a business authority has approved them."]
(root / "results/local-configuration-inspection.md").write_text("\n".join(report) + "\n", encoding="utf-8")
print(f"{sum(checks.values())}/{len(checks)} local configuration checks passed.")
raise SystemExit(0 if all(checks.values()) else 1)