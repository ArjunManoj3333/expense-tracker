# Expense Tracker

A simple personal expense tracking web application built with Flask and SQLite.

The application allows users to record, manage, filter, and analyze their expenses through a clean web interface.

---

## Project Overview

Expense Tracker helps users manage daily expenses by:

- Adding expenses
- Editing expenses
- Deleting expenses
- Viewing expense history
- Filtering expenses
- Viewing monthly spending summaries
- Viewing category-wise spending breakdowns

The application stores data locally using SQLite and runs entirely on a local machine.

---

## Features

### Expense Management

- Add a new expense
- Edit existing expenses
- Delete expenses
- View all recorded expenses

### Expense Details

Each expense contains:

- Title
- Amount
- Category
- Date
- Note (optional)

### Categories

Supported categories:

- Food
- Transport
- Shopping
- Bills
- Entertainment
- Other

### Filters

Filter expenses by:

- Category
- Title (partial search)
- From Date
- To Date

### Monthly Summary

Displays:

- Total amount spent during the current month
- Category-wise expense breakdown

### Validation

The application validates:

- Empty titles
- Invalid amounts
- Negative amounts
- Zero amounts
- Invalid categories
- Invalid date ranges

---

## Technology Stack

### Backend

- Python 3
- Flask

### Database

- SQLite

### Frontend

- HTML
- Bootstrap 5
- Jinja2 Templates

---

## Project Structure

```text
expense-tracker/
├── database/
│   └── expenses.db
├── static/
│   ├── css/
│   └── js/
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── all_expenses.html
│   └── index.html
├── app.py
├── database.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Database Design

### Expenses Table

```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    amount REAL NOT NULL CHECK(amount > 0),
    category TEXT NOT NULL,
    expense_date DATE NOT NULL,
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd expense-tracker
```

### Create Virtual Environment

```bash
python -m venv expensetracker
```

### Activate Virtual Environment

Windows:

```bash
expensetracker\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the Flask server:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

in your browser.

---

## What Is Implemented

### Completed

- Expense creation
- Expense editing
- Expense deletion
- Expense listing
- Expense filtering
- Monthly summary
- Category breakdown
- SQLite persistence
- Input validation
- Flash messages
- Dashboard page
- Expense history page

---

## Edge Cases Handled

- Empty expense list
- Invalid amount values
- Negative amounts
- Zero amounts
- Missing title
- Invalid categories
- Invalid date ranges
- Non-existent expense edits

---

## Design Decisions & Tradeoffs

### Why Flask?

Flask is lightweight and ideal for small CRUD applications. It allows rapid development while keeping the codebase simple and maintainable.

### Why SQLite?

SQLite requires no external database setup and stores data in a single file, making it suitable for local development and small applications.

### Why Server-Side Rendering?

Using Flask templates (Jinja2) reduces complexity and allows the application to remain simple while meeting all assignment requirements.

---

## What Was Not Implemented

Due to time constraints and project scope, the following were intentionally omitted:

- User authentication
- Multi-user support
- Charts and graphs
- CSV export
- Pagination
- Dark mode
- Automated testing
- Deployment

These features can be added in future iterations.

---

## Future Improvements

- Expense charts and visualizations
- CSV export functionality
- User authentication
- Multi-user support
- Budget tracking
- Recurring expenses
- Advanced reporting
- REST API support

---

## Author

Built as a personal expense tracking application using Flask and SQLite.