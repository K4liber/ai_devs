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
    input_sections = task_dict['blog']
    outputs = []

    for input_section in input_sections:
        input = \
            'Napisz proszę krótki rozdział (max 4 zdania) na temat ' \
            'przyrządzania pizzy Margheritta. Tytuł rozdziału to: ' \
            f'"{input_section}"'
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": "system", "content": "Jesteś bloggerem kulinarnym."},
                {"role": "user", "content": input}
            ]
        )
        output = response['choices'][0]['message']['content']
        print(f'Section "{input_section}", output = {output}')
        outputs.append(output)
    
    answer(answer=outputs)
