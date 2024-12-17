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
    elif model == "GPT-o1-mini":
        handle_gpto1mini_response(content)
    elif model == "GPT-o1-preview":
        handle_gpto1preview_response(content)
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
            messages=messages
        )

        response_content = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": response_content})
        txt.markdown(response_content)

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
            messages=messages
        )
        response_content = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": response_content})
        txt.markdown(response_content)

def handle_gpt4o_response(content: str):
    with st.chat_message("assistant"):
        txt = st.header("Waiting for response...")
        messages = st.session_state.messages + [{"role": "user", "content": content}]
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        response_content = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": response_content})
        txt.markdown(response_content)

def handle_gpto1mini_response(content: str):
    with st.chat_message("assistant"):
        txt = st.header("Waiting for response...")
        messages = st.session_state.messages + [{"role": "user", "content": content}]
        completion = client.chat.completions.create(
            model="gpt-o1-mini",
            messages=messages
        )
        response_content = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": response_content})
        txt.markdown(response_content)

def handle_gpto1preview_response(content: str):
    with st.chat_message("assistant"):
        txt = st.header("Waiting for response...")
        messages = st.session_state.messages + [{"role": "user", "content": content}]
        completion = client.chat.completions.create(
            model="gpt-o1-preview",
            messages=messages
        )
        response_content = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": response_content})
        txt.markdown(response_content)

def handle_gpt35turbo_response(content: str):
    with st.chat_message("assistant"):
        txt = st.header("Waiting for response...")
        messages = st.session_state.messages + [{"role": "user", "content": content}]
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        response_content = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": response_content})
        txt.markdown(response_content)

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
    st.markdown(article_content)
    
    # Generate images
    for _ in range(2):
        image_url = openai_create_image(f"Crée une image d'illustration pour un article sur : {topic}. Tes images doivent être en rapport avec le sujet.")
        if image_url:
            st.image(image_url)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

model = st.selectbox("Choisi ton modèle", ["GPT-4o-mini", "GPT-4o", "GPT 3.5 Turbo", "DALL-E", "GPT-o1-mini", "GPT-o1-preview", "Python Code Expert", "Générateur d'articles"])
value = st.chat_input("Your message here")
if value and value != "" and model != "Générateur d'articles":
    new_message(value, model)
    value = ""

if model == "Générateur d'articles":
    topic = st.text_input("Enter a topic for the article")
    if topic:
        generate_article(topic)