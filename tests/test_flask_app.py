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


@pytest.mark.parametrize("url, inputs", [
    ("/", True),
    ("/history", False),
    ("/about", False),
    ("/ourteam", False)
])


def test_html_valid(client, url, inputs):
    """
    Test if GET requests to different URLs return a 200 status code (success)
    and whether the sourcecode from those URLs is valid HTML5
    :param client: test client for Flask app
    :param url: URLs for testing different templates (str)
    :param inputs: whether the template expects input (bool)
    """

    # checks if get.request returns a 200 status code (success)
    response = client.get(url)
    assert response.status_code == 200

    # tries to check if source code is valid HTML5
    try:
        parse = html5lib.HTMLParser(strict=True, namespaceHTMLElements=False)
        htmldoc = parse.parse(response.data)

    # fails the pytest if source code is not valid HTML5 and returns error
    except html5lib.html5parser.ParseError as error:
        pytest.fail(f"{error.__class__.__name__}: {str(error)}", pytrace=False)

    forms = htmldoc.findall("./body/div/form")

    # if-statement for when inputs = True (on '/' URL)
    if inputs:
        # checks if the amount of forms found is equal to 1
        assert len(forms) == 1

        form = forms[0]
        names = set()

        for inp in form.iter('input'):
            print(list(inp.attrib.items()))
            names.add(inp.attrib['name'])

        # checks if the form contains the following attributes
        assert names == {"pdb_file", "mol2_file", "dock_slider", "RMSD_slider", \
                         "name_file", "project_name"}
