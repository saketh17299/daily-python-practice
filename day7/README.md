# Day 7 - Basic URL Shortener API

## Overview

This project is a basic URL Shortener API built with Flask and SQLite.

## Features

- Create short URLs
- Redirect to original URLs using short code
- View all shortened URLs
- Store URL mappings in SQLite

## Tech Used

- Python
- Flask
- SQLite

## API Endpoints

### GET /

Shows basic API information.

### POST /shorten

Create a short URL.

Sample JSON:

```json
{
  "original_url": "https://www.google.com"
}
```

### GET /urls

Get all shortened URLs.

### GET /<short_code>

Redirect to the original URL.

## How to Run

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Server runs at:

```text
http://127.0.0.1:5000
```

## Example Test Commands

### Create short URL

```bash
curl -X POST http://127.0.0.1:5000/shorten \
-H "Content-Type: application/json" \
-d '{
  "original_url": "https://www.google.com"
}'
```

### Get all URLs

```bash
curl http://127.0.0.1:5000/urls
```

### Open in browser

```text
http://127.0.0.1:5000/abc123
```

## Scope for Next Improvements

- Add click count tracking
- Add delete endpoint
- Add custom short code support
- Add user authentication
- Add URL validation improvements
