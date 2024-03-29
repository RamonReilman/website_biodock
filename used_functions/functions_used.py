"""
Used functions for run_app.py
    - Authors: Ramon Reilman, Stijn Vermeulen, Yamila Timmer

This module provides functions for managing settings, files, and directories
related to the BioDock Visualiser webtool.

Functions:
    -   clear_me()
        Function that deletes the session history of the webtool

    -   save_settings(save_dir, **kwargs)
        Saves user specified settings to .json_file

    -   load_settings(save_dir)
        Retrieves saved settings, to be viewed again in temp.html through history page
    
    -   settings_dok_file(new_save_path_dock, rmsd_slider, dock_slider)
        Saves user specified settings from webtool form to dock.in file
    
    -   mol2_to_ligands(path)
        Writes name of .mol2 file to a 'ligands' file.


"""
import os
import json
from shutil import rmtree
import configparser


def clear_me(img_path):
    """
    This function deletes the history ("static/history") folder and makes a new 
    folder with the same name.

    """

    rmtree(img_path)
    os.mkdir(img_path)


def save_settings(save_dir, **kwargs):
    """
    Saves user specified settings from webtool page (dock_slider, RMSD_slider and name_file)
    as a JSON file in the specified dir.
    :param save_dir: dir path in which the .json-file gets created.
    :param **kwargs: keyword arguments for the settings

    """
    # converts keyword arguments into json formatted string
    json_object = json.dumps(kwargs, indent=4)

    # creates a file in write mode with the path "{save_dir}/settings.json"
    with open(f"{save_dir}/settings.json", "w", encoding="utf-8") as settings_file:
        settings_file.write(json_object)

        return json_object


def load_settings(save_dir):
    """
     Loads settings from a JSON file, uses this for retrieving settings from a previous session,
     used for temp.html

    :param save_dir: dir path in which settings.json is located (str)

    :return data: a dict containing the saved settings (dock_slider, RMSD_slider and name_file)

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
    :param dock_slider: no. of docking poses (dock.in setting) submitted by user in 
        webtool form (str)

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

    return new_save_path_dock

def mol2_to_ligands(path):
    """
    Writes name of .mol2 file
     to a 'ligands' file.

    :param path: dir path to .mol2-file (str)
        
    """

    # loops through files in path
    for file in os.listdir(path):

        # checks if file ends with .mol2
        if file.endswith(".mol2"):
            path = path.join('ligands')

            # writes name of .mol2 file to ligands file
            with open(path, "w", encoding="utf-8") as ligands_file:
                ligands_file.write(file)
    return path


def parse_config():
    """
    Reads the config.ini file and parses it
    
    return parser: object containing all information from the config.ini file.
    """
    parser = configparser.ConfigParser()
    parser.read("used_functions/config.ini")
    return parser
