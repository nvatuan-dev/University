# VIETNAM AVIATION ACADEMY 

[VAA](vaa.edu.vn)

## This repo is about project 1-2 and all Researches, Graduate Thesis project in Vietnam Aviation Academy

### Coding Structure:

1. `./project2/` folder: source code using LaTex to report project.
2. `./radar/` folder: source code processing the radar.
	1. `./src/` folder: CPP code in my project.
	2. `./platfromio.ini`: Project configuration file.
	
### How to run CPP code in PlatformIO IDE:
1. Download Visual Studio Code is given [here](https://code.visualstudio.com/).
2. Download PlatformIO IDE extension in VS Code.
3. Find the input/output USB device ports by using command:
``sudo dmesg | grep tty``
4. Run this command in folder contains the project:

``sudo chmod a+rw /dev/tty....``
