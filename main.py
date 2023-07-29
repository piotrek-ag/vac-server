from flask import Flask
from flask_restful import Api
from resources.personas import Persona, AllPersonas
from resources.sounds import Sound, AllSounds
from resources.characters import Character, AllCharacters

app = Flask(__name__)
api = Api(app)

api.add_resource(Persona, '/api/personas', '/api/personas/<int:id>')
api.add_resource(AllPersonas, '/api/personas/all')
api.add_resource(Sound, '/api/sounds', '/api/sounds/<int:id>')
api.add_resource(AllSounds, '/api/sounds/all')
api.add_resource(Character, '/api/characters', '/api/characters/<int:id>')
api.add_resource(AllCharacters, '/api/characters/all')

if __name__ == '__main__':
    app.run(debug=True)
