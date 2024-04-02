from run_app import app
import io
import os
import time
from pathlib import Path
from used_functions.functions_used import parse_config

import shutil
import pytest

het_pad = Path(__file__).parent / "resources"
@pytest.fixture
def client():
    return app.test_client()

# opens a normal pdb file
with open(het_pad / "4zel.pdb", 'r', encoding="utf-8") as pdb_file:
    pdb_test_file = pdb_file.read()

# opens a pdb file with some incorrect parts
with open(het_pad / "error.pdb", 'r', encoding="utf-8") as pdb_file:
    pdb_test_error_file = pdb_file.read()

# opens a normal mol2 file
with open(het_pad / "pytest.mol2", 'r', encoding="utf-8") as mol2_file:
    mol2_test_file = mol2_file.read()

# opens a mol2 file near the max file size
with open(het_pad / "new_169196800.mol2", 'r', encoding="utf-8") as mol2_file:
    big_mol2_test_file = mol2_file.read()

with open(het_pad / "error.mol2", 'r', encoding="utf-8") as mol2_file:
    mol2_error_test_file = mol2_file.read()

# opens a empty file with pdb extention
with open(het_pad / "empty.pdb", 'r', encoding="utf-8") as pdb_file:
    pdb_empty_test_file = pdb_file.read()

# opens a empty file
with open(het_pad / "empty.mol2", 'r', encoding="utf-8") as mol2_file:
    mol2_empty_test_file = mol2_file.read()

# opens a mol2 file over the max file limit
with open(het_pad / "lig.mol2", 'r', encoding="utf-8") as mol2_file:
    mol2_toobig_test_file = mol2_file.read()

config_path = parse_config()
img_path = config_path['paths']['img_path']



def test_index(client):

    response = client.get("/")
    assert response.status_code == 200



@pytest.mark.parametrize("data, verwacht",[
    (dict(dock_slider=12, RMSD_slider=1, name_file='tester',
           pdb_file=(io.BytesIO(b"Data"), "test.txt"),
           mol2_file=(io.BytesIO(b"Mol2 informatie"), "dsafsaf.mol2")), 415),
    (dict(dock_slider=12, RMSD_slider=1, name_file='-check',
           pdb_file=(io.BytesIO(pdb_test_file.encode('utf-8')), "4zel.pdb"),
           mol2_file=(io.BytesIO(mol2_test_file.encode("utf-8")), "dopa.mol2")), 302),
    # takes a long time
    (dict(dock_slider=20, RMSD_slider=0.5, name_file='12345678901234567890',
           pdb_file=(io.BytesIO(pdb_test_file.encode('utf-8')), "4zel.pdb"),
           mol2_file=(io.BytesIO(big_mol2_test_file.encode("utf-8")), "new_169196800.mol2")), 302),
    # gets a repeat name so should work and be short 
    # NOTE: the repeat name in this example is 4zel.pdb IF THIS DIRECTORY IS REMOVED THE NAME SHOULD BE REPLACED WITH A DIFFERENT TEST DIRECTORY
    (dict(dock_slider=20, RMSD_slider=0.5, name_file='4zel.pdb',
           pdb_file=(io.BytesIO(pdb_test_file.encode('utf-8')), "4zel.pdb"),
           mol2_file=(io.BytesIO(big_mol2_test_file.encode("utf-8")), "new_169196800.mol2")), 200),
    # too big mol2 file
    (dict(dock_slider=20, RMSD_slider=0.5, name_file='TooBig',
           pdb_file=(io.BytesIO(pdb_test_file.encode('utf-8')), "4zel.pdb"),
           mol2_file=(io.BytesIO(mol2_toobig_test_file.encode("utf-8")), "lig.mol")), 415),
    # gives wrong status code since the minimum file name lenght check happens before this gets executed
    # (dict(dock_slider=1, RMSD_slider=4.0, name_file='1',
    # pdb_file=(io.BytesIO(pdb_test_file.encode('utf-8')), "4zel.pdb"),
    # mol2_file=(io.BytesIO(big_mol2_test_file.encode("utf-8")), "new_169196800.mol2")), 200),
    # gets held because of name
    (dict(dock_slider=12, RMSD_slider=1, name_file='!@#$%^&*()[]/\\`~\'',
           pdb_file=(io.BytesIO(pdb_test_file.encode('utf-8')), "4zel.pdb"),
           mol2_file=(io.BytesIO(mol2_test_file.encode("utf-8")), "dopa.mol2")), 200),
    # gives error because files are corrupted
    (dict(dock_slider=2, RMSD_slider=4.0, name_file='corrupt',
           pdb_file=(io.BytesIO(pdb_test_error_file.encode('utf-8')), "error.pdb"),
           mol2_file=(io.BytesIO(mol2_error_test_file.encode("utf-8")), "error.mol2")), 500),
    # gives error because the files are empty
    (dict(dock_slider=20, RMSD_slider=0.5, name_file='empty',
           pdb_file=(io.BytesIO(pdb_empty_test_file.encode('utf-8')), "empty.pdb"),
           mol2_file=(io.BytesIO(mol2_empty_test_file.encode("utf-8")), "empy.mol2")), 500)
])

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


