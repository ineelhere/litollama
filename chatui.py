import streamlit as st
import ollama
import sqlite3
from datetime import datetime

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('chatbot_conversations.db')
    c = conn.cursor()
    
    # Check if the conversations table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='conversations'")
    if not c.fetchone():
        # Create the conversations table if it doesn't exist
        c.execute('''CREATE TABLE conversations
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      timestamp TEXT,
                      model TEXT,
                      title TEXT)''')
    else:
        # Add the title column if it doesn't exist
        c.execute("PRAGMA table_info(conversations)")
        columns = [column[1] for column in c.fetchall()]
        if 'title' not in columns:
            c.execute("ALTER TABLE conversations ADD COLUMN title TEXT")

    # Check if the messages table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='messages'")
    if not c.fetchone():
        # Create the messages table if it doesn't exist
        c.execute('''CREATE TABLE messages
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      conversation_id INTEGER,
                      role TEXT,
                      content TEXT)''')

    conn.commit()
    return conn

# Save conversation to database
def save_conversation(conn, model, messages):
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    title = messages[0]['content'][:50] + '...' if len(messages[0]['content']) > 50 else messages[0]['content']
    c.execute("INSERT INTO conversations (timestamp, model, title) VALUES (?, ?, ?)",
              (timestamp, model, title))
    conversation_id = c.lastrowid
    
    for message in messages:
        c.execute("INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                  (conversation_id, message['role'], message['content']))
    conn.commit()
    return conversation_id

# Load conversation from database
def load_conversation(conn, conversation_id):
    c = conn.cursor()
    c.execute("SELECT model FROM conversations WHERE id = ?", (conversation_id,))
    model = c.fetchone()[0]
    c.execute("SELECT role, content FROM messages WHERE conversation_id = ? ORDER BY id", (conversation_id,))
    messages = [{"role": role, "content": content} for role, content in c.fetchall()]
    return model, messages

# Get conversation list
def get_conversation_list(conn):
    c = conn.cursor()
    c.execute("SELECT id, timestamp, title FROM conversations ORDER BY timestamp DESC")
    return c.fetchall()

# Streamlit app
def main():
    st.title("Ollama Chatbot")

    # Initialize database connection
    conn = init_db()

    # Sidebar for conversation history
    st.sidebar.title("Conversation History")
    conversations = get_conversation_list(conn)
    selected_conversation = st.sidebar.radio("Select a conversation:", 
                                             ["New Conversation"] + [f"{conv[1]} - {conv[2]}" for conv in conversations])

    # Get available models
    models = ollama.list()['models']
    model_names = [model['name'] for model in models]

    if selected_conversation == "New Conversation":
        # Model selection
        selected_model = st.selectbox("Choose a model:", model_names)

        # Initialize chat history
        if "messages" not in st.session_state or st.session_state.get('current_conversation') != "New Conversation":
            st.session_state.messages = []
            st.session_state.current_conversation = "New Conversation"
    else:
        conversation_id = conversations[conversations.index(next(conv for conv in conversations if f"{conv[1]} - {conv[2]}" == selected_conversation))][0]
        selected_model, st.session_state.messages = load_conversation(conn, conversation_id)
        st.session_state.current_conversation = conversation_id

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("What is your question?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in ollama.chat(
                model=selected_model,
                messages=st.session_state.messages,
                stream=True,
            ):
                full_response += response['message']['content']
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Save conversation to database if it's a new conversation
        if st.session_state.current_conversation == "New Conversation":
            conversation_id = save_conversation(conn, selected_model, st.session_state.messages)
            st.session_state.current_conversation = conversation_id
        else:
            # Update existing conversation
            c = conn.cursor()
            c.execute("DELETE FROM messages WHERE conversation_id = ?", (st.session_state.current_conversation,))
            for message in st.session_state.messages:
                c.execute("INSERT INTO messages (conversation_id, role, content) VALUES (?, ?, ?)",
                          (st.session_state.current_conversation, message['role'], message['content']))
            conn.commit()

    # Close database connection
    conn.close()
