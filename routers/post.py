from fastapi import APIRouter, Depends, HTTPException, Security, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
import cachetools
from utilits.auth import Auth
from db.mysql import get_db
from services.user_service import UserService
from schemas import schemas
from typing import List

router = APIRouter()
security = HTTPBearer()
auth_handler = Auth()

cache = cachetools.TTLCache(maxsize=100, ttl=300)

@router.post("/", response_model=schemas.PostResponse)
def add_post(post: schemas.PostCreate, request: Request, credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    if request.headers.get('content-length') and int(request.headers['content-length']) > 1024 * 1024:
        raise HTTPException(status_code=413, detail="Payload too large")

    id = auth_handler.decode_token(credentials.credentials)
    user = UserService.get_user_by_id(db, id=id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return UserService.create_post(db=db, post=post, user_id=user.id)

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    id = auth_handler.decode_token(credentials.credentials)
    user = UserService.get_user_by_id(db, id=id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if id in cache:
        return cache[id]
    posts = UserService.get_posts_by_user(db, user_id=user.id)
    cache[id] = posts
    return posts

@router.delete("/{post_id}", response_model=str)
def delete_post(post_id: int, credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    id = auth_handler.decode_token(credentials.credentials)
    user = UserService.get_user_by_id(db, id=id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    UserService.delete_post(db=db, post_id=post_id, user_id=user.id)
    return "Post deleted successfully"
