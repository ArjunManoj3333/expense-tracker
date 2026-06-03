from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from database import init_db, get_connection
app = Flask(__name__)
app.secret_key = "expense-tracker-secret"
init_db()

CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"]

def get_monthly_summary(cursor):
    current_month = date.today().strftime("%Y-%m")
    
    # Total
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0) FROM expenses 
        WHERE strftime('%Y-%m', expense_date) = ?
    """, (current_month,))
    monthly_total = cursor.fetchone()[0]

    # Breakdown
    cursor.execute("""
        SELECT category, SUM(amount) AS total FROM expenses
        WHERE strftime('%Y-%m', expense_date) = ?
        GROUP BY category ORDER BY total DESC
    """, (current_month,))
    category_breakdown = cursor.fetchall()

    return monthly_total, category_breakdown

@app.route("/")
def dashboard():
    conn = get_connection()
    cursor = conn.cursor()

    monthly_total, category_breakdown = get_monthly_summary(cursor)

    cursor.execute("""
        SELECT * FROM expenses 
        ORDER BY expense_date DESC, created_at DESC LIMIT 5
    """)
    recent_expenses = cursor.fetchall()
    conn.close()

    # Get the current month name (e.g., "June")
    current_month_name = datetime.now().strftime("%B")

    return render_template(
        "dashboard.html",
        categories=CATEGORIES,
        today=date.today().isoformat(),
        recent_expenses=recent_expenses,
        monthly_total=monthly_total,
        category_breakdown=category_breakdown,
        edit_expense=None,
        current_month_name=current_month_name # <--- Pass it to the template
    )

@app.route("/all-expenses")
def all_expenses():
    conn = get_connection()
    cursor = conn.cursor()

    category = request.args.get("category", "")
    title = request.args.get("title", "").strip()
    date_from = request.args.get("date_from", "")
    date_to = request.args.get("date_to", "")

    if date_from and date_to and date_from > date_to:
        return "From date cannot be later than To date", 400

    query = "SELECT * FROM expenses WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)
    if title:
        query += " AND title LIKE ?"
        params.append(f"%{title}%")
    if date_from:
        query += " AND expense_date >= ?"
        params.append(date_from)
    if date_to:
        query += " AND expense_date <= ?"
        params.append(date_to)

    query += " ORDER BY expense_date DESC, created_at DESC"

    cursor.execute(query, params)
    expenses = cursor.fetchall()
    conn.close()

    return render_template(
        "all_expenses.html",
        categories=CATEGORIES,
        today=date.today().isoformat(),
        expenses=expenses,
        filters={"category": category, "title": title, "date_from": date_from, "date_to": date_to},
        edit_expense=None
    )

@app.route("/expenses", methods=["POST"])
def add_expense():
    title = request.form.get("title", "").strip()
    amount = request.form.get("amount")
    category = request.form.get("category")
    expense_date = request.form.get("expense_date")
    note = request.form.get("note", "").strip()

    if not title:
        flash("Title is required", "danger")
        return redirect(url_for("dashboard"))

    try:
        amount = float(amount)

        if amount <= 0:
            flash("Amount must be greater than 0", "danger")
            return redirect(url_for("dashboard"))

    except (ValueError, TypeError):
        flash("Invalid amount", "danger")
        return redirect(url_for("dashboard"))

    if category not in CATEGORIES:
        flash("Invalid category", "danger")
        return redirect(url_for("dashboard"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (title, amount, category, expense_date, note)
        VALUES (?, ?, ?, ?, ?)
    """, (
        title,
        amount,
        category,
        expense_date,
        note
    ))

    conn.commit()
    conn.close()

    flash("Expense added successfully", "success")

    return redirect(url_for("dashboard"))

@app.route("/expenses/edit/<int:expense_id>")
def edit_expense(expense_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM expenses WHERE id = ?",
        (expense_id,)
    )

    expense = cursor.fetchone()

    if expense is None:
        conn.close()
        return "Expense not found", 404

    monthly_total, category_breakdown = get_monthly_summary(cursor)

    cursor.execute("""
        SELECT *
        FROM expenses
        ORDER BY expense_date DESC, created_at DESC
        LIMIT 5
    """)

    recent_expenses = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        categories=CATEGORIES,
        today=date.today().isoformat(),
        recent_expenses=recent_expenses,
        monthly_total=monthly_total,
        category_breakdown=category_breakdown,
        edit_expense=expense,
        current_month_name=datetime.now().strftime("%B")
    )

@app.route("/expenses/update/<int:expense_id>", methods=["POST"])
def update_expense(expense_id):
    title = request.form.get("title", "").strip()
    amount = request.form.get("amount")
    category = request.form.get("category")
    expense_date = request.form.get("expense_date")
    note = request.form.get("note", "").strip()

    if not title:
        flash("Title is required", "danger")
        return redirect(url_for("dashboard"))

    try:
        amount = float(amount)

        if amount <= 0:
            flash("Amount must be greater than 0", "danger")
            return redirect(url_for("dashboard"))

    except (ValueError, TypeError):
        flash("Invalid amount", "danger")
        return redirect(url_for("dashboard"))

    if category not in CATEGORIES:
        flash("Invalid category", "danger")
        return redirect(url_for("dashboard"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM expenses WHERE id = ?",
        (expense_id,)
    )

    if cursor.fetchone() is None:
        conn.close()
        flash("Expense not found", "danger")
        return redirect(url_for("dashboard"))

    cursor.execute("""
        UPDATE expenses
        SET
            title = ?,
            amount = ?,
            category = ?,
            expense_date = ?,
            note = ?
        WHERE id = ?
    """, (
        title,
        amount,
        category,
        expense_date,
        note,
        expense_id
    ))

    conn.commit()
    conn.close()

    flash("Expense updated successfully", "success")

    return redirect(url_for("dashboard"))

@app.route("/expenses/delete/<int:expense_id>", methods=["POST"])
def delete_expense(expense_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()
    
    # Check referring page so we redirect back to where they clicked delete
    return redirect(request.referrer or url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)