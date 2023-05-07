import openai
import json
import os
from django.conf import settings

config_file = os.path.join(settings.BASE_DIR, 'config.json')
with open(config_file, 'r') as f:
    config = json.load(f)
    api_key = config['openai_api_key']
    openai.api_key = api_key
def chat_with_gpt_3_5_turbo(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response['choices'][0]['message']['content']
