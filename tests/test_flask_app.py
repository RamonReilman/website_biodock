from run_app import app
import io
import os
import time
from pathlib import Path
from used_functions.functions_used import parse_config
import html5lib
import shutil
import pytest

het_pad = Path(__file__).parent / "resources"


def client():
    """
    creates a client to run the webserver through
    :return: the client to run the webserver
    """
    return app.test_client()


all_files = ["4zel.pdb", "pytest.mol2", "new_169196800.mol2", "lig.mol2",
             "error.pdb", "error.mol2", "empty.pdb", "empty.mol2"]

opened_files = []

for file in all_files:
    # opens the file and puts it in the file list
    with open(het_pad / file, 'r', encoding="utf-8") as open_file:
        opened_files.append(open_file.read())

config_path = parse_config()
img_path = config_path['paths']['img_path']


def test_index(client):
    """
    activates the predefined client
    :param client: the client created in the client() function
    """
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.parametrize("data, verwacht", [

    # tests a wrong data file given
    ({
        "dock_slider": 12,
        "RMSD_slider": 1,
        "name_file": "tester",
        "pdb_file": (io.BytesIO(b"Data"), "test.txt"),
        "mol2_file": (io.BytesIO(b"Mol2 informatie"), "dsafsaf.mol2")}, 415),

    # tests s a basic data set
    ({
        "dock_slider": 12,
        "RMSD_slider": 1,
        "name_file": "-check",
        "pdb_file": (io.BytesIO(opened_files[0].encode('utf-8')), "4zel.pdb"),
        "mol2_file": (io.BytesIO(opened_files[2].encode("utf-8")), "dopa.mol2")}, 302),

    # tests files that are borderline small enough to pass
    ({
        "dock_slider": 20,
        "RMSD_slider": 0.5,
        "name_file": '12345678901234567890',
        "pdb_file": (io.BytesIO(opened_files[0].encode('utf-8')), "4zel.pdb"),
        "mol2_file": (io.BytesIO(opened_files[2].encode("utf-8")), "new_169196800.mol2")}, 302),

    # tests when a repeat name is given
    # NOTE: the test now expects that a test dir named 4zel.pdb exists if the file is removed,
    # this name should be replaced
    ({
        "dock_slider": 20,
        "RMSD_slider": 0.5,
        "name_file": '12345678901234567890',
        "pdb_file": (io.BytesIO(opened_files[0].encode('utf-8')), "4zel.pdb"),
        "mol2_file": (io.BytesIO(opened_files[2].encode("utf-8")), "new_169196800.mol2")}, 200),

    # tests if a input is refused if the mol2 file is too big
    ({
        "dock_slider": 20,
        "RMSD_slider": 0.5,
        "name_file": 'TooBig',
        "pdb_file": (io.BytesIO(opened_files[0].encode('utf-8')), "4zel.pdb"),
        "mol2_file": (io.BytesIO(opened_files[3].encode("utf-8")), "lig.mol2")}, 415),

    # test if a file is refused if the given dir name has characters that can intercept with code
    ({
        "dock_slider": 12,
        "RMSD_slider": 1,
        "name_file": '!@#$%^&*()[]/\\`~\'',
        "pdb_file": (io.BytesIO(opened_files[0].encode('utf-8')), "4zel.pdb"),
        "mol2_file": (io.BytesIO(opened_files[2].encode("utf-8")), "dopa.mol2")}, 200),

    # tests a corrupted file (a file that can't run because it has changes made to the source)
    ({
        "dock_slider": 2,
        "RMSD_slider": 4.0,
        "name_file": 'corrupt',
        "pdb_file": (io.BytesIO(opened_files[4].encode('utf-8')), "error.pdb"),
        "mol2_file": (io.BytesIO(opened_files[5].encode("utf-8")), "error.mol2")}, 500),

    # tests if empty files are given
    ({
        "dock_slider": 20,
        "RMSD_slider": 0.5,
        "name_file": 'empty',
        "pdb_file": (io.BytesIO(opened_files[6].encode('utf-8')), "empty.pdb"),
        "mol2_file": (io.BytesIO(opened_files[7].encode("utf-8")), "empy.mol2")}, 500)
]
)
def test_index_post(client, data, verwacht):
    """
    takes the data and puts it through the tools and the response code is checked,
    while this happends the time of the docking is taken and checked if it takes too long
    """
    name = data['name_file']

    # start timer to check if the docking doesn't take too long
    start = time.time()

    response = client.post("/", data=data)

    # checks if the status code is correct
    assert response.status_code == verwacht

    # calculates time passed
    end = time.time()
    time_passed = start - end

    # removes the directory created in the test run
    if name in os.listdir(img_path) and name != "4zel.pdb":
        path_to_remove = os.path.join(img_path, name)
        shutil.rmtree(path_to_remove)

    # if too much time has passed it returns a fail
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



