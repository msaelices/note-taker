import requests
from io import BytesIO


class AssemblyAI:
    transcript = "https://api.assemblyai.com/v2/transcript"
    upload = "https://api.assemblyai.com/v2/upload"


def transcribe(api_key: str, language, audio_file: BytesIO) -> str:
    headers = {"authorization": api_key, "content-type": "application/json"}
    upload_response = requests.post(AssemblyAI.upload, headers=headers, data=audio_file)

    audio_url = upload_response.json()["upload_url"]

    json = {
        "audio_url": audio_url,
        "iab_categories": True,
        "language_code": language,
        "speaker_labels": True,
    }

    response = requests.post(AssemblyAI.transcript, json=json, headers=headers)

    if not response.ok:
        # TODO: Handle errors
        return response.json()

    polling_endpoint = f'{AssemblyAI.transcript}/{response.json()["id"]}'

    status = "submitted"
    while status != "completed":
        polling_response = requests.get(polling_endpoint, headers=headers)
        status = polling_response.json()["status"]

    # TODO: Remove this
    print(polling_response.json())

    # TODO: Return the speakers and their text
    return polling_response["text"]


def summarize_transcript(
    openai_api_key: str,
    transcript: str,
    openai_model: str = "gpt-4",
    prompt: str = "Summarize the following audio transcription with a list of the key points with the speakers in the original language:",
) -> str:
    """Summarize the transcription using OpenAI's API"""
    # TODO: Implement this
    return "This is a summary of the transcription."
