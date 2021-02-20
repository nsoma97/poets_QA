import pandas as pd
from wikidata.client import Client


def triplet_for_id(_id):
    client = Client()

    entity = client.get(_id, load=True)

    triplets = []

    if 'descriptions' in entity.attributes:
        if 'hu' in entity.attributes['descriptions']:
            triplets.append((_id, 'T_description', entity.attributes['descriptions']['hu']['value']))

    if 'aliases' in entity.attributes:
        if 'hu' in entity.attributes['aliases']:
            for a in entity.attributes['aliases']['hu']:
                triplets.append((_id, 'T_alias', a['value']))

    for k, v in entity.attributes['claims'].items():
        try:
            for lv in v:
                triplets.append((_id, k, lv['mainsnak']['datavalue']['value']))
        except:
            pass

    return pd.DataFrame(triplets, columns=['source', 'edge', 'destination'])


def get_properties(_id):
    client = Client()
    prop = client.get(_id, load=True)

    name, description = '', ''
    aliases = []
    if 'hu' in prop.attributes['labels']:
        name = prop.attributes['labels']['hu']['value']

    if 'hu' in prop.attributes['descriptions']:
        description = prop.attributes['descriptions']['hu']['value']

    if 'hu' in prop.attributes['aliases']:
        aliases = [a['value'] for a in prop.attributes['aliases']['hu']]

    return {
        'wikidata_id': _id,
        'name': name,
        'description': description,
        'aliases': aliases
    }
