from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from db.exceptions.user_exception import DBUserNotFoundException
from db.requests.email_requests import confirm_email
from db.requests.user_requests import get_user_on_email
from routers.depends import get_db

router = APIRouter()


@router.get("/email/verification/", tags=["email"])
async def verification_email_endpoint(token: str, email: str, db: Session = Depends(get_db)):
    try:
        db_user = get_user_on_email(db, email)
        if db_user.token == token:
            confirm_email(db, email)
            return {"status": "confirm"}
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
    except DBUserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
