import pytest

from run_app import app
import io
from pathlib import Path
het_pad = Path(__file__).parent / "resources"
@pytest.fixture
def client():
    return app.test_client()

with open(het_pad / "4zel.pdb", 'r', encoding="utf-8") as pdb_file:
    pdb_test_file = pdb_file.read()

with open(het_pad / "pytest.mol2", 'r', encoding="utf-8") as mol2_file:
    mol2_test_file = mol2_file.read()
def test_index(client):

    response = client.get("/")
    assert response.status_code == 200

@pytest.mark.parametrize("data, verwacht",[
    (dict(dock_slider=12, RMSD_slider=1, name_file='tester', pdb_file=(io.BytesIO(b"Data"), "test.txt"), mol2_file=(io.BytesIO(b"Mol2 informatie"), "dsafsaf.mol2")), 415),
    (dict(dock_slider=12, RMSD_slider=1, name_file='-check', pdb_file=(io.BytesIO(pdb_test_file.encode('utf-8')), "4zel.pdb"), mol2_file=(io.BytesIO(mol2_test_file.encode("utf-8")), "dopa.mol2")), 200)
])
def test_index_post(client, data, verwacht):
    name_file = data["name_file"]

    response = client.post("/", data=data)
    assert response.status_code == verwacht