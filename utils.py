import requests
from bs4 import BeautifulSoup
from database import SessionLocal
import models
import logging

logger = logging.getLogger(__name__)

def scrape_articles():
    try:
        url = "https://news.ycombinator.com/"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []
            for item in soup.select('.storylink'):
                articles.append(item.get_text())

            if articles:
                db = SessionLocal()
                for article in articles:
                    new_document = models.Document(content=article, score=1.0)  # Default score
                    db.add(new_document)
                db.commit()
                db.close()
                logger.info(f"Scraped Articles: {articles}")
            else:
                logger.warning("No articles found during scraping.")
        else:
            logger.error(f"Failed to fetch articles. Status code: {response.status_code}")
    except Exception as e:
        logger.error(f"Error occurred while scraping articles: {str(e)}")
