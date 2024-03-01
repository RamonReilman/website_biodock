# Biodock
### version 0.0.0
### Authors: 
    Ramon Reilman
    Yamila Timmer
    Stijn Vermeulen

## Wat/waarom/wie
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.l images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Installation(vereisten systeem +handleiding installatie)
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## gebruikershandleiding voor ontwikkelaar/programmeur
Before running the tools you must already have:
- A .pdb file of the protein
- A .mol2 file of the ligand
- A ligand file without extensions that holds the filenames of all the .mol2 ligand files

Lepro takes a .pdb file and creates a simplified copy called pro.pdb in which things like hydrogen atoms, ligands, ions and cofactors are removed.\
It also creates a dock.in file that looks like this:
>Receptor\
>pro.pdb\
>\
>RMSD\
>1.0\
>\
>Binding pocket\
>74.066 96.508\
>93.153 124.53\
>80.721 106.061\
>\
>Number of binding poses\
>20\
>\
>Ligands list\
>ligands\
>\
>END

(in this example the ligands file under Ligands list is a file without extension that houses all of the .mol2 ligand files)\
The dock.in is used to run ledock. Ledock uses the file references in the dock.in to effectively get all the data.
ledock uses that data to dock the given ligands and it returns a .dok file with the specified number of binding poses sorted
on score(a lower number is a higher score).\
plip takes a .pdb file to create an image, in this case the .pdb file needs to have the protein and the appropriate ligands
The best way to do this here is to take the appropriate ligands from the .dok file and put them in the pro.pdb.
You can do this because this .dok file is just a .pdb made by ledock.


### voorbeeld commandline
To get pictures out of the .pdb file you usually run:
>$ lepro XXXXX.pdb
>
>$ ledock dock.in
> 
>$ plip -f pro.pdb -p --peptides 1 2 3


## in/output data

## bekende bugs (optioneel)

## Support (contactgegevens)
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.
