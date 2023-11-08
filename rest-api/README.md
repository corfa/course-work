# REST-API

## Stack
- Python 3
- Postgres
- RabbitMQ
- FastAPI
- Alembic
- SQLAlchemy

## Features
- User creation, sending a task to the message broker for email confirmation ([email confirmation service](https://github.com/corfa/email-confirmation-service)).
- User authentication and JWT token creation.

## Future Goals
1) Add the ability for authorized users to interact with an ML service that will process user photos.
2) Add full CRUD functionality for users.

## Running the Service
1) Install all the required dependencies: ```pip install -r requirements.txt```
2) Create a ```.env``` file in the project's root directory and fill it with the necessary configuration variables. Refer to the example file ```.template.env.```
3) Run the migrations to create the required tables in the database:```alembic upgrade head```
4) Execute the ```main.py``` file.
