import os
import streamlit as st

from dotenv import load_dotenv

import apis

# Load environment variables from .env file before importing any other modules
load_dotenv()


def main():
    st.set_page_config(
        page_title='Note Taker',
        page_icon='🎙️',
        layout='centered',
        initial_sidebar_state='expanded',
    )

    title = '🎙️ Meetings Note Taker 🎙️'
    st.title(title)
    st.write(
        'Upload an audio file, transcribe it using Assembly.AI, and sgenerate meeting notes using your selected model.'
    )

    openai_api_key = os.environ.get('OPENAI_API_KEY') or st.text_input(
        'Enter your OpenAI API key:', type='password'
    )
    assemblyai_api_key = os.environ.get('ASSEMBLYAI_API_KEY') or st.text_input(
        'Enter your AssemblyAI API key:', type='password'
    )

    openai_model = os.environ.get('OPENAI_MODEL') or st.selectbox(
        'Select a model:', ['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-4-0613']
    )

    uploaded_audio = st.file_uploader(
        'Upload an audio file',
        type=['aac', 'm4a', 'mp3', 'webm', 'mp4', 'mpga', 'wav', 'mpeg'],
        accept_multiple_files=False,
    )
    language = os.environ.get('AUDIO_LANGUAGE') or st.selectbox(
        'Language code of the audio:', ['en', 'es']
    )

    if st.button('Generate Notes'):
        if uploaded_audio:
            if openai_api_key and assemblyai_api_key:
                st.markdown('Transcribing the audio...')
                transcription = apis.transcribe(
                    assemblyai_api_key, language, uploaded_audio
                )

                st.markdown(
                    f'###  Transcription:\n\n<details><summary>Click to view</summary><p><pre><code>{transcription}</code></pre></p></details>',
                    unsafe_allow_html=True,
                )

                st.markdown('Summarizing the transcription...')

                summary = apis.summarize_transcript(
                    openai_api_key, transcription, openai_model,
                )

                st.markdown(f'### Summary:')
                st.write(summary)
            else:
                st.error('We need valid OpenAI and AssemblyAI API keys')


if __name__ == '__main__':
    main()
