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
    
    if model == "ChatGPT":
        handle_chatgpt_response(content)
    elif model == "DALL-E":
        handle_dalle_response(content)
    elif model == "Python Code Expert":
        handle_python_expert_response(content)

def handle_chatgpt_response(content: str):
    with st.chat_message("assistant"):
        txt = st.header("Waiting for response...")
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": content}]
        )
        response_content = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": response_content})
        txt.text(response_content)

def handle_dalle_response(content: str):
    image_url = openai_create_image(content)
    st.session_state.messages.append({"role": "assistant", "content": image_url})
    st.image(image_url)

def handle_python_expert_response(content: str):
    with st.chat_message("assistant"):
        txt = st.header("Waiting for response...")
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es un expert en code Python. Réponds en format Markdown et aide à comprendre et corriger le code Python."},
                {"role": "user", "content": content}
            ]
        )
        response_content = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": response_content})
        txt.text(response_content)

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
    st.write(article_content)
    
    # Generate images
    for _ in range(2):
        image_url = openai_create_image(f"Crée une image d'illustration pour un article sur : {topic}. Tes images doivent être en rapport avec le sujet.")
        if image_url:
            st.image(image_url)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

model = st.selectbox("Choisi ton modèle", ["ChatGPT", "DALL-E", "Générateur d'articles", "Python Code Expert"])
value = st.chat_input("Your message here")
if value and value != "" and model != "Générateur d'articles":
    new_message(value, model)
    value = ""

if model == "Générateur d'articles":
    topic = st.text_input("Enter a topic for the article")
    if topic:
        generate_article(topic)