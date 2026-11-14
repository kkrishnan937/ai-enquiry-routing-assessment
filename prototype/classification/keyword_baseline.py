"""Small transparent keyword baseline. Input: enquiry text only, never expected labels."""
import re

VERSION = "0.1"
PATTERNS = {
    "missed_collection": [
        r"\bmissed\b", r"\bpartial (?:pickup|collection)\b",
        r"\b(?:wasn't|was not|weren't|were not|not) (?:emptied|collected)\b",
        r"\b(?:pickup|collection) (?:never happened|didn't happen|did not happen)\b",
        r"\b(?:cart|bin|container)\b.{0,45}\b(?:still full|still has everything|untouched)\b",
    ],
    "reported_dumped_waste": [
        r"\bdump(?:ed|ing)\b", r"\babandon(?:ed|ing)\b",
        r"\b(?:unload(?:ed|ing)?|tipp(?:ed|ing))\b",
        r"\bsomeone left\b.{0,70}\b(?:bags|rubbish|waste)\b",
        r"\bemptied sacks\b",
    ],
    "other": [
        r"\brepair(?:ed)?\b", r"\b(?:broken|damaged|cracked)\b",
        r"\b(?:bill|billing|charge)\b",
        r"\b(?:when|what day)\b.{0,60}\b(?:pickup|collection)\b",
        r"\b(?:holiday|date changes|proper disposal)\b",
    ],
}


def classify(text):
    normalised = text.lower().replace("’", "'")
    matches = {label: [pattern for pattern in patterns if re.search(pattern, normalised)]
               for label, patterns in PATTERNS.items()}
    active = [label for label, hits in matches.items() if hits]
    return {"type": active[0] if len(active) == 1 else None,
            "review_required": len(active) != 1,
            "matched_patterns": {label: hits for label, hits in matches.items() if hits}}
