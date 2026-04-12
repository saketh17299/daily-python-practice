# Day 5 - Task Manager REST API

## Overview

This project is a Task Manager REST API built with Flask and SQLite.

## Features

- Create tasks
- View all tasks
- View a single task by ID
- Update a task
- Update only task status using PATCH
- Delete a task
- Filter tasks by status
- Filter tasks by priority
- Validate due date format
- Return JSON responses
- Get summary of tasks by status and priority
- Get overdue tasks

## Tech Used

- Python
- Flask
- SQLite
- REST API development

## Task Fields

- id
- title
- description
- status
- priority
- due_date

## Valid Values

### Status

- pending
- in_progress
- completed

### Priority

- low
- medium
- high

## API Endpoints

### GET /tasks

Get all tasks.

### GET /tasks?status=pending

Filter tasks by status.

### GET /tasks?priority=high

Filter tasks by priority.

### GET /tasks/summary

Get counts of tasks grouped by status and priority.

### GET /tasks/overdue

Get tasks whose due date has passed and are not completed.

### GET /tasks/{id}

Get task by ID.

### POST /tasks

Create a new task.

Sample JSON:

```json
{
  "title": "Finish Flask API",
  "description": "Complete Day 5 project",
  "status": "pending",
  "priority": "high",
  "due_date": "2026-04-13"
}
```
