# Python rest API for the air conditioning controller

This is a project for the USE course Detailing, realization and RPC test - group 17. Instructions on how to use GitHub and the Flask server are below.

## Installation

1. Install a text editor or IDE (I can recommend VS Code).
2. Make a GitHub account.
3. Install git (download current [here](https://git-scm.com/downloads)).
   - In the install wizard you can leave default on almost everything.
   - But you can choose your text editor, just select it in the dropdown.
   - Also make sure **Git from the command line and also from 3rd-party software** is checked.
   - After installation run ```git config --global user.name "Your GitHub name here"```.
   - And run ```git config --global user.email "Your GitHub email here"```.
4. Download or make sure **Python3** is installed, from [here](https://www.python.org/downloads/).
5. Run ```pip install websockets uvicorn fastapi``` to install the dependencies using pip.
6. Make a folder for the project on your pc (no spaces to make it easier).
7. Run ```cd path/project/directory``` in the terminal to navigate to your project folder.
8. Run ```git clone https://github.com/TychoBrouwer/ac-controller-rest-api-python.git``` to clone the Git repository in the current directory.
9. Run ```git branch -M main``` to set the Git branch.
10. Run ```flask --app server run``` to start the Python server.

### To pull updates from the origin repository

1. Run ```cd path/project/directory``` to navigate to your project folder.
2. Run ```git pull``` to pull the changes from the repository.

### To push updates to the origin repository

1. Run ```cd path/project/directory``` to navigate to your project folder.
2. Run ```git add .``` to track the changes made.
3. Run ```git commit -m "USEFUL UPDATE MESSAGE"``` to commit the changes to the branch.
4. Run ```git push``` to push the changes to the repository.

## Running the Flask Server

Run the server with ```flask --app server run```

Run the other scripts with ```python "SCRIPT_NAME"``` or ```python3 "SCRIPT_NAME"```

## Project

This project aims to allow an IR controlled air conditioner to become a smart air conditioner. The user can control their AC unit remotely using an app. This is achieved by forwaring the request from the remote device to a local device, which uses an IR transmitter to control the AC unit. The server can also relay weather information to the local device for smart temperature control by the air conditioner.

This repository hosts the code for the server which acts as the bridge between the local device and the remote client.
