from pathlib import Path
import sys
import os
import tempfile
import openai
import requests

sys.path.append(os.getcwd())

from script.task import answer, set_token


if __name__ == '__main__':
    openai.api_key = os.getenv("OPENAI_API_KEY")
    set_token()
    mp3_url = 'https://zadania.aidevs.pl/data/mateusz.mp3'
    get_mp3_response = requests.request("GET", mp3_url)

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file_path = Path(tmp_dir) / 'file.mp3'

        with open(tmp_file_path, "wb") as tmp_file:
            tmp_file.write(get_mp3_response.content)

        with open(tmp_file_path, "rb") as tmp_file:
            response = openai.Audio.transcribe(
                model='whisper-1',
                file=tmp_file, 
                response_format="text"
            )

    answer(answer=response)
