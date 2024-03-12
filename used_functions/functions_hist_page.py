import os
from shutil import rmtree

def clear_me():
    rmtree("templates/history")
    os.mkdir("templates/history")

    rmtree("static/history")
    os.mkdir("static/history")

