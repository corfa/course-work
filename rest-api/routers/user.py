from types import NoneType

from fastapi import APIRouter, Depends, Path, HTTPException
from pika.adapters.blocking_connection import BlockingChannel
from sqlalchemy.orm import Session
from starlette import status

import helper
from broker.actions import put_in_queue
from db.exceptions.user_exception import UsernameOrEmailAlreadyExists, DBUserNotFoundException
from db.requests.user_requests import create_user, get_user_on_login
from helper import read_token, verify_password, generate_confirmation_token
from routers.depends import get_db, verification, get_broker

from shemas.user import User

router = APIRouter()


@router.post("/user/", tags=["users"])
async def create_user_endpoint(user: User, db: Session = Depends(get_db),
                               broker: BlockingChannel = Depends(get_broker)):
    try:
        user.password = helper.hash_password(user.password)
        email_token = generate_confirmation_token(user.email)
        id_user = create_user(db, user, email_token)
        put_in_queue(broker, user.email, email_token)
        return {"id": id_user}
    except UsernameOrEmailAlreadyExists:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username {user.username} or email {user.email} already exists"
        )


@router.post("/user/auth", tags=["users"])
async def auth_user_endpoint(user: User, db: Session = Depends(get_db)):
    try:
        user_db = get_user_on_login(db, user.username)
        verify_password(user.password, user_db.password)
        if user_db.confirmed is False:
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email not confirmed"
            )
        token = helper.create_token({"id": user_db.id})
        return {"X-token": token}
    except:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid login or password"
        )
