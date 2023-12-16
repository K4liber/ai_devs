from qdrant_client import QdrantClient

import sys
import os

sys.path.append(os.getcwd())

from script.task import answer, get_task_dict, set_token
from script.qdrant_loading import COLLECTION_NAME


if __name__ == '__main__':
    client = QdrantClient(host="localhost", port=6333)
    client.set_model('intfloat/multilingual-e5-large')
    set_token()
    task_dict = get_task_dict()
    question = task_dict['question']
    print(f'Question = {question}')
    search_result = client.query(
        collection_name=COLLECTION_NAME,
        query_text=question,
        limit=1
    )
    document = search_result[0].metadata['document']
    url = search_result[0].metadata['source']
    print(f'Document = "{document}", URL = {url}')
    answer(answer=url)
