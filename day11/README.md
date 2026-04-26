# Day 11 - Weather Journal API

## Overview

This project is a Weather Journal API built with Flask and SQLite.

## Features

- Create daily journal entries
- Store weather, mood, productivity score, and notes
- View all entries
- View one entry by ID
- Update an entry
- Delete an entry
- Validate date format
- Validate productivity score

## Tech Used

- Python
- Flask
- SQLite

## Entry Fields

- id
- entry_date
- weather
- mood
- productivity_score
- notes

## Valid Moods

- happy
- neutral
- sad
- tired
- focused
- stressed

## API Endpoints

### GET /

Shows API information.

### GET /entries

Get all journal entries.

### GET /entries/<{id}>

Get one journal entry by ID.

### POST /entries

Create a journal entry.

Sample JSON:

```json
{
  "entry_date": "2026-04-25",
  "weather": "sunny",
  "mood": "focused",
  "productivity_score": 8,
  "notes": "Worked on Flask API practice and completed Day 11."
}
```

### PUT /entries/<{id}>

Update a journal entry.

### DELETE /entries/<{id}>

Delete a journal entry.

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

### Create entry

```bash
curl -X POST http://127.0.0.1:5000/entries \
-H "Content-Type: application/json" \
-d '{
  "entry_date": "2026-04-25",
  "weather": "sunny",
  "mood": "focused",
  "productivity_score": 8,
  "notes": "Worked on Flask API practice and completed Day 11."
}'
```

### Get all entries

```bash
curl http://127.0.0.1:5000/entries
```

### Get one entry

```bash
curl http://127.0.0.1:5000/entries/1
```

### Update entry

```bash
curl -X PUT http://127.0.0.1:5000/entries/1 \
-H "Content-Type: application/json" \
-d '{
  "entry_date": "2026-04-25",
  "weather": "cloudy",
  "mood": "neutral",
  "productivity_score": 7,
  "notes": "Updated my journal entry after testing the API."
}'
```

### Delete entry

```bash
curl -X DELETE http://127.0.0.1:5000/entries/1
```

## Scope for Next Improvements

- Filter entries by mood
- Add average productivity score endpoint
- Add weekly productivity summary
- Add date range filter
