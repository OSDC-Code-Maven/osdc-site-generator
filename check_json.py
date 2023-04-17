import re
import pathlib

from generate import read_json_files


VALID_FIELDS = ['name', 'linkedin', 'github', 'gitlab', 'devto', 'posts', 'github_page', 'projects']
REQURED_FIELD = ['name', 'github']
data_dir = pathlib.Path.cwd()

def check_json():
    errors = 0
    for folder in ['mentors', 'participants']:
        people = read_json_files(data_dir.joinpath(folder))
        for person in people:
            for field in person.keys():
                if field != field.lower():
                    print(f"ERROR: Field '{field}' in file '{person['github']}.json'  is not lower case")
                    error += 1

                if field not in VALID_FIELDS:
                    print(f"ERROR: Field '{field}' in file '{person['github']}.json'  is not in the list of VALID_FIELDS")
                    error += 1

                if person[field] == "":
                    print(f"ERROR: Field '{field}' in file '{person['github']}.json' is empty")
                    error += 1

                for field in ['linkedin', 'github', 'gitlab', 'devto']:
                    if field in person:
                        match = re.search(r'^[a-zA-Z0-9-.]+$', person[field])
                        if not match:
                            print(f"ERROR: Invalid format for '{field}'='{person[field]}' in file '{person['github']}.json'")
                            error += 1

            if 'posts' in person:
                if person['posts'].__class__.__name__ != 'list':
                    print(f"ERROR: Type of posts is not list in file '{person['github']}.json'")
                    errors += 1

                for post in person['posts']:
                    if not post['url'].startswith('https://'):
                        print(f"ERROR: URL '{post['url']} does not start with 'https://' in file '{person['github']}.json'")
                        errors += 1
                    if post['url'].startswith('https://dev.to/'):
                        if list(post.keys()) != ['url']:
                            print(f"ERROR: If the post is on dev.to then we only need the url to be listed. in file '{person['github']}.json'")
                            errors += 1
                    else:
                        if sorted(post.keys()) != ['published_at', 'title', 'url']:
                            print(f"ERROR: If the post is not on dev.to then we need the url, the title, and the published_at fields.  in file '{person['github']}.json'")
                            errors += 1

            for field in REQURED_FIELD:
                if field not in person:
                    print(f"ERROR: Required field '{field}' is missing in file '{person['github']}.json'")
                    errors += 1

    if errors:
        exit("There were {errors} errors")

check_json()
