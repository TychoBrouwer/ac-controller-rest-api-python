# Python rest API for the air conditioning controller

This is a project for the USE course Detailing, realization and RPC test - group 17. Instructions on how to use GitHub are below.

## Installation

1. Install a text editor or IDE (I can recommend VS Code).
2. Make a GitHub account.
3. Install git (download current [here](https://git-scm.com/downloads)).
   - In the install wizard you can leave default on almost everything.
   - But you can choose your text editor, just select it in the dropdown.
   - Also make sure **Git from the command line and also from 3rd-party software** is checked.
   - After installation run ```git config --global user.name "Your GitHub name here"```.
   - And run ```git config --global user.email "Your GitHub email here"```.
4. Download or make sure **Python3** is installed, [here](https://www.python.org/downloads/).
5. Make a folder for the project on your pc (no spaces to make it easier).
6. Run ```cd path/project/directory``` in the terminal to navigate to your project folder.
7. Run ```git clone https://github.com/TychoBrouwer/ac-controller-rest-api-python.git``` to clone the Git repository in the current directory.
8. Set the **SERVER_IP** in the ```src/api/constants.js``` file.
9. Run ```python .\server.py``` to start the Python server.

### To pull updates from the origin repository

1. Run ```cd path/project/directory``` to navigate to your project folder.
2. Run ```git pull origin main``` to pull the changes from the repository.

### To push updates to the origin repository

1. Run ```cd path/project/directory``` to navigate to your project folder.
2. Run ```git add .``` to track the changes made.
3. Run ```git commit -m "USEFUL UPDATE MESSAGE"``` to commit the changes to the branch.
4. Run ```git push origin main``` to push the changes to the repository.
