from flask import Flask, request
from flask_restful import Resource, Api
from utils.util import generate_id
import json

app = Flask(__name__)
api = Api(app)

def get_sounds():
    with open('resources/sounds.json') as f:
        return json.load(f)

def save_sounds(characters):
    with open('resources/sounds.json', 'w') as f:
        json.dump(characters, f, indent=4)

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
        save_sounds(sounds)
        return {'result': 'Sound deleted'}

class AllSounds(Resource):
    def get(self):
        # Load characters from JSON file
        with open('resources/sounds.json') as f:
            sounds = json.load(f)
        return sounds