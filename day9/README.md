# Day 9 - Student Grades API

## Overview

This project is a Student Grades API built with Flask and SQLite.

## Features

- Add student records
- View all students
- View one student by ID
- Update student marks
- Delete student record
- Automatically calculate average
- Automatically calculate pass/fail result
- Automatically calculate grade letter
- Filter students by result

## Tech Used

- Python
- Flask
- SQLite

## Student Fields

- id
- name
- math_marks
- science_marks
- english_marks
- average
- result
- grade

## Result Logic

- A student passes only if marks in all subjects are 35 or above
- Otherwise result is Fail

## Grade Logic

- A: 90 and above
- B: 75 to 89.99
- C: 60 to 74.99
- D: 50 to 59.99
- F: below 50

## API Endpoints

### GET /

Shows API information.

### GET /students

Get all student records.

### GET /students?result=Pass

Get only passed students.

### GET /students?result=Fail

Get only failed students.

### GET /students/{id}

Get one student by ID.

### POST /students

Create a new student record.

Sample JSON:

```json
{
  "name": "Sharath",
  "math_marks": 85,
  "science_marks": 78,
  "english_marks": 90
}
```

### PUT /students/{id}

Update a student record.

### DELETE /students/{id}

Delete a student record.

## How to Run

```bash
rm students.db
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

### Create student

```bash
curl -X POST http://127.0.0.1:5000/students \
-H "Content-Type: application/json" \
-d '{
  "name": "Sharath",
  "math_marks": 85,
  "science_marks": 78,
  "english_marks": 90
}'
```

### Get all students

```bash
curl http://127.0.0.1:5000/students
```

### Get only passed students

```bash
curl "http://127.0.0.1:5000/students?result=Pass"
```

### Get only failed students

```bash
curl "http://127.0.0.1:5000/students?result=Fail"
```

### Get one student

```bash
curl http://127.0.0.1:5000/students/1
```

### Update student

```bash
curl -X PUT http://127.0.0.1:5000/students/1 \
-H "Content-Type: application/json" \
-d '{
  "name": "Sharath Reddy",
  "math_marks": 88,
  "science_marks": 82,
  "english_marks": 91
}'
```

### Delete student

```bash
curl -X DELETE http://127.0.0.1:5000/students/1
```

## Scope for Next Improvements

- Add topper endpoint
- Add search by student name
- Add pagination
- Add subject-wise analytics
