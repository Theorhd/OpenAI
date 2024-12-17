from openai import OpenAI
import os
import streamlit as st

API_KEY = os.getenv("api_key")
client = OpenAI(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

def new_message(content: str, model: str):
    with (st.chat_message("user")):
        st.session_state.messages.append({"role": "user", "content": content})
        st.write(content)
    
    if model == "ChatGPT":
        with (st.chat_message("assistant")):
            txt = st.header("Waiting for response...")

            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": content}
                ]
            )

            st.session_state.messages.append({"role": "assistant", "content": completion.choices[0].message.content})
            txt.text(completion.choices[0].message.content)
    elif model == "DALL-E":
        image_url = openai_create_image(content)
        st.session_state.messages.append({"role": "assistant", "content": image_url})
        st.image(image_url)

def openai_create_image(prompt: str):
    response = client.images.generate(  # Use Image.create directly
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

model = st.selectbox("Choose a model", ["ChatGPT", "DALL-E"])
value = st.chat_input("Your message here")
if value and value != "":
    new_message(value, model)
    value = ""