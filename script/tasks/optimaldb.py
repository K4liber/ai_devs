import json
import os
from pathlib import Path
import sys

import openai

sys.path.append(os.getcwd())

from script.task import set_token, answer


def get_optimal_db(db: str) -> str:
    input_no_bytes = len(db_str.encode('utf-8'))
    print(f'Input db length = {len(db_str)} ({input_no_bytes} bytes)')
    system = ' '.join([
        'Jesteś optymalizatorem baz danych.',
        'Twoim zadaniem jest zminimalizowanie rozmiaru bazy.',
        'Na podany ciąg znaków odpowiadasz zoptymalizowanym ciągiem znaków.',
        'Musisz zachować wszystkie pierwotne informacje.',
        'Na podstawie twojej odpowiedzi użytkownik jest w stanie',
        'znaleść wszystkie informacje, które były zawarte w pierwotnej bazie.',
        'Pamiętaj aby zachować imiona osób, których dotyczą podane stwierdzenia.',
        'Postaraj się, aby zoptymalizwana baza była jak najkrótszym ciągiem znaków.',
        'Głównym celem ma być zachowanie pierwotnych informacji.',
        'Nie możesz zgubić żadnych pierwotnych danych.',
        'Angielski jest bardziej optymalnym językiem.',
        'Przetłumasz proszę podane informację na język angielski.',
        'Pamiętaj aby zachować wszystkie pierwotne informacje.',
        'Pamiętaj aby zooptymalizować wszystkie informacje, tak',
        'aby ostateczna baza danych zawierała jak najkrótszy ciąg znaków.',
        'Nie zgób żadnej informacji po drodze, to najważniejsze, aby zachować',
        'wszystkie informacje.'
    ])
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": db
            }
        ]
    )
    optimal_db = str(response['choices'][0]['message']['content'])
    output_no_bytes = len(optimal_db.encode('utf-8'))
    print(f'Output db length = {len(optimal_db)} ({output_no_bytes} bytes)')
    return optimal_db


if __name__ == '__main__':
    openai.api_key = os.getenv("OPENAI_API_KEY")

    with open(Path('data') / '3friends.json', 'r') as archive_file:
        db_json = json.load(archive_file)

    optimized_infos = []

    for person_name, person_info_list in db_json.items():
        db_str = ' '.join(person_info_list)
        print(f'{person_name} origin data:\n\n{db_str}\n\n')
        optimal_db_str = f'{person_name}:\n\n {get_optimal_db(db=db_str)}\n\n'
        print(optimal_db_str)
        optimized_infos.append(optimal_db_str)

    set_token()
    answer(answer=' '.join(optimized_infos))
