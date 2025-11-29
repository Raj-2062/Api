from sqlalchemy.orm import Session
from database import User
from utils import generate_verification_code, is_code_expired
import datetime

def create_user(db: Session, email: str, password: str):
    code = generate_verification_code()
    user = User(
        email=email, password=password, verification_code=code, is_verified=False, code_created_at=datetime.datetime.utcnow()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_user(db: Session, email: str, code: str):
    user = db.query(User).filter(User.email==email).first()
    if not user:
        return "User not found"
    if is_code_expired(user.code_created_at):
        return "Code expired"
    if user.verification_code == code:
        user.is_verified = True
        user.verification_code = None
        db.commit()
        return "Verified"
    return "Invalid code"

def update_user(db: Session, email: str, data: dict):
    user = db.query(User).filter(User.email==email, User.is_verified==True).first()
    if not user:
        return None
    for key, value in data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def login_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email==email, User.password==password, User.is_verified==True).first()
    return user
