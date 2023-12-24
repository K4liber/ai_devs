import os
import sys
from fastapi import FastAPI
import uvicorn

sys.path.append(os.getcwd())

from script.tasks.ownapi.common import AiDevsAsnwer, AiDevsQuestion, get_ai_answer, trigger
from script.task import set_token

app = FastAPI()


@app.post("/ownapi")
async def ownapi(question: AiDevsQuestion) -> AiDevsAsnwer:
    print(f'Get a question: {question.question}')
    set_token()
    reply = get_ai_answer(question=question.question)
    print(f'Sending an answer: {reply}')
    return AiDevsAsnwer(reply=reply)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'trigger':
        trigger()
    else:
        uvicorn.run(app, host="localhost", port=8080)
