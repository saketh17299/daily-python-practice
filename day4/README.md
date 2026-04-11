# Day 4 - Expense Tracker REST API with Flask

## Overview

This project converts the earlier expense tracker into a REST API using Flask and SQLite.

## Features

- Get all expenses
- Get an expense by ID
- Create a new expense
- Update an existing expense
- Delete an expense
- Validate JSON input
- Validate date format and amount values

## Tech Used

- Python
- Flask
- SQLite
- REST API design
- JSON request and response handling

## API Endpoints

### GET `/expenses`

Returns all expenses.

### GET `/expenses/<id>`

Returns a single expense by ID.

### POST `/expenses`

Creates a new expense.

Sample JSON:

```json
{
  "title": "Coffee",
  "category": "Food",
  "amount": 5.5,
  "expense_date": "2026-04-10"
}
```
