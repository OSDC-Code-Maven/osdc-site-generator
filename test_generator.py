import os
import pathlib
import shutil
import time
import pytest
import capture
import shlex


@pytest.fixture(autouse = False, scope="function", params=["name"])
def generate(name, tmpdir):
    image = f"osdc-test-{str(time.time())}"
    token = os.environ.get('MY_GITHUB_TOKEN')
    shutil.copytree(os.path.join(os.getcwd(), name), os.path.join(tmpdir, name))

    print(f"\n-------- building docker image {image} --------------")
    exit_code = os.system(f'docker build -t {image} .')
    if exit_code != 0:
        raise Exception("Failed to build docker image")

    print(f"\n-------- running docker container based on {image} --------------")
    cmd = f'docker run --rm -w /data --env MY_GITHUB_TOKEN={token} -v{tmpdir}/{name}:/data  {image}'
    exit_code, out, err = capture.separated(shlex.split(cmd))
    print(out)
    print(err)
    #if exit_code != 0:
    #    raise Exception("Failed to run the docker")

    yield {"exit_code": exit_code, "out": out, "err": err}

    print(f"\n--------removing docker image {image}")
    exit_code = os.system(f'docker rmi {image}')
    if exit_code != 0:
        raise Exception("Failed to remove docker image")

@pytest.mark.parametrize("name", ["test1"])
def test_one(name, tmpdir, generate):
    print(f"in test: {generate}")
    assert generate['exit_code'] == 0
    root = pathlib.Path(tmpdir).joinpath(name)
    site = root.joinpath('_site')
    assert site.exists()
    assert site.joinpath('index.html').exists()
    pages = site.joinpath('osdc-skeleton')
    assert pages.exists()

    print(pages.joinpath('about.html'))
    with pages.joinpath('about.html').open() as fh:
        html = fh.read()
    assert '<title>About</title>' in html

    with pages.joinpath('articles.html').open() as fh:
        html = fh.read()
    assert '<a href="https://dev.to/szabgab/open-source-development-courses-5d4b">Open Source Development Courses</a> by <a href="p/szabgab">Gabor Szabo</a><br>' in html


    with pages.joinpath('p/szabgab.html').open() as fh:
        html = fh.read()
    assert 'GitHub page of <a href="https://Szabgab.github.io/">Gabor Szabo</a><br>' in html

@pytest.mark.parametrize("name", ["test2"])
def test_two(name, generate):
    print(f"in test: {generate}")
    assert generate["exit_code"] == 1
    assert "ERROR: Exception: value of github fields 'other-demo' is not the same as the filename 'cm-demo.json'" in generate["err"]
    assert "There were 1 errors" in generate["err"]

