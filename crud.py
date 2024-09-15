import models
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

# User-related CRUD
def get_user_by_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.user_id == user_id).first()

def create_user(db: Session, user_id: str):
    db_user = models.User(user_id=user_id, request_count=1)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def increment_user_request_count(db: Session, db_user: models.User):
    db_user.request_count += 1
    db.commit()
    db.refresh(db_user)
    return db_user

# Document-related CRUD
def get_top_documents(db: Session, top_k: int, threshold: float):
    return db.query(models.Document).filter(models.Document.score >= threshold).order_by(models.Document.score.desc()).limit(top_k).all()

# Cache-related CRUD
def get_cached_result(db: Session, query: str):
    return db.query(models.Cache).filter(models.Cache.query == query).first()

def cache_result(db: Session, query: str, result: str):
    db_cache = models.Cache(query=query, result=result)
    db.add(db_cache)
    db.commit()
    return db_cache

# Cache cleanup function
def clean_old_cache(db: Session, max_age_hours: int = 24):
    expiration_time = datetime.utcnow() - timedelta(hours=max_age_hours)
    db.query(models.Cache).filter(models.Cache.timestamp < expiration_time).delete()
    db.commit()
