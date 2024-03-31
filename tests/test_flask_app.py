"""
PyTest script for testing the flask app (as seen in run_app.py)
    - Authors: Ramon Reilman, Stijn Vermeulen, Yamila Timmer

test_flask_app.py tests the following things:
    - whether rendering the templates yields a 200 response code (OK/success status)
    - whether the source code when rendering the templates is valid

Usage:
    Run pytest to test the used functions, using this script.

Commandline usage: 
    - pytest

"""
import pytest
import html5lib
from run_app import app


@pytest.fixture
def client():
    """
    Fixture to create a test client for the Flask app
    """
    return app.test_client()

@pytest.mark.parametrize("urls", [
    "/",
    "/history",
    "/about",
    "/ourteam"
])


def test_get(client, urls):
    """
    Tests if GET requests to different urls return a 200 status code (succes)

    :param client: test client for Flask app
    :param urls: URLs for testing different templates (str)
    """
    response = client.get(urls)
    assert response.status_code == 200

@pytest.mark.parametrize("uri, inputs", [
    ("/", True),
    ("/history", False),
    ("/about", False),
    ("/ourteam", False)
])


def test_html_valid(client, uri, inputs):
    """
    Test if the sourcecode from specified URLs is valid HTML5
    :param client:
    :param uri:
    :param inputs:
    """
    response = client.get(uri)
    assert response.status_code == 200

    try:
        parse = html5lib.HTMLParser(strict=True, namespaceHTMLElements=False)
        htmldoc = parse.parse(response.data)

    except html5lib.html5parser.ParseError as error:
        pytest.fail(f"{error.__class__.__name__}: {str(error)}", pytrace=False)

    forms = htmldoc.findall("./body/div/form")

    if inputs:
        assert len(forms) == 1
        form = forms[0]
        names = set()

        for inp in form.iter('input'):
            print(list(inp.attrib.items()))
            names.add(inp.attrib['name'])

        assert names == {"pdb_file", "mol2_file", "dock_slider", "RMSD_slider", \
                         "name_file", "project_name"}
