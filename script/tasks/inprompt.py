import re
import sys
import os
import openai

sys.path.append(os.getcwd())

from script.task import answer, get_task_dict, set_token


def _get_name_from_question(question: str) -> str:
    words = question.split()

    for word in words:
        if word[0].isupper():
            return re.sub(r'[^\w]', '', word)


def _filter_descriptions(descriptions: list[str], name: str) -> list[str]:
    return [
        description 
        for description in descriptions
        if description.startswith(name)
    ]


if __name__ == '__main__':
    openai.api_key = os.getenv("OPENAI_API_KEY")
    set_token()
    task_dict = get_task_dict()
    descriptions: list[str] = task_dict['input']
    question: str = task_dict['question']
    name = _get_name_from_question(question=question)
    filtered_descriptions = _filter_descriptions(
        descriptions=descriptions,
        name=name
    )
    user = f'Question: "{question}"'
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                "role": "system",
                "content": "You answer questions. "
            },
            {
                "role": "user",
                "content": '. '.join(filtered_descriptions)
            },
            {
                "role": "user",
                "content": user
            }
        ]
    )
    gpt_answer: str = response['choices'][0]['message']['content']
    answer(answer=gpt_answer)
