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

## Installation(vereisten systeem +handleiding installatie)
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## gebruikershandleiding voor ontwikkelaar/programmeur
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

### voorbeeld commandline

## in/output data

## bekende bugs (optioneel)

## Support (contactgegevens)
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

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
