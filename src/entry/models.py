from sqlalchemy import Integer, String, Column , Date , ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Entry(Base):
    __tablename__ = "entry"
    
    id = Column(Integer, primary_key=True , index=True , unique=True,  autoincrement=True)
    name = Column(String)
    title = Column(String)
    description = Column(String)
    submission_date = Column(Date)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), unique=True)

    users = relationship("User",back_populates="entries")