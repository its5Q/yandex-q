# import orjson as json
from parse import compile

p = compile('"id2":"{}"')

ids = set()

with open('search_questions.jsonl', 'r', encoding="utf-8") as ifile:
    for line in ifile:
        ids.add(p.search(line)[0])

print(f'Got {len(ids)} unique ids')

with open('ids.txt', 'a', encoding='utf-8') as ofile:
    for i in ids:
        ofile.write(f'{i}\n')