import sys
import os
import openai
import requests

sys.path.append(os.getcwd())

from script.task import answer, get_task_dict, set_token


if __name__ == '__main__':
    openai.api_key = os.getenv("OPENAI_API_KEY")
    set_token()
    task_dict = get_task_dict()
    question = task_dict['question']
    print(f'Question = "{question}"')
    url = task_dict['input']
    content = requests.get(url).text
    system = f'You are answering questions based on the ' \
             f'following content: "{content}"'
    user = f'Question: {question}'
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": user
            }
        ]
    )
    gpt_answer = response['choices'][0]['message']['content']
    print(f'Answer = "{gpt_answer}"')
    answer(answer=gpt_answer)
