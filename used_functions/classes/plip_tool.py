import subprocess
class Plip():
    """
    Class to represent the plip tool

    ...

    Attributes
    ----------
    output_lccation : str
        path to where images will be saved
    pro_pdb : str
        The path to pro.pdb file

    Methods
    -------
    run():
        runs the plip

    """
    def __init__(self, project_name):
        """
        Constructs all the necessary attributes for the tool

        Parameters
        ----------
        project_name : str
            project name, given for history

        """

        self.output_location = f"static/history/{project_name}"
        self.pro_pdb = f"static/history/{project_name}/pro.pdb"
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
        subprocess.run(["python3", plip_path, "-f", self.pro_pdb, "-p", "--peptides",
                        "1", "2", "3", "-o", self.output_location], check=True)

    def __str__(self):
        return f"""Creates images using the {self.pro_pdb} file,
                and saves these images in {self.output_location}"""