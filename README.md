# NKL

Repository for kyykka.com 2.0

# Setting up a local development environment

Clone this repository

Install python 3.6

Optional but highly recommended: create virtual environment for this project, see https://docs.python.org/3/tutorial/venv.html

At root of the cloned project (where requirements.txt is), install requirements

`pip install -r requirements.txt`

Start the development server

`python manage.py runserver`

# Setting up the local development environment for frontend

First install Nodejs from:
https://nodejs.org/en/download/

After that go to the root of the project and install requirements

`npm install`

This will install all the packages listed in "devDependencies" of frontend/package.json.

After the installation is completed go to the frontend from root

`cd frontend`

And start up the vue server

`npm run serve`
