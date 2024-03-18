import subprocess
from time import sleep
import os
class Plip():
    def __init__(self, venv_path, path_to_pro, project_name):
        self.path_to_venv = venv_path
        self.path_to_pro = path_to_pro
        self.project_name = project_name
        

    def run(self):
        path = f"static/history/{self.project_name}/pro.pdb"
        subprocess.run(["python3", f"{self.path_to_venv}/lib/python3.11/site-packages/plip/plipcmd.py", "-f", path, "-p", "--peptides", "1","2", "3", "-o", f"static/history/{self.project_name}"])

    def __str__(self):
        return f"Creates images using the {self.path_to_pro} file, and saves these images in static/history/{self.project_name}"