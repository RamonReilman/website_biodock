"""
MODULE DOCSTRING

"""
import os
import json
from shutil import rmtree

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
    Function that saves user-supplied settings from the form in 
    index.html, to the dock.in file.
    :param new_save_path_dock:  (str)
    :param rmsd_slider: ()
    :param dock_slider: ()
    type, explanation, and the default value if set), and the return value (type and explanation).
    FUNCTION DOCSTRING
    """
    with open(new_save_path_dock, 'r+', encoding="utf-8") as dock_file:
        lines = dock_file.readlines()

    with open(new_save_path_dock, 'w', encoding="utf-8") as dock_file_write:
        for i, line in enumerate(lines):

            if i == 4:
                dock_file_write.write(rmsd_slider + '\n')
                print(type(dock_slider))
                print(type(rmsd_slider))
                print(type(new_save_path_dock))

            elif i == 12:
                dock_file_write.write(dock_slider + '\n')

            else:
                dock_file_write.write(line)
