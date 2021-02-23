# TRAINS

## Prerequisites 

We will be developing in a windows 10 enviroment to ensure compatibility, Parallels is fine  
You must have python installed on your system **Not From the Windows Store**  
Get it from [here](https://www.python.org/downloads/)  
Make sure to select the option for pylauncher as well as the add to environment variables option. 

We have powershell scripts for automated building  
To use them you must first enable unsigned powershell scripts  
Open a powershell terminal with admin rights and run `Set-ExecutionPolicy Unrestricted`


## Setting up the Enviornment  **Do these steps Once**
1. Run buildEnv.ps1 - be patient no text will appear in the console
2. Go to DevEnv and run installDependencies.ps1


## Development 
run installDependencies.ps1 and updateDependencies.ps1 each time you pull the repo  
under DevEnv/src there is a folder for each module 
In each module folder there is a build script along with a src folder
For now write your module in the file that already exits in your src folder
To build run the ModuleBuild.ps1 script, the exe will be in the dist folder that is generated. **Dont Move the ExE**

## Adding Dependencies 
Anytime you use pip3 to install a module  please run the setDependencies.ps1 script to update the dependency list. 




