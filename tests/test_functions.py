"""
MODULE DOCSTRING
"""
import os
import json
from used_functions.functions_used import clear_me, save_settings


def test_clear_me():
    """
    Tests clear_me() function.
    """
  
    # creates a temporary directory
    tmp_img_path = 'static/history'

    # create a temporary file within the directory
    tmp_path = os.path.join(tmp_img_path, 'file.pdb')
    with open(tmp_path, 'w', encoding='utf-8') as tmp_file:
        tmp_file.write('PDB content')

    # checks if the created temporary file exists
    assert os.path.exists(tmp_path)

    # calls clear_me() function
    clear_me(tmp_img_path)

    # checks if the the file has been removed
    assert not os.path.exists(tmp_path)

    # checks if the directory is empty
    assert not os.listdir(tmp_img_path)

def test_save_settings():
    """
    Tests save_settings() function.
    """

    # initiates needed variables
    json_object = {"a": 1, "b": 2, "c": 3}
    img_path = 'static/history'
    save_dir = os.path.join(img_path, 'name_file')

    # makes dir
    os.makedirs(save_dir, exist_ok=True)

    # checks if dir exists
    assert os.path.exists(save_dir)

    # runs function
    save_settings(save_dir, **json_object)

    with open(f"{save_dir}/settings.json", "r", encoding="utf-8") as settings_file:
        json_file = json.load(settings_file)

    # checks if the saved data matches the original data
    assert json_file == json_object

def test_load_settings():
    