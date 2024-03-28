"""
    Script used to merge a .dok file and pro.pdb file,
    This is needed to get the plip tool working
    - Authors: Ramon Reilman, Stijn Vermeulen, Yamila Timmer

    This script merges the information about different ligand positions
    with the pdb file of the protein.
    It also gives each ligand a number so it's optional for plip to generate an image.

Usage:
    Import into run_app.py
"""
import string


def process_lig_file(path_to_lig):
    """
    Opens ligand file and readies it to be merged with pro.pdb

    :param path_to_lig: the path to the .dok file

    return string_with_ligand: string that contains the ligands added to the pro.pdb file

    """
    string_with_ligand =""
    amount_ends = 0
    alphabet = list(string.ascii_lowercase)

    # Opens ligand file
    with open(path_to_lig, 'r', encoding='utf-8') as ligand_file:
        for line in ligand_file:

            # Counts amount of ligands
            if line.startswith("END"):
                amount_ends += 1

            else:
                # Gives every ligand a chain name, so that plip can render these ligands
                if not line.startswith("REMARK"):
                    line = line.replace("LIG     0      ", f"LIG {alphabet[amount_ends]}   0      ")
                    string_with_ligand += line

    return string_with_ligand, amount_ends


def update_pro(path_to_pro, lig_string):
    """
    Reads the pro.pdb file and merges it with the lig_string

    :param path_to_pro: the path to the pro.pdb file
    :param lig_string: string that contains ligands, ready to merge

    return combined_string: returns combined string of pro.pdb and .dok file

    """

    # Opens and reads pro.pdb file
    with open(path_to_pro, "r", encoding="utf-8") as pro_file:
        string_pdb = pro_file.read()

        # Merges the ligand and pdb file
        combined_string = lig_string + string_pdb

    return combined_string


def main(pdb_file, lig_file):
    """
    Acts like the main function of this script
    
    :param pdb_file: Path to a pdb file
    :param lig_file: path to the .dok file
    
    return n_ligands: int with number of ligands in .dok file.
    """
    lig_string, n_ligands= process_lig_file(lig_file)
    combined_string = update_pro(pdb_file, lig_string)

    # Writes merged pdb and ligand file to new pro.pdb file.
    with open(pdb_file, 'w', encoding='utf-8') as file:
        file.write(combined_string)

    return n_ligands
