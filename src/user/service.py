from src.user import repository , schemas
from fastapi import Depends
from database import get_db
from sqlalchemy.orm import Session



def register(request: schemas.User, db: Session = Depends(get_db)):
    return repository.register_user(request,db)

def login(request: schemas.User, db: Session = Depends(get_db)):
    return repository.login(request, db)

def get_all(db: Session = Depends(get_db)):
    return repository.get_all(db)


def create(request: schemas.User, db: Session = Depends(get_db)):
    return repository.create_user(request, db)

def get_id(id: int, db: Session = Depends(get_db)):
    return repository.get_user(id, db)


def update_user(id: int, request: schemas.User, db: Session = Depends(get_db)):
    return repository.update_user(id, db, request)


def delete_user( id: int, db: Session = Depends(get_db)):
    return repository.delete_user(id, db)
