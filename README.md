# Personality Test Flask Example
Simple personality test app developed using Flask. The questions are taken from [psychologies.co.uk](https://www.psychologies.co.uk/self/are-you-an-introvert-or-an-extrovert.html).

Dependencies:
* (Poetry package manager)[https://python-poetry.org/docs/#installation]
* (Flask)[https://flask.palletsprojects.com/en/2.0.x/quickstart/#]
* (SQLite)[https://flask.palletsprojects.com/en/2.0.x/patterns/sqlite3/]
* (Black)[https://github.com/psf/black]

## Setup Instructions
1. Install requirements with `Poetry`:
```bash
poetry init
```
If you do not have `Poetry` already installed on your machine, please see their home page 
for installation instructions.

2. Open a python terminal to initate the database:
```bash
poetry run python
```
From the python interpreter, run:
```python
from app import init_db
init_db()
exit()
```
The `schema.sql` file holds the schema of the database as well as some inital data.

3. Start development server:
```bash
bash run_app.sh
```

## Running Tests
You can run the unit tests with the command bellow:
```bash
poetry run python test_app.py
```
