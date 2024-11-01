from fastapi import Response,status,HTTPException,Depends,APIRouter

from sqlalchemy.orm import Session
from .. import database,schemas,models,utils,oauth2

from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
    tags=['Authenticaiton']
)

#The `login` function authenticates a user by checking their credentials
#If the email and password match, it generates and returns a JWT token.
#If credentials are invalid, it raises a `403 Forbidden` error.

@router.post('/login',response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm=Depends(),db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Invalid Credentials')
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'Invalid Credenetials')
    
    access_token = oauth2.create_access_token(data={'user_id':user.id})

    return {'access_token' : access_token,'token_type':'bearer'}
    
