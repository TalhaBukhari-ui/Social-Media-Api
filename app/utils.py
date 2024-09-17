from passlib.context import CryptContext
#telling what hashing algo to use (in this case its bcrypt)
pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')

def hash(password: str):
    return pwd_context.hash(password)

#Raw password take in and compare it to hash

def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)