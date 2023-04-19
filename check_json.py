import re
import sys
import pathlib

from generate import read_json_files


VALID_FIELDS = ['name', 'linkedin', 'github', 'gitlab', 'devto', 'posts', 'github_page', 'projects']
REQURED_FIELD = ['name', 'github']
data_dir = pathlib.Path.cwd()

def _error(text):
    print(f"ERROR: {text}", file=sys.stderr)

def check_json():
    errors = 0
    for folder in ['mentors', 'participants']:
        try:
            people = read_json_files(data_dir.joinpath(folder))
        except Exception as err:
            _error(f"Exception: {err}")
            errors += 1
            continue
        for person in people:
            for field in person.keys():
                if field != field.lower():
                    _error(f"Field '{field}' in file '{person['github']}.json'  is not lower case")
                    errors += 1

                if field not in VALID_FIELDS:
                    _error(f"Field '{field}' in file '{person['github']}.json'  is not in the list of VALID_FIELDS")
                    errors += 1

                if person[field] == "":
                    _error(f"Field '{field}' in file '{person['github']}.json' is empty")
                    errors += 1

                for field in ['linkedin', 'github', 'gitlab', 'devto']:
                    if field in person:
                        match = re.search(r'^[a-zA-Z0-9-.]+$', person[field])
                        if not match:
                            _error(f"Invalid format for '{field}'='{person[field]}' in file '{person['github']}.json'")
                            errors += 1

            if 'posts' in person:
                if person['posts'].__class__.__name__ != 'list':
                    _error(f"Type of posts is not list in file '{person['github']}.json'")
                    errors += 1

                for post in person['posts']:
                    if not post['url'].startswith('https://'):
                        _error(f"URL '{post['url']} does not start with 'https://' in file '{person['github']}.json'")
                        errors += 1
                    if post['url'].startswith('https://dev.to/'):
                        if list(post.keys()) != ['url']:
                            _error(f"If the post is on dev.to then we only need the url to be listed. in file '{person['github']}.json'")
                            errors += 1
                    else:
                        if sorted(post.keys()) != ['published_at', 'title', 'url']:
                            _error(f"If the post is not on dev.to then we need the url, the title, and the published_at fields.  in file '{person['github']}.json'")
                            errors += 1

            for field in REQURED_FIELD:
                if field not in person:
                    _error(f"Required field '{field}' is missing in file '{person['github']}.json'")
                    errors += 1

    if errors:
        exit(f"There were {errors} errors")

check_json()
