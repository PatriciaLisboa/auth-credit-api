from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.database import get_db
from app.models import Debt, User
from app.schemas import DebtCreate, DebtResponse
from app.auth import get_current_user, get_current_active_admin

router = APIRouter(tags=["debts"])

@router.get("/debts", response_model=List[DebtResponse])
def get_user_debts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    debts = db.query(Debt).filter(Debt.owner_cpf == current_user.cpf).all()
    return debts

@router.post("/debts", response_model=DebtResponse, status_code=status.HTTP_201_CREATED)
def create_debt(debt: DebtCreate, current_user: User = Depends(get_current_active_admin), db: Session = Depends(get_db)):
    # Check if the user exists
    user = db.query(User).filter(User.cpf == debt.owner_cpf).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with CPF {debt.owner_cpf} not found"
        )
    
    new_debt = Debt(
        id=str(uuid.uuid4()),
        amount=debt.amount,
        due_date=debt.due_date,
        owner_cpf=debt.owner_cpf
    )
    
    db.add(new_debt)
    db.commit()
    db.refresh(new_debt)
    return new_debt