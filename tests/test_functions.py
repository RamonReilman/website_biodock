"""
PyTest script for functions_used.py
    - Authors: Ramon Reilman, Stijn Vermeulen, Yamila Timmer

test_functions.py tests the following functions from functions_used.py:
    - clear_me()
    - save_settings()
    - load_settings()
    - settings_dok_file()
    - mol2_to_ligands()

Usage:
    Run pytest to test the used functions, using this script.

Commandline usage: 
    - pytest


"""
import os
import json
from used_functions.functions_used import clear_me, save_settings, load_settings, \
    settings_dok_file, mol2_to_ligands


def test_clear_me(tmpdir):
    """
    Tests clear_me() function.

    :param tmpdir: creates a temporary dir to 'recreate' the original path
    """

    # create a temporary file within the directory
    tmp_path = tmpdir.join('file.pdb')
    with open(tmp_path, 'w', encoding='utf-8') as tmp_file:
        tmp_file.write('PDB content')

    # checks if the created temporary file exists
    assert os.path.exists(tmp_path)

    # calls clear_me() function
    clear_me(tmpdir)

    # checks if the the file has been removed
    assert not os.path.exists(tmp_path)

    # checks if the directory is empty
    assert not os.listdir(tmpdir)


def test_save_settings(tmpdir):
    """
    Tests save_settings() function.

    :param tmpdir: creates a temporary dir to 'recreate' the original path
    """

    # initiates needed variables
    json_object = {"a": 1, "b": 2, "c": 3}
    tmpdir.join('name_file')

    # makes dir
    os.makedirs(tmpdir, exist_ok=True)

    # checks if dir exists
    assert os.path.exists(tmpdir)

    # runs function
    save_settings(tmpdir, **json_object)

    with open(f"{tmpdir}/settings.json", "r", encoding="utf-8") as settings_file:
        json_file = json.load(settings_file)

    # checks if the saved data matches the original data
    assert json_file == json_object


def test_load_settings(tmpdir):
    """
    Tests load_settings function.
    
    :param tmpdir: creates a temporary dir to 'recreate' the original path
    """

    json_object = {"a": 1, "b": 2, "c": 3}
    saved_data = json.loads(save_settings(tmpdir, **json_object))
    loaded_data = load_settings(tmpdir)

    # checks if data from save_settings function is equal to data in load_settings
    assert saved_data == loaded_data


def test_settings_dok_file():
    """
    Tests settings_dok_file function.
    """
    # defines needed variables
    rmsd_slider = '2.5'
    dock_slider = '18'

    # calls settings_dok_file function in which the dock.in file gets changed based on attributes
    new_save_path_dock = settings_dok_file(new_save_path_dock='tests/dock.in', \
                                           rmsd_slider=rmsd_slider, dock_slider=dock_slider)

    # opens dock.in and asserts if lines 4 and 12 got changed to the given values
    with open(new_save_path_dock, 'r', encoding="utf-8") as dock_file_read:
        lines = dock_file_read.readlines()
        assert lines[4].strip() == rmsd_slider
        assert lines[12].strip() == dock_slider

    # reverts changes in dock.in file, so it's ready for future testing
    with open(new_save_path_dock, 'w', encoding="utf-8") as dock_file_read:
        for i, line in enumerate(lines):
            if i == 4:
                dock_file_read.write('1.0' + '\n')
            elif i == 12:
                dock_file_read.write('20' + '\n')
            else:
                dock_file_read.write(line)


def test_mol2_to_ligands():
    """
    Tests mol2_to_ligands function.
    
    """
    # defines needed variables for test
    path = mol2_to_ligands('tests')
    expected_content = ['test.mol2']

    # opens ligands file that got created by mol2_to_ligands function
    with open (f'{path}/ligands', 'r', encoding='utf-8') as ligands_file:
        content = ligands_file.readlines()

        # checks if the content of ligands_file is equal to the expected content (name of mol2 file)
        assert content == expected_content
