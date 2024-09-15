
## Document Retrieval API

### Overview

This project provides a backend service for retrieving documents, designed using **FastAPI**. The application is Dockerized to ensure easy deployment and scalability. The backend also supports user management, response caching, and background web scraping tasks to gather news articles. This API is ideal for building search engines, document retrieval systems, or any other application that requires efficient document management and retrieval.

### Features

- **Document Storage**: Stores documents in an SQLite database.
- **User Management**: Tracks user requests and limits the number of API calls to prevent abuse.
- **Caching**: Caches responses for faster retrieval and improved performance.
- **Background Scraping**: Automatically scrapes news articles from a source (like Hacker News) in the background when the server starts.
- **Logging**: Provides detailed logs for monitoring API activities and debugging.
- **Dockerized**: The application is containerized using Docker, making it easy to deploy and run in any environment.

### Project Structure

```
document-retrieval-system/
├── Dockerfile
├── README.md
├── commands.txt
├── crud.py
├── database.py
├── main.py
├── models.py
├── requirements.txt
├── utils.py
├── static/
│   └── favicon.ico (optional)
└── .gitignore
```

### Getting Started

#### Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd document-retrieval-system
   ```

2. **Run Using Docker**

   Build and run the Docker container:

   ```bash
   docker build -t document-retrieval-app .
   docker run -p 8000:8000 document-retrieval-app
   ```

   This will start the FastAPI server on `http://localhost:8000`.

3. **Run Locally (Without Docker)**

   If you prefer to run the application locally without Docker:

   ```bash
   # Create a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

   # Install dependencies
   pip install -r requirements.txt

   # Start the FastAPI server
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

### API Endpoints

| Endpoint             | Method | Description                                                                                       |
|----------------------|--------|---------------------------------------------------------------------------------------------------|
| `/health`            | GET    | Returns a simple response to check if the API is active.                                           |
| `/search`            | GET    | Returns a list of top results based on a query. Accepts parameters: `query`, `top_k`, `threshold`, `user_id`. |
| `/documents`         | GET    | Lists all documents stored in the database.                                                        |
| `/clear-database`    | DELETE | Clears all documents from the database. Requires a DELETE request.                                 |

#### Example Requests

- **Check API Health**

  ```bash
  curl -X GET http://localhost:8000/health
  ```

- **Search Documents**

  ```bash
  curl -X GET "http://localhost:8000/search?query=example&top_k=5&threshold=0.5&user_id=testuser"
  ```

- **Clear Database**

  ```bash
  curl -X DELETE http://localhost:8000/clear-database
  ```

### Caching Strategy

The application currently uses SQLite for caching query results. This is suitable for a small-scale application or development environment. 

**Future Considerations**:
- For a production environment, consider using **Redis** for caching:
  - **Performance**: Redis is an in-memory data store, making it faster for caching purposes.
  - **Persistence**: Unlike memcached, Redis can persist cache to disk, reducing the risk of data loss during restarts.
  - **Data Structures**: Redis supports complex data types, which provides flexibility in managing cache data.

### Logging

The application includes logging to both the console and a file named `app.log`. Logs include information about incoming requests, responses, errors, and background tasks, providing useful insights into the application's behavior.

### Background Scraping Task

When the server starts, a background task is initiated to scrape news articles from a source (like Hacker News). This is handled in the `utils.py` file and is triggered during the application startup event. The scraped articles are then stored in the SQLite database.

### Rate Limiting

To prevent abuse, the application limits the number of API calls a user can make. If a user makes more than 5 requests, the API returns an HTTP 429 status code ("Too Many Requests"). The user’s request count is tracked in the database and updated with each request.

### Development Notes

- **Database**: Uses SQLite for simplicity, but can be replaced with a more robust database (e.g., PostgreSQL or MySQL) if needed.
- **Caching**: Currently implemented using SQLite; consider switching to Redis for production.
- **Scraping**: The scraping task is a simple demonstration. In a real-world application, consider handling retries, rate limiting, and failures more robustly.

### Improvements and Future Enhancements

- **Caching**: Replace SQLite-based caching with Redis for better performance and scalability.
- **Enhanced Rate Limiting**: Implement a more advanced rate-limiting mechanism using Redis or an API Gateway.
- **Background Jobs**: Use a task queue (like Celery) for more robust background processing.

### Troubleshooting

- **Scraping Issues**: If no articles are being scraped, check the HTML structure of the source website and update the scraping logic accordingly.
- **Rate Limiting**: If you encounter HTTP 429 too frequently during testing, consider increasing the limit or resetting the user request count in the database.
- **Database Errors**: Ensure the SQLite file (`test.db`) is accessible and not locked by another process.

