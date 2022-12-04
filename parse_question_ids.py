import requests
from multiprocessing.dummy import Pool
import random
import traceback

from requests.adapters import HTTPAdapter, Retry

global ofile

def parse_page(id2):
    s = requests.Session()
    retries = Retry(total=5,
                backoff_factor=0.15,
                status_forcelist=[ 500, 502, 503, 504 ])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    try:
        resp = s.get(
            f'https://yandex.ru/znatoki/web-api/aggregate/lazyData/questionRecommends',
            params={
                'eventName': 'qQuestionRoute',
                'id2': id2,
                'slug': 'q',
                'exp_flags': 'new_quality',
                'exp_flags': 'full_tag_info'
            }
        )
        resp = resp.json()
        ids = ''.join(str(question['id2']) + '\n' for question in resp['entities']['question'].values())
        ofile.write(ids)
        print(id2)
    except Exception:
        traceback.print_exc()
        return
    
with open('ids.txt', 'r', encoding='utf-8') as id_file:
    ids = list(set(line.strip() for line in id_file))

random.shuffle(ids)

ofile = open('ids.txt', 'a', encoding='utf-8')
pool = Pool(32)
pool.map(parse_page, ids)
pool.close()
pool.join()


    
