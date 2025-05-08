from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import uuid
import traceback

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, Token, Login, MessageResponse
from app.auth import get_password_hash, verify_password, create_access_token, get_current_user
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, ADMIN_DOMAIN
from datetime import timedelta

router = APIRouter(tags=["users"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.cpf == user.cpf).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CPF already registered"
        )
    
    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    is_admin = user.email.endswith(ADMIN_DOMAIN)
    
    hashed_password = get_password_hash(user.password)
    db_user = User(
        cpf=user.cpf,
        name=user.name,
        birth_date=user.birth_date,
        email=user.email,
        password=hashed_password,
        is_admin=is_admin
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login(user_credentials: Login, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.cpf == user_credentials.cpf).first()
        if not user or not verify_password(user_credentials.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect CPF or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.cpf, "is_admin": user.is_admin},
            expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print(f"Error during login: {str(e)}")
        print("Traceback:")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/logout", response_model=MessageResponse)
def logout(current_user: User = Depends(get_current_user)):
    # In a token-based auth system like this, the logout is typically handled client-side
    # by removing the token. The server doesn't need to do anything special.
    return {"message": "Successfully logged out"}