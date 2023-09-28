from sqlalchemy.orm import Session
from src.user import models , schemas
from fastapi import  HTTPException, status , Depends
import bcrypt

# Read all
def get_all(db: Session):
    return db.query(models.User).all()

# Create
def create_user(user_request: schemas.User, db: Session):
    existing_user = db.query(models.User).filter(models.User.email == user_request.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    user = models.User(**user_request.model_dump())
    hashed_password = bcrypt.hashpw(user_request.password.encode(), bcrypt.gensalt())
    user = models.User(
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        email=user_request.email,
        password=hashed_password.decode(),
        birth_date=user_request.birth_date
    )
    db.add(user) 
    db.commit()
    db.refresh(user)
    return user

# Read by ID
def get_user(id: int, db: Session):
    return db.query(models.User).filter(models.User.id == id).first()

# Update
def update_user(id: int, request: schemas.User, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    for key, value in request.model_dump().items():
        setattr(user, key, value)
    db.commit()
    return {'Updated Successfully'}

# Delete
def delete_user(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).delete(synchronize_session='fetch')
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.commit()
    return {'Delete Successfully'}
