# Tutor_Match
StudyConnect is a web-based platform that allows students to search, view, and book tutors online. The project uses **Flask**, **Python**, and **HTML**.

## Database setup if error occurs 
Make a directory in the root directory of the project by running this command in the root (if not already made by main):

mkdir instance

Then after running (see how to run flask below) the program, run this in the terminal:

chmod 777 instance/tutors.db    # Mac/Linux

icacls "instance/tutors.db" /grant Everyone:F   # Windows

Run the program now, the tutors.db should exist and have the necessary permisions.

## Project Setup

### 1. Clone the Repository

git clone https://github.com/TutorMatch22/Tutor_Match.git

cd Tutor_Match

### 2. Create & Activate a Virtual Environment
#### MacOS/Linux:

python3 -m venv venv

source venv/bin/activate

#### Windows:

python -m venv venv

venv\Scripts\activate

### 3. Install Dependencies
pip install -r requirements.txt

## Running Tests
pytest

## Running the Application
export FLASK_APP=main  # For MacOS/Linux

set FLASK_APP=main     # For Windows

$env:FLASK_APP = "main" # For Windows Powershell

flask run   # select one line above and then run flask

## Deactivate (optional)
deactivate

## Afterwards: You only need to activate the virtual environment again if you deactivated it:
## Mac/Linux
source venv/bin/activate
## Windows:
venv\Scripts\activate



## Steps in terminal for github
## Create a new branch
git checkout -b feature-branch-name

## Commit the changes
git add .

git commit -m "Describe your changes here"


## Push the branch to github
git push origin feature-branch-name

## Create a pull request to merge the branch into the develop or main branch.

## Pull
git pull origin main
