from database import Base
from sqlalchemy import Column, Integer, String, Float, DateTime, func

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    request_count = Column(Integer, default=0)

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    score = Column(Float)

class Cache(Base):
    __tablename__ = "cache"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, unique=True, index=True)
    result = Column(String)
    timestamp = Column(DateTime, server_default=func.now())
