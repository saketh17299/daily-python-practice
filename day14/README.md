# Day 14 - Job Application Tracker API

## Overview

This project is a Job Application Tracker API built using Flask and SQLite.

It helps track job applications, including company, role, status, and notes — useful for organizing your job search.

---

## Features

- Add a new job application
- View all applications
- View application by ID
- Update application details
- Delete an application

---

## Tech Stack

- Python
- Flask
- SQLite

---

## Application Fields

- id
- company
- role
- status
- applied_date
- notes (optional)

---

## Valid Status Values

- applied
- interview
- offer
- rejected
- withdrawn

---

## API Endpoints

### GET /

Returns API info.

---

### GET /applications

Get all applications.

---

### GET /applications/<{id}>

Get application by ID.

---

### POST /applications

Create a new application.

#### Sample Request

```json
{
  "company": "Google",
  "role": "Software Engineer Intern",
  "status": "applied",
  "applied_date": "2026-05-01",
  "notes": "Applied via careers page"
}
```
