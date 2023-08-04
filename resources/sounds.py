import json
import os

from flask import Flask, request
from flask_restful import Resource, Api

from services.personas_s import get_personas, save_personas
from services.sounds_s import get_sounds, save_sounds
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
        sounds = get_sounds()
        sound = request.get_json()
        sound['id'] = generate_id(sounds)
        sounds.append(sound)
        save_sounds(sounds)
        return sound, 201

    def put(self, id):
        sounds = get_sounds()
        sound = next((p for p in sounds if p['id'] == id), None)
        if sound is None:
            return {'error': 'Sound not found'}, 404
        update = request.get_json()
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
