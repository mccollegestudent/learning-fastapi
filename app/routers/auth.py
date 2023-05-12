from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from fastapi.security.oauth2 import OAuth2PasswordRequestForm #instead of doing the user credentials

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=["Authentification"])

@router.post('/login')
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    print(user_credentials)

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first() 

    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail = f"invalid Credentials") #we don't want to make it easy attacker to know that they are missing

    #utils.verify(user_credentials, user.password)
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException( status_code = status.HTTP_403_FORBIDDEN, detail = f"invalid Credentials") #make it hard
    
    #create token then return token

    access_token = oauth2.create_access_token(data = {"user_id" : user.id}) # we decide to put only the userid in the data section  we could add role scope of endpoints they can access etc

    return {"access_token" : access_token, "token_type": "bearer"}  

    #^ return access token (and) tell user what type of token this is this is considerd a bearer token (configered on the front end)
    #literay in authorization header righting the word bearer then porviding the token 