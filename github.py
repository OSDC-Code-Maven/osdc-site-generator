import requests
import sys
from pprint import pprint
import logging


def get_user_info(username):
    url = f"https://api.github.com/users/{username}"
    logging.info(url)
    user_data = requests.get(url).json()
    logging.info(user_data)
    return user_data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit(f"Usage {sys.argv[0]} USERNAME")
    username = sys.argv[1]
    pprint(get_user_info(username))

