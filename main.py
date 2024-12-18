from openai import OpenAI
import os
import streamlit as st
import time
from pathlib import Path

API_KEY = os.getenv("api_key")
client = OpenAI(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

def new_message(content: str, model: str):
    with st.chat_message("user"):
        st.session_state.messages.append({"role": "user", "content": content})
        st.write(content)
    
    model_handlers = {
        "GPT-4o": handle_gpt4o_response,
        "GPT-4o-mini": handle_chatgpt_response,
        "GPT 3.5 Turbo": handle_gpt35turbo_response,
        "DALL-E": handle_dalle_response,
        "Python Code Expert": handle_python_expert_response,
        "Translation": handle_translation_response,
        "TTS": handle_tts_response,
        "STT Translation": handle_whisper_stt_translation_response,
        "Real Time Conversation": handle_stt_to_gpt4o_to_tts_no_translation
    }

    if model in model_handlers:
        model_handlers[model](content)
    st.experimental_rerun()  # Force Streamlit to rerun the script

def handle_chatgpt_response(content: str):
    handle_response(content, "gpt-4o-mini")

def handle_dalle_response(content: str):
    image_url = openai_create_image(content)
    st.session_state.messages.append({"role": "assistant", "content": image_url})
    st.image(image_url)

def handle_python_expert_response(content: str):
    handle_response(content, "gpt-4o-mini")

def handle_gpt4o_response(content: str):
    handle_response(content, "gpt-4o")

def handle_gpt35turbo_response(content: str):
    handle_response(content, "gpt-3.5-turbo")

def handle_translation_response(content: str):
    with st.chat_message("assistant"):
        txt = st.header("Waiting for response...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Tu es un assistant qui traduit des textes. Ta tâche est de traduire des textes en différentes langues. Tu vas traduire le texte suivant dans les 6 langues les plus parlées."},
                {"role": "user", "content": content}
                ],
            stream=True
        )
        full_text = ""
        for chunk in response:
            if chunk.choices and len(chunk.choices) > 0 and chunk.choices[0].delta.content is not None:
                chunk_text = chunk.choices[0].delta.content
                full_text += chunk_text
                txt.markdown(full_text)
        st.session_state.messages.append({"role": "assistant", "content": full_text})

def handle_whisper_stt_translation_response():
    audio = st.audio_input("Dites quelque chose")
    if audio:
        file_path = Path(__file__).parent / "input.mp3"
        with open(file_path, "wb") as file:
            file.write(audio.getbuffer())
        with open(file_path, "rb") as file:
            translation = client.audio.translations.create(
                model="whisper-1",
                file=file
            )
            st.write("Translated text : " + translation.text)
            st.session_state.messages.append({"role": "assistant", "content": translation.text})

def handle_tts_response(content: str):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=content
    )
    file_path = Path(__file__).parent / "output.mp3"
    response.stream_to_file(file_path)
    st.audio("output.mp3", autoplay=True)
    st.session_state.messages.append({"role": "assistant", "content": f"Génération de l'audio pour : {content}"})

def handle_stt_to_gpt4o_to_tts():
    audio = st.audio_input("Dites quelque chose")
    if audio:
        file_path = Path(__file__).parent / "input.mp3"
        with open(file_path, "wb") as file:
            file.write(audio.getbuffer())
        with open(file_path, "rb") as file:
            translation = client.audio.translations.create(
                model="whisper-1",
                file=file
            )
            st.write("Translated text : " + translation.text)
            st.session_state.messages.append({"role": "user", "content": translation.text})
            handle_response(translation.text, "gpt-4o-mini")
            response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=st.session_state.messages[-1]["content"]
            )
            output_file_path = Path(__file__).parent / "output.mp3"
            response.stream_to_file(output_file_path)
            st.audio("output.mp3", autoplay=True)
            st.session_state.messages.append({"role": "assistant", "content": f"Génération de l'audio pour : {st.session_state.messages[-1]['content']}"})
            
def handle_stt_to_gpt4o_to_tts_no_translation():
    audio = st.audio_input("Dites quelque chose")
    if audio:
        file_path = Path(__file__).parent / "input.mp3"
        with open(file_path, "wb") as file:
            file.write(audio.getbuffer())
        with open(file_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=file
            )
            st.write("Transcribed text : " + transcription.text)
            st.session_state.messages.append({"role": "user", "content": transcription.text})
            handle_response(transcription.text, "gpt-4o-mini")
            response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=st.session_state.messages[-1]["content"]
            )
            output_file_path = Path(__file__).parent / "output.mp3"
            response.stream_to_file(output_file_path)
            st.audio("output.mp3", autoplay=True)
            st.session_state.messages.append({"role": "assistant", "content": f"Génération de l'audio pour : {st.session_state.messages[-1]['content']}"})
            
def handle_response(content: str, model: str):
    with st.chat_message("assistant"):
        txt = st.header("Waiting for response...")
        messages = st.session_state.messages + [{"role": "user", "content": content}]
        completion = client.chat.completions.create(
            model=model,
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
        ],
        stream=True
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

value = st.chat_input("Votre message ici...")

if st.button("Clear Chat"):
    st.session_state.messages = []

model = st.selectbox("Choisi ton modèle", ["GPT-4o-mini", "GPT-4o", "GPT 3.5 Turbo", "DALL-E", "Python Code Expert", "Générateur d'articles", "Translation", "TTS", "STT Translation", "Real Time Conversation"])

if value and value != "" and model != "Générateur d'articles":
    new_message(value, model)
    value = ""
    st.experimental_rerun()  # Force Streamlit to rerun the script

elif model == "STT Translation":
    handle_whisper_stt_translation_response()
    st.experimental_rerun()  # Force Streamlit to rerun the script

elif model == "Générateur d'articles":
    topic = st.text_input("Enter a topic for the article")
    if topic:
        generate_article(topic)
        st.experimental_rerun()  # Force Streamlit to rerun the script

elif model == "Real Time Conversation":
    handle_stt_to_gpt4o_to_tts_no_translation()
    st.experimental_rerun()  # Force Streamlit to rerun the script