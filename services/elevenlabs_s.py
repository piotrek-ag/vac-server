import json
import os

import requests
from elevenlabs import generate, play, voices
from elevenlabs import set_api_key

api_key = os.getenv('ELEVENLABS_API_KEY')
if api_key:
    set_api_key(api_key)
else:
    print('ELEVENLABS_API_KEY environment variable is not set.')


def get_voices():
    if os.path.exists("resources/voices.json") and os.path.getsize("resources/voices.json") > 0:
        with open("resources/voices.json", "r") as file:
            return json.load(file)['voices']

    url = "https://api.elevenlabs.io/v1/voices"
    headers = {"xi-api-key": api_key}
    response = requests.get(url, headers=headers)
    return response.json()['voices']


def text_to_speech(line,
                   voice,
                   model='eleven_monolingual_v1'):
    # Placeholder for the API call
    # Replace this with the actual API call
    audio = generate(
        text=line,
        voice=voice,
        model=model
    )
    return audio


def filter_by_gender(json_obj, gender):
    # parse json
    data = json.loads(json_obj)

    # get voices
    voices = data.get('voices')

    # filter voices by gender
    filtered_voices = [voice for voice in voices if voice.get('labels').get('gender') == gender]

    return filtered_voices
