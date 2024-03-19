"""
MODULE DOCSTRING
"""
import subprocess
import os 
class LePro:
    """
    class docstring
    """
    def __init__(self, pdb_save_path, **kwargs):
        self.name_file = kwargs["name_file"]
        self.dock_slider = kwargs["dock_slider"]
        self.rmsd_slider = kwargs["RMSD_slider"]
        self.pdb_save_path = pdb_save_path
        

    def run(self):
        """
        method docstring
        """
        lepro_path = subprocess.run(["find", "-name", "lepro_linux_x86"], check=True,
                                    capture_output=True, text=True)
        lepro_path = lepro_path.stdout.strip()
        print(lepro_path, self.pdb_save_path)
        subprocess.run([lepro_path, self.pdb_save_path], check=True, capture_output=True)

    def mv_files(self):
        """
        
        """
        new_save_path_dock = os.path.join("static/history/", self.name_file, "dock.in")
        new_save_path_pro = os.path.join("static/history/", self.name_file, "pro.pdb")
        subprocess.run(["mv", "dock.in", new_save_path_dock], check=True)
        subprocess.run(["mv", "pro.pdb", new_save_path_pro], check=True)
        print("New save:", new_save_path_dock)
    
        with open(new_save_path_dock, 'r+', encoding="utf-8") as dock_file:
            lines = dock_file.readlines()
      
        with open(new_save_path_dock, 'w', encoding="utf-8") as dock_file_write:
            for i, line in enumerate(lines):
                
                if i == 4:
                    print(line)
                    dock_file_write.write(self.rmsd_slider + '\n') 

                elif i == 12:
                    dock_file_write.write(self.dock_slider + '\n')

                else:
                    dock_file_write.write(line)        

    def ligands_list(self):
        pass


    def __str__(self):
        return f'File received:{self.pdb_save_path}, located in session: {self.name_file}.'
    

if __name__ == "__main__":
    lepro_instance = LePro("2BSM.pdb", name_file="webtool_test")
    print(lepro_instance)
    lepro_instance.run()

