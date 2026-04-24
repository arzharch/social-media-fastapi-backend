import jwt
import dotenv
from datetime import datetime, timedelta
from . import schemas, database, models, config
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status


oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = config.settings.SECRET_KEY
ALGORITHM = config.settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = int(config.settings.ACCESS_TOKEN_EXPIRE_MINUTES)


def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    print(data)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        id: int = payload.get("user_id")

        if not id:
            raise credentials_exception
        
        token_data=schemas.TokenData(id=id)

    except jwt.PyJWTError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(token:str = Depends(oauth2_scheme), db : Session = Depends(database.get_db)):
    """
    This function uses FastAPI dependency injection to enforce authentication at route level
    It separates extraction (OAuth2PasswordBearer) from validation (verify_access_token), which keeps auth reusable and testable.
    WWW-Authenticate: Bearer is set to follow OAuth2 error semantics.
    
    """
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})

    token=verify_access_token(token,credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
