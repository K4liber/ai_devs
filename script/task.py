import json
import os
from dotenv import load_dotenv
from pathlib import Path
import requests
import urllib.parse
import sys


ROOT_DIR = Path(__file__).parent.parent

def load_envs():
    for env_file_name in ['.envs', '.token']:
        load_dotenv(ROOT_DIR / env_file_name)

load_envs()
API_KEY = os.getenv('API_KEY')
API_URL = os.getenv('API_URL')
TASK_NAME = os.getenv('TASK_NAME')
TOKEN = os.getenv('TOKEN')


def set_token() -> None:
    api_token_dict = {
        'apikey': API_KEY
    }
    get_token_url = urllib.parse.urljoin(API_URL, f'token/{TASK_NAME}')
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


def print_task() -> None:
    get_token_url = urllib.parse.urljoin(API_URL, f'task/{TOKEN}')
    print(f'Print task URL: {get_token_url}')
    response = requests.get(get_token_url)
    response_dict = json.loads(response.text)
    print(f'Response: {response_dict}')


def answer_with_str(answer_str: str) -> None:
    answer_url = urllib.parse.urljoin(API_URL, f'answer/{TOKEN}')
    answer_dict = {'answer': answer_str}
    print(f'Answer URL: {answer_url}')
    response = requests.post(answer_url, json = answer_dict)
    response_dict = json.loads(response.text)
    print(f'Response: {response_dict}')


cmd = sys.argv[1]
print(f'Running command "{cmd}" ...')

cmd_to_func = {
    'set_token': (set_token, lambda: {}),
    'print_task': (print_task, lambda: {}),
    'answer_with_str': (answer_with_str, lambda: {'answer_str': sys.argv[2]}),
}
func_and_kwargs = cmd_to_func.get(cmd, None)

if func_and_kwargs is None:
    raise ValueError(f'Uknown command "{cmd}"')

func_to_execute, kwargs = func_and_kwargs
func_to_execute(**kwargs())