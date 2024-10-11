import streamlit as st
import re
import io
import fitz
import os
import ollama
from deep_translator import GoogleTranslator
from gtts import gTTS
import base64
from streamlit_pdf_viewer import pdf_viewer

languages = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'Dutch': 'nl',
    'Hindi': 'hi',
    'Kannada': 'kn'
}

def normalize_whitespace(text):
    return re.sub(r'\s+', ' ', text).strip()

def split_text_into_sentences(text):
    return [s.strip() for s in re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text) if s.strip()]

def chunk_text(sentences, max_chunk_size):
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 > max_chunk_size:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
        else:
            if current_chunk:
                current_chunk += " "
            current_chunk += sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def text_to_speech(text, lang='en'):
    tts = gTTS(text=text, lang=lang)
    speech_bytes = io.BytesIO()
    tts.write_to_fp(speech_bytes)
    speech_bytes.seek(0)

    speech_base64 = base64.b64encode(speech_bytes.read()).decode('utf-8')
    return speech_base64

def truncate_text(text, max_length):
    if len(text) > max_length:
        truncated = text[:max_length]
        last_punctuation = max(truncated.rfind('.'), truncated.rfind('?'), truncated.rfind('!'))
        if last_punctuation != -1:
            return truncated[:last_punctuation + 1]
        else:
            return truncated
    return text

st.header("Upload your own file and ask questions")
st.subheader('File types supported: TXT/PDF :city_sunrise:')

if 'history' not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    uploaded_file = st.file_uploader("Please upload a file", type=["txt", "pdf"])
    st.markdown("# Language")
    selected_language = st.selectbox('Select your language and press Enter:', list(languages.keys()))

    if uploaded_file:
        st.markdown("### Uploaded File Preview:")

        if uploaded_file.type == "application/pdf":
            binary_data = uploaded_file.getvalue()
            pdf_viewer(input=binary_data, width=700)

context = ""

if uploaded_file:
    file_path = os.path.join(os.getcwd(), uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    st.write("Processing your file... Please wait.")

    if uploaded_file.type == "text/plain":
        with open(file_path, "r") as file:
            content = file.read()
        normalized_text = normalize_whitespace(content)
        sentences = split_text_into_sentences(normalized_text)
        chunks = chunk_text(sentences, max_chunk_size=200)
        context = " ".join(chunks)
        st.write("Processed TXT Content:")

    elif uploaded_file.type == "application/pdf":
        all_text = ""
        with fitz.open(file_path) as pdf:
            for page in pdf:
                all_text += page.get_text()

        normalized_text = normalize_whitespace(all_text)
        sentences = split_text_into_sentences(normalized_text)
        chunks = chunk_text(sentences, max_chunk_size=200)
        context = " ".join(chunks)
        st.write("PDF has been processed successfully!")

prompt = st.chat_input("Your message:")

if prompt:
    st.session_state.history.append({"role": "user", "content": prompt})

    formatted_prompt = f"CONTEXT: {context}\nQUESTION: {prompt}\n(NOTE: PLEASE ENSURE THAT THE RESPONSE DOES NOT EXCEED 2800 WORDS.)"

    with st.spinner("Thinking..."):
        result = ollama.chat(
            model="smollm:135m-instruct-v0.2-q8_0",
            messages=[{"role": "system", "content": formatted_prompt}],
        )
        response = result["message"]["content"]

        truncated_response = truncate_text(response, max_length=3000)

        translator = GoogleTranslator(source='auto', target=languages[selected_language])
        translated_response = translator.translate(truncated_response)

        speech_base64 = text_to_speech(translated_response, lang=languages[selected_language])

        st.session_state.history.append({"role": "assistant", "content": translated_response, "speech": speech_base64})

for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message["role"] == "assistant" and "speech" in message:
            audio_data = f"data:audio/mp3;base64,{message['speech']}"
            st.audio(audio_data, format="audio/mp3")
