# ucsd_data_science_final_project
## Installation and steps to run the app:
**NOTE**: These install instructions is only for setting up your environment the first time. No need to rerun all steps after you've created your database. Simply run the following command: `pipenv shell`.
- cd Deployment-flask
- python3 —version -> make sure python version is 3.*
- pip3 install pipenv -> virtual enviornment
- pipenv shell -> activate the virtual env
- pipenv install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy scikit-learn -> install the relevant libraries in your virtual env
- python3 -> go python shell
- from app import db 
- db.create.all() -> creating the sqlite database