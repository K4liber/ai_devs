import sys
import os
import openai

sys.path.append(os.getcwd())

from script.task import answer, get_task_dict, set_token



def get_answer(image_url: str) -> dict[str, str]:
    system = [
        'Odpowiedz jakiego koloru czapkę ma postać?',
        'Jeśli obrazek nie zawiera postaci w czapce odpowiedz "error".'
    ]
    response = openai.ChatCompletion.create(
        model='gpt-4-vision-preview',
        messages=[
            {
                "role": "system",
                "content": ' '.join(system)
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    },
                ],
            }
        ]
    )
    return response['choices'][0]['message']['content']


if __name__ == '__main__':
    openai.api_key = os.getenv("OPENAI_API_KEY")
    set_token()
    task_dict = get_task_dict()
    image_url = task_dict['url']
    print(f'Image URL: {image_url}')
    answer_str = get_answer(image_url=image_url)
    print(f'Answer: {answer_str}')
    answer(answer=answer_str)
