import sys
import os
import openai

sys.path.append(os.getcwd())

from script.task import answer, get_task_dict, set_token


if __name__ == '__main__':
    openai.api_key = os.getenv("OPENAI_API_KEY")
    set_token()
    task_dict = get_task_dict()
    print(task_dict)
    input_sentences = task_dict['input']
    outputs = []

    for input_sentence in input_sentences:
        response = openai.Moderation.create(
            input=input_sentence
        )
        output = int(response["results"][0]['flagged'])
        print(f'Sentence "{input_sentence}", output = {output}')
        outputs.append(output)
    
    answer(answer=outputs)
