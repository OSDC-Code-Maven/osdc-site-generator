import os
import pathlib
import time
import pytest


@pytest.fixture(autouse = True, scope="function", params=["name"])
def generate(name):
    image = f"osdc-test-{str(time.time())}"
    os.system(f'docker build -t {image} .')
    token = os.environ.get('MY_GITHUB_TOKEN')
    os.system(f'docker run --rm -w /data --env MY_GITHUB_TOKEN={token} -v{os.getcwd()}/{name}:/data  {image}')
    yield
    os.system(f'docker rmi {image}')

@pytest.mark.parametrize("name", ["test1"])
def test_one(name):
    root = pathlib.Path(name)
    site = root.joinpath('_site')
    assert site.exists()
    assert site.joinpath('index.html').exists()
    pages = site.joinpath('osdc-skeleton')
    assert pages.exists()

    with pages.joinpath('about.html').open() as fh:
        html = fh.read()
    assert '<title>About</title>' in html

    with pages.joinpath('articles.html').open() as fh:
        html = fh.read()
    assert '<a href="https://dev.to/szabgab/open-source-development-courses-5d4b">Open Source Development Courses</a> by <a href="p/szabgab">Gabor Szabo</a><br>' in html


    with pages.joinpath('p/szabgab.html').open() as fh:
        html = fh.read()
    assert 'GitHub page of <a href="https://Szabgab.github.io/">Gabor Szabo</a><br>' in html
