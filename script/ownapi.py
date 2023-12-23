import os
import sys
from fastapi import FastAPI
import openai
from pydantic import BaseModel
import uvicorn

sys.path.append(os.getcwd())

from script.task import ENVS, answer, get_task_dict, set_token

app = FastAPI()


class AiDevsQuestion(BaseModel):
    question: str


class AiDevsAsnwer(BaseModel):
    reply: str


def trigger():
    set_token()
    url = ENVS.OWN_API_URL
    print(f'Sending own API URL = {url}')
    answer(answer=url)


def get_ai_answer(question: str) -> str:
    openai.api_key = ENVS.OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                "role": "system",
                "content": "Odpowiadasz na zadane pytanie."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )
    return response['choices'][0]['message']['content']


@app.post("/ai_devs")
async def ai_devs_question(question: AiDevsQuestion):
    print(f'Get a question: {question.question}')
    set_token()
    reply = get_ai_answer(question=question.question)
    return AiDevsAsnwer(reply=reply)


@app.get("/ai_devs")
async def ai_devs_test(question):
    print(question)
    set_token()
    task_dict = get_task_dict()
    answer()
    return {"task_dict": task_dict}


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'trigger':
        trigger()
    else:
        uvicorn.run(app, host="localhost", port=8080)
