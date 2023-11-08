from fastapi import HTTPException
from fastapi.params import Header
from starlette import status
from starlette.websockets import WebSocketDisconnect

import helper
from broker.session_rabbitMQ import ConnectionBroker

from db.session_db import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_broker():
    broker = ConnectionBroker.channel()
    return broker


async def verification(token: str = Header(..., convert_underscores=True, alias="X-Token")):
    try:
        data = helper.read_token(token)
        return data
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
