# NKL

Repository for kyykka.com 2.0

# Setting up a local development environment

Clone this repository

Install python 3.6

Optional but highly recommended: create virtual environment for this project, see https://docs.python.org/3/tutorial/venv.html

MySQL:

`sudo apt-get install python3-dev default-libmysqlclient-dev`

At root of the cloned project (where requirements.txt is), install requirements

`pip install -r requirements.txt`

After opening mysql instance and selecting database `nkl` run migrations

`python manage.py migrate`

After the migrations are complete populate the tables

`python manage.py shell`

In the python shell run the following code and wait for it to complete

`from utils.dummyGen import *`
`initGen()`

Start the development server

`python manage.py runserver localhost:8000`

# Setting up the local development environment for frontend

First install Nodejs from:
https://nodejs.org/en/download/

After that go to the root of the vue project where package.json resides

`cd frontend`

and install requirements

`npm install`

This will install all the packages listed in "devDependencies" of package.json.

And start up the vue server

`npm run serve`
