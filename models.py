from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    friend = Column(String, nullable=True)        # Assigned friend
    is_assigned = Column(Boolean, default=False)  # Marks if this person was assigned to someone else
