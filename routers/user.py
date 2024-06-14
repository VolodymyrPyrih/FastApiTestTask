from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from utilits.auth import Auth
from db.mysql import get_db
from schemas import schemas
from services.user_service import UserService

router = APIRouter()
security = HTTPBearer()
auth_handler = Auth()


@router.post('/signup', response_model=schemas.UserResponse)
def signup(user_details: schemas.UserSchemas, db: Session = Depends(get_db)):
    existing_user = UserService.get_user_by_email(db, user_details.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    try:
        user = UserService.create_user(db, user_details)
        return user
    except Exception as e:
        db.rollback()
        error_msg = f"Failed to signup user. Error: {str(e)}"
        raise HTTPException(status_code=500, detail=error_msg)

@router.post('/login', response_model=schemas.Token)
def login(user_details: schemas.UserSchemas, db: Session = Depends(get_db)):
    user = UserService.get_user_by_email(db, user_details.email)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid username or password')

    if not auth_handler.verify_password(user_details.password, user.password):
        raise HTTPException(status_code=401, detail='Invalid username or password')

    access_token = auth_handler.encode_token(str(user.id))
    refresh_token = auth_handler.encode_refresh_token(str(user.id))
    return {'access_token': access_token, 'refresh_token': refresh_token}

@router.get('/refresh_token', response_model=schemas.TokenResponse)
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    refresh_token = credentials.credentials
    new_access_token, new_refresh_token = auth_handler.refresh_token(refresh_token)
    if not new_access_token or not new_refresh_token:
        raise HTTPException(status_code=401, detail='Invalid refresh token')
    return {
        'access_token': new_access_token,
        'refresh_token': new_refresh_token,
        'token_type': 'bearer'
    }



