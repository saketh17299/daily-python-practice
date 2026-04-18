# Day 8 - Notes API with Tags and Search

## Overview

This project is a Notes API built with Flask and SQLite.

## Features

- Create notes
- View all notes
- View a single note by ID
- Update a note
- Delete a note
- Search notes by keyword
- Filter notes by tag

## Tech Used

- Python
- Flask
- SQLite

## Note Fields

- id
- title
- content
- tags

## API Endpoints

### GET /

Shows API information.

### GET /notes

Get all notes.

### GET /notes/{id}

Get one note by ID.

### POST /notes

Create a new note.

Sample JSON:

```json
{
  "title": "Flask Practice",
  "content": "Today I built a Notes API using Flask and SQLite.",
  "tags": "python,flask,backend"
}
```

### PUT /notes/{id}

Update a note.

### DELETE /notes/{id}

Delete a note.

### GET /notes/search?q=flask

Search notes by keyword.

### GET /notes/tag/python

Get notes by tag.

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

### Create note

```bash
curl -X POST http://127.0.0.1:5000/notes \
-H "Content-Type: application/json" \
-d '{
  "title": "Flask Practice",
  "content": "Today I built a Notes API using Flask and SQLite.",
  "tags": "python,flask,backend"
}'
```

### Get all notes

```bash
curl http://127.0.0.1:5000/notes
```

### Get one note

```bash
curl http://127.0.0.1:5000/notes/1
```

### Search notes

```bash
curl "http://127.0.0.1:5000/notes/search?q=flask"
```

### Get notes by tag

```bash
curl http://127.0.0.1:5000/notes/tag/python
```

### Update note

```bash
curl -X PUT http://127.0.0.1:5000/notes/1 \
-H "Content-Type: application/json" \
-d '{
  "title": "Updated Flask Practice",
  "content": "I updated my Notes API project.",
  "tags": "python,flask,api"
}'
```

### Delete note

```bash
curl -X DELETE http://127.0.0.1:5000/notes/1
```

## Scope for Next Improvements

- Archive notes
- Favorite or star notes
- Add created_at and updated_at timestamps
- Add pagination
- Add authentication

## New Features (Day 8.1)

- Added `created_at` timestamp for note creation
- Added `updated_at` timestamp for note updates
- Automatically updates `updated_at` when note is modified
