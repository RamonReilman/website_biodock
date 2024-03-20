import subprocess
import os
class LePro:
    """
    class docstring
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
        method docstring
        """
        subprocess.run([self.lepro_path, self.pdb_save_path], check=True)

    def mv_files(self):
        """
        method docstring
        """
        subprocess.run(["mv", "dock.in", self.new_save_path_dock], check=True)
        subprocess.run(["mv", "pro.pdb", self.new_save_path_pro], check=True)

    def __str__(self):

        return (f'LePro installation detected: {self.lepro_path}\n'
                f'PDB file received by LePro:{self.pdb_save_path}, located in session: {self.name_file}.\n'
                f'Generated dock.in location: {self.new_save_path_dock}\n'
                f'Generated pro.pdb location: {self.new_save_path_pro}\n')

if __name__ == "__main__":
    lepro_instance = LePro("2BSM.pdb", name_file="webtool_test")
    print(lepro_instance)
    lepro_instance.run()
