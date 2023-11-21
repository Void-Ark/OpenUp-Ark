from fastapi import APIRouter, status, Depends, HTTPException
import schemas, database, oauth2
from typing import Annotated
from sqlalchemy.orm import Session

router = APIRouter(prefix="/votes", tags=['Votes']) 

@router.post(path="/", 
    status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, 
    db: Annotated[Session, Depends(database.get_db)], 
    current_user: Annotated[int, Depends(oauth2.get_current_user)]
): 
    found_post = database.crud.get_post_by_id(id=vote.post_id, db=db)
    if not found_post : raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ERROR: Given post id {vote.post_id} is not found !!!!")
    
    found_vote = database.crud.vote_find(post_id=vote.post_id, user_id=current_user.id, db=db) # type: ignore

    if found_vote : 
        deleted_vote = database.crud.vote_delete(post_id=vote.post_id, user_id=current_user.id, db=db) # type: ignore
        return {"message": "successfully deleted vote", "details": deleted_vote}
    else : 
        new_vote = database.crud.vote_create(post_id=vote.post_id, user_id=current_user.id, db=db) # type: ignore
        return {"message": "Successfully voted post", "details": new_vote} 
        
