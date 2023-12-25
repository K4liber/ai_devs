import sys
import os
import openai
import requests

sys.path.append(os.getcwd())

from script.task import ENVS, answer, get_task_dict, set_token


if __name__ == '__main__':
    openai.api_key = os.getenv("OPENAI_API_KEY")
    set_token()
    task_dict = get_task_dict()
    meme_image_url = task_dict['image']
    meme_text = task_dict['text']
    meme_image_width, meme_image_height = 1080, 1080
    render_form_api_url = 'https://get.renderform.io/api/v2/render'
    template_id = 'high-oxen-slip-joyously-1383'
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": ENVS.RENDER_FORM_API_KEY
    }
    data = {
        "template": template_id,
        "data": {
            "text.text": meme_text,
            "image.src": meme_image_url
        }
    }
    response = requests.post(
        url=render_form_api_url,
        headers=headers,
        json=data
    )
    response_dict = response.json()
    print(f"Response: {response_dict}")
    meme_url = response_dict['href']
    answer(answer=meme_url)
