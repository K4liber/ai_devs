import os
import sys
from fastapi import FastAPI
import openai
import uvicorn

sys.path.append(os.getcwd())

from script.tasks.ownapi.common import AiDevsAsnwer, AiDevsQuestion, get_ai_answer, trigger
from script.task import ENVS, set_token

app = FastAPI()
infos = []


def is_question(sentence: str) -> bool:
    openai.api_key = ENVS.OPENAI_API_KEY
    system = '\n'.join([
        'Musisz stwierdzić czy podany tekst to informacja czy pytanie.',
        'Jeśli podany tekst to informacja, w odpowiedzi odsyłasz tylko słowo INFO.',
        'Jeśli podany tekst to pytanie, w odpowiedzi odsyłasz tylko słowo QUESTION.',
        'Pamiętaj aby odpowiadać tylko pojedyńczym słowem INFO lub QUESTION.',
        'Przykład 1:',
        'Uzytkownik:',
        'Mam na imię Jakub.',
        'Asystent:',
        'INFO',
        'Przykład 2:',
        'Uzytkownik:',
        'Gdzie mieszka prezydent Obama?',
        'Asystent:',
        'QUESTION'
    ])
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": sentence
            }
        ]
    )
    answer_content = str(response['choices'][0]['message']['content'])
    return 'info' not in answer_content.lower()


@app.post("/ownapipro")
async def ownapipro(question: AiDevsQuestion) -> AiDevsAsnwer:
    print(f'Get a potential question: {question.question}')
    set_token()

    if is_question(sentence=question.question):
        system_additional_context = '\n'.join(infos)
        print(f'Asking a question with following infos:\n{system_additional_context}')
        reply = get_ai_answer(
            question=question.question,
            system_additional_context=system_additional_context
        )
        print(f'Sending an answer: {reply}')
        return AiDevsAsnwer(reply=reply)
    else:
        infos.append(question.question)
        return AiDevsAsnwer(reply='Thanks for the info.')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'trigger':
        trigger()
    else:
        uvicorn.run(app, host="localhost", port=8080)
