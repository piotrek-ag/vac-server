from flask import Flask, request
from flask_restful import Resource, Api

from services.personas import get_personas, save_personas
from services.sounds import generate_lines_and_sounds
from utils.util import generate_id

app = Flask(__name__)
api = Api(app)


class Persona(Resource):
    def get(self, id=None):
        if id is None:
            return {'error': 'No id provided'}, 400
        persona = next((p for p in get_personas() if p['id'] == id), None)
        if persona is None:
            return {'error': 'Persona not found'}, 404
        return persona

    def post(self):
        personas = get_personas()
        persona = request.get_json()

        if 'name' not in persona:
            return {"error": "The 'name' field is missing from the request"}, 400

        if 'character' not in persona:
            return {"error": "The 'character' field is missing from the request"}, 400

        persona['id'] = generate_id(personas)

        persona['sounds'] = []
        persona = generate_lines_and_sounds(persona)

        personas.append(persona)
        save_personas(personas)
        return persona, 201

    def put(self, id):
        personas = get_personas()
        persona = next((p for p in personas if p['id'] == id), None)
        if persona is None:
            return {'error': 'Persona not found'}, 404
        update = request.get_json()

        # openapi call to populate sounds.line
        # elevenlabs call to populate sounds

        persona.update(update)
        save_personas(personas)
        return persona

    def delete(self, id):
        personas = [p for p in get_personas() if p['id'] != id]
        save_personas(personas)
        return {'result': 'Persona deleted'}


class AllPersonas(Resource):
    def get(self):
        return get_personas()
