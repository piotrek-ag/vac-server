import concurrent.futures
import json

from services.elevenlabs import generate_sound
from services.openapi import generate_lines
from utils.util import generate_id


def generate_sound_file(line):
    return {'line': line, 'path': generate_sound(line)}


def generate_line_and_sound(args):
    character, occasion, num_lines = args
    lines = generate_lines(character, occasion, num_lines)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        sounds = list(executor.map(generate_sound_file, lines))

    return [{'id': generate_id(sounds), 'occasion': occasion, **sound} for sound in sounds]


def generate_lines_and_sounds(persona):
    occasions = [('dock_in', 1), ('dock_out', 1), ('random', 7), ('bump', 7)]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(generate_line_and_sound, [(persona['character'], occ, num) for occ, num in occasions])

    sounds = get_sounds()  # Fetch existing sounds
    for result in results:
        for sound in result:
            sounds.append(sound)  # Add the new sound to the list of sounds
            persona['sounds'].append(sound['id'])  # Add the sound ID to the persona's sound IDs
    save_sounds(sounds)  # Save the updated list of sounds
    return persona


def get_sounds():
    with open('resources/sounds.json') as f:
        return json.load(f)


def save_sounds(sounds):
    with open('resources/sounds.json', 'w') as f:
        json.dump(sounds, f, indent=4)
