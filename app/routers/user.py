
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import schemas, models, utils
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
 

router=APIRouter()

@router.post("/users",status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db:Session=Depends(get_db)):

    user.password=utils.password_hash.hash(user.password)

    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/users/{id}", response_model=schemas.User, status_code=status.HTTP_200_OK)
async def get_user(id : int, db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} was not found")
    
    return user