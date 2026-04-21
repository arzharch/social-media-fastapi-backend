import jwt
import os
import dotenv
from datetime import datetime, timedelta
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status


oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')

dotenv.load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


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
        print(id)

        if not id:
            raise credentials_exception
        
        token_data=schemas.TokenData(id=id)

    except jwt.PyJWTError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(token:str = Depends(oauth2_scheme)):

    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})

    return verify_access_token(token, credentials_exception)
