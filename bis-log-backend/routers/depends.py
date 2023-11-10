from db.session_db import SessionLocal
from fastapi import HTTPException
from fastapi.params import Header
from starlette import status

from minio import Minio

from broker.session_rabbitMQ import ConnectionBroker


from helper.token import read_token

import os
from dotenv import load_dotenv

load_dotenv()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def verification(token: str = Header(..., convert_underscores=True, alias="X-Token")):
    try:
        data = read_token(token)
        return data
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )



def get_minio_client():
    minio_client = Minio(
    os.getenv('MINIO_URL', ''),
    access_key=os.getenv('MINIO_USER', ''),
    secret_key=os.getenv('MINIO_PASSWORD', ''),
    secure=False,  
    )
    return minio_client


def get_broker():
    broker = ConnectionBroker.channel()
    return broker