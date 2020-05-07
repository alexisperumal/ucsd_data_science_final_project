# ucsd_data_science_final_project
## Installation and steps to run the app:
- cd Deployment-flask
- python3 —version -> make sure python version is 3.*
- pip3 install pipenv -> virtual enviornment
- pipenv shell -> activate the virtual env
- pipenv install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy sklearn -> install the relevant libraries in your virtual env
- python3 -> go python shell
- from app import db 
- db.create.all() -> creating the sqlite database