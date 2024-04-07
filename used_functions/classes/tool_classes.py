"""
A module containing all classes that allows the 3 tools (LePro, LeDock, PLIP) to 
be integrated into the webtool.

Classes
-------
LePro:
    A class representing the 'LePro' tool that generates dock.in and pro.pdb

Ledock:
    A class representing the 'LeDock' tool that generates a .dok file

Plip:
    A class representing the 'PLIP' tool for generating molecular images based off the .dok file


"""
import subprocess
import os
import string



class LePro:
    """
    Class that represents the 'LePro'-tool

    ...

    Attributes
    ----------
    - pdb_save_path : str
        path to user-submitted .pdb file
    - name_file : str
        user given session name, used for history
    - new_save_path_dock: str
        path that dock.in gets moved to, after it gets created in same dir as LePro

    Methods
    -------
    run():
        runs LePro and moves generated files to new location

    """

    def __init__(self, name_file, dir_path, lepro_path):
        self.name_file = name_file
        self.dir_path = dir_path
        self.lepro_path = lepro_path


    def run(self):
        """
        Runs LePro with the specified lepro installation path and the .pdb file path and
        moves the generated files to the specified locations.

            Parameters
            ----------
        - pdb_save_path : str
            path to user-submitted .pdb file
        - name_file : str
            user given session name, used for history
        - new_save_path_dock: str
            path that dock.in gets moved to, after it gets created in same dir as LePro
        - new_save_path_pro: str
            path that pro.pdb gets moved to, after it gets created in same dir as LePro
        - lepro_path: str
            path to LePro installation on PC

        """
        #functie toevoegen die input checkt
        #cwd toevoegen
        subprocess.run([self.lepro_path, self.name_file], check=True, cwd=self.dir_path)


    def __str__(self):
        return (f'LePro installation detected: {self.lepro_path}\n'
                f'PDB file received by LePro:{self.name_file},\n'
                'located in session: {self.dir_path}.')


class Ledock:
    """
    A class that runs ledock

    ...

    Attributes
    ----------
    path : the path to the directory housing the files you want to run ledock on
    dock_path : the path to the ledock executable

    Methods
    -------
    run(self):
        runs ledock on the correct files in the directory
    """
    def __init__(self, path, ledock_path):
        """
        Constructs all the necessary attributes for the Ledock object

        :param path: the path to the directory housing the files you want to run ledock on
        """
        self.path = path
        self.ledock_path = ledock_path

    def run(self):
        """
        modifies the dock_path to be able to access ledock from the directory in 
        static/history and runs ledock on the files in the self.path
        :return: creates the .dok file in the given directory
        """
       
        # runs ledock in the directory on the dock.in
        subprocess.run([f'{self.ledock_path}', 'dock.in'], cwd=f"{self.path}/", check=True)


    def __str__(self):
        """
        gives this return when printing this class
        :return: The path given when creating first creating the class
        """
        return (f"LeDock installation found {self.ledock_path}.\n"
                f"Generated .dok-file in {self.path}")


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
    img_n : int
        int that contains the number of images that need to be rendered.

    Methods
    -------
    run():
        runs the plip

    """
    def __init__(self, project_name, img_n, img_path):
        """
        Constructs all the necessary attributes for the tool

        Parameters
        ----------
        project_name : str
            project name, given for history
        img_n : int
            int that contains the number of images that need to be rendered.

        """

        self.output_location = img_path + project_name
        self.pro_pdb = f"{img_path}{project_name}/pro.pdb"
        self.img_n = img_n


    def run(self):
        """
        Runs the plip tool via command line

        Returns
        -------
        None
        """

        plip_path = subprocess.run(["find", "-name", "plipcmd.py"],
                                   check=True, capture_output=True, text=True)
        plip_path = plip_path.stdout.split("\n")
        plip_path = plip_path[0]
        command = ["python3", plip_path, "-f", self.pro_pdb, "-p", "-o", self.output_location,
                   "--peptides",]

        # Adds correct ligand chains to command
        alphabet = list(string.ascii_lowercase)
        for num in range(0, self.img_n):
            command.append(alphabet[num])

        # Runs tool
        subprocess.run(command, check=True)


    def __str__(self):
        return f"""Created images using the {self.pro_pdb} file,
                and saved these images in {self.output_location}"""