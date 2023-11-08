# Email confirmation service
## Stack
- Python 3
- Celery
- RabbitMQ
## Features
- Retrieving a message from the message broker (the message is placed in the message broker by this [service](https://github.com/corfa/REST-API-ML))
- Sending a message via SMTP
## Running the Service
1) Install all the required dependencies: ```pip install -r requirements.txt```
2) Create a ```.env``` file in the project's root directory and fill it with the necessary configuration variables. Refer to the example file ```.template.env.```
3) Execute the ```main.py``` file.
