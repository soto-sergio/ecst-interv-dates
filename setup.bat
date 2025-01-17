@echo off
echo Installing Git...
winget install --id Git.Git -e --source winget

echo Cloning repository...
mkdir ecst_project
cd ecst_project
git clone https://github.com/soto-sergio/ecst-interv-v3.git

echo Installing Miniconda...
winget install -e --id Anaconda.Miniconda3

echo Setting up environment...
conda env create -f environment.yml
conda activate eduenv

echo Setup complete!! You can now run the project.
pause