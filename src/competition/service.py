from src.competition import repository , schemas
from fastapi import Depends
from database import get_db
from sqlalchemy.orm import Session

def get_all_user(db: Session = Depends(get_db)):
    return repository.get_all(db)


def create_user(request: schemas.Competition, db: Session = Depends(get_db)):
    return repository.create(request, db)

def get_id(id: int, db: Session = Depends(get_db)):
    return repository.get(id, db)


def update_user(id: int, request: schemas.Competition, db: Session = Depends(get_db)):
    return repository.update(id, db, request)


def delete_user( id: int, db: Session = Depends(get_db)):
    return repository.delete(id, db)