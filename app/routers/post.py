from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # print(limit)

    # posts = db.query(models.Post).filter(
    # models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(search)

    query = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote,
                                                                                       models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id)

    query = query.filter(models.Post.title.contains(
        search)).limit(limit).offset(skip)

    posts = query.all()
    return posts


@ router.get("/{id}", response_model=schemas.PostOut)
def get_posts(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    # cursor.execute(""" SELECT * FROM posts WHERE id = {0} """ .format(str(id)))
    # post = cursor.fetchone()

    #post = db.query(models.Post).filter(models.Post.id == id).first()

    query = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote,
                                                                                       models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id)
    query = query.filter(models.Post.id == id)
    post = query.first()

    # print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"you post with {id} was not found")

    return post


@ router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title,content,published)  VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # print(post.dict())
    # print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    # new_post = models.Post(
    #     title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@ router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     """ DELETE FROM posts WHERE id=%s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"you post with {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    # return {'deleted post': f"{post}"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@ router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s returning * """,
    #                (post.title, post.content, post.published, id))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"you post with {id} was not found")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
