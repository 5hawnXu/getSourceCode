from random import randint
from getsourcecode.common import handle_exception
from getsourcecode.config import api_keys

def get_keys():
    try:
        return api_keys
    except KeyError as e:
        handle_exception(e)


def get_key():
    try:
        keys = get_keys()
        random_num = randint(0, len(keys) - 1)
        return keys[random_num]
    except IndexError as e:
        handle_exception(e)


def print_key():
    try:
        keys = get_keys()
        if keys:
            output_keys = "\n".join(keys)
            print(output_keys)
    except Exception as e:
        handle_exception(e)
