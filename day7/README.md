# Day 7 - Basic URL Shortener API

## Overview

This project is a basic URL Shortener API built with Flask and SQLite.

## Features

- Create short URLs
- Redirect to original URLs using short code
- View all shortened URLs
- Track number of clicks for each short URL
- View stats for a short URL
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

### GET /urls/<short_code>/stats

Get analytics for a short URL.

### GET /<short_code>

Redirect to the original URL and increase click count.

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

### Get stats for a short URL

```bash
curl http://127.0.0.1:5000/urls/abc123/stats
```

### Open in browser

```text
http://127.0.0.1:5000/abc123
```

## Scope for Next Improvements

- Add delete endpoint
- Add custom short code support
- Add user authentication
- Add better URL validation
- Add expiration dates
