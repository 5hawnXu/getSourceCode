from random import randint
from getSourceCode.common import handle_exception
from getSourceCode.config import api_keys

API_KEYS = api_keys.keys()


def get_keys(network):
    try:
        if network not in API_KEYS:
            return None
        keys = api_keys[network]
        return keys
    except KeyError as e:
        handle_exception(e)


def get_key(network):
    try:
        keys = get_keys(network)
        if not keys:
            return "Cronos do not need a api key."
        random_num = randint(0, len(keys) - 1)
        return keys[random_num]
    except IndexError as e:
        handle_exception(e)


def print_key(network):
    try:
        keys = get_keys(network)
        if keys:
            output_keys = "\n".join(keys)
            print(output_keys)
        else:
            print("Please choose a right network. For example: get_code -k -n BSC")
    except Exception as e:
        handle_exception(e)
