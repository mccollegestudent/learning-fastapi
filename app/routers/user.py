from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from .. database import get_db 
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)#, response_model=schemas.Post)   
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password  #we here we now updateting the pydantic user model
    new_user = models.User(**user.dict()) #auto unpacking dictionary to name = user.name
    db.add(new_user)
    db.commit()
    db.refresh(new_user) #retrieve new post

    return new_user  

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db),):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with {id} does not exist")
    
    return user