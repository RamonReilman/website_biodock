"""
MODULE DOCSTRING
"""
import pytest
import html5lib
from run_app import app


@pytest.fixture
def client():
    """
    DOCSTRING
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
    DOCSTRING
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
    DOCSTRING
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
