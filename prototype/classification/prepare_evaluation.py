"""Freeze approach and author candidate synthetic evaluation data. Never runs classifiers."""
import datetime as dt
import difflib
import hashlib
import json
from pathlib import Path
import random
import shutil

root = Path(__file__).resolve().parents[2]
destination = root / 'data/classification-evaluation'
if destination.exists():
    raise SystemExit('Evaluation directory already exists; do not overwrite frozen evidence.')
destination.mkdir()
snapshot = destination / 'frozen-approach'
snapshot.mkdir()
sources = ['data/labelling-guide.md', 'docs/06-evaluation/classification-evaluation-plan.md',
           'docs/06-evaluation/classification-dataset-plan.md',
           'prototype/classification/keyword_baseline.py', 'prototype/classification/classification-prompt.txt',
           'prototype/classification/run_ai_development.py']
manifest = {'frozen_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
            'purpose': 'Freeze approach before authoring held-out candidates; labels still require second-pass review.',
            'model': 'qwen2.5:3b', 'model_digest': '357c53fb659c5076de1d65ccb0b397446227b71a42be9d1603d46168015c9e4b',
            'settings': {'temperature': 0, 'seed': 42, 'num_ctx': 2048, 'num_predict': 128},
            'files': []}
for name in sources:
    path = root / name
    target = snapshot / path.name
    shutil.copyfile(path, target)
    manifest['files'].append({'source': name, 'snapshot': target.name,
                              'sha256': hashlib.sha256(target.read_bytes()).hexdigest()})
(snapshot / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')

# Candidates are authored only after the approach snapshots above have been saved.
groups = {
 'missed_collection': [
 ('communal-skipped', "Every waste container at our small apartment building was skipped on the advertised collection day, although the rest of the block was served."),
 ('single-compartment', "The collection vehicle took the waste from one compartment of our shared container and drove away leaving the other compartment full. This is a report about that incomplete service."),
 ('tagged-skip', "I found a tag on my refuse container after the round. Its contents were not taken. Please log the uncompleted collection; I am not asking you to decide whether a return visit is owed."),
 ('repeated-skip', "This is the second scheduled round in succession when our household rubbish has been left behind. Could this recurring failure be recorded?"),
 ('emptied-wrong-premises', "The vehicle stopped at the property next door instead of ours during yesterday's round. Our container was never serviced."),
 ('residual-contents', "Following this morning's collection visit, the bottom section of the container is still packed with refuse. I am reporting that it was only partly emptied."),
 ('collection-confirmed-later', "I waited until the end of collection day to check. The designated refuse container at our building has not been serviced at all."),
 ('explicit-no-dumping', "Nobody has left extra rubbish at our home. The issue is that the booked waste round failed to empty our container."),
 ('report-without-location', "Could you log an uncompleted scheduled rubbish pickup? I can supply the service location when you contact me."),
 ('access-restored', "Access to our refuse container was restored before the scheduled vehicle arrived, but the operator passed it without taking the contents. I want to report the skipped pickup.")],
 'reported_dumped_waste': [
 ('riverbank-deposition', "I saw a contractor discharge a load of broken plasterboard down the riverbank instead of using a disposal facility. Please record this report."),
 ('public-planter', "An unknown person has used the large public planter as a place to discard household refuse. There are food wrappers and household bags packed into it."),
 ('bicycle-path-appliances', "Two discarded washing machines have been abandoned across the cycle path. They were not placed there for an arranged collection."),
 ('unauthorised-skip-disposal', "Someone used our construction skip without permission to get rid of their household rubbish. We are reporting that disposal incident, not a problem with the collection round."),
 ('creek-furniture', "Furniture has been tipped into the creek behind the recreation ground. A neighbour witnessed it being pushed from a vehicle."),
 ('disposal-hedgerow', "A load of domestic waste has been deliberately thrown into the hedge surrounding the sports field. It is not material waiting for our normal service."),
 ('empty-plot-rubble', "There is a newly abandoned heap of demolition rubble on the empty lot; I saw people carrying it from a renovation and leaving it there."),
 ('waste-stairwell', "Somebody has dumped unwanted household belongings in the public stairwell by the pedestrian bridge. Please take a report about that incident."),
 ('container-misuse', "I witnessed a business tipping its refuse into the park's public litter container without permission, instead of arranging disposal. I want to report that action."),
 ('park-screen', "An old television has been deliberately discarded in the flower bed at the park entrance. It is not awaiting any scheduled pickup.")],
 'other': [
 ('cart-size', "I want to change to a smaller household waste container. What is the process for requesting a size change?"),
 ('new-home-service', "We have just moved into a newly built home. How do we register for the normal waste service?"),
 ('stolen-container', "Our empty rubbish container disappeared from the garage. How do I request a replacement for a stolen container?"),
 ('accepted-material', "Can clean aluminium foil go into household recycling? I only need sorting advice."),
 ('opening-hours', "What are the disposal facility's opening hours on a weekday?"),
 ('fee-explanation', "Please explain how the waste-service charge is calculated for different container sizes."),
 ('food-storage', "Could you suggest how to keep food scraps from smelling between normal collections?"),
 ('recreation-registration', "How can I register my child for municipal swimming lessons?"),
 ('holiday-before-service', "I am planning ahead for next month's public holiday and need the revised service calendar. There has been no failed pickup."),
 ('lodged-lid', "The hinge has snapped off our container lid. I am only asking about a replacement part, not collection or rubbish left elsewhere.")],
 'unclear': [
 ('unexplained-attachment', "Please see the attachment about the rubbish issue. I need help with it."),
 ('unclear-still-waiting', "Any update on our waste request? We are still waiting."),
 ('unexplained-third-party', "The neighbours told us to contact you about the refuse situation, but I do not know what happened."),
 ('unspecified-service', "Something went wrong with the waste service today. Can you look into it?"),
 ('unexplained-request-number', "Could you reopen my previous waste case? I do not have any other details here.")],
 'mixed': [
 ('missed-plus-stolen', "Our scheduled refuse service left the full container behind. In a separate matter, another container has been stolen and needs replacement."),
 ('dumped-plus-sorting', "Someone tipped renovation waste onto the public green. I also have a separate question about which plastics can be recycled at home."),
 ('two-target-active', "Please log yesterday's uncompleted household waste round and a separate incident in which a driver threw building rubble into the creek."),
 ('missed-plus-accounts', "The last expected pickup did not happen for our property. Separately, please explain the waste-service fee on my account."),
 ('dumped-plus-recreation', "I need to report a discarded freezer deliberately left on the public footpath, and I would also like instructions for registering for an exercise class.")]
}
rows = []
for label, items in groups.items():
    for family, text in items:
        review = label in ('unclear', 'mixed')
        rows.append({'family': family, 'text': text, 'expected_type': None if review else label,
                     'review_required': review, 'review_group': label if review else None,
                     'author_reason': {'unclear': 'No sufficient current intent; essential context or attachment unavailable.',
                                       'mixed': 'Distinct active requests span types under the single-label task.'}.get(label, 'Explicit current intent matches the frozen type definition.')})
random.Random(20261114).shuffle(rows)
for index, row in enumerate(rows, 1):
    row['id'] = f'EVAL-{index:03d}'
assert len(rows) == 40
development = json.loads((root / 'data/classification-development.json').read_text())['examples']
checks = []
for row in rows:
    best = max(development, key=lambda d: difflib.SequenceMatcher(None, row['text'].lower(), d['text'].lower()).ratio())
    score = difflib.SequenceMatcher(None, row['text'].lower(), best['text'].lower()).ratio()
    assert row['text'].lower() != best['text'].lower()
    checks.append({'id': row['id'], 'closest_development_id': best['id'], 'character_similarity': round(score, 3)})
inputs = {'split': 'held_out_candidate', 'status': 'Authored after approach freeze; unscored; review pending',
          'examples': [{'id': row['id'], 'text': row['text']} for row in rows]}
labels = {'status': 'Author labels awaiting second-pass review; no predictions inspected',
          'provenance': 'Root assistant authored synthetic text and initial labels after development-based choices were fixed. This is not statistically independent real-world ground truth.',
          'examples': [{k: v for k, v in row.items() if k != 'text'} for row in rows]}
for filename, value in [('inputs.json', inputs), ('author-labels.json', labels), ('development-overlap-check.json', {
        'method': 'Character similarity screen plus explicit scenario-family authoring; not proof of semantic independence.',
        'checks': checks})]:
    (destination / filename).write_text(json.dumps(value, indent=2), encoding='utf-8')
print('Approach snapshotted; 40 candidate texts and separate author labels saved. No classifier executed.')

