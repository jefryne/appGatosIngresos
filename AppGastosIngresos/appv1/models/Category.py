from sqlalchemy import create_engine, Column, Integer, String, SmallInteger, Boolean
from sqlalchemy.orm import relationship
from appv1.models.base_class import Base


class Category(Base):
    __tablename__ = 'category'

    category_id = Column(SmallInteger, primary_key=True, autoincrement=True)
    category_name = Column(String(50))
    category_description = Column(String(120))
    category_status = Column(Boolean, default=True)

    transactions = relationship("Transactions", back_populates="category")