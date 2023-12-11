import sys
import os
import openai

sys.path.append(os.getcwd())

from script.task import answer, set_token


if __name__ == '__main__':
    openai.api_key = os.getenv("OPENAI_API_KEY")
    set_token()
    add_user_dict = {
        "name": "addUser",
        "description": "Add an user to my database",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "provide name of the user"
                },
                "surname": {
                    "type": "string",
                    "description": "provide surname of the user"
                },
                "year": {
                    "type": "integer",
                    "description": "provide the user's year of birth"
                }
            }
        }
    }
    answer(answer=add_user_dict)
