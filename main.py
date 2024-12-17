from openai import OpenAI
import os
import streamlit as st

API_KEY = os.getenv("api_key")
client = OpenAI(api_key=API_KEY)

# Initialize session state if not already done
if 'messages' not in st.session_state:
    st.session_state.messages = []

value = st.chat_input("Prompt")

if value:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": value})

    with st.chat_message("user"):
        st.write(value)

    with st.chat_message("assistant"):
        st.header("Waiting for api...")

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages
    )

    assistant_message = completion.choices[0].message.content
    # Add assistant message to session state
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})

    st.markdown(assistant_message)

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])