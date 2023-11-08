import os
from dotenv import load_dotenv

load_dotenv()


class PostgresConfig:
    db = os.getenv('POSTGRES_DB', 'tasks')
    user = os.getenv('POSTGRES_USER', 'admin')
    password = os.getenv('POSTGRES_PASSWORD', 'qwerty')
    host = os.getenv('POSTGRES_HOST', 'app-database')
    port = os.getenv('POSTGRES_PORT', '5432')
    url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}'
