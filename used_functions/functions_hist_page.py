import os, json
from shutil import rmtree

def clear_me():
    rmtree("templates/history")
    os.mkdir("templates/history")

    rmtree("static/history")
    os.mkdir("static/history")


def save_settings(save_dir, **kwargs):
    name_file = kwargs["name_file"]
    json_object = json.dumps(kwargs, indent=4)
    with open(f"{save_dir}/settings.json", "w") as settings_file:
        settings_file.write(json_object)

def load_settings(save_dir):
    with open(f'{save_dir}/settings.json', "r") as settings_file:
        data = json.load(settings_file)
        return data

