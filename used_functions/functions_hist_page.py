"""
MODULE DOCSTRING

"""
import os
import json
from shutil import rmtree
import subprocess

def clear_me():
    """
    FUNCTION DOCSTRING
    """
    rmtree("templates/history")
    os.mkdir("templates/history")

    rmtree("static/history")
    os.mkdir("static/history")


def save_settings(save_dir, **kwargs):
    """
    FUNCTION DOCSTRING
    """
    json_object = json.dumps(kwargs, indent=4)
    with open(f"{save_dir}/settings.json", "w", encoding="utf-8") as settings_file:
        settings_file.write(json_object)

def load_settings(save_dir):
    """
    FUNCTION DOCSTRING
    """
    with open(f'{save_dir}/settings.json', "r", encoding="utf-8") as settings_file:
        data = json.load(settings_file)
        return data

def settings_dok_file(new_save_path_dock, rmsd_slider, dock_slider):
    """
    Function that saves user-supplied settings from the webtool form in 
    index.html, to the dock.in file.
    :param new_save_path_dock: path to dock.in (str)
    :param rmsd_slider: rmsd cutoff (dock.in setting) submitted by user in webtool form (str)
    :param dock_slider: no. of docking poses (dock.in setting) submitted by user in webtool form (str)

    """
    # opens original dock.in file and reads all lines 
    with open(new_save_path_dock, 'r+', encoding="utf-8") as dock_file:
        lines = dock_file.readlines()

    with open(new_save_path_dock, 'w', encoding="utf-8") as dock_file_write:
        # iterates through each line of original dock.in file
        for i, line in enumerate(lines):

            if i == 4:
                # replaces line 5 with user-input for rmsd_slider
                dock_file_write.write(rmsd_slider + '\n')

            elif i == 12:
                # replaces line 13 with user-input for no. of docking poses
                dock_file_write.write(dock_slider + '\n')

            else:
                # writes out lines from original dock.in file
                dock_file_write.write(line)


def mol2_to_ligands(path):

    # loops through files in path
    for file in os.listdir(path):

        # checks if it ends with mol2
        if file.endswith(".mol2"):
            # writes name to ligands file
            with open(f"{path}/ligands", "w", encoding="utf-8") as ligands_file:
                ligands_file.write(file)
