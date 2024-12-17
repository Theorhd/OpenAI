from openai import OpenAI;
import os
import streamlit as st

API_KEY = os.getenv("api_key")

client = OpenAI(api_key=API_KEY)

value = st.chat_input("Prompt")

if (value):
    with (st.chat_message("user")):
        txt = st.write(value)
        
    with (st.chat_message("assistant")):
        txt = st.header("Waiting for api...")

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": value}
        ]
    )

    txt.markdown(completion.choices[0].message.content)