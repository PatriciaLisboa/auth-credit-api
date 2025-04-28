from sqlalchemy import Column, String, Float, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database import Base

class User(Base):
    __tablename__ = "users"

    cpf = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    
    debts = relationship("Debt", back_populates="owner")

class Debt(Base):
    __tablename__ = "debts"

    id = Column(String, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=False)
    owner_cpf = Column(String, ForeignKey("users.cpf"))
    
    owner = relationship("User", back_populates="debts")