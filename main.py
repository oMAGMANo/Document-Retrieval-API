import logging
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud, utils
import time
import sqlite3

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log"),
    ]
)

logger = logging.getLogger(__name__)

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health_check():
    logger.info("Health check endpoint called")
    return {"status": "API is active"}

@app.get("/search")
def search(
    query: str = Query(..., description="Search text query"),
    top_k: int = Query(5, description="Number of top results to fetch"),
    threshold: float = Query(0.5, description="Threshold for similarity score"),
    user_id: str = Query(..., description="Unique user identifier"),
    db: Session = Depends(get_db)
):
    start_time = time.time()
    logger.info(f"Search request received - User: {user_id}, Query: {query}, Top K: {top_k}, Threshold: {threshold}")

    user = crud.get_user_by_id(db, user_id)
    if user:
        if user.request_count >= 5:
            logger.warning(f"User {user_id} has exceeded the maximum number of requests")
            raise HTTPException(status_code=429, detail="Too many requests")
        crud.increment_user_request_count(db, user)
    else:
        crud.create_user(db, user_id)

    cached_result = crud.get_cached_result(db, query)
    if cached_result:
        inference_time = time.time() - start_time
        logger.info(f"Cache hit for query '{query}' - User: {user_id}, Inference Time: {inference_time:.4f} seconds")
        return {"cached": True, "documents": cached_result.result, "inference_time": inference_time}

    documents = crud.get_top_documents(db, top_k, threshold)
    crud.cache_result(db, query, str(documents))

    inference_time = time.time() - start_time
    logger.info(f"Search completed - User: {user_id}, Query: {query}, Inference Time: {inference_time:.4f} seconds")
    return {"cached": False, "documents": documents, "inference_time": inference_time}

@app.get("/documents")
def list_documents(db: Session = Depends(get_db)):
    documents = db.query(models.Document).all()
    return {"documents": documents}

@app.delete("/clear-database")
def clear_database():
    try:
        logger.info("Database clear request received")
        conn = sqlite3.connect('test.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM documents")
        conn.commit()
        logger.info("Database cleared successfully")
        return {"status": "Database cleared"}
    except Exception as e:
        logger.error(f"Error clearing database: {str(e)}")
        return {"error": str(e)}
    finally:
        conn.close()

@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    crud.clean_old_cache(db)
    db.close()
    utils.scrape_articles()
