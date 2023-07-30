import json
import random
import string


# Simple ID generation
def generate_id(data):
    return max([0] + [item['id'] for item in data]) + 1


def convert_to_double_quotes(string):
    if string[0] == "'" and string[-1] == "'":
        return '"' + string[1:-1] + '"'
    return string


def find_highest_id(objects_list):
    try:
        # Check if the list is empty
        if not objects_list:
            return 0

        # Find the highest value of the 'id' field using the 'max' function
        highest_id = max(objects_list, key=lambda obj: obj['id'])

        return highest_id['id']

    except (json.JSONDecodeError, KeyError):
        # If there's an error parsing JSON or the 'id' field is missing, return None (or any appropriate value)
        return None


def flatten_list(list_of_lists):
    flattened = []
    for item in list_of_lists:
        if isinstance(item, list):
            flattened.extend(flatten_list(item))
        else:
            flattened.append(item)
    return flattened


def generate_random_filename():
    characters = string.ascii_lowercase + string.digits
    random_filename = ''.join(random.choice(characters) for _ in range(9))
    return random_filename + '.mp3'
