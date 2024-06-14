from sqlalchemy.orm import Session
from schemas import schemas
from db import user as models
from utilits.auth import Auth
from fastapi import HTTPException, status
auth = Auth()
class UserService:

    @staticmethod
    def create_user(db: Session, user: schemas.UserSchemas):
        db_user = models.User(email=user.email, password=auth.encode_password(user.password))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_email(db: Session, email: str):
        return db.query(models.User).filter(models.User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, id: int):
        return db.query(models.User).filter(models.User.id == id).first()

    @staticmethod
    def create_post(db: Session, post: schemas.PostCreate, user_id: int):
        db_post = models.Post(text=post.text, owner_id=user_id)
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post

    @staticmethod
    def get_posts_by_user(db: Session, user_id: int):
        return db.query(models.Post).filter(models.Post.owner_id == user_id).all()

    @staticmethod
    def delete_post(db: Session, post_id: int, user_id: int):
        post = db.query(models.Post).filter(models.Post.id == post_id, models.Post.owner_id == user_id).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        db.delete(post)
        db.commit()
