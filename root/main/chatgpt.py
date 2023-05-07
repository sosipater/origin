import openai
import sqlite3
from db_operations import insert_conversation, insert_message, insert_metadata

# Set up OpenAI API key
openai.api_key = "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"


def start_conversation(conn, title: str, model: str, user_id: int) -> int:
    conversation_id = insert_conversation(conn, title, "", "", model, user_id)
    return conversation_id


def chat(conn, conversation_id: int, model: str, prompt: str) -> str:
    # Send API request
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.8,
    )

    reply = response.choices[0].text.strip()

    # Store user input and the generated response in the database
    user_message_id = insert_message(conn, conversation_id, prompt, "user", "")
    bot_message_id = insert_message(conn, conversation_id, reply, "bot", "")

    # Add any metadata if necessary

    return reply
