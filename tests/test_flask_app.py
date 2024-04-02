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
import io
import time
from pathlib import Path
import pytest
import html5lib
from run_app import app


path = Path(__file__).parent / "resources"
@pytest.fixture
def client():
    """
    DOCSTRING
    """

    return app.test_client()

# opens a normal pdb file
with open(path / "4zel.pdb", 'r', encoding="utf-8") as pdb_file:
    pdb_test_file = pdb_file.read()

# opens a pdb file with some incorrect parts
with open(path / "error.pdb", 'r', encoding="utf-8") as pdb_file:
    pdb_test_error_file = pdb_file.read()

# opens a normal mol2 file
with open(path / "pytest.mol2", 'r', encoding="utf-8") as mol2_file:
    mol2_test_file = mol2_file.read()

# opens a mol2 file near the max file size
with open(path / "new_169196800.mol2", 'r', encoding="utf-8") as mol2_file:
    big_mol2_test_file = mol2_file.read()

with open(path / "error.mol2", 'r', encoding="utf-8") as mol2_file:
    mol2_error_test_file = mol2_file.read()

# opens a empty file with pdb extention
with open(path / "empty.pdb", 'r', encoding="utf-8") as pdb_file:
    pdb_empty_test_file = pdb_file.read()

# opens a empty file
with open(path / "empty.mol2", 'r', encoding="utf-8") as mol2_file:
    mol2_empty_test_file = mol2_file.read()

# opens a mol2 file over the max file limit
with open(path / "lig.mol2", 'r', encoding="utf-8") as mol2_file:
    mol2_toobig_test_file = mol2_file.read()


def test_index(client):
    """
    DOCSTRING
    """

    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.parametrize("data, expected",[
    ({
        "dock_slider": 12,
        "RMSD_slider": 1,
        "name_file": "tester",
        "pdb_file": (io.BytesIO(b"Data"), "test.txt"),
        "mol2_file": (io.BytesIO(b"Mol2 informatie"), "dsafsaf.mol2")}, 415),

    ({
        "dock_slider": 12,
        "RMSD_slider": 1,
        "name_file": "-check",
        "pdb_file": (io.BytesIO(pdb_test_file.encode('utf-8')), "4zel.pdb"),
        "mol2_file": (io.BytesIO(mol2_test_file.encode("utf-8")), "dopa.mol2")}, 302),

    ({
        "dock_slider": 20,
        "RMSD_slider": 0.5,
        "name_file": '12345678901234567890',
        "pdb_file": (io.BytesIO(pdb_test_file.encode('utf-8')), "4zel.pdb"),
        "mol2_file": (io.BytesIO(big_mol2_test_file.encode("utf-8")), \
                      "new_169196800.mol2")}, 302),

    ({
        "dock_slider": 20,
        "RMSD_slider": 0.5,
        "name_file": '12345678901234567890',
        "pdb_file": (io.BytesIO(pdb_test_file.encode('utf-8')), "4zel.pdb"),
        "mol2_file": (io.BytesIO(big_mol2_test_file.encode("utf-8")), "new_169196800.mol2")}, 200),

    ({
        "dock_slider": 20,
        "RMSD_slider": 0.5,
        "name_file": 'TooBig',
        "pdb_file": (io.BytesIO(pdb_test_file.encode('utf-8')), "4zel.pdb"),
        "mol2_file": (io.BytesIO(mol2_toobig_test_file.encode("utf-8")), "lig.mol")}, 415),

    ({
        "dock_slider": 12,
        "RMSD_slider": 1,
        "name_file": '!@#$%^&*()[]/\\`~\'',
        "pdb_file": (io.BytesIO(pdb_test_file.encode('utf-8')), "4zel.pdb"),
        "mol2_file": (io.BytesIO(mol2_test_file.encode("utf-8")), "dopa.mol2")}, 200),

    ({
        "dock_slider": 2,
        "RMSD_slider": 4.0,
        "name_file": 'corrupt',
        "pdb_file": (io.BytesIO(pdb_test_error_file.encode('utf-8')), "error.pdb"),
        "mol2_file": (io.BytesIO(mol2_error_test_file.encode("utf-8")), "error.mol2")}, 500),

    ({
        "dock_slider": 20,
        "RMSD_slider": 0.5,
        "name_file": 'empty',
        "pdb_file": (io.BytesIO(pdb_empty_test_file.encode('utf-8')), "empty.pdb"),
        "mol2_file": (io.BytesIO(mol2_empty_test_file.encode("utf-8")), "empy.mol2")}, 500)
]
)


def test_index_post(client, data, expected):
    """
    takes the data and puts it through the tools and the response code is checked,
    while this happends the time of the docking is taken and checked if it takes too long
    """
    # start timer to check if the docking doesn't take too long
    start = time.time()

    response = client.post("/", data=data)

    assert response.status_code == expected
    end = time.time()

    time_passed = start - end

    assert time_passed < 10


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
