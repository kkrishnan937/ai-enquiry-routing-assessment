"""Render portfolio figures from the retained evaluation; does not rerun inference.
Requires matplotlib (optional, for figures only).
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
DATA = json.loads((ROOT / "results/classification/held-out-final/predictions.json").read_text(encoding="utf-8"))
OUT = ROOT / "docs/images"
OUT.mkdir(parents=True, exist_ok=True)
SUMMARY = DATA["summary"]
COLORS = ["#376485", "#c36b28"]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.spines.top": False, "axes.spines.right": False})

def save(fig, name):
    fig.savefig(OUT / (name + ".png"), dpi=160, facecolor="white")
    plt.close(fig)

fig, axes = plt.subplots(1, 3, figsize=(13, 5.5))
measures = [
    ("Clear enquiries classified correctly", "correct_automatic_classifications", "classifiable_total", "Higher is better"),
    ("Unclear / mixed cases sent for review", "correct_review_flags", "review_expected_total", "Higher is better"),
    ("Review cases given a forced type", "forced_types_on_review_cases", "review_expected_total", "Lower is better"),
]
for ax, (title, key, denominator, direction) in zip(axes, measures):
    for i, method in enumerate(["baseline", "ai"]):
        s = SUMMARY[method]
        value, total = s[key], s[denominator]
        pct = value / total * 100
        ax.bar(i, pct, color=COLORS[i], width=.6)
        ax.text(i, pct + 3, f"{value}/{total} ({pct:.1f}%)", ha="center", fontsize=11, weight="bold")
    ax.set_ylim(0, 108)
    ax.set_yticks([0, 25, 50, 75, 100], ["0%", "25%", "50%", "75%", "100%"])
    ax.set_xticks([0, 1], ["Keyword rules", "Qwen2.5 3B"])
    ax.set_title(title + "\n" + direction, fontsize=11, pad=16)
    ax.set_axisbelow(True)
    ax.grid(axis="y", alpha=.15)
fig.suptitle("Classification improved; review handling worsened", fontsize=19, weight="bold", y=.98)
fig.text(.5, .07, "38 synthetic evaluation examples | Same inputs for both methods | One frozen run", ha="center", fontsize=11)
fig.text(.5, .025, "The model did not meet the agreed review safeguard. These results do not establish operational performance.", ha="center", fontsize=10, color="#444444")
fig.subplots_adjust(left=.055, right=.985, bottom=.22, top=.76, wspace=.3)
save(fig, "classification-comparison")

fig, ax = plt.subplots(figsize=(11, 6))
subsets = [("Missed collection", "per_type", "missed_collection", "correct"), ("Reported dumped waste", "per_type", "reported_dumped_waste", "correct"), ("Other", "per_type", "other", "correct"), ("Unclear: review required", "review_subsets", "unclear", "correct_flags"), ("Mixed: review required", "review_subsets", "mixed", "correct_flags")]
for i, method in enumerate(["baseline", "ai"]):
    vals = [SUMMARY[method][group][key] for _, group, key, _ in subsets]
    rates = [v[field] / v["total"] * 100 for v, (_, _, _, field) in zip(vals, subsets)]
    y = [j + (i - .5) * .34 for j in range(len(subsets))]
    ax.barh(y, rates, height=.3, color=COLORS[i], label=["Keyword rules", "Qwen2.5 3B"][i])
    for yy, rate, v, (_, _, _, field) in zip(y, rates, vals, subsets):
        ax.text(rate + 1.5, yy, f"{v[field]}/{v['total']}", va="center", fontsize=11)
ax.set_yticks(range(len(subsets)), [x[0] for x in subsets])
ax.invert_yaxis()
ax.set_xlim(0, 117)
ax.set_xticks([0, 25, 50, 75, 100], ["0%", "25%", "50%", "75%", "100%"])
ax.set_xlabel("Correct outcome within each subset (higher is better)")
ax.grid(axis="x", alpha=.15)
ax.set_axisbelow(True)
ax.legend(loc="lower right", frameon=False)
fig.suptitle("Where each method succeeded", fontsize=19, weight="bold", y=.97)
fig.text(.5, .025, "Small synthetic subsets; counts shown beside bars. No independent service-owner validation.", ha="center", fontsize=10, color="#444444")
fig.subplots_adjust(left=.28, right=.94, top=.85, bottom=.15)
save(fig, "classification-by-type")
