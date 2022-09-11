from src import oauth2
from .. import models, schemas
from .. database import get_db
from fastapi import Response, status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, session: Session = Depends(get_db)):
    post = session.query(models.Post).get(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    return post


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(session: Session = Depends(get_db)):
    return session.query(models.Post).all()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, session: Session = Depends(get_db), get_current_usr: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict())
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostUpdate, session: Session = Depends(get_db)):
    query = session.query(models.Post).filter(models.Post.id == id)
    post = query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    query.update(updated_post.dict(), synchronize_session=False)
    session.commit()

    return query.first()


@router.delete("/{id}")
def delete_post(id: int, session: Session = Depends(get_db)):
    post = session.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    post.delete(synchronize_session=False)
    session.commit()

    return Response(status_code=status.HTTP_410_GONE)