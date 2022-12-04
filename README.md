# yandex-q
Scripts that were used to scrape and process data from Yandex.Q. The resulting dataset can be found [here](https://huggingface.co/datasets/its5Q/yandex-q).  
Some scripts are messy, but they get the job done.

# Scripts used
- `parse_questions_search.py` - to parse questions by searching all 4 letter combinations, because of the 1000 items limit per search
- `parse_question_ids.py` - to parse question ids by using question recommendation endpoint
- `get_ids.py` - to extract ids from questions that were retrieved from search
- `parse_qa.py` - to parse all question info from ids collected
