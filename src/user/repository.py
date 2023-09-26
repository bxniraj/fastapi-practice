from sqlalchemy.orm import Session
from src.user import models , schemas
from fastapi import  HTTPException, status , Depends
from database import get_db , SECRET_KEY , ALGORITHM , PASSWORD_REGEX , EMAIL_REGEX, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext 
from datetime import timedelta , datetime
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
import bcrypt , re , jwt
from jose import jwt, JWTError


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# JWT

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError: 
        raise credentials_exception


# Login
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email = data.email
    password = data.password
    if not re.match(EMAIL_REGEX, email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    # Validate password format using regex
    if not re.match(PASSWORD_REGEX, password):
        raise HTTPException(status_code=400, detail="Invalid password format")
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if user and pwd_context.verify(password, user.password):
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    

# Function to generate JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Read all
def get_all(db: Session):
    return db.query(models.User).all()


# Register a new user
def register_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = create_user(user,db)
    return db_user


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
def update_user(id: int, db: Session, request: schemas.User):
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
