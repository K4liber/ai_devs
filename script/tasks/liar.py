import sys
import os
import openai

sys.path.append(os.getcwd())

from script.task import answer, post_task_dict, set_token


if __name__ == '__main__':
    openai.api_key = os.getenv("OPENAI_API_KEY")
    set_token()
    question = 'Who won the football World Cup in 2022?'
    task_dict = post_task_dict(
        question=question
    )
    print(task_dict)
    answer_str = task_dict['answer']
    outputs = []
    user = f'Question: "{question}".\nAnswer: "{answer_str}"'
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                "role": "system",
                "content": "You will get a quesion and an answer. "
                           "Your task is to reply with just YES if the answer "
                           "for the question makes sense. Otherwise reply with just NO."
            },
            {
                "role": "user",
                "content": user
            }
        ]
    )
    output = response['choices'][0]['message']['content']
    print(f'Output = {output}')
    answer(answer=output)
