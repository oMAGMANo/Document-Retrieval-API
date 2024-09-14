from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Query
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud, utils

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Welcome to the Document Retrieval API!"}

@app.get("/health")
def health_check():
    return {"status": "API is active"}

@app.get("/search")
def search(
    query: str = Query(..., description="Search text query"),
    top_k: int = Query(5, description="Number of top results to fetch"),
    threshold: float = Query(0.5, description="Threshold for similarity score"),
    user_id: str = Query(..., description="Unique user identifier"),
    db: Session = Depends(get_db)
):
    # Check user and increment request count
    user = crud.get_user_by_id(db, user_id)
    if user:
        if user.request_count >= 5:
            raise HTTPException(status_code=429, detail="Too many requests")
        crud.increment_user_request_count(db, user)
    else:
        crud.create_user(db, user_id)
    
    # Cached search implementation
    cached_result = utils.cached_search(query)
    if cached_result:
        print(cached_result)
    
    # Fetch documents from the database
    documents = crud.get_top_documents(db, top_k, threshold)
    return {"documents": documents}

@app.on_event("startup")
async def startup_event():
    # Run the scraping task on server startup
    utils.scrape_articles()

@app.get("/documents")
def list_documents(db: Session = Depends(get_db)):
    documents = db.query(models.Document).all()
    return {"documents": documents}

@app.get("/add-dummy-data")
def add_dummy_data_endpoint(db: Session = Depends(get_db)):
    dummy_documents = [
        {"content": "Introduction to Python programming", "score": 0.9},
        {"content": "FastAPI for building APIs", "score": 0.85},
        {"content": "Understanding SQLAlchemy ORM", "score": 0.7},
        {"content": "Latest trends in AI and machine learning", "score": 0.95},
        {"content": "How to scrape websites using BeautifulSoup", "score": 0.6},
    ]
    
    for doc in dummy_documents:
        new_doc = models.Document(content=doc['content'], score=doc['score'])
        db.add(new_doc)
    
    db.commit()
    return {"message": "Dummy data added successfully"}
