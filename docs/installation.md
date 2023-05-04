# Installation

Note: this guide assumes that you have an existing PIP, postgres and python3.10 installation.

To make the setup of the backend of Kayak-trip-planner convenient we provide a Pip file that you can use.
To make things even more convenient we run everything inside a venv made using pipenv.

Use the following command to install pipenv.
```bash
pip install pipenv
```

Once you have pipenv installed you will use it to create a venv using
```bash
pipenv install
```
After running creating the python virtual environment you should get something like this
```bash
Creating a virtualenv for this project...
Pipfile: /home/jondoe/Desktop/kayak-trip-planner/Pipfile
Using /usr/bin/python3.10 (3.10.11) to create virtualenv...
⠋ Creating virtual environment...created virtual environment CPython3.10.11.final.0-64 in 584ms
  creator CPython3Posix(dest=/home/jondoe/.local/share/virtualenvs/kayak-trip-planner-KtTF46qY, clear=False, no_vcs_ignore=False, global=False)
  seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=/home/jondoe/.local/share/virtualenv)
    added seed packages: pip==23.0.1, setuptools==67.4.0, wheel==0.38.4
  activators BashActivator,CShellActivator,FishActivator,NushellActivator,PowerShellActivator,PythonbsultanActivator

✔ Successfully created virtual environment!
Virtualenv location: /home/jondoe/.local/share/virtualenvs/kayak-trip-planner-KtTF46qY
Installing dependencies from Pipfile.lock (3717c6)...
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
```
Now you can enter the python virtual environment using
```bash
pipenv shell
```

## Configuring the app

The app uses environment variables to determine which database to use, so we define our env variable:
```bash
CONFIG_MODE="testing"
```
The CONFIG_MODE variable can have values: development, testing, staging, production

In this same vein we also configure the DB connection url
```bash
DEVELOPMENT_DATABASE_URL="postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
TEST_DATABASE_URL="postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
STAGING_DATABASE_URL="postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
PRODUCTION_DATABASE_URL="postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
```
You don't have to have all of these DBs, but only the ones you are going to use.