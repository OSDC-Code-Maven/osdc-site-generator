#!/usr/bin/env python

import json
import os
import pathlib
from jinja2 import Environment, FileSystemLoader
import requests
import forem
import github
import time
import datetime
import logging
import re

logging.basicConfig(level = logging.INFO)
data_dir = pathlib.Path.cwd()
code_dir = pathlib.Path(__file__).parent
cache_dir = data_dir.joinpath('cache')
logging.info(f"cache_dir: {cache_dir}")
prod = os.environ.get('GITHUB_ACTIONS')
now = datetime.datetime.utcnow().replace(microsecond=0)

#print(data_dir)
#print(code_dir)

class JsonError(Exception):
    pass

def read_course_json():
    with data_dir.joinpath('course.json').open() as fh:
        return json.load(fh)

def load_cache(name):
    path = cache_dir.joinpath(f'{name}.json')
    logging.info(f"load_cache({path})")
    cache = {}
    if path.exists():
        with path.open() as fh:
            cache = json.load(fh)
    return cache

def save_cache(name, cache):
    path = cache_dir.joinpath(f'{name}.json')
    with path.open('w') as fh:
        json.dump(cache, fh)

def update_devto_posts(people):
    cache = load_cache('forem')

    for person in people:
        if 'posts' not in person:
            continue
        for page in person['posts']:
            url = page['url']
            if url not in cache:
                cache[url] = forem.fetch(url)
                time.sleep(0.2) # self imposed rate limit
            page['details'] = cache[url]

    save_cache('forem', cache)


def check_projects(people):
    for person in people:
        if 'projects' not in person:
            continue
        for url in person['projects']:
            url_type = check_project(url)
            if not url_type:
                logging.error(f"Invalid project '{url}' by {person['name']} github='{person['github']}'")
                exit(f"Invalid project '{url}' by {person['name']} github='{person['github']}'")

def check_project(url):
    match = re.search('^https://github.com/([^/]+)$', url)
    if match:
        return 'github_organization'

    match = re.search('^https://github.com/([^/]+)/([^/]+)$', url)
    if match:
        return 'github_repo'

    match = re.search('^https://foss.heptapod.net/([^/]+)/([^/]+)$', url)
    if match:
        return 'heptapod_repo'


def update_github_data(people):
    cache = load_cache('github_people')
    for person in people:
        github_id = person['github']
        if github_id not in cache:
            cache[github_id] = github.get_user_info(github_id)
            time.sleep(0.2) # self imposed rate limit
        person['gh'] = cache[github_id]
    save_cache('github_people', cache)

def render(template, filename, **args):
    templates_dir = pathlib.Path(__file__).parent.joinpath('templates')
    env = Environment(loader=FileSystemLoader(templates_dir), autoescape=True)
    html_template = env.get_template(template)
    html_content = html_template.render(**args)
    with open(filename, 'w') as fh:
        fh.write(html_content)


def read_json_files(folder):
    people = []
    for filename in os.listdir(folder):
        if filename == '.gitkeep':
            continue
        if not filename.endswith('.json'):
           raise JsonError("file does not end with .json")
        if filename != filename.lower():
            raise Exception(f"filename {filename} should be all lower-case")
        with folder.joinpath(filename).open() as fh:
            person = json.load(fh)

        if 'github' not in person:
            raise Exception(f"github field is missing from {filename}")
        if person['github'].lower() != filename[:-5]:
            raise Exception(f"value of github fields '{person['github']}' is not the same as the filename '{filename}'")


        people.append(person)
    return people

def check_github_acc_for_participant(url: str) -> bool:
    logging.info(url)
    # params: URL of the participant for github.
    headers = {'Accept-Encoding': 'gzip, deflate'}
    r = requests.head(url, headers=headers)
    return r.status_code == requests.codes.ok

def collect_posts(people):
    posts = []
    for person in people:
        if 'posts' in person:
            for post in person['posts']:
                if post['details']:
                    post['details']['author'] = person
                    posts.append(post['details'])
                else:
                    posts.append({
                        'url': post['url'],
                        'title': post['title'],
                        'description': '',
                        'author': person,
                        'published_at': post['published_at'],
                    })
    posts.sort(key=lambda post: post['published_at'], reverse=True)
    return posts

def main():
    logging.info("Starting to generate site")

    mentors = read_json_files(data_dir.joinpath('mentors'))
    participants = read_json_files(data_dir.joinpath('participants'))
    course = read_course_json()

    out_dir = site_dir = data_dir.joinpath("_site")
    out_dir.mkdir(exist_ok=True)

    cache_dir.mkdir(exist_ok=True)
    if not prod:
        out_dir = out_dir.joinpath(course['id'])
        out_dir.mkdir(exist_ok=True)

    out_dir.joinpath("p").mkdir(exist_ok=True)
    if not prod:
        with site_dir.joinpath('index.html').open('w') as fh:
            fh.write(f'<a href="{course["id"]}/">{course["id"]}</a>')

    update_devto_posts(mentors)
    update_devto_posts(participants)
    update_github_data(mentors)
    update_github_data(participants)

    check_projects(mentors)
    check_projects(participants)

    posts = collect_posts(mentors + participants)

    participants.sort(key=lambda person: person['name'])

    for person in mentors + participants:
        render('person.html', out_dir.joinpath('p', f'{person["github"].lower()}.html'),
            title = person['name'],
            mentors = mentors,
            participants = participants,
            course = course,
            person = person,
        )

    render('index.html', out_dir.joinpath('index.html'),
        mentors = mentors,
        participants = participants,
        course = course,
        title = course['title'],
    )
    render('articles.html', out_dir.joinpath('articles.html'),
        mentors = mentors,
        participants = participants,
        articles = posts,
        course = course,
        title = 'Articles',
    )

    render('about.html', out_dir.joinpath('about.html'),
        mentors = mentors,
        participants = participants,
        course = course,
        title = 'About',
        now = now,
    )


if __name__ == "__main__":
    main()


