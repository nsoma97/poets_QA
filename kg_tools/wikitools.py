import requests
import pandas as pd

from bs4 import BeautifulSoup


def get_entities_of_category(category_url, url_prefix='https://hu.wikipedia.org'):
    resp = requests.get(category_url)
    soup = BeautifulSoup(resp.text, features="lxml")
    page_urls = [a['href'] for a in soup.find('td', {'class': 'hlist'}).find_all('a')]

    entities = []
    for url in page_urls:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, features="lxml")
        res = [(a['title'], a['href']) for a in
               soup.find('div', {'id': 'mw-pages'}).find_all('a', href=lambda s: s.startswith('/wiki/') if s else '')]
        entities.extend(res)

    entities = list(set(entities))

    res_list = []

    for name, url_suffix in entities:
        try:
            res = requests.get(url_prefix + url_suffix)
            soup = BeautifulSoup(res.text, features="lxml")
            wikidata_id = soup.find('li', {'id': 't-wikibase'}).find('a')['href']
            res_list.append((name, url_suffix, wikidata_id))
        except:
            print(name, 'failed.')

    entity_df = pd.DataFrame(res_list, columns=['name', 'wiki_url', 'wikidata_url'])

    return entity_df
