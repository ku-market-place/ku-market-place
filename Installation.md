# Run and Install

### Steps to install and run the project.
#### [Step 1](#step-1-clone-the-repository-1): Clone the Repository
#### [Step 2](#step-2-check-the-directory-1): Check the Directory
#### [Step 3](#step-3-install-the-required-modules-1) Install the Required Modules
#### [Step 4](#step-4-database-migrations-1): Database Migrations

## Step 1: Clone the repository
Clone the repository and using this command on terminal:
```commandline
git clone https://github.com/ku-market-place/ku-market-place.git
```

## Step 2: Check the directory
To ensure that your are in the correct directory (ku-polls), run the following command:

Windows:
```commandline
cd
```

macOS / Linux:
```commandline
pwd
```

If you are not in the correct directory, navigate to the project directory before proceeding with the installation:
```commandline
cd ku-market-place
```

## Step 3: Install the required modules

Installing the required `Python` modules by executing the following command:
```commandline
pip install -r requirements.txt
```

To verify that all modules are installed, run the following command:
```commandline
pip list
```

## Step 4: Database migrations

To create a new database, run the following command:
```commandline
python manage.py migrate
```
or
```commandline
python3 manage.py migrate
```

Load the initial data for the polls app, run the following command:

```commandline
python manage.py loaddata product/polls.json data/user.json
```
or
```commandline
python3 manage.py loaddata product/polls.json data/user.json
```
