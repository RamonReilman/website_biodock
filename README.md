# BioDock Visualiser (V. 1.0)

## Authors: 
- Ramon Reilman (https://git.bioinf.nl/rreilman)
- Stijn Vermeulen (https://git.bioinf.nl/svermeulen)
- Yamila Timmer (https://git.bioinf.nl/ytimmer2)


## Description
BioDock Visualiser is a webtool that allows users to dock ligands onto proteins and visualise the results afterwards. The process of 'docking' refers to predicting the most likely configuration of a ligand when it attaches itself to a protein.

Understanding interactions between proteins and ligands is of great importance for various branches of molecular biology. Examples of its usage include, but are not limited to, developing new medicines or improving existing ones, as well as getting a better understanding of various biochemical processes.

### Key-features
- Docks selected ligand onto selected protein,
- Returns lig.dok-file with (up to 20) possible ligand configurations, sorted from most-likely to least-likely configuration*,
- Returns visualisation of all ligand configurations (as PNG), in which the ligand and the part of the protein that is bound to the ligand are visible,
- User-friendly webtool interface, that allows user to change settings like RMSD-cutoff and number of docking poses, making it so that the user can tweak the output of the program.

*This is based on the amount of kcal/mol that the ligand configuration gives when binding to a protein, the more kcal/mol, the more likely the configuration is.

## System requirements and installation<br>
### System requirements: <br>
- OS, Linux
- Python 3.0 or higher
- Pip3

### Installing tools: <br>
To setup and install website:
```bash
# Get the project
~$ git clone git@git.bioinf.nl:biodock_vis/website_biodock.git
~$ cd website_biodock

# Setup tools and venv for website
~$ setup/setup.sh
```
## Tools
### LePro
LePro takes the .pdb file and creates a modified version named pro.pdb, in which things like water molecules and ligands are removed and hydrogen atoms are added. This is an important step in order to make the file ready to be used by LeDock.\
\
It also creates a dock.in file that looks like this:
>Receptor\
>pro.pdb\
>\
>RMSD\
>1.0\
>\
>Binding pocket\
>x<sub>min</sub> x<sub>max</sub>\
>y<sub>min</sub> y<sub>max</sub>\
>z<sub>min</sub> z<sub>max</sub>\
>\
>Number of binding poses\
>20\
>\
>Ligands list\
>ligands_list\
>\
>END

### Ledock
The dock.in is used to run LeDock. LeDock uses the file references in the dock.in to effectively get all the data. LeDock uses that data to dock the given ligands and it returns a .dok file with the specified number of binding poses sorted on score (a lower number is a higher score).

### PLIP (Protein-Ligand Interaction Profiler)
PLIP takes a modified pro.pdb file and uses PyMOL to create the images. The pro.pdb has to be modified so that the data of the protein, aswell as the data of the ligand is in the file. We have created a function that does this, so the user does not have to manually change anything.

## User's manual
In order to run the tools, the user must provide the following files:
- A .pdb file of the protein (can be obtained from: https://www.rcsb.org/)
- A .mol2 file of the ligand (can be obtained from: https://zinc.docking.org/)

### Adjustable settings:
The webtool offers 2 settings that allow the user to make changes to the dock.in file. The user can choose the RMSD-cutoff and the number of docking poses. A lower number for docking poses as well as a higher RMSD-cutoff leads to quicker processing times, whereas a higher number of docking poses and a lower RMSD-cutoff makes the program run slower. 

- <b>Number of docking poses</b> (slider range 1-20, with increments of 1)\
The number of iterations LeDock will go through, each with a chance of finding a new ligand configuration.

- <b>RMSD-cutoff</b> (slider range 0.5-4.0, with increments of 0.1)\
The cutoff of the Root Mean Square Division (RMSD). This is the average distance between atoms of different ligand configurations. It is measured in Ångström (Å). Different ligand configurations with a smaller distance in atoms than the given RMSD-cutoff, will be merged together into 1 ligand configuration. A high RMSD-cutoff will cause most of the docking poses that are even slightly similar, to be merged together. A low RMSD-cutoff makes it so that (almost) every ligand configuration will remain as a unique one and will not be merged, and thus is a more specific method. 


### Commandline example
If you want to run the tools this through the commandline, instead of using the webtool, you can run the following: 

```bash
# Runs LePro, using the user-supplied .pdb file
~$ /path/to/lepro_linux_x8 XXXXX.pdb

# Runs LeDock, using the generated dock.in file
~$ /path/to/ledock_linux_x8 dock.in

# Runs PLIP, using the generated pro.pdb file and creates images
~$ plip -f pro.pdb -p --peptides 1 2 3
```

## In/output data
### Input data
To use the tools you need:
- <b>A .pdb file of a protein</b> <br>
    - This contains information about the peptide

- <b>A .mol2 file of a ligand</b>
    - Molecular information about the ligand, can be used to render it in PyMOL for example.

### Output data
- <b>A .dok file</b>
    - This contains a number of position the ligand could be in, it is in an decreasing order. The first ligand has the most optimal position
    
- <b>Images of the ligand docked onto the protein</b>
    - These images show how a ligand is fit into the binding site. There are also bonds formed and showed. PLIP is used for this and gives us a legend to use in said pictures.

### PLIP legend:

| Description  | RGB | PyMOL color | Representation |
| ------------ | --- | ------------| ---------------|
| Protein  | [43, 131, 186] | myblue (custom) | sticks |
| Ligand  | [253, 174, 97] | myorange (custom) | sticks |
| Water  | [191, 191, 255]  | lightblue | nb_spheres |
| Charge Center | [255, 255, 0] | yellow | spheres |
| Aromatic Ring Center  | [230, 230, 230] | grey90 | spheres |
| Ions | [250, 255, 128] | hotpink | spheres |

[1]
### Interactions

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


## Support
In case of any bugs or needed support, open up an issue at our repo: <br>
https://git.bioinf.nl/biodock_vis/website_biodock


## Acknowledgments
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


## Sources
1. https://github.com/pharmai/plip/blob/master/DOCUMENTATION.md?plain=1
2. Docking (moleculair). (2024, 31 januari). Wikipedia. https://nl.wikipedia.org/wiki/Docking_(moleculair)#:~:text=Op%20het%20gebied%20van%20moleculair,vormt%20met%20een%20ander%20molecuul.
3. Lephar Research. (z.d.). Tutorial for LeDock. 
4. Ligand (biochemie). (2023, 23 juni). Wikipedia. https://nl.wikipedia.org/wiki/Ligand_(biochemie)
5. Salentin, S. (2015). PLIP: fully automated protein–ligand interaction profiler. https://www.semanticscholar.org/paper/PLIP%3A-fully-automated-protein%E2%80%93ligand-interaction-Salentin-Schreiber/9fb2bf7b0fb083b764794b82486189b314e6e9ab/figure/0  
