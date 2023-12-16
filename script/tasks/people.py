from dataclasses import dataclass
import json
from pathlib import Path
import sys
import os
import openai

sys.path.append(os.getcwd())

from script.task import answer, get_task_dict, set_token


@dataclass(frozen=True)
class PersonID:
    name: str
    surname: str


if __name__ == '__main__':
    person_id_to_data_str = dict()

    with open(Path('data') / 'people.json') as file:
        data = json.load(file)

        for person_dict in data:
            person_id = PersonID(
                name=person_dict['imie'],
                surname=person_dict['nazwisko']
            )
            person_id_to_data_str[person_id] = str(person_dict)
    
    openai.api_key = os.getenv("OPENAI_API_KEY")
    set_token()
    task_dict = get_task_dict()
    question = task_dict['question']
    # Get person ID
    system_msg_list = [
        'Z podanego pytanie wyodrębij tylko imię i nazwiko i zwróć ',
        'w odpowiedzi. Nie zwracaj niz poza tym. Tylko imię i nazwisko w ',
        'mianowniku.\n',
        'Przykład 1:\n',
        'Użytkownik:\n'
        'Czy Lechowi Wałęsie należy się emerytura?\n',
        'Asystent:\n',
        'Lech Wałęsa'
    ]
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                "role": "system",
                "content": "".join(system_msg_list)
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )
    output = response['choices'][0]['message']['content'].strip().split(' ')
    print(f'Person = {output}')
    person_id = PersonID(
        name=output[0],
        surname=output[1]
    )
    person_data_str = person_id_to_data_str[person_id]
    # Answer the question
    system_msg_list = [
        'Otrzymasz zbiór informacji o danej osobie. ',
        'Twoim zadaniem jest odpowiedzieć na pytanie o tej osobie.\n',
        'Zbiór informacji:\n',
        f'{person_data_str}'
    ]
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                "role": "system",
                "content": "".join(system_msg_list)
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )
    output = response['choices'][0]['message']['content'].strip()
    print(f'Output = {output}')
    answer(answer=output)
