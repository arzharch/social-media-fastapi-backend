from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import Optional
from .. import schemas, models, oauth2
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

router=APIRouter(prefix="/posts", tags=['Posts'])

@router.get("/",response_model=List[schemas.PostOut] )
async def get_posts(db: Session = Depends(get_db), currrent_user : int = Depends(oauth2.get_current_user), limit: int =10, offset: int = 0, search: Optional[str] = ""):

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)\
        .group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()

    return [{"Post": post, "votes": votes} for post, votes in results]

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
async def create_posts(post : schemas.PostCreate, db: Session  =Depends(get_db), currrent_user : int = Depends(oauth2.get_current_user)): 

    new_post=models.Post(user_id = currrent_user.id, **post.dict())
    db.add(new_post)
    db.commit() 
    db.refresh(new_post) 

    
    return new_post


@router.get("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.PostOut)
async def get_post(id: int, db: Session = Depends(get_db), currrent_user : int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)\
        .group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id = {id} was not found")
    
    return post


@router.put("/{id}",status_code=status.HTTP_200_OK,response_model=schemas.Post)
async def update_post(id: int, post: schemas.PostCreate, db : Session = Depends(get_db), currrent_user : int = Depends(oauth2.get_current_user)): #Post is used here so that it sticks to the schema defined in Post class
    
    post_query= db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with the id = {id} was not found")
    
    if post_query.first().id != currrent_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Not authorized to perform this action")

    post_dict=post.dict()
    post_query.update(post_dict)
    db.commit()


    return post_query.first()


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db : Session = Depends(get_db), currrent_user : int = Depends(oauth2.get_current_user)):
    


    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id = {id} was not found")
    
    if post_query.first().id != currrent_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Not authorized to perform this action")

    post_query.delete()
    db.commit()


    return Response(status_code=status.HTTP_204_NO_CONTENT)