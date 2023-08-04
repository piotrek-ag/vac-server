import concurrent.futures
import json
import os
import random

from services.characters_s import get_character_by_id
from services.elevenlabs_s import text_to_speech, get_voices
from services.openapi_s import generate_lines, determine_gender
from utils.util import convert_to_double_quotes, find_highest_id, flatten_list, generate_random_filename, filter_voices_by_gender


def generate_lines_and_sounds(persona):
    if 'gender' not in persona:
        persona['gender'] = determine_gender(persona['name'])

    occasions = [('dock_in', 1), ('dock_out', 1), ('random', 7), ('bump', 7)]
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results_without_sound_file = list(executor.map(generate_new_sounds,
                                                       [(persona['character'], occ, num) for occ, num in occasions]))

    results_without_sound_file = flatten_list(results_without_sound_file)

    voices = get_voices()
    voices = filter_voices_by_gender(voices, persona['gender'])
    voice = random.choice(voices)

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        results_with_sound_file = list(executor.map(generate_audio_file,
                                                    [(res, voice['voice_id']) for res in results_without_sound_file]))

    sounds = get_sounds()  # Fetch existing sounds
    highest_id = find_highest_id(sounds) + 1
    for sound in results_with_sound_file:
        sound['id'] = highest_id
        sounds.append(sound)  # Add the new sound to the list of sounds
        persona['sounds'].append(sound['id'])  # Add the sound ID to the persona's sound IDs
        highest_id = highest_id + 1
    save_sounds(sounds)  # Save the updated list of sounds
    return persona


def generate_new_sounds(args):
    character_id, occasion, num_lines = args

    # Generate lines for a given character and occasion
    lines = generate_lines(get_character_by_id(character_id), occasion, num_lines)
    clean_lines = [convert_to_double_quotes(string) for string in lines]

    # Create a new sound for each line
    new_sounds = []
    for line in clean_lines:
        sound = {
            "occasion": occasion,
            "line": line
        }
        new_sounds.append(sound)

    return new_sounds


def generate_audio_file(args):
    sound, voice = args

    # Call the API and get the sound file
    # Please replace this with the actual API call
    sound_file = text_to_speech(sound['line'], voice)

    # Save the sound file in memory and get the path
    # Please replace this with the actual file operation
    path = save_audio_file_to_memory(sound_file)
    sound['path'] = path
    return sound


def save_audio_file_to_memory(audio_file):
    # Placeholder for the file operation
    # Replace this with the actual file operation
    if not os.path.exists('assets/'):
        os.makedirs('assets/')

    sound_file_path = "assets/" + generate_random_filename()
    with open(sound_file_path, "wb") as file:
        file.write(audio_file)
    return sound_file_path


def get_sounds():
    with open('resources/sounds.json') as f:
        return json.load(f)


def save_sounds(sounds):
    with open('resources/sounds.json', 'w') as f:
        json.dump(sounds, f, indent=4)
