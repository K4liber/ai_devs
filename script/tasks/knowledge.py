from dataclasses import dataclass
import json
import sys
import os
import openai
import requests

sys.path.append(os.getcwd())

from script.task import answer, get_task_dict, set_token


@dataclass
class Question:
    category: str
    value: str


def get_exchange_rate_data(currency: str) -> float:
    url = f'https://api.nbp.pl/api/exchangerates/rates/a/{currency}/?format=json'
    data = requests.get(url).text
    data_dict = json.loads(data)
    return data_dict['rates'][0]['mid']


def get_population_data(country: str) -> int:
    url = f'https://restcountries.com/v3.1/name/{country}'
    data = requests.get(url).text
    data_dict = json.loads(data)
    return data_dict[0]['population']


def get_general_knowledge_data(question: str) -> str:
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                "role": "system",
                "content": "Odpowiadasz na zadanie pytania."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )
    return response['choices'][0]['message']['content']


def get_formalized_question(question: str) -> Question:
    system = [
        "Twoim zadaniem jest nadać kategorie zadanemu pytaniu.",
        "Masz do wybory trzy kategorie: currency, population, knowledge.\n",
        "Wiedza jest kategorią domyślną jeśli jest to pytanie z poza " \
        "jednej z kategorii waluta lub populacja.\n" \
        "Odpowiadasz w formacie json.\n",
        "Jeśli kategorią jest waluta, do odpowiedzi dodajesz 3 literowy skrót tej waluty.\n",
        "Jeśli kategorią jest populacja, do odpowiedzi dodajesz angielską nazwę kraju ",
        "o którego populację zapytano.\n",
        "Jeśli kategorią jest wiedza do odpowiedzi dodajesz otrzymane pytanie.\n\n",
        "Przykład 1:\n",
        "Użytkownik:\n",
        "Jaką populację mają Niemcy?\n",
        "Asystent:\n",
        '{"category": "population", "value": "germany"}\n\n',
        "Przykład 2:\n",
        "Użytkownik:\n",
        "Jaki jest kurs dolara amerykańskiego?\n",
        "Asystent:\n",
        '{"category": "currency", "value": "usd"}'
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
    return Question(
        category=response_dict['category'],
        value=response_dict['value']
    )

if __name__ == '__main__':
    openai.api_key = os.getenv("OPENAI_API_KEY")
    set_token()
    task_dict = get_task_dict()
    question = task_dict['question']
    print(f'Question: {question}')
    formalized_question = get_formalized_question(question=question)
    print(f'Fromalized question: {formalized_question}')
    category_to_function = {
        'currency': get_exchange_rate_data,
        'population': get_population_data,
        'knowledge': get_general_knowledge_data
    }
    answer_value = category_to_function[formalized_question.category](
        formalized_question.value
    )
    print(f'Answer: {answer_value}')
    answer(answer=answer_value)
