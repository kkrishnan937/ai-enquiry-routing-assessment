"""Development-only diagnostics. Never described as unseen accuracy."""
import datetime as dt
import hashlib
import json
from pathlib import Path
from keyword_baseline import classify, VERSION

root = Path(__file__).resolve().parents[2]
source = root / "data/classification-development.json"
dataset = json.loads(source.read_text(encoding="utf-8"))
assert dataset["split"] == "development"
rows = []
for example in dataset["examples"]:
    prediction = classify(example["text"])
    correct = (prediction["type"] == example["expected_type"] and
               prediction["review_required"] == example["review_required"])
    rows.append({"id": example["id"], "text": example["text"],
                 "expected_type": example["expected_type"], "expected_review": example["review_required"],
                 "review_group": example["review_group"], "prediction": prediction, "matches_expected": correct})
clear = [r for r in rows if not r["expected_review"]]
review = [r for r in rows if r["expected_review"]]
classified = [r for r in clear if not r["prediction"]["review_required"]]
stamp = dt.datetime.now(dt.timezone.utc)
destination = root / "results/classification" / ("development-" + stamp.strftime("%Y%m%dT%H%M%S%fZ"))
destination.mkdir(parents=True)
summary = {"total": len(rows), "matching_outcomes": sum(r["matches_expected"] for r in rows),
           "classifiable_total": len(clear), "correct_automatic_classifications": sum(r["matches_expected"] for r in clear),
           "classifiable_receiving_type": len(classified), "review_expected_total": len(review),
           "correct_review_flags": sum(r["matches_expected"] for r in review),
           "forced_types_on_review_cases": sum(not r["prediction"]["review_required"] for r in review)}
report = {"executed_utc": stamp.isoformat(), "scope": "development only; not held-out performance", "baseline_version": VERSION,
          "dataset_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
          "baseline_sha256": hashlib.sha256(Path(__file__).with_name("keyword_baseline.py").read_bytes()).hexdigest(),
          "summary": summary, "predictions": rows}
(destination / "predictions.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
lines = ["# Keyword baseline — development diagnostics", "", "These are development results, not unseen evaluation or operational performance.",
         "", f"Executed UTC: {stamp.isoformat()}", f"Baseline version: {VERSION}", "", "| Measure | Count |", "|---|---|"]
lines += [f"| {key} | {value} |" for key, value in summary.items()]
lines += ["", "## Disagreements", "", "| Example | Expected | Predicted |", "|---|---|---|"]
lines += [f'| {r["id"]} | {r["expected_type"] or "review"} | {r["prediction"]["type"] or "review"} |' for r in rows if not r["matches_expected"]]
lines += ["", "## Limits", "", "The rules use lexical matches, not full meaning. They do not handle negation, historical context or distinguish a separate request from contextual wording. Multiple matched types trigger review, and no match also triggers review. Error reasons must be inspected in the prediction file before changing rules. Rules were authored with development examples visible; these results are not independent validation. No held-out set or AI predictions exist yet."]
(destination / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(json.dumps(summary, indent=2))
print("Report:", destination / "report.md")
