from flask import Flask, request
from flask_restful import Resource, Api
from utils.util import generate_id
import json

app = Flask(__name__)
api = Api(app)

def get_personas():
    with open('resources/personas.json') as f:
        return json.load(f)

def save_personas(characters):
    with open('resources/personas.json', 'w') as f:
        json.dump(characters, f, indent=4)

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
        persona['id'] = generate_id(personas)
        personas.append(persona)
        save_personas(personas)
        return persona, 201

    def put(self, id):
        personas = get_personas()
        persona = next((p for p in personas if p['id'] == id), None)
        if persona is None:
            return {'error': 'Persona not found'}, 404
        update = request.get_json()
        persona.update(update)
        save_personas(personas)
        return persona

    def delete(self, id):
        personas = [p for p in get_personas() if p['id'] != id]
        save_personas(personas)
        return {'result': 'Persona deleted'}

class AllPersonas(Resource):
    def get(self):
        # Load characters from JSON file
        with open('resources/personas.json') as f:
            personas = json.load(f)
        return personas
