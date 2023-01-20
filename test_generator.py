import pathlib

def test_one():
    root = pathlib.Path('test1')
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
