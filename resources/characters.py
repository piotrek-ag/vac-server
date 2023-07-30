from flask import Flask, request
from flask_restful import Resource, Api

from services.characters import get_characters, save_characters
from utils.util import generate_id

app = Flask(__name__)
api = Api(app)


class Character(Resource):
    def get(self, id=None):
        if id is None:
            return {'error': 'No id provided'}, 400
        character = next((c for c in get_characters() if c['id'] == id), None)
        if character is None:
            return {'error': 'Character not found'}, 404
        return character

    def post(self):
        characters = get_characters()
        character = request.get_json()
        character['id'] = generate_id(characters)
        characters.append(character)
        save_characters(characters)
        return character, 201

    def put(self, id):
        characters = get_characters()
        character = next((c for c in characters if c['id'] == id), None)
        if character is None:
            return {'error': 'Character not found'}, 404
        update = request.get_json()
        character.update(update)
        save_characters(characters)
        return character

    def delete(self, id):
        characters = [c for c in get_characters() if c['id'] != id]
        save_characters(characters)
        return {'result': 'Character deleted'}


class AllCharacters(Resource):
    def get(self):
        return get_characters()
