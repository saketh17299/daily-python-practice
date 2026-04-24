# Day 10 - File Upload API

## Overview

This project is a File Upload API built with Flask and SQLite.

## Features

- Upload files
- Store files locally
- Save file metadata in database
- List uploaded files
- Download files

## Tech Used

- Python
- Flask
- SQLite

## API Endpoints

### POST /upload

Upload a file.

Use Postman:

- Body → form-data
- Key: `file`
- Type: File

### GET /files

Get all uploaded files.

### GET /files/<{id}>/download

Download a file.

## How to Run

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

## Scope for Next Improvements

- Delete file endpoint
- File validation
- Authentication
- Cloud storage (AWS S3)

## New Features (Day 10.1)

- Added file delete endpoint
- Added allowed file type validation
- Added max file size validation

### Allowed File Types

- txt
- pdf
- png
- jpg
- jpeg

### Max File Size

5 MB

### Delete File

DELETE /files/<{id}>
