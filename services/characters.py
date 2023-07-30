import json


def get_characters():
    with open('resources/characters.json') as f:
        return json.load(f)


def save_characters(characters):
    with open('resources/characters.json', 'w') as f:
        json.dump(characters, f, indent=4)
