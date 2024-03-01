## Projectinformatie
Choose a self-explaining name for your project.

## Wat/waarom/wie
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.l images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

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

~$ wget http://www.lephar.com/download/lefrag_linux_x86

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
    - Moelculair information about the ligand, can be used to render it in pymol for example.

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
- y.timmer@st.hanze.nl

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## sources
1. https://github.com/pharmai/plip/blob/master/DOCUMENTATION.md?plain=1
