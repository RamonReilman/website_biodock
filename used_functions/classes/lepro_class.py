import subprocess
import os
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
    def __init__(self, pdb_save_path, name_file, new_save_path_dock):
        self.name_file = name_file
        self.pdb_save_path = pdb_save_path
        self.lepro_path = subprocess.run(["find", "-name", "lepro_linux_x86"], check=True,
                                    capture_output=True, text=True).stdout.strip()
        self.new_save_path_dock = new_save_path_dock
        self.new_save_path_pro = os.path.join("static/history/", self.name_file, "pro.pdb")

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
        subprocess.run([self.lepro_path, self.pdb_save_path], check=True)
        subprocess.run(["mv", "dock.in", self.new_save_path_dock], check=True)
        subprocess.run(["mv", "pro.pdb", self.new_save_path_pro], check=True)

    def __str__(self):
        return (f'LePro installation detected: {self.lepro_path}\n'
                f'PDB file received by LePro:{self.pdb_save_path}, \
                    located in session: {self.name_file}.\n'
                f'Generated dock.in location: {self.new_save_path_dock}\n'
                f'Generated pro.pdb location: {self.new_save_path_pro}\n')
