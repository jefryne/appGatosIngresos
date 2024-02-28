from sqlalchemy import Column, String, Enum, Integer,Boolean, TIMESTAMP, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from appv1.models.Transactions import Transactions
from appv1.models.base_class import Base


class User(Base):
    __tablename__ = "users"
    user_id = Column(String(30), primary_key=True)
    full_name = Column(String(80))
    mail = Column(String(100), unique=True)
    passhash = Column(String(140))
    user_role = Column(Enum('admin', 'user'))
    user_status = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    update_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    transactions = relationship("Transactions", back_populates="user")