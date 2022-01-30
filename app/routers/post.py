from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import models, oauth2, schemas
from app.database import get_db


router = APIRouter(
    prefix='/posts',
    tags=['posts']
)


@router.get("/", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), 
              current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: None | str = ''):
    
    
    page = skip*limit

    results = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).outerjoin(
        models.Vote, models.Vote.post_id == models.Post.id).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(
        limit).offset(page).all()
    
    return results


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), 
             current_user: int = Depends(oauth2.get_current_user)):
    # post_detail = db.query(models.Post).filter(models.Post.id == id).first()

    post_detail = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).outerjoin(
        models.Vote, models.Vote.post_id == models.Post.id).group_by(
        models.Post.id).filter(models.Post.id == id).first()

    if not post_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return post_detail


@router.post("/", status_code=status.HTTP_201_CREATED, 
          response_model=schemas.PostResponse)
def create_post(post: schemas.Post, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    updated_post = db.query(models.Post).filter(models.Post.id == id)

    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} does not exist")
    if updated_post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")

    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()

    return updated_post.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} does not exist")
    if deleted_post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")

    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
