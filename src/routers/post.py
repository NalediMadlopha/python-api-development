from .. import models, schemas, oauth2
from .. database import get_db
from fastapi import Response, status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, session: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id %s """, (str(id),))
    # post = cursor.fetchone()

    # post = session.query(models.Post.id == id).first()
    post = session.query(models.Post).get(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    return post


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(session: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user),
              limit: int = 10, offset: int = 0, search: Optional[str] = ""):
    # Return all posts
    # session.query(models.Post).all()

    # Return posts belonging to a specific user
    return session.query(models.Post)\
        .filter(models.Post.owner_id == current_user.id)\
        .filter(models.Post.title.contains(search))\
        .limit(limit)\
        .offset(offset)\
        .all()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, session: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict())
    new_post.owner_id = current_user.id

    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostUpdate, session: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    query = session.query(models.Post).filter(models.Post.id == id)
    post = query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    if post.owner_id != oauth2.get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    query.update(updated_post.dict(), synchronize_session=False)
    session.commit()

    return query.first()


@router.delete("/{id}")
def delete_post(id: int, session: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):

    # cursor.execute(
    #       """DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    query = session.query(models.Post).filter(models.Post.id == id)
    post = query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    query.delete(synchronize_session=False)
    session.commit()

    return Response(status_code=status.HTTP_410_GONE)
