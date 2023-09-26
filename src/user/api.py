from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.user import schemas, service
from database import get_db
from src.user.repository import *

router = APIRouter()

# Register
@router.post("/register/")
def register_user(request: schemas.User, db: Session = Depends(get_db)):
    return service.register(request,db)

# Login
@router.post("/login/")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return service.login(request, db)  

# Read all
@router.get("/")
def get(db: Session = Depends(get_db), get_current_user: schemas.User = Depends(get_current_user)):
    return service.get_all(db, get_current_user)

# Create
@router.post("/")
def create(request: schemas.User, db: Session = Depends(get_db)):
    return service.create(request, db)

# Read by id
@router.get("/{id}")
def get_id(id: int, db: Session = Depends(get_db)):
    return service.get_id(id, db)

# Update
@router.put("/{id}")
def update_user(id: int, request: schemas.User, db: Session = Depends(get_db)):
    return service.update_user(id, request, db)

# Delete
@router.delete("/{id}")
def delete_user( id: int, db: Session = Depends(get_db)):
    return service.delete_user(id, db)
