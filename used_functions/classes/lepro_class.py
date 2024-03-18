"""
MODULE DOCSTRING
"""
import subprocess
class LePro:
    """
    class docstring
    """
    def __init__(self, pdb_file_name, **kwargs):
        self.name_file = kwargs["name_file"]
        self.pdb_file_name = pdb_file_name

    def run(self):
        """
        method docstring
        """
        pdb_path = f"website_biodock/static/history/{self.name_file}/{self.pdb_file_name}"
        #pdb_path = f"static/history/{self.name_file}/{self.pdb_file_name}"
        lepro_path = subprocess.run(["find", "-name", "lepro_linux_x86"], check=True,
                                    capture_output=True, text=True)
        lepro_path = lepro_path.stdout.strip()
        print(lepro_path, pdb_path)
        subprocess.run([lepro_path, pdb_path], check=True, capture_output=True)


    def __str__(self):
        return f'File received:{self.pdb_file_name}, located in session: {self.name_file}.'

if __name__ == "__main__":
    lepro_instance = LePro("2BSM.pdb", name_file="webtool_test")
    print(lepro_instance)
    lepro_instance.run()
