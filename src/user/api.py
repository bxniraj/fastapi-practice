from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.user import schemas, service
from database import get_db
from src.user.auth import *


router = APIRouter()


# Login
@router.post("/login/")
def login(request: schemas.User, db: Session = Depends(get_db)):
    return service.login(request,db)  

# Read all
@router.get("/")
def get(token: str = Depends(decode_token), db: Session = Depends(get_db)):
    return service.get_all(db)

# Create
@router.post("/")
def create(request: schemas.User, db: Session = Depends(get_db)):
    return service.create(request, db)

# Read by id
@router.get("/{user_id}")
def get_id(id: int, db: Session = Depends(get_db)):
    return service.get_id(id, db)

# Update
@router.put("/{id}")
def update_user(id: int, request: schemas.User, db: Session = Depends(get_db)):
    return service.update_user(id, db, request)

# Delete
@router.delete("/{user_id}")
def delete_user( id: int, db: Session = Depends(get_db)):
    return service.delete_user(id, db)
