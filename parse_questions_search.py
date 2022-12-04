import requests
from multiprocessing.dummy import Pool
import orjson
from itertools import combinations_with_replacement
import traceback

from requests.adapters import HTTPAdapter, Retry

ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

global ofile

def parse_search(query):
    query = ''.join(query)
    s = requests.Session()
    retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    next = {"next": 10}
    while next is not None and int(next["next"]) <= 1000:
        print(query, next["next"])
        try:
            resp = s.get(
                f'https://yandex.ru/znatoki/web-api/request/api/v2/search_q',
                params={
                    'query': query,
                    'type': 'question',
                    'sort': 'time',
                    'formula': 'new_matrix_net_popularity_trtitle_v1',
                    'next': next["next"],
                    '_key': 'feed',
                    '_collection': True,
                    'exp_flags': 'new_quality',
                    'exp_flags': 'full_tag_info'
                }
            )
            resp = resp.json()
            next = resp["result"]["next"]
            for item in resp['result']['items']:
                question = resp['entities']['question'][item['id']]
                ofile.write(orjson.dumps(question, option=orjson.OPT_APPEND_NEWLINE))
        except Exception:
            traceback.print_exc()


ofile = open(f'search_questions.jsonl', 'wb')
pool = Pool(64)
pool.map(parse_search, combinations_with_replacement(ALPHABET, 4))
pool.close()
pool.join()