import subprocess
import os
class LePro:
    """
    class docstring
    """
    def __init__(self, pdb_save_path, **kwargs):
        self.name_file = kwargs["name_file"]
        self.pdb_save_path = pdb_save_path
        self.lepro_path = subprocess.run(["find", "-name", "lepro_linux_x86"], check=True,
                                    capture_output=True, text=True).stdout.strip()

    def run(self):
        """
        method docstring
        """
        subprocess.run([self.lepro_path, self.pdb_save_path], check=True, capture_output=True)

    def mv_files(self):
        """
        method docstring
        """
        new_save_path_dock = os.path.join("static/history/", self.name_file, "dock.in")
        new_save_path_pro = os.path.join("static/history/", self.name_file, "pro.pdb")
        subprocess.run(["mv", "dock.in", new_save_path_dock], check=True)
        subprocess.run(["mv", "pro.pdb", new_save_path_pro], check=True)
        print("New save:", new_save_path_dock)

    def __str__(self):
        return f'LePro installation detected: {self.lepro_path}\n PDB file received \
            by LePro:{self.pdb_save_path}, located in session: {self.name_file}.'

if __name__ == "__main__":
    lepro_instance = LePro("2BSM.pdb", name_file="webtool_test")
    print(lepro_instance)
    lepro_instance.run()
