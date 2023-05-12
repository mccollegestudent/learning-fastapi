from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database , models
from fastapi import Depends, status , HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login') #will be the login endpoint

SECRET_KEY = settings.secret_key #could be any string really
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict): #access token will have a payload - the data we will include will be type dict in this case
    to_encode = data.copy() #data we will encode into the jwt token 

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) #time it will expire in (time delta ) mow should be utcnow
    to_encode.update({"exp": expire})#this is a copy of the dictionaly we are just parsing in that expiry time

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) #this method will actually create the token - payload - secretkey - algo

    return encoded_jwt

def verify_access_token(token: str, credentials_exception): #decoding token  #always use exception in the event of an error occuring

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id:str =  payload.get("user_id") #extract id

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id) #validate with the schema then extract the data

    except JWTError as e:
        print(e)
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):

    #if there are any issues with the token

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not validate credentials", 
                            headers = {"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)  
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
