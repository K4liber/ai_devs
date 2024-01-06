import os
import sys
from fastapi import FastAPI
import openai
import requests
import uvicorn
import serpapi

sys.path.append(os.getcwd())

from script.tasks.ownapi.common import AiDevsAsnwer, AiDevsQuestion, trigger
from script.task import set_token, ENVS

app = FastAPI()


def get_ai_url_answer(
        html_page_content: str,
        question: str
    ) -> str:
    openai.api_key = ENVS.OPENAI_API_KEY
    system = ' '.join([
        'You will get an html page content and',
        'based on that you need to answer the question.',
        'Your answer should be only a URL, nothing more.',
        '\nEXAMPLE:',
        '\nUSER:',
        '\nContent:',
        '\n<html><body>Football is beautiful 90minut.pl<body></html>',
        '\nQuestion:',
        '\nWhat is an url for a polish site with footbal news?',
        '\nAssistant:',
        '\nhttp://90minut.pl'
    ])
    user = '\n'.join([
        'Content:',
        html_page_content,
        'Question:',
        question
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
                "content": user
            }
        ]
    )
    return response['choices'][0]['message']['content']


def get_google_first_result_content(question: str) -> str:
    client = serpapi.Client(api_key=ENVS.SERP_API_KEY)
    results = client.search({
        'q': question,
        'engine': "google",
        'location': "Warsaw, Poland",
        'hl': "en",
        'gl': "us",
        'num': 1
    })
    first_result_link = results["organic_results"][0]['link']
    response = requests.get(first_result_link)
    print(f'Response:\n{response.text[:500]}')
    return response.text[:10000]


def get_url(question: str) -> str:
    google_first_result_conent = get_google_first_result_content(
        question=question
    )
    return get_ai_url_answer(
        html_page_content=google_first_result_conent,
        question=question
    )


@app.post("/google")
async def google(question: AiDevsQuestion) -> AiDevsAsnwer:
    print(f'Got a question: {question.question}')
    set_token()
    url = get_url(question=question.question)
    print(f'Sending an URL: {url}')
    return AiDevsAsnwer(reply=url)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'trigger':
        trigger()
    else:
        uvicorn.run(app, host="localhost", port=8080)
