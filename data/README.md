# Synthetic enquiry examples

This is a small starter set for BA review, not a representative sample of municipal demand or a model evaluation dataset. Enquiries are invented. Broadway Avenue and College Drive are Saskatoon street names; house numbers are explicit placeholders, not actual property addresses. Street-name reference: https://www.saskatoon.ca/sites/default/files/7200_1.pdf. These locations do not establish actual service incidents, property boundaries, or service eligibility. No dates, transfers, or durations establish actual operational performance.

Read `synthetic_enquiries.csv`; the JSON copy contains the same eight records for convenient inspection. Expected actions and answer wording are provisional. Blank receiving teams mean responsibility has not been established; do not fill them by guessing.

The missed-collection example uses the authored practice article, not a verified Saskatchewan municipal routing rule. Other examples explicitly identify missing sources. No reference answer has been approved by an actual municipality.

Review each example for clear wording, sufficient information, supported expected action, source limitations, and ambiguity. Keep unresolved labels visible. This small set is deliberately useful for discussion; its category balance does not reflect demand and must not be used to calculate real-world benefit.

No training/evaluation split has been made. Define the task, labelling guide, independent review and evaluation design before building a model or reporting accuracy.

## Received date

Each starter example uses the scenario received date November 4, 2026 (Saskatoon local calendar date). This field provides context for relative wording; it is not a measured operational timestamp. E001 therefore reports a missed collection on November 3. Clarify relative wording if the message may have been delayed or forwarded, or its reference date is otherwise ambiguous. The date does not prove the actual scheduled collection day.
