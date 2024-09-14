from functools import lru_cache
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import Session
from database import SessionLocal
import models

@lru_cache(maxsize=100)
def cached_search(query):
    # Simulate a caching mechanism
    return f"Cached result for {query}"

def scrape_articles():
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    articles = []
    for item in soup.select('.storylink'):
        articles.append(item.get_text())

    # Save scraped articles to the database
    db = SessionLocal()
    for article in articles:
        new_document = models.Document(content=article, score=1.0)  # Default score for demonstration
        db.add(new_document)
    db.commit()
    db.close()

    print("Scraped Articles:", articles)
