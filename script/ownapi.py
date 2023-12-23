import os
import sys
from fastapi import FastAPI
import uvicorn

sys.path.append(os.getcwd())

from script.task import ENVS, answer, get_task_dict, set_token

app = FastAPI()


def trigger():
    set_token()
    url = ENVS.OWN_API_URL
    print(f'Sending own API URL = {url}')
    answer(answer={'url': url})


@app.post("/ai_devs")
async def root(request):
    print(request)
    set_token()
    task_dict = get_task_dict()
    answer()
    return {"task_dict": task_dict}


@app.get("/ai_devs")
async def root(request):
    print(request)
    set_token()
    task_dict = get_task_dict()
    answer()
    return {"task_dict": task_dict}


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'trigger':
        trigger()
    else:
        uvicorn.run(app, host="localhost", port=8080)
