from curses.ascii import HT
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import schemas, models, oauth2
from app.database import get_db

router = APIRouter(
    prefix="/vote",
    tags=['vote']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db),
         current_user: int = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)
    found_vote = vote_query.first()

    if vote.direction:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                detail=f'user {current_user.id} has already voted on that post')
        new_vote = models.Vote(post_id = vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f'vote does not exist')
        print(f'post id: {found_vote.post_id} user id: {found_vote.user_id}')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}
