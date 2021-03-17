from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import pandas as pd
import spacy
from spaczz.matcher import FuzzyMatcher


def filter_kg(node, edge):
    entity_triplets = triplets[triplets.source.apply(lambda d: d['wikidata_id'] in node)]
    edge_triplets = entity_triplets[entity_triplets.edge.apply(lambda d: d['wikidata_id'] == edge)]

    res = []
    if len(edge_triplets):
        for d in edge_triplets.destination.tolist():
            if 'name' in d:
                res.append(d['name'])
            else:
                res.append(d)

    return res


def ask_single_hop(text, edge_m):
    doc = nlp(text)
    matches = source_matcher(doc)

    source_matches = []

    for match_id, start, end, ratio in matches:
        source_matches.append((ratio, match_id))

    source_matches = sorted(source_matches, reverse=True)

    if source_matches:
        source_m = [x[1] for x in source_matches if x[0] >= 80]

        return filter_kg(source_m, edge_m)
    else:
        return []


triplets = pd.read_json('/home/soma/Desktop/poets_kg/poets_QA/data/poet_triplets.json')

nlp = spacy.blank("hu")
source_matcher = FuzzyMatcher(nlp.vocab)

sources = []

for d in triplets.source.tolist():
    tup = (d['wikidata_id'], d['name'])
    if tup not in sources:
        sources.append(tup)

for _id, name in sources:
    source_matcher.add(_id, [nlp(name)])

mapping = {'halálozási_hely': 'P20',
           'halál_oka': 'P509',
           'születési_idő': 'P569',
           'testvér': 'P3373',
           'foglalkozás': 'P106',
           'anya': 'P25',
           'születési_hely': 'P19',
           'beszélt_nyelvek': 'P1412',
           'születési_név': 'P1477',
           'nem': 'P21',
           'politikai_párt': 'P102',
           'gyermek': 'P40',
           'nyughely': 'P119',
           'apa': 'P22',
           'díj': 'P166',
           'alias': None,
           'állampolgárság': 'P27',
           'vallás': 'P140',
           'tagság': 'P463',
           'halálozási_idő': 'P570'}


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_query_graph"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        msg = tracker.latest_message['text']
        relation = tracker.latest_message['intent'].get('name')
        relation_id = mapping[relation]

        ans = ask_single_hop(msg, relation_id)

        dispatcher.utter_message(text=str(ans))

        return []
