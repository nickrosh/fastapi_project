from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from app import schemas, models, utils
from app.database import get_db


router = APIRouter(tags=['Authentication'])


@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
                    models.User.email == user_credentials.email).first()

    # make sure that user email (unique) exists
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail='invalid Credentials')

    # check that the passwords are equal
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail='invalid Credentials')

    # Create JWT Token
    return {"message": "example token"}