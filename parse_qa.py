import requests
from multiprocessing.dummy import Pool
import orjson
import traceback
from threading import Lock
from tqdm import tqdm

from requests.adapters import HTTPAdapter, Retry

global ofile

def parse_question(id2):
    s = requests.Session()
    retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    try:
        resp = s.get(
            f'https://yandex.ru/znatoki/web-api/aggregate/page/qQuestionRoute',
            params={
                'eventName': 'qQuestionRoute',
                'id2': id2,
                'exp_flags': 'new_quality',
                'exp_flags': 'full_tag_info'
            }
        )
        resp = resp.json()
        question = list(resp['entities']['question'].values())[0]
        question['answers'] = list(resp['entities'].get('answer', {}).values())

        with writelock:
            ofile.write(orjson.dumps(question, option=orjson.OPT_APPEND_NEWLINE))
        
        pbar.update()
    except Exception:
        pbar.update()
        traceback.print_exc()

with open('ids.txt', 'r', encoding='utf-8') as ids_file:
    ids = [line.strip() for line in ids_file]

writelock = Lock()
ofile = open(f'dataset2.jsonl', 'wb')
pbar = tqdm(total=len(ids))
pool = Pool(50)
pool.map(parse_question, ids)
pool.close()
pool.join()