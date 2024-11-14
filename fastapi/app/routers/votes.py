from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import database,models, schemas, oauth

router = APIRouter(prefix="/vote", tags=['Vote'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote, db: Session = Depends(database.get_db), 
               current_user: int = Depends(oauth.get_current_user)):
    
    #query the vote table to retrieve to see if the post even exist 
    post_exist = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post= {vote.post_id} does not exist.")

    #query the vote table to retrieve post_id and user_id of current user, to check if already voted
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
   
                 
    if(vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"User= {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return{"message" : "successfully added vote"}       

    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User= {current_user.id} has not voted on post {vote.post_id}")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return{"message" : "successfully deleted vote"} 


   
    
    print(search)
    return sqlalchemy_post
  
