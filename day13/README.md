# Day 13 - API Key + Rate Limiter

## Overview

This project simulates a basic API Gateway with API key authentication and rate limiting.

## Features

- Generate API keys
- Validate API keys
- Protect endpoints
- Rate limit requests (5 per minute per key)

## Endpoints

### POST /generate-key

Generate a new API key.

### GET /protected

Access protected endpoint.

Requires header:
x-api-key: YOUR_API_KEY

## How to Run

```bash
python3 app.py
```

## New Features (Day 13.1)

- Added SQLite database for persistent API keys
- API keys remain available after server restart
- Added API key labels
- Added endpoint to list generated API keys

### Generate API Key

POST /generate-key

```json
{
  "label": "testing-key"
}
```

---

## Test commands

### Generate key

```bash
curl -X POST http://127.0.0.1:5000/generate-key \
-H "Content-Type: application/json" \
-d '{
  "label": "local-test-key"
}'
```
