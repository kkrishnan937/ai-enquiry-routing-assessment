# Waste-enquiry classification — public-source check

Reviewed: November 14, 2026  
Status: Initial source check; experiment definitions proposed for BA review

## Purpose and source boundary

Check whether public service information supports a narrow distinction between missed collection and reported dumped waste. These are portfolio classification definitions, not official municipal labels, legal determinations, departmental ownership decisions or service eligibility rules.

## Sources inspected

| Reference | Public page | Information used |
|---|---|---|
| S-01 | [City of Saskatoon — Use our Online Services](https://www.saskatoon.ca/services-residents/connect-your-city/use-our-online-services) | Separately lists missed/partial curbside waste collection, damaged containers and waste violations. Illegal dumping is one example within the broader waste-violation category. |
| S-02 | [City of Saskatoon — Illegal Dumping](https://www.saskatoon.ca/services-residents/waste-recycling/illegal-dumping) | Describes unauthorised waste disposal on public or private property. |
| S-03 | [City of Saskatoon — Curbside Garbage (Black Cart)](https://www.saskatoon.ca/services-residents/waste-recycling/garbage/curbside-garbage-black-cart) | Describes scheduled collection and directs residents to check their collection calendar. Used for scheduled-collection context only. |

Access date for all pages: November 14, 2026. Page publication/effective dates were not established for the category descriptions. No form was submitted, internal procedure inspected or operational approval obtained. Exclude prices, penalties, response promises and provider-routing claims from this experiment; they are unnecessary to distinguish enquiry intent.

## Proposed definitions

| Experiment label | Include when the enquiry reports | Exclude / review boundary | Source basis |
|---|---|---|---|
| Missed collection | Expected scheduled waste collection did not happen, or only part was collected. | A resident reporting this is not proof a service failure occurred or that a return collection is due. Damaged/stolen carts and schedule questions alone are other topics. | S-01; scheduled context S-03. |
| Reported dumped waste | Waste has allegedly been deposited or abandoned outside its intended disposal arrangement, such as someone leaving bags on a verge. | Do not infer illegality or responsibility from a complaint. Uncollected waste in the resident's own cart is not enough to infer dumping. Road debris, overflow or unclear location/context may require review. | Portfolio interpretation grounded in S-02; S-01 distinguishes wider waste violations. |
| Other | An identifiable topic outside these two types, such as a damaged cart, a collection-calendar question or water billing. | Not a catch-all for ambiguous text. Unknown intent and multiple competing intents need review rather than a forced Other label. | Experiment-defined remainder, not a municipal service category; examples supported by S-01 and S-03. |

## Separate review and missing-information decisions

- A missing address/date does not by itself change a clear enquiry type. Record missing details separately; do not assume they prevent type classification or automatically require model abstention.
- If the text does not establish intent, or contains multiple types that cannot be represented by the single-label task, flag human review. Do not force an unsupported destination/type.
- The sources support a semantic distinction; they do not establish dataset labels, real-world performance or operational readiness. Enquiry examples, review rules and independent evaluation design still need preparation.

## Initial conclusion

Public information supports a narrow experiment comparing reported missed collection with reported dumped waste, subject to the boundaries above. Other is an experiment-defined residual category. The next step is a concise experiment brief and reviewed examples, not implementation or a claim that departmental routing rules have been verified.
