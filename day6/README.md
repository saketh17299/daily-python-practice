# Day 6 - Task Manager API with Basic Authentication

## Overview

This project extends the Task Manager REST API by adding basic user authentication using Flask and SQLite.

## Features

- User registration
- User login
- Token-based authentication
- Protected task endpoints
- Create, read, update, and delete tasks
- Update only task status
- Filter tasks by status and priority
- Task summary endpoint
- Overdue tasks endpoint

## Tech Used

- Python
- Flask
- SQLite
- REST API development

## Authentication Flow

- Logout endpoint to invalidate token

### Register

`POST /register`

Sample JSON:

```json
{
  "username": "sharath",
  "password": "1234"
}
```

### Logout

`POST /logout`
Invalidates the current user's token.
