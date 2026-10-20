from sqlalchemy import Column
from sqlalchemy import Integer, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship, mapped_column
from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    balance = Column(Float, default=0)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    password = Column(String, nullable=False)

  