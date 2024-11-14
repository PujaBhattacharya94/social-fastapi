from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix = '/users', tags=['Users'])

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.UserCreateResponse)
def create_user(create_user : schemas.UserCreate,db: Session = Depends(get_db)):

    #hash the user password - user.password
    hashed_password = utils.hash(create_user.password)
    create_user.password = hashed_password

    new_user_create = models.User(**create_user.dict())
    db.add(new_user_create)
    db.commit()
    db.refresh(new_user_create)
    return new_user_create


#get userinformation based on {id}
@router.get("/{id}",  response_model = schemas.UserCreateResponse)
def get_user(id : int,db: Session = Depends(get_db)):
    get_user = db.query(models.User).filter(models.User.id == id).first()
    if not get_user:
         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                             detail = f"User with id :{id} does not exist")
    return get_user
    

    
    