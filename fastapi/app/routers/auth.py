from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils
import app.oauth as oauth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session=Depends(database.get_db)):
    #user_credentials:schemas.UserLogin
    # OAuth2PasswordRequestForm returns this - 
    # {
    #     "username" : 
    #     "password" :
    # }
    user_email_check = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user_email_check:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user_email_check.password):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = f"Invalid Credentials")
    

    #create a token 
    #return token

    access_token = oauth.create_access_token(data = {"user_id" : user_email_check.id})
    return{"access_token" : access_token,"token_type" : "bearer"}
