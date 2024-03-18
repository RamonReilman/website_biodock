import subprocess

class Plip():
    def __init__(self, path_to_plip, path_to_pro):
        self.path_to_plip = path_to_plip
        self.path_to_pro = path_to_pro

    def run(self):
        path = "../../static/history/4zel.pdb/pro.pdb"
        subprocess.run(["python", "../../venv_website/lib/python3.10/site-packages/plip/plipcmd.py", "-f", path, "-p", "--peptides", "1 2 3"])

plip = Plip("pass", "lol")
plip.run()
