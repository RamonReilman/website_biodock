import subprocess
class Plip():
    """
    Class to represent the plip tool

    ...

    Attributes
    ----------
    path_to_pro : str
        path to pro.pdb file
    project_name : str
        project name, given for history

    Methods
    -------
    run():
        runs the plip

    """
    def __init__(self, path_to_pro, project_name):
        """
        Constructs all the necessary attributes for the tool

        Parameters
        ----------
        path_to_pro : str
            path to pro.pdb file
        project_name : str
            project name, given for history
        """

        self.path_to_pro = path_to_pro
        self.project_name = project_name
    def run(self):
        """
        Runs the plip tool via command line

        Returns
        -------
        None
        """

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
