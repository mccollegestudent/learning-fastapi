from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from .. database import get_db 
from sqlalchemy.orm import Session

from sqlalchemy import  desc, asc, func
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


#@router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id,  isouter = True ).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)   
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ): 

    post.dict() # converts to dictionary 

    print(current_user.email)

    new_post = models.Post(owner_id = current_user.id,**post.dict()) #auto unpacking dictionary 'title':'t1' to title = t1 much neater
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #retrieve new post

    return new_post                                                   
    
@router.get("/{id}",  response_model=schemas.PostOut) #path parameter
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):     #id is converted from string to integer

    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))   
    #post = cursor.fetchone()
 
    post =  db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id,  isouter = True ).group_by(models.Post.id).filter(models.Post.id == id).first()  #just need 1 dot first
   
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} was not found")
    
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):  
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id) #a query

    post = post_query.first()

    if post == None: #avoid 500 internal error deleting a non existant post
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with {id} does not exist")
    
    if post.owner_id != current_user.id:   #checks that post to delete belongs to user
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action')
    
    post_query.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)#dont send any data back

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #all data recieved will be stored in post as pydantic 
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s
    #                  RETURNING *""", (post.title, post.content, post.published, str(id),))
    #updated_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:                     #avoid 500 internal error deleting a non existant post
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"post with {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action')
    
    post_query.update(updated_post.dict(), synchronize_session= False)
    db.commit()
    
    return  post_query.first()