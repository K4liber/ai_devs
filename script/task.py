import json
import os
from dotenv import load_dotenv
from pathlib import Path
import requests
import urllib.parse
import sys

load_dotenv(Path(__file__).parent.parent / '.envs')

API_KEY = os.getenv('API_KEY')
API_TOKEN = os.getenv('API_TOKEN')
API_URL = os.getenv('API_URL')
TASK_NAME = os.getenv('TASK_NAME')


def print_token() -> None:
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

    print(f"Token: {response_dict['token']}")


def print_task() -> None:
    get_token_url = urllib.parse.urljoin(API_URL, f'task/{API_TOKEN}')
    print(f'Print task URL: {get_token_url}')
    response = requests.get(get_token_url)
    response_dict = json.loads(response.text)
    print(f'Response: {response_dict}')


def answer(answer_str: str) -> None:
    answer_url = urllib.parse.urljoin(API_URL, f'answer/{API_TOKEN}')
    answer_dict = {'answer': answer_str}
    print(f'Answer URL: {answer_url}')
    response = requests.post(answer_url, json = answer_dict)
    response_dict = json.loads(response.text)
    print(f'Response: {response_dict}')


cmd = sys.argv[1]
print(f'Running command "{cmd}" ...')

cmd_to_func = {
    'print_token': (print_token, lambda: {}),
    'print_task': (print_task, lambda: {}),
    'answer': (answer, lambda: {'answer_str': sys.argv[2]}),
}
func_to_execute, kwargs = cmd_to_func.get(cmd, None)

if func_to_execute is None:
    raise ValueError(f'Uknown command "{cmd}"')

func_to_execute(**kwargs())
