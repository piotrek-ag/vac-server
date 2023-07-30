import json


def get_personas():
    # Load characters from JSON file
    with open('resources/personas.json') as f:
        return json.load(f)


def save_personas(characters):
    with open('resources/personas.json', 'w') as f:
        json.dump(characters, f, indent=4)
