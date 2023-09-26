from sqlalchemy import Integer, String, Column , Boolean , Date , ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Competition(Base):
    __tablename__ = "competition"

    id = Column(Integer, primary_key=True, index=True , unique=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    prize = Column(Boolean)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), unique=True)

    users = relationship("User",back_populates="competitions")
    