from openai import OpenAI
import os
import streamlit as st

API_KEY = os.getenv("api_key")
client = OpenAI(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

def new_message(content: str):
    with (st.chat_message("user")):
        st.session_state.messages.append({"role": "user", "content": content})
        st.write(value)
    
    with (st.chat_message("assistant")):
        txt = st.header("Waiting for response...")

        completion = client.chat.completions.create(
            model = "gpt-4o-mini",
            messages = [
                {"role" : "user", "content" : value}
            ]
        )

        st.session_state.messages.append({"role": "assistant", "content": completion.choices[0].message.content})
        txt.text(completion.choices[0].message.content)

def openai_create_image(prompt: str):
    response = client.images.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']

def openai_create_image_variation(image: str, prompt: str):
    response = client.images.create_variation(
        image=image,
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

value = st.chat_input("Your message here")
if (value and value != ""):
    new_message(value)
    value = ""