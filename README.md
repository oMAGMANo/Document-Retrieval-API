# Document Retrieval API

This API allows users to retrieve documents, cache responses, and scrape news articles in the background.

## Caching Strategy

We are using SQLite as the primary database for both document storage and caching. This allows us to persist cached results and optimize retrieval performance without relying on external services like Redis.

The cache is stored in the `cache` table and uses the search query as the key. Each result is cached with a timestamp, and old cache entries are cleaned up on server startup.

## Setup

1. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

2. Run the application:
    ```
    uvicorn main:app --reload
    ```

3. To run with Docker:
    ```
    docker build -t document-retrieval .
    docker run -p 8000:8000 document-retrieval
    ```
