import openai

openai.api_key = "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"

def chat_with_gpt_3_5_turbo(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response['choices'][0]['message']['content']
