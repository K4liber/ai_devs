import sys
import os
import openai

sys.path.append(os.getcwd())

from script.task import answer, set_token


if __name__ == '__main__':
    openai.api_key = os.getenv("OPENAI_API_KEY")
    set_token()
    phrase = 'Hawaiian pizza'
    response = openai.Embedding.create(
        model='text-embedding-ada-002',
        input=phrase
    )
    embedding_answer: list[float] = response['data'][0]['embedding']
    answer(answer=embedding_answer)
