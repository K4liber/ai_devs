"""
Module should use a fine-tuned model.
The task was simple enough to provide all the necesary information
in the system content.
If the length of a content is more complex one need to consider a fine-tuned model.
Fine-tuning improves on few-shot learning by training on 
many more examples than can fit in the prompt.
It can also save some costs on repeating the same data in the system content 
since the fine-tuned model already has those information.
But one need to provide a well prepared data set in order to fine-tune the model.
It takes some time and effort.
Moreover, fine-tuning is not for free and each usage of fine-tuned model 
is a bit more expensive than using a model provided by OpenAI.

More on fine-tuning: https://platform.openai.com/docs/guides/fine-tuning
Example fine-tuning data:
https://huggingface.co/datasets/jamescalam/agent-conversations-retrieval-tool/viewer/default/train?p=2

"""
import os
import sys
from fastapi import FastAPI
import openai
import uvicorn

sys.path.append(os.getcwd())

from script.tasks.ownapi.common import AiDevsAsnwer, AiDevsQuestion, trigger
from script.task import set_token, ENVS

app = FastAPI()


def get_translated_md2html(
        markdown_text: str
    ) -> str:
    openai.api_key = ENVS.OPENAI_API_KEY
    system = ' '.join([
        'Your task is to translate the markdown formatted document',
        'into HTML formatted document.',
        'Please do not send anything else but an correctly formatted HTML document.',
        'Do not add any additional words at the start or the end.',
        'The answer have to start with proper element tag.',
        'Do not start the answer with word HTML: or something like this.',
        'Your answer should be a correctly formatted HTML document without anything else.',
        'Do not add <html> tags to the document.',
        'Start with the HTML tag that is sufficient for the first line of the content.',
        'Please use <b> tag instead <strong> tag.',
        'Please use <i> tag instead <em> tag.',
        '\n\nExample 1:',
        '\nUser:',
        '\n# My Big Heading',
        '\nThis is a citation with some *emphasis* on this word.'
        '\nAssistant:',
        '\n<h1>My Big Heading</h1>',
        '\n<blockquote>This is a paragraph with some <i>emphasis</i> on this word.</blockquote>',
        '\n\nExample 2:',
        '\nUser:',
        '\n- Item **one**',
        '\n- Item **two**',
        '\n- Item **three**',
        '\nAssistant:',
        '\n<ul>',
        '\n  <li>Item <b>one</b></li>',
        '\n  <li>Item <b>two</b></li>',
        '\n  <li>Item <b>three</b></li>',
        '\n</ul>',
        '\n\nExample 3:',
        '\nUser:',
        '\n[Visit Google!](http://google.com)',
        '\n![Alt text for the image](http://example.com/image.jpg)',
        '\nAssistant:',
        '\n<a href="http://google.com">Visit Google!</a>',
        '\n<img src="http://example.com/image.jpg" alt="Alt text for the image" />',
        '\n\nExample 3:',
        '\nUser:',
        '\n[Visit Google!](http://google.com)',
        '\n![Alt text for the image](http://example.com/image.jpg)',
        '\nAssistant:',
        '\n<a href="http://google.com">Visit Google!</a>',
        '\n<img src="http://example.com/image.jpg" alt="Alt text for the image" />',
    ])
    user = '\n'.join([
        'Markdown:',
        markdown_text
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
                "content": user
            }
        ]
    )
    return response['choices'][0]['message']['content']


@app.post("/md2html")
async def md2html(question: AiDevsQuestion) -> AiDevsAsnwer:
    print(f'Got a question:\n{question.question}')
    set_token()
    html_format = get_translated_md2html(markdown_text=question.question)
    print(f'Sending an answer:\n{html_format}')
    return AiDevsAsnwer(reply=html_format)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'trigger':
        trigger()
    else:
        uvicorn.run(app, host="localhost", port=8080)
