# Day 12 - Expense Tracker API

## Overview

This project is a simple Expense Tracker API built using Flask and SQLite.

It allows users to track daily expenses, categorize them, and filter based on category or date range.

---

## Features

- Add a new expense
- View all expenses
- Update an expense
- Delete an expense
- Filter expenses by category
- Filter expenses by date range

---

## Tech Stack

- Python
- Flask
- SQLite

---

## Expense Fields

- id
- title
- amount
- category
- expense_date
- notes (optional)

---

## Valid Categories

- food
- travel
- shopping
- bills
- health
- other

---

## API Endpoints

### GET /

Returns API information and available endpoints.

---

### GET /expenses

Get all expenses.

---

### GET /expenses?category=food

Filter expenses by category.

---

### GET /expenses?start_date=2026-04-01&end_date=2026-04-30

Filter expenses by date range.

---

### POST /expenses

Create a new expense.

#### Sample Request

```json
{
  "title": "Lunch",
  "amount": 12.5,
  "category": "food",
  "expense_date": "2026-04-28",
  "notes": "Ate at a restaurant"
}
```
