from fastapi import Response, status, HTTPException, APIRouter
from .. import schemas, database, models, oauth2
from fastapi.params import Depends
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, session: Session = Depends(database.get_db), current_user=Depends(oauth2.get_current_user)):

    query = session.query(models.Post).filter(models.Post.id == vote.post_id)
    post = query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} was not found")

    query = session.query(models.Vote)\
        .filter(models.Vote.post_id == vote.post_id,
                models.Vote.user_id == current_user.id)
    found_vote = query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'User {current_user.id} has already voted on post {vote.post_id}')
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        session.add(new_vote)
        session.commit()
        return {"message": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Vote does not exist')

        query.delete(synchronize_session=False)
        session.commit()

        return {"message": "Successfully deleted vote"}
