## Biodock visualiser (v. 1.0)

## Description
Understanding interactions between proteins and ligands is of great importance for various branches of molecular biology. Examples of its usage include, but are not limited to, developing new medicines or improving existing ones, as well as getting a better understanding of various biochemical processes.

BioDock Visualiser is a webtool that allows users to dock ligands onto proteins and visualise the result afterwards. The process of 'docking' refers to predicting the most likely configuration of a ligand when it attaches itself to a protein.


### Key-features
- Docks selected ligand onto selected protein,
- Returns lig.dok-file with (up to 20) possible ligand configurations, sorted from most-likely to least-likely configuration*,
- Returns visualisation of selected ligand configurations, in which part of the protein will be visible and showing the bonds between ligand and protein,
- User-friendly webtool interface, with options like which configurations the user wants to be visible in the visualisation, etc.

*This is based on the amount of kcal/mol that the ligand configuration gives when binding to a protein, the more kcal/mol, the more likely the configuration will be.

## Installation and system requirements <br>
### system requirements: <br>
- OS, linux
- Python 3.0 or higher
- pip3


### Installing tools: <br>
To install the tools ledock/lepro/lefrag:
```bash
~$ wget http://www.lephar.com/download/ledock_linux_x86

~$ wget http://www.lephar.com/download/lepro_linux_x86

# Now make the tools executable
~$ chmod +x /path/to/tool

# To use the tools
~$ /path/to/tool
```
But you could also create an alias in the .bash_aliases or .bashrc files. <br>
<br>
Plip: <br>
There are 2 ways to install plip, depending on if you're installing it on your own computer or the bin computers. <br>

On your own laptop/computer:
```bash
~$ pip3 install -r /path/to/requirements.txt --no-deps plip
```

To install plip on a bin computer, you will need to install it in a virtual enviroment. <br>
```bash
~$ python3 -m venv /path/to/newvenv --system-site-packages
# Activate the venv
~$ source /path/to/newvenv/bin/activate
# Install package into the venv
~$ pip3 install -r /path/to/requirements.txt --no-deps plip
```
plip can now be used within the venv. <br>
## gebruikershandleiding voor ontwikkelaar/programmeur
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

### voorbeeld commandline

## in/output data
### Input data
To use the tools you need:
- A pdb file of a peptide <br>
    - This contains information about the peptide
- A mol2 file of a ligand
    - Molecular information about the ligand, can be used to render it in pymol for example.

### Output data
- a .dok file
    - This contains a number of position the ligand could be in, it is in an decreasing order. The first ligand has the most optimal position
    
- Pictures of ligand in binding site
    - These pictures show how a ligand is fit into the binding site. There are also bonds formed and showed. PLIP is used for this and gives us a legend to use in said pictures.

Plip legend:

| Description  | RGB | PyMOL color | Representation |
| ------------ | --- | ------------| ---------------|
| Protein  | [43, 131, 186] | myblue (custom) | sticks |
| Ligand  | [253, 174, 97] | myorange (custom) | sticks |
| Water  | [191, 191, 255]  | lightblue | nb_spheres |
| Charge Center | [255, 255, 0] | yellow | spheres |
| Aromatic Ring Center  | [230, 230, 230] | grey90 | spheres |
| Ions | [250, 255, 128] | hotpink | spheres |

[1]
#### Interactions

| Description  | RGB | PyMOL color | Representation |
| ------------ | --- | ------------| -------------- |
| Hydrophobic Interaction  | [128, 128, 128] | grey50 | dashed |
| Hydrogen Bond  | [0, 0, 255] | blue | solid line |
| Water Bridges  | [191, 191, 255]  | lightblue | solid line |
| pi-Stacking (parallel) | [0, 255, 0] | green | dashed line |
| pi-Stacking (perpendicular)  | [140, 179, 102] | smudge | dashed line |
| pi-Cation Interaction | [255, 128, 0] | orange | dashed line |
| Halogen Bond | [54, 255, 191] | greencyan | solid line |
| Salt Bridge | [255, 255, 0] | yellow | dashed line |
| Metal Complex | [140, 64, 153] | violetpurple | dashed line |

[1]
## bekende bugs (optioneel)

## Support (contactgegevens)
Incase of any bugs, or needed support, please mail one of the following emails: <br>
- r.reilman@st.hanze.nl
- s.vermeulen@st.hanze.nl
- y.timmer.2@st.hanze.nl

## Authors and acknowledgments
Authors:
- Ramon Reilman (github link)
- Stijn Vermeulen (github link)
- Yamila Timmer (https://git.bioinf.nl/ytimmer2)

BioDock Visualiser integrates the following tools and libraries:


- **LePro**
  - Description: program that removes/adds certain elements from the user-provided PDB-file, to simplify the docking-process.
  - Repository: http://www.lephar.com/download.htm
  - License: Not Specified

- **LeDock**
  - Description: program that does the calculations for docking the ligand onto the protein.
  - Repository: http://www.lephar.com/download.htm
  - License: Not Specified

- **PLIP**
  - Description: program that visualises the ligand configurations and bonds when bound to the protein.
  - Repository: https://github.com/pharmai/plip
  - License: GNU General Public License v2.0

- **NumPy**
  - Description: library used for scientific computing with Python (required with PLIP).
  - Repository: https://github.com/numpy/numpy
  - License: BSD License

- **lxml**
  - Description: library used for processing XML and HTML in Python (required with PLIP).
  - Repository: https://github.com/lxml/lxml
  - License: BSD License

- **openbabel-wheel**
  - Description: library used for processing data from molecular modeling (required with PLIP). 
  - Repository: https://github.com/njzjz/openbabel-wheel
  - License: GNU General Public License v2.0
