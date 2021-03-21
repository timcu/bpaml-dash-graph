# Beginners' Python and Machine Learning
This git repo is the complementary source code for 
- https://youtu.be/zxwSezObVkQ   (macOS)
- https://youtu.be/78RaVmb-c30   (Windows)

The project will show how to create an interactive chart plotting cases of COVID-19 by country or state.

## Setup environment
- Install Python 3.9.2 from https://www.python.org/downloads/release/python-392/
  - Add python to path when installing, or know where it is for later
  - (3.6 or later should be fine, anaconda also fine) 
- Install Git from https://git-scm.com/download/
- Install IDE eg PyCharm Community Edition 2020.3.3 from https://www.jetbrains.com/pycharm/download/
- Clone repository and setup virtual environment

### Command line - clone git repository
    cd ~/PycharmProjects
    git clone https://github.com/timcu/bpaml-dash-graph.git
    cd bpaml-dash-graph
    git checkout challenge1

### PyCharm - clone git repository
    VCS > Get from version control... >
        Git
        https://github.com/timcu/bpaml-dash-graph.git
        ~/PycharmProjects/bpaml-dash-graph
    Git > Branches... > Checkout tag or revision
        challenge1

### Command line - create virtual environment
    python -m venv venv                         # Windows
    python3 -m venv venv                        # Mac or Linux
    conda create --name venv-dash-graph python  # Anaconda

### Command line - Activate virtual environment
    source venv/bin/activate                    # Mac or Linux
    conda activate venv-dash-graph              # Anaconda
    source venv/Scripts/activate                # Windows Git-Bash
    venv\Scripts\activate.bat                   # Windows command prompt
    venv\Scripts\Activate.ps1                   # Windows powershell

### Command line - Install requirements
    pip install -r requirements.txt             # Windows, Mac or Linux without Anaconda
    conda install --name venv-dash-graph --file requirements.txt       # Anaconda

### Pycharm - create and activate virtual environment and install requirements
    PyCharm > Preferences > Project > Python Interpreter
        Project Interpreter > Show all > +
        Virtualenv: New environment
            Location: ./venv
            Base Interpreter: ...bin/python3.9 or AppData\Local\Programs\Python\Python39\python.exe

### checkout task 2
    git checkout challenge2

