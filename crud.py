import models
from sqlalchemy.orm import Session

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

def get_top_documents(db: Session, top_k: int, threshold: float):
    # Example query to get documents based on score threshold
    return db.query(models.Document).filter(models.Document.score >= threshold).order_by(models.Document.score.desc()).limit(top_k).all()
