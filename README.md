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
```
The 3 tools are now downloaded on your computer. <br>
They need to be changed into an executable
```bash
~$ chmod +x /path/to/tool
```
The tools can now be used by calling them
```bash
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
~$ source /path/to/newvenv/bin/activate
~$ pip3 install -r /path/to/requirements.txt --no-deps plip
```
plip can now be used within the venv. <br>
## gebruikershandleiding voor ontwikkelaar/programmeur
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

### voorbeeld commandline

## in/output data

## bekende bugs (optioneel)

## Support (contactgegevens)
Incase of any bugs, or needed support, please mail one of the following emails: <br>
- r.reilman@st.hanze.nl
- s.vermeulen@st.hanze.nl
- y.timmer@st.hanze.nl


## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.
