import os
import pytest
from functions_used import clear_me



@pytest.mark.parametrize("img_path,expected", [
    ("img_path", not os.listdir("img_path"))
])

def test_clear_me(img_path, expected):
    found = clear_me(img_path)
    assert found == expected


#def test_clear_me(img_path):
#     assert clear_me(not os.listdir(img_path))