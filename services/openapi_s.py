import os

import openai

api_key = os.environ['OPENAI_API_KEY']
if api_key:
    openai.api_key = api_key
else:
    print('OPENAI_API_KEY environment variable is not set.')


def generate_lines(character, occasion, num_lines):
    return ""


def determine_sex(name):
    delimiter = "####"

    user_message = f"{delimiter}{name}{delimiter}"
    system_message = """
    You will be provided with a name. It will be delimited with \
    {delimiter} characters.
    Classify the provided name as male, female, or non-binary.
    Allowed output values are: male, female, and non-binary.
    """

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message},
    ]

    try:
        response = get_completion_from_messages(messages)
        if response:
            print(response)
            return response
        else:
            print("No response from the model.")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_completion_from_messages(messages,
                                 model="gpt-3.5-turbo",
                                 temperature=0,
                                 max_tokens=500):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message["content"]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
