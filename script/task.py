from dataclasses import dataclass
import json
import os
from dotenv import load_dotenv
from pathlib import Path
import requests
import urllib.parse
import sys


ROOT_DIR = Path(__file__).parent.parent

@dataclass
class _Envs:
    API_KEY = os.getenv('API_KEY')
    API_URL = os.getenv('API_URL')
    TASK_NAME = os.getenv('TASK_NAME')
    TOKEN = os.getenv('TOKEN')
    OWN_API_URL = os.getenv('OWN_API_URL')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    RENDER_FORM_API_KEY = os.getenv('RENDER_FORM_API_KEY')


ENVS = _Envs()


def load_envs():
    global ENVS

    for env_file_name in ['.envs', '.token']:
        load_dotenv(ROOT_DIR / env_file_name)
    
    ENVS.API_KEY = os.getenv('API_KEY')
    ENVS.API_URL = os.getenv('API_URL')
    ENVS.TASK_NAME = os.getenv('TASK_NAME')
    ENVS.TOKEN = os.getenv('TOKEN')
    ENVS.OWN_API_URL = os.getenv('OWN_API_URL')
    ENVS.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    ENVS.RENDER_FORM_API_KEY = os.getenv('RENDER_FORM_API_KEY')


load_envs()

def set_token() -> None:
    api_token_dict = {
        'apikey': ENVS.API_KEY
    }
    get_token_url = urllib.parse.urljoin(ENVS.API_URL, f'token/{ENVS.TASK_NAME}')
    print(f'Get token URL: {get_token_url}')
    response = requests.post(get_token_url, json = api_token_dict)
    response_dict = json.loads(response.text)
    response_code = response_dict.get('code', None)

    if response_code != 0:
        raise ValueError(f'Response code != 0, code = {response_code}')

    token = response_dict['token']
    print(f"Token: {token}")

    with open(ROOT_DIR / '.token', 'w') as file:
        file.write(f'TOKEN={token}')

    load_envs()


def post_task_dict(question: str) -> dict:
    task_question_url_post = urllib.parse.urljoin(ENVS.API_URL, f'task/{ENVS.TOKEN}')
    print(f'Task question URL: {task_question_url_post}, question: {question}')
    json_dict = {
        'question': question
    }
    response = requests.post(task_question_url_post, data=json_dict)
    response_dict = json.loads(response.text)
    return response_dict


def get_task_dict() -> dict:
    get_token_url = urllib.parse.urljoin(ENVS.API_URL, f'task/{ENVS.TOKEN}')
    print(f'Print task URL: {get_token_url}')
    response = requests.get(get_token_url)
    response_dict = json.loads(response.text)
    return response_dict


def print_task() -> None:
    response_dict = get_task_dict()
    print(f'Response: {response_dict}')


def answer(answer: str | list | dict, final_answer: bool = False) -> None:
    answer_url = urllib.parse.urljoin(ENVS.API_URL, f'answer/{ENVS.TOKEN}')

    if final_answer:
        answer_dict = answer
    else:
        answer_dict = {'answer': answer}

    print(f'Answer URL: {answer_url}')
    response = requests.post(answer_url, json=answer_dict)

    try:
        response_dict = json.loads(response.text)
        print(f'Response: {response_dict}')
    except json.decoder.JSONDecodeError:
        print(f'Decoding error. Response = {response.text}')


if __name__ == '__main__':
    cmd = sys.argv[1]
    print(f'Running command "{cmd}" ...')

    cmd_to_func = {
        'set_token': (set_token, lambda: {}),
        'print_task': (print_task, lambda: {}),
        'answer_with_str': (answer, lambda: {'answer': sys.argv[2]}),
    }
    func_and_kwargs = cmd_to_func.get(cmd, None)

    if func_and_kwargs is None:
        raise ValueError(f'Uknown command "{cmd}"')

    func_to_execute, kwargs = func_and_kwargs
    func_to_execute(**kwargs())
