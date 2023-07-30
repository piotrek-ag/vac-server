import json


def get_characters():
    with open('resources/characters.json') as f:
        return json.load(f)


def save_characters(characters):
    with open('resources/characters.json', 'w') as f:
        json.dump(characters, f, indent=4)


def get_character_by_id(id):
    return next((c for c in get_characters() if c['id'] == id), None)
