import json
import sys
import os
import openai

sys.path.append(os.getcwd())

from script.task import answer, get_task_dict, set_token



def get_function_calling_question(question: str) -> dict[str, str]:
    system = [
        "Twoim zadaniem jest wybrać narzędzie dla zadanego polecenia.",
        "Masz do wybory dwa narzędzia: ToDo i Calendar.\n",
        "Odpowiadasz w formacie json.\n",
        "Jeśli narzędziem jest ToDo, do odpowiedzi dodajesz opis zadania.\n",
        "Jeśli narzędziem jest Calendar, do odpowiedzi dodajesz opis zadania ",
        "oraz datę.\n",
        "Przykład 1:\n",
        "Użytkownik:\n",
        "Przypomnij mi, że mam kupić 1 kg ziemniaków.\n",
        "Asystent:\n",
        '{"tool": "ToDo", "desc": "Kupić 1 kg ziemniaków"}\n\n',
        "Przykład 2:\n",
        "Użytkownik:\n",
        "Jutro mam spotkanie z Marianem.\n",
        "Asystent:\n",
        '{"tool": "Calendar", "desc": "Spotkanie z Marianem.", "date": "2023-12-18"}\n\n',
        "Przykład 3:\n",
        "Użytkownik:\n",
        "Pojutrze mam kupić 1 kg ziemniaków.\n",
        "Asystent:\n",
        '{"tool": "Calendar", "desc": "Kupić 1 kg ziemniaków", "date": "2023-12-18"}\n\n',
        "Pamiętaj aby data była w formacie YYYY-MM-DD."
    ]
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                "role": "system",
                "content": ' '.join(system)
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )
    response_str = response['choices'][0]['message']['content']
    response_dict = json.loads(response_str)
    return response_dict


if __name__ == '__main__':
    openai.api_key = os.getenv("OPENAI_API_KEY")
    set_token()
    task_dict = get_task_dict()
    question = task_dict['question']
    print(f'Question: {question}')
    function_calling_dict = get_function_calling_question(question=question)
    print(f'Function calling: {function_calling_dict}')
    answer(answer=function_calling_dict)
