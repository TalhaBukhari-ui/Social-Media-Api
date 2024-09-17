from .database import Base

from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from sqlalchemy.orm import relationship

from sqlalchemy import Column,Integer,String,Boolean,ForeignKey

class Post(Base):
    #creating a table called 'posts'
    __tablename__ = 'posts'
    #we have to import the datatypes "integer,string etc" from sqlalchemy
    id = Column(Integer,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,nullable=False,server_default='TRUE')
    created_at = Column(TIMESTAMP,server_default=text('now()'),nullable=False)
    owner_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False) #ForeignKey(table.colname,action,nullable)
    owner = relationship('User')
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    

class Vote(Base):
    __tablename__ = 'votes'
    user_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),primary_key=True)
    post_id = Column(Integer,ForeignKey('posts.id',ondelete='CASCADE'),primary_key=True)

