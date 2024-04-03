from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__= "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String,nullable= False)  
    published = Column(Boolean, server_default='True', nullable= False) 
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 

    owner_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE" ), nullable = False)   

    #this will return the class of another model - not referencing user table but rather sql class
    #this will return owner owner property this will determine the relationship
    owner = relationship("User") #here i'm referencing the actual class

class User(Base):
    __tablename__ = "users" 
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 
    phone_number = Column(String)

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete ="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete ="CASCADE"), primary_key=True)


 
