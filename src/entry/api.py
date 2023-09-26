from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from src.entry import schemas, repository

router = APIRouter()


@router.get("/")
def get(db: Session = Depends(get_db)):
    return repository.get_all(db)


@router.post("/")
def create(request: schemas.Entry, db: Session = Depends(get_db)):
    return repository.create(request, db)


@router.get("/{id}")
def get_id(id: int, db: Session = Depends(get_db)):
    return repository.get(id, db)


@router.put("/{id}")
def update_user(id: int, request: schemas.Entry, db: Session = Depends(get_db)):
    return repository.update(id, db, request)


@router.delete("/{id}")
def delete_user( id: int, db: Session = Depends(get_db)):
    return repository.delete(id, db)
