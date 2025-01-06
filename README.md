# Automating Interventions with Selenium and Python v3.0 (GUI Version)
***

This program will let you automate the documention of academic interventions in ecst (a student management system) 
on any given day (GUI version of [ecst_intrv](https://github.com/soto-sergio/ecst_intrv))
***
<p align = "center">
  <img src = "https://user-images.githubusercontent.com/104229323/227680381-a2e1ef6a-05fd-4bc7-be44-952c86c02da7.png" width = 300". height = 400>        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <img src = "https://user-images.githubusercontent.com/104229323/230721948-4d7d8f03-7f30-497a-916a-5985e6717246.png" width = 340, height = 400>
</p>

## Quickstart (Windows)

a. Open Windows Command Prompt and Install Git using `winget install --id Git.Git -e --source winget`  

b. Create folder to download Git Repository and initialize git with `git init` in the CMD 

c. Pull repo with ` git pull https://github.com/soto-sergio/ecst_intrv_v2.0.git`  

d. Install miniconda using  `winget install -e --id Anaconda.Miniconda3`  

e. Create environment variables  

> conda env create -f environment.yml  
> conda activate eduenv  

## Steps

1. Download ChromeDriver. Google Chrome is the required web browser for this project to run. [Link](https://googlechromelabs.github.io/chrome-for-testing/) 
- Install and keep `chromedriver.exe` in the project's folder. [Not required. Driver already included for Windows systems]

2. The program requires you to download your Homeroom Roster as follows:
- Go to Frontline SIS (TEAMS). 
- Click on `Enter Classroom Grading` > Select your Homeroom class > Reports > Class Student Listing with Addresses (Excel)
- Save the roster inside the project's folders `data/raw/`  

  IMPORTANT: Keep the name of the file as it is `ClassStudentListingwithAddresses`. Save as type: `Microsoft Excel Worksheet`.  
  If you are updating an older roster, make sure the name is saved exactly as mentioned.   

3. Run the script in the Command Prompt by typing `python ecst_main.py`  


## NOTES
>
> * Amount of minutes of each intervention entry is set to 30. Changing it seems to produce an error.


