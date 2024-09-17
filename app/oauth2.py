from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schemas,models,database

from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login') #login is name of url path
#secret key
#algorithm,
#expiration

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

#Generates a JWT token
def create_access_token(data: dict):
    #copy the input passed to function
    to_encode = data.copy()
    #set expire time now + sometime diff
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    #update the to_encode dict
    to_encode.update({'exp':expire})
    #encode into JWT token
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


#It decodes the token, checks for the presence of the user_id, 
#and handles exceptions if the token is invalid or expired. It 
# returns a TokenData object if the token is valid.
def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM] )
        id: str = payload.get('user_id')
        
        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=str(id))
    except JWTError:
        raise credentials_exception

    return token_data

#Extracts and verifies the JWT token from the request
#get the token from the request header
#, verifies it using verify_access_token, and raises an HTTP 401 
# error if the token is invalid.
def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f'coud not validate headers', headers={'WWW-Authenticate':'Bearer'})

    token = verify_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user