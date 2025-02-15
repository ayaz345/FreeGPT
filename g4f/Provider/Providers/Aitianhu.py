import os, requests
from ...typing import sha256, Dict, get_type_hints
import json

url = "https://www.aitianhu.com/api/chat-process"
model = ['gpt-3.5-turbo']
supports_stream = True
needs_auth = False

def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    try:
        base = (
            ''.join(
                '%s: %s\n' % (message['role'], message['content'])
                for message in messages
            )
            + 'assistant:'
        )
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        }
        data = {
            "prompt": base,
            "options": {},
            "systemMessage": "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown.",
            "temperature": 0.8,
            "top_p": 1
        }
        response = requests.post(url, headers=headers, json=data, stream=True)
        if response.status_code == 200:
            lines = response.text.strip().split('\n')
            res = json.loads(lines[-1])
            if 'text' in res:
                yield res['text']
            else:
                raise KeyError("No 'text' key in response")
        else:
            print(f"Error Occurred::{response.status_code}")
            raise Exception(f"Aitianhu server error: Status Code {response.status_code}")
    except Exception as e:
        print(f"Error in Aitianhu provider: {e}")
        raise e 

params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])