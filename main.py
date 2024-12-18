from openai import OpenAI
import os
import streamlit as st

API_KEY = os.getenv("api_key")
client = OpenAI(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

def new_message(content: str, model: str):
    with st.chat_message("user"):
        st.session_state.messages.append({"role": "user", "content": content})
        st.write(content)
    
    if model == "GPT-4o":
        handle_gpt4o_response(content)
    elif model == "GPT-4o-mini":
        handle_chatgpt_response(content)
    elif model == "GPT 3.5 Turbo":
        handle_gpt35turbo_response(content)
    elif model == "DALL-E":
        handle_dalle_response(content)
    elif model == "Python Code Expert":
        handle_python_expert_response(content)

def handle_chatgpt_response(content: str):
    with st.chat_message("assistant"):
        txt = st.header("Waiting for response...")
        messages = st.session_state.messages + [{"role": "user", "content": content}]
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True
        )

        full_text = ""
        for chunk in completion:
            if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
                chunk_text = chunk.choices[0].delta.content
                full_text += chunk_text
                txt.markdown(full_text)
        st.session_state.messages.append({"role": "assistant", "content": full_text})

def handle_dalle_response(content: str):
    image_url = openai_create_image(content)
    st.session_state.messages.append({"role": "assistant", "content": image_url})
    st.image(image_url)

def handle_python_expert_response(content: str):
    with st.chat_message("assistant"):
        txt = st.header("Waiting for response...")
        messages = st.session_state.messages + [{"role": "user", "content": content}]
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True
        )
        full_text = ""
        for chunk in completion:
            if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
                chunk_text = chunk.choices[0].delta.content
                full_text += chunk_text
                txt.markdown(full_text)
        st.session_state.messages.append({"role": "assistant", "content": full_text})

def handle_gpt4o_response(content: str):
    with st.chat_message("assistant"):
        txt = st.header("Waiting for response...")
        messages = st.session_state.messages + [{"role": "user", "content": content}]
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            stream=True
        )
        full_text = ""
        for chunk in completion:
            if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
                chunk_text = chunk.choices[0].delta.content
                full_text += chunk_text
                txt.markdown(full_text)
        st.session_state.messages.append({"role": "assistant", "content": full_text})

def handle_gpt35turbo_response(content: str):
    with st.chat_message("assistant"):
        txt = st.header("Waiting for response...")
        messages = st.session_state.messages + [{"role": "user", "content": content}]
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True
        )
        full_text = ""
        for chunk in completion:
            if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
                chunk_text = chunk.choices[0].delta.content
                full_text += chunk_text
                txt.markdown(full_text)
        st.session_state.messages.append({"role": "assistant", "content": full_text})

def openai_create_image(prompt: str):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return response.data[0].url
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def generate_article(topic: str):
    st.header(f"Génération de l'article sur le sujet : {topic} ...")
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Tu es un assistant qui rédige des articles. Ta taches est de générer 3 paragraphes par sujet qui te seront demandés."},
            {"role": "user", "content": f"Rédige un article sur le sujet : {topic}"}
        ]
    )
    article_content = completion.choices[0].message.content
    st.text(article_content)
    
    # Generate images
    for _ in range(2):
        image_url = openai_create_image(f"Crée une image d'illustration pour un article sur : {topic}. Tes images doivent être en rapport avec le sujet.")
        if image_url:
            st.image(image_url)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

value = st.chat_input("Votre message ici...")

if st.button("Clear Chat"):
    st.session_state.messages = []

model = st.selectbox("Choisi ton modèle", ["GPT-4o-mini", "GPT-4o", "GPT 3.5 Turbo", "DALL-E", "Python Code Expert", "Générateur d'articles"])

if value and value != "" and model != "Générateur d'articles":
    new_message(value, model)
    value = ""

if model == "Générateur d'articles":
    topic = st.text_input("Enter a topic for the article")
    if topic:
        generate_article(topic)
