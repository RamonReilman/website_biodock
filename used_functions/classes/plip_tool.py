import subprocess
class Plip():
    def __init__(self, path_to_pro, project_name):
        self.path_to_pro = path_to_pro
        self.project_name = project_name


    def run(self):

        plip_path = subprocess.run(["find", "-name", "plipcmd.py"],
                                   check=True, capture_output=True, text=True)
        plip_path = plip_path.stdout.strip()
        path = f"static/history/{self.project_name}/pro.pdb"
        print(path, plip_path)
        subprocess.run(["python3", plip_path, "-f", path, "-p", "--peptides",
                        "1","2", "3", "-o", f"static/history/{self.project_name}"], check=True)

    def __str__(self):
        return f"""Creates images using the {self.path_to_pro} file,
                and saves these images in static/history/{self.project_name}"""

plip = Plip("static/history/4zel.pdb/pro.pdb","4zel.pdb")
plip.run()
