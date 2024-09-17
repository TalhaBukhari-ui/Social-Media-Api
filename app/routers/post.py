from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas,oauth2
from ..database import engine,get_db
from typing import List,Optional
from sqlalchemy import func
router = APIRouter(
    prefix='/posts'
)

#Getting all posts
@router.get('/',response_model=List[schemas.PostOut]) #response_model=List[schemas.PostOut]
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),limit:int =10, skip: int = 0, search: Optional[str] = ''):

    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts

#Creating posts
@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostBase,db: Session = Depends(get_db),get_current_user: int = Depends(oauth2.get_current_user),current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.email)
    
    new_post = models.Post(owner_id=current_user.id, **post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post) #similar to RETURNING *
    return new_post


#Getting individual post
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):  #,user_id: int = Depends(oauth2.get_current_user) makes u use token

    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} was not found')
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} doesnt exist')
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Not authorized to perform this')

    post_query.delete(synchronize_session = False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT) #in fast api u dont send anything back


@router.put('/{id}',response_model=schemas.Post)
def update_post(id: int,updated_post:schemas.PostBase,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} doesnt exist')
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Not authorized to perform this')
    
    post_query.update(updated_post.dict(),synchronize_session = False)
    db.commit()
    return post_query.first()
