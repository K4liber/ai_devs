import openai
from pydantic import BaseModel
from script.task import ENVS, answer, set_token


def trigger() -> None:
    set_token()
    url = ENVS.OWN_API_URL
    print(f'Sending own API URL = {url}')
    answer(answer=url)


def get_ai_answer(
        question: str,
        system_additional_context: str | None = None
    ) -> str:
    openai.api_key = ENVS.OPENAI_API_KEY
    system = "Odpowiadasz na zadane pytanie." + \
        (
            '\nOto dodatkowe informacje, które możesz wykorzystać ' +
            'przy udzielaniu odpowiedzi:\n' +
            system_additional_context
        ) if system_additional_context else ''
    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )
    return response['choices'][0]['message']['content']


class AiDevsQuestion(BaseModel):
    question: str


class AiDevsAsnwer(BaseModel):
    reply: str
