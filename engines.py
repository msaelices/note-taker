from typing import Protocol
from io import BytesIO

import requests

from google.cloud import speech


class TranscriptEngine(Protocol):
    """Protocol for a transcription engine"""

    def transcribe(self, language, audio_file: bytes) -> str:
        """transcribe audio file to text"""
        ...


class AssemblyAI:
    transcript = 'https://api.assemblyai.com/v2/transcript'
    upload = 'https://api.assemblyai.com/v2/upload'

    def __init__(self, api_key: str):
        self.api_key = api_key

    def transcribe(self, language, audio_file: BytesIO) -> str:
        headers = {'authorization': self.api_key, 'content-type': 'application/json'}
        upload_response = requests.post(
            AssemblyAI.upload, headers=headers, data=audio_file
        )

        audio_url = upload_response.json()['upload_url']

        json = {
            'audio_url': audio_url,
            'iab_categories': True,
            'language_code': language,
            'speaker_labels': True,
        }

        response = requests.post(AssemblyAI.transcript, json=json, headers=headers)

        if not response.ok:
            # TODO: Handle errors
            return response.json()

        polling_endpoint = f'{AssemblyAI.transcript}/{response.json()["id"]}'

        status = 'submitted'
        while status != 'completed':
            polling_response = requests.get(polling_endpoint, headers=headers)
            status = polling_response.json()['status']

        # TODO: Remove this
        print(polling_response.json())

        # TODO: Return the speakers and their text
        return polling_response.json()['text']


class GoogleCloud:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def transcribe(self, language, audio_file: BytesIO) -> str:
        client = speech.SpeechClient()

        audio = speech.RecognitionAudio(content=audio_file.read())

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
            language_code=language,
            diarization_config=speech.SpeakerDiarizationConfig(
                enable_speaker_diarization=True,
            ),
        )

        operation = client.long_running_recognize(config=config, audio=audio)
        response = operation.result()

        return ' '.join(
            result.alternatives[0].transcript for result in response.results
        )


def get_engine(engine_type: str, api_key: str | None) -> TranscriptEngine:
    engine_cls = {
        'AssemblyAI': AssemblyAI,
        'Google': GoogleCloud,
    }[engine_type]

    return engine_cls(api_key)
