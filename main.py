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
    try:
        response = client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            n=1,
            size="240x240"
        )
        return response.data[0].url
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def generate_article(topic: str):
    st.header(f"Article on {topic}")
    
    for i in range(3):
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f"Write paragraph {i+1} about {topic}"}
            ]
        )
        paragraph = completion.choices[0].message.content
        st.write(paragraph)
    
    # Generate images
    for _ in range(2):
        image_url = openai_create_image(f"Image about {topic}")
        if image_url:
            st.image(image_url)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

model = st.selectbox("Choose a model", ["ChatGPT", "DALL-E", "Article Generator"])
value = st.chat_input("Your message here")
if value and value != "" and model != "Article Generator":
    new_message(value, model)
    value = ""

if model == "Article Generator":
    topic = st.text_input("Enter a topic for the article")
    if topic:
        generate_article(topic)