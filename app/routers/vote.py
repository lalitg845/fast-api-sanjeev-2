from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2, database

router = APIRouter(
    prefix='/votes',
    tags=['Votes']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def post_vote(vote: schemas.Vote,
              db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with {vote.post_id} does not exit')

    found_vote = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

    if vote.dir == 1:
        if found_vote.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'user already vote on {vote.post_id} ')
        else:
            new_vote = models.Vote(post_id=vote.post_id,
                                   user_id=current_user.id)
            db.add(new_vote)
            db.commit()
        return {'message': 'vote successfully added'}
    else:
        if not found_vote.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'votes does not exit')
        else:
            found_vote.delete(synchronize_session=False)
            db.commit()
        return {'message': 'vote successfully deleted'}
