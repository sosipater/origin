from typing import List, Tuple, Dict
import sqlite3

def insert_conversation(conn, title: str, start_time: str, end_time: str, model: str, user_id: int) -> int:
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO conversations (title, start_time, end_time, model, user_id) VALUES (?, ?, ?, ?, ?)
    """, (title, start_time, end_time, model, user_id))
    conn.commit()
    return cursor.lastrowid

def insert_message(conn, conversation_id: int, content: str, message_type: str, timestamp: str) -> int:
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO messages (conversation_id, content, message_type, timestamp) VALUES (?, ?, ?, ?)
    """, (conversation_id, content, message_type, timestamp))
    conn.commit()
    return cursor.lastrowid

def insert_metadata(conn, message_id: int, conversation_id: int, key: str, value: str):
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO metadata (message_id, conversation_id, key, value) VALUES (?, ?, ?, ?)
    """, (message_id, conversation_id, key, value))
    conn.commit()

def get_conversations(conn) -> List[Tuple[int, str, str, str, str, int]]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM conversations")
    return cursor.fetchall()

def get_messages(conn, conversation_id: int) -> List[Tuple[int, int, str, str, str]]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages WHERE conversation_id = ?", (conversation_id,))
    return cursor.fetchall()

def get_metadata(conn, message_id: int) -> List[Tuple[int, int, int, str, str]]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM metadata WHERE message_id = ?", (message_id,))
    return cursor.fetchall()
