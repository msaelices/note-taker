import requests
from io import BytesIO

from engines import TranscriptEngine



def transcribe(engine: TranscriptEngine, language: str, audio_file: BytesIO) -> str:
    return engine.transcribe(language, audio_file)


def summarize_transcript(
    openai_api_key: str,
    transcript: str,
    openai_model: str = 'gpt-4',
    prompt: str = 'Summarize the following audio transcription with a list of the key points with the speakers in the original language:',
) -> str:
    """Summarize the transcription using OpenAI's API"""
    # TODO: Implement this
    return 'This is a summary of the transcription.'
