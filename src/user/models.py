from sqlalchemy import Integer, String, Column , Date
from sqlalchemy.orm import relationship
from database import Base


class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True , unique=True, autoincrement=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String, unique=True)
    birth_date = Column(Date)
    
    competitions = relationship("Competition", back_populates="users", cascade="all, delete-orphan")
    entries = relationship("Entry", back_populates="users", cascade="all, delete-orphan")
