import openai
import re
import json

from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Your OpenAI API Key
openai.api_key = "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"

def chat_with_gpt_3_5_turbo(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response['choices'][0]['message']['content']

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    # Initialize the conversation history with a system message
    conversation_history = [
        {"role": "system", "content": "You are a helpful assistant."},
    ]

    # Append user message to the conversation history
    conversation_history.append({"role": "user", "content": incoming_msg})

    # Get the chatbot's response and append it to the conversation history
    chatbot_response = chat_with_gpt_3_5_turbo(conversation_history)
    conversation_history.append({"role": "assistant", "content": chatbot_response})

    # Send the chatbot's response as a reply
    msg.body(chatbot_response)

    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)
