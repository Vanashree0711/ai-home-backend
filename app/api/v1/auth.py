from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token, PasswordResetRequest, PasswordReset
from app.models.schema import User, Session as DBSession
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token
from datetime import datetime, timedelta
from pydantic import BaseModel

router = APIRouter()

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/signup", response_model=UserResponse)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user_in.password)
    new_user = User(email=user_in.email, password_hash=hashed_password, full_name=user_in.full_name)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    print(f"New user registered: {new_user.email}")
    return new_user

@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user or not verify_password(user_in.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    
    access_token = create_access_token(subject=user.id)
    refresh_token_val = create_refresh_token(subject=user.id)
    
    db_session = DBSession(
        user_id=user.id,
        refresh_token=refresh_token_val,
        expires_at=datetime.utcnow() + timedelta(days=30)
    )
    db.add(db_session)
    db.commit()
    
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token_val, 
        "token_type": "bearer",
        "full_name": user.full_name
    }

@router.post("/refresh", response_model=Token)
def refresh_tokens(req: RefreshRequest, db: Session = Depends(get_db)):
    try:
        payload = decode_token(req.refresh_token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    db_session = db.query(DBSession).filter(DBSession.refresh_token == req.refresh_token).first()
    if not db_session or db_session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token expired or not found")
    
    user_id = payload.get("sub")
    new_access_token = create_access_token(subject=user_id)
    new_refresh_token = create_refresh_token(subject=user_id)
    
    db_session.refresh_token = new_refresh_token
    db_session.expires_at = datetime.utcnow() + timedelta(days=30)
    db.commit()
    
    return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}

@router.post("/forgot-password")
def forgot_password(req: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if user:
        reset_token = "mock-reset-token-123"
        print(f"MOCK EMAIL: Password reset token {reset_token} for {req.email}")
    return {"message": "If the email is registered, a password reset link has been sent."}

@router.post("/reset-password")
def reset_password(req: PasswordReset, db: Session = Depends(get_db)):
    if req.token != "mock-reset-token-123":
        raise HTTPException(status_code=400, detail="Invalid token")
    return {"message": "Password has been successfully reset."}
