from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import crud, schemas

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(crud.User).filter(crud.User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    new_user = crud.create_user(db, user.email, user.password)
    return {"message": "Sign up successful", "verification_code": new_user.verification_code}

@app.post("/verify")
def verify(code: schemas.VerifyCode, db: Session = Depends(get_db)):
    result = crud.verify_user(db, code.email, code.code)
    if result == "Verified":
        return {"message": "You are verified"}
    elif result == "Code expired":
        raise HTTPException(status_code=400, detail="Code expired")
    else:
        raise HTTPException(status_code=400, detail="Invalid code")

@app.put("/update")
def update(data: schemas.UserUpdate, email: str, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db, email, data.dict(exclude_unset=True))
    if not updated_user:
        raise HTTPException(status_code=400, detail="User not verified or not found")
    return {"message": "Updated successfully"}

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.login_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials or user not verified")
    return {"message": "Login successful"}
