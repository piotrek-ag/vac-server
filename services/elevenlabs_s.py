import os

from elevenlabs import set_api_key

api_key = os.getenv('ELEVENLABS_API_KEY')
if api_key:
    set_api_key(api_key)
else:
    print('ELEVENLABS_API_KEY environment variable is not set.')

def generate_sound(line):
    return ""
