from sqlalchemy.orm import Session
from src.user import models , schemas
from fastapi import  HTTPException , Depends, Header
from database import get_db , SECRET_KEY , ALGORITHM , PASSWORD_REGEX , EMAIL_REGEX
from passlib.context import CryptContext 
from datetime import timedelta , datetime
import re , jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Login
def login(data: schemas.User, db: Session = Depends(get_db)):

    email = data.email
    password = data.password

    if not re.match(EMAIL_REGEX, email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    # Validate password format using regex
    if not re.match(PASSWORD_REGEX, password):
        raise HTTPException(status_code=400, detail="Invalid password format")

    user = db.query(models.User).filter(models.User.email == email).first()

    if user and pwd_context.verify(password, user.password):

        access_token = create_token(data={"sub": user.email})

        return {'access_token' : access_token,
                # 'refresh_token' : refresh_token,
                'token_type': 'Bearer' }
    else:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    

# Function to generate JWT token
def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=10)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Decode Tokens
def decode_token(authorization: str = Header(), db: Session = Depends(get_db)):
    
    try:
        parts = authorization.split(' ')
        verify = parts[1]

        # Decode
        payload = jwt.decode(verify, SECRET_KEY, algorithms=ALGORITHM)

        # Extract the email from the payload
        email_ext = payload.get("sub")

        user_ext = db.query(models.User).filter(models.User.email == email_ext).first()

        if not email_ext:
            raise HTTPException(status_code=400, detail="Email not found in the token")
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
