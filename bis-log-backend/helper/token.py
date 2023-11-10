import jwt
import os
from dotenv import load_dotenv


load_dotenv()
secret = os.getenv('SECRET', 'SUPER_SECRET_KEY')



def read_token(token: str) -> dict:
    try:
        return jwt.decode(token, secret, algorithms='HS256')
    except:
        raise Exception