import string

def process_lig_file(path_to_lig, amount_ligands):
    """
    Opens ligand file and readies it to be merged with pro.pdb

    :param path_to_lig: the path to the .dok file
    :param amount_ligands: the amount of ligands to be added to the pro.pdb file

    return string_with_ligand: string that contains the ligands added to the pro.pdb file

    """
    string_with_ligand =""
    amount_ends = 0
    alfabet = list(string.ascii_lowercase)
    # Opens ligand file
    with open(path_to_lig, 'r', encoding='utf-8') as ligand_file:
        for line in ligand_file:
            if line.startswith("END"):
                print(amount_ends)
                amount_ends += 1
                if amount_ends >= int(amount_ligands):
                    return string_with_ligand
            else:
                # Updates ligand lines
                if not line.startswith("REMARK"):
                    line = line.replace("LIG     0      ", f"LIG {amount_ends+1}   0      ")
                    string_with_ligand += line
    return string_with_ligand

def update_pro(path_to_pro, lig_string):
    """
    Reads the pro.pdb file and merges it with the lig_string

    :param path_to_pro: the path to the pro.pdb file
    :param lig_string: string that contains ligands, ready to merge

    return new_string: returns combined string of pro.pdb and .dok file

    """
    with open(path_to_pro, "r", encoding="utf-8") as pro_file:
        string_pdb = pro_file.read()
        new_string = lig_string + string_pdb
    return new_string   

def main(pdb_file, lig_file, amount_of_ligands):
    lig_string = process_lig_file(lig_file, amount_of_ligands)
    new_string = update_pro(pdb_file, lig_string)
    with open(pdb_file, 'w', encoding='utf-8') as file:
        file.write(new_string)
