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
