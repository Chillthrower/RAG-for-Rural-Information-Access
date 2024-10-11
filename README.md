# Streamlit RAG Application

This application allows users to upload TXT or PDF files, ask questions about the content, and receive responses in the selected language. It operates offline and leverages various libraries for text processing, translation, and text-to-speech functionality.

![Application Screenshot](Screenshot (31).png)  <!-- Replace with your screenshot path -->

## How It Works

### Libraries Used
- **Streamlit**: For building the web application interface.
- **re**: For regular expression operations to process text.
- **io**: For handling in-memory byte streams.
- **fitz (PyMuPDF)**: For reading PDF files.
- **ollama**: For using the Ollama model to generate responses.
- **deep_translator**: For translating text between languages.
- **gtts**: For converting text to speech.
- **base64**: For encoding audio data.
- **streamlit_pdf_viewer**: For previewing PDF files in the Streamlit app.

### Key Functions
1. **normalize_whitespace(text)**: Normalizes whitespace in the input text.
2. **split_text_into_sentences(text)**: Splits the input text into a list of sentences.
3. **chunk_text(sentences, max_chunk_size)**: Chunks the list of sentences into manageable pieces based on a specified maximum size.
4. **text_to_speech(text, lang)**: Converts text to speech using the Google Text-to-Speech API and returns the audio as a base64 string.
5. **truncate_text(text, max_length)**: Truncates the input text to a specified length while preserving sentence structure.

### User Interface
- **File Upload**: Users can upload TXT or PDF files.
- **Language Selection**: Users can choose their preferred language from a predefined list.
- **Processing Files**: The application reads the uploaded file, normalizes the text, splits it into sentences, and chunks it for easier processing.
- **User Interaction**: Users can input questions, and the application retrieves context from the uploaded document to provide relevant answers using the Ollama model.
- **Translation and Speech**: The response can be translated into the selected language and converted to speech.

### Code Explanation
- The application starts by displaying a header and a file uploader in the sidebar.
- When a file is uploaded, it previews the content for PDFs and processes TXT files by normalizing and chunking the text.
- A chat input allows users to ask questions, and the application's history maintains the conversation context.
- Upon receiving a prompt, the application formats it for the Ollama model, retrieves a response, translates it, and generates speech.
- The conversation history is displayed, and if the assistant responds, the corresponding audio is played.

## Benefits for Rural Areas

This application is particularly useful in rural areas for several reasons:

1. **Accessibility of Information**: In rural communities, access to information can be limited. This application allows users to upload educational materials, government documents, or health information in PDF or TXT formats, making vital knowledge more accessible.

2. **Language Support**: The ability to translate responses into multiple languages ensures that non-English speakers can interact with the content comfortably, promoting inclusivity and understanding.

3. **Offline Functionality**: Since the application operates offline, it can be used in areas with limited or no internet connectivity. This ensures that users can still engage with the content without needing a constant online connection.

4. **User Engagement**: The interactive chat feature encourages users to ask questions and seek clarifications, fostering a learning environment. This can be particularly beneficial for educational initiatives or local training programs.

5. **Text-to-Speech Feature**: The ability to convert text to speech is especially helpful for users with literacy challenges, enabling them to listen to content instead of reading it.

## Installation

To install the necessary packages, use `requirements.txt`

```plaintext
pip install -r requirements.txt
