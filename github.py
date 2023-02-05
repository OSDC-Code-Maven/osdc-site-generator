import os
import requests
import sys
from pprint import pprint
import logging


def get_user_info(username):
    token = os.environ.get('MY_GITHUB_TOKEN')
    if not token:
        logging.error('MY_GITHUB_TOKEN is missing')
        exit(1)
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {token}',
        'X-GitHub-Api-Version': '2022-11-28',
    }

    url = f"https://api.github.com/users/{username}"
    logging.info(url)
    user_data = requests.get(url, headers=headers).json()
    logging.info(user_data)
    return user_data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit(f"Usage {sys.argv[0]} USERNAME")
    username = sys.argv[1]
    pprint(get_user_info(username))

