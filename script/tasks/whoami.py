import sys
import os
import openai

sys.path.append(os.getcwd())

from script.task import answer, get_task_dict, set_token


if __name__ == '__main__':
    openai.api_key = os.getenv("OPENAI_API_KEY")
    set_token()
    answered = False
    system = f'Na podstawie podanego masz za zadanie stwierdzić ' \
             f'kogo dotyczy opis. Jeśli nie jesteś pewny o kogo chodzi ' \
             f'wysyłasz w odpowiedzi pojedyncze słowo NIE.' \
             f'Jeśli wiesz o kogo chodzi, wysyłasz w odpowiedzi tylko nazwę ' \
             f'opisywanej osoby i nie poza tym. Pamiętaj, że musisz być pewny odpowiedzi. ' \
             f'Odpowiadasz poprzez NIE jeśli masz jakąkolwiek wątpliwość.'
    hints = []
    left_tries = 10
    
    while answered is False and left_tries > 0:
        left_tries -= 1
        task_dict = get_task_dict()
        hint = task_dict['hint']
        hints.append(hint)
        print(f'hint = "{hint}"')
        user = ' '.join(hints)
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

        if 'NIE' not in gpt_answer:
            answer(answer=gpt_answer)
            answered = True
