import sqlite3

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def create_tables(conn):
    cursor = conn.cursor()

    # Create Conversations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY,
        title TEXT,
        start_time DATETIME,
        end_time DATETIME,
        model TEXT,
        user_id INTEGER
    )
    """)

    # Create Messages table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        conversation_id INTEGER,
        content TEXT,
        message_type TEXT,
        timestamp DATETIME,
        FOREIGN KEY (conversation_id) REFERENCES conversations (id)
    )
    """)

    # Create Metadata table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metadata (
        id INTEGER PRIMARY KEY,
        message_id INTEGER,
        conversation_id INTEGER,
        key TEXT,
        value TEXT,
        FOREIGN KEY (message_id) REFERENCES messages (id),
        FOREIGN KEY (conversation_id) REFERENCES conversations (id)
    )
    """)

    conn.commit()

def setup_database(db_file):
    conn = create_connection(db_file)
    create_tables(conn)
    return conn
