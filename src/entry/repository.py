from sqlalchemy.orm import Session
from src.entry import models , schemas
from fastapi import  HTTPException, status

def get_all(db: Session):
    user = db.query(models.Entry).all()
    return user

def create(user_request: schemas.Entry, db: Session):
    user = models.Entry(**user_request.model_dump())
    existing_user = db.query(models.Entry).filter(models.Entry.id == user_request.id).first()
    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="User already exists")
    user = models.Entry(
        name=user_request.name,
        title=user_request.title,
        description=user_request.description,
        submission_date=user_request.submission_date,
        user_id=user_request.user_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get(id: int, db: Session):
    user = db.query(models.Entry).filter(models.Entry.id == id).first()
    return user

def update(id: int, db: Session, request: schemas.Entry):
    user = db.query(models.Entry).filter(models.Entry.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    for key, value in request.model_dump().items():
        setattr(user, key, value)
    db.commit()
    return {'Updated Successfully'}

def delete(id: int, db: Session):
    user = db.query(models.Entry).filter(models.Entry.id == id).delete(synchronize_session=False)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.commit()
    return {'Delete Successfully'}
