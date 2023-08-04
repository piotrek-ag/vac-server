import json
import os

from flask import Flask, request
from flask_restful import Resource, Api

from services.personas_s import get_personas, save_personas
from services.sounds_s import get_sounds, save_sounds, create_or_update_audio_file
from utils.util import generate_id

app = Flask(__name__)
api = Api(app)


class Sound(Resource):
    def get(self, id):
        if id is None:
            return {'error': 'No id provided'}, 400
        sound = next((s for s in get_sounds() if s['id'] == id), None)
        if sound is None:
            return {'error': 'Sound not found'}, 404
        return sound

    def post(self):
        sound = request.get_json()

        # Validate the 'occasion' field
        valid_occasions = {'random', 'dock_in', 'dock_out', 'bump'}
        if 'occasion' in sound and sound['occasion'] not in valid_occasions:
            return {'error': 'Invalid occasion value, must be one of: ' + ', '.join(valid_occasions)}, 400

        # Validate the keys in the incoming JSON data
        valid_keys = {'occasion', 'line'}
        if not set(sound.keys()).issubset(valid_keys):
            return {'error': 'Invalid keys, only "occasion" and/or "line" are allowed'}, 400

        sounds = get_sounds()
        sound['id'] = generate_id(sounds)
        sounds.append(sound)
        save_sounds(sounds)
        return sound, 201

    def put(self, id):
        # Get the incoming JSON data
        update = request.get_json()

        # Validate the 'occasion' field
        valid_occasions = {'random', 'dock_in', 'dock_out', 'bump'}
        if 'occasion' in update and update['occasion'] not in valid_occasions:
            return {'error': 'Invalid occasion value, must be one of: ' + ', '.join(valid_occasions)}, 400

        # Validate the keys in the incoming JSON data
        valid_keys = {'occasion', 'line'}
        if not set(update.keys()).issubset(valid_keys):
            return {'error': 'Invalid keys, only "occasion" and/or "line" are allowed'}, 400

        sounds = get_sounds()
        sound = next((p for p in sounds if p['id'] == id), None)
        if sound is None:
            return {'error': 'Sound not found'}, 404

        # Check if the 'line' field is being updated
        if 'line' in update:
            # Get all personas
            personas = get_personas()
            # Check if the sound is used by a persona
            for persona in personas:
                if id in persona['sounds']:
                    # Create a new audio file for the updated line
                    update = create_or_update_audio_file((update, persona['voice'])) #sound, voice = args
                    break

        sound.update(update)
        save_sounds(sounds)
        return sound

    def delete(self, id):
        sounds = [p for p in get_sounds() if p['id'] != id]

        # Get the sound to be deleted
        sound_to_delete = next((sound for sound in get_sounds() if sound['id'] == id), None)

        if sound_to_delete is not None:
            file_path = sound_to_delete['path']
            # Check if the file exists and delete it
            if os.path.isfile(file_path):
                os.remove(file_path)
            else:
                raise FileNotFoundError(f"No such file or directory: '{file_path}'")

        save_sounds(sounds)

        # Remove the sound ID from all personas
        personas = get_personas()
        for persona in personas:
            persona['sounds'] = [sound_id for sound_id in persona['sounds'] if sound_id != id]
        save_personas(personas)
        return {'result': 'Sound deleted'}


class AllSounds(Resource):
    def get(self):
        # Load characters from JSON file
        with open('resources/sounds.json') as f:
            sounds = json.load(f)
        return sounds
