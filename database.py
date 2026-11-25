import sqlite3
from datetime import date, datetime

DB_NAME = "library.db"


def connect():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = connect()

    conn.executescript("""
    CREATE TABLE IF NOT EXISTS books (
        book_id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        category TEXT,
        isbn TEXT,
        publication_year INTEGER,
        total_copies INTEGER,
        available_copies INTEGER,
        price REAL
    );

    CREATE TABLE IF NOT EXISTS members (
        member_id TEXT PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT,
        email TEXT UNIQUE NOT NULL,
        phone TEXT,
        membership_type TEXT,
        registration_date TEXT,
        status TEXT DEFAULT 'Active'
    );

    CREATE TABLE IF NOT EXISTS borrowing (
        borrow_id TEXT PRIMARY KEY,
        book_id TEXT,
        member_id TEXT,
        borrow_date TEXT,
        due_date TEXT,
        return_date TEXT,
        status TEXT DEFAULT 'Issued',
        FOREIGN KEY(book_id) REFERENCES books(book_id),
        FOREIGN KEY(member_id) REFERENCES members(member_id)
    );

    CREATE TABLE IF NOT EXISTS fines (
        fine_id TEXT PRIMARY KEY,
        borrow_id TEXT,
        member_id TEXT,
        fine_amount REAL,
        fine_date TEXT,
        payment_status TEXT DEFAULT 'Unpaid',
        payment_date TEXT,
        FOREIGN KEY(borrow_id) REFERENCES borrowing(borrow_id),
        FOREIGN KEY(member_id) REFERENCES members(member_id)
    );
    """)

    conn.commit()
    conn.close()


# Books
def get_all_books(search=""):
    conn = connect()

    books = conn.execute("""
        SELECT * FROM books
        WHERE title LIKE ? OR author LIKE ? OR book_id LIKE ?
        ORDER BY title
    """, (f"%{search}%", f"%{search}%", f"%{search}%")).fetchall()

    conn.close()
    return [dict(b) for b in books]


def add_new_book(book_id, title, author, category, isbn, year, copies, price):
    conn = connect()

    try:
        conn.execute("""
            INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (book_id, title, author, category, isbn, year,
              copies, copies, price))

        conn.commit()
        return True, "Book added successfully"

    except sqlite3.IntegrityError:
        return False, "Book ID or ISBN already exists"

    finally:
        conn.close()


def delete_book(book_id):
    conn = connect()

    try:
        conn.execute("DELETE FROM books WHERE book_id=?", (book_id,))
        conn.commit()
        return True, "Book deleted"

    except sqlite3.IntegrityError:
        return False, "This book has borrowing records"

    finally:
        conn.close()


# Members
def get_all_members():
    conn = connect()
    members = conn.execute("SELECT * FROM members").fetchall()
    conn.close()
    return [dict(m) for m in members]


def add_new_member(member_id, first_name, last_name, email, phone, membership_type):
    conn = connect()

    try:
        conn.execute("""
            INSERT INTO members
            (member_id, first_name, last_name, email, phone,
             membership_type, registration_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'Active')
        """, (member_id, first_name, last_name, email, phone,
              membership_type, str(date.today())))

        conn.commit()
        return True, "Member added successfully"

    except sqlite3.IntegrityError:
        return False, "Member ID or email already exists"

    finally:
        conn.close()


# Issue book
def issue_book(book_id, member_id, due_date):
    conn = connect()

    try:
        book = conn.execute(
            "SELECT available_copies FROM books WHERE book_id=?",
            (book_id,)
        ).fetchone()

        member = conn.execute(
            "SELECT status FROM members WHERE member_id=?",
            (member_id,)
        ).fetchone()

        if not book:
            return False, "Book not found"

        if book["available_copies"] <= 0:
            return False, "Book is not available"

        if not member:
            return False, "Member not found"

        if member["status"] != "Active":
            return False, "Member is not active"

        borrow_id = "BR" + str(
            conn.execute("SELECT COUNT(*) FROM borrowing").fetchone()[0] + 1001
        )

        today = str(date.today())

        conn.execute("""
            INSERT INTO borrowing
            (borrow_id, book_id, member_id, borrow_date, due_date, status)
            VALUES (?, ?, ?, ?, ?, 'Issued')
        """, (borrow_id, book_id, member_id, today, due_date))

        conn.execute("""
            UPDATE books
            SET available_copies = available_copies - 1
            WHERE book_id=?
        """, (book_id,))

        conn.commit()
        return True, "Book issued successfully"

    except Exception as e:
        conn.rollback()
        return False, str(e)

    finally:
        conn.close()


# Return book
def return_book(borrow_id, return_date=None, daily_fine=2):
    conn = connect()

    try:
        record = conn.execute("""
            SELECT * FROM borrowing WHERE borrow_id=?
        """, (borrow_id,)).fetchone()

        if not record:
            return False, "Borrowing record not found"

        if record["status"] == "Returned":
            return False, "Book already returned"

        return_date = return_date or str(date.today())

        due = datetime.strptime(record["due_date"], "%Y-%m-%d").date()
        returned = datetime.strptime(return_date, "%Y-%m-%d").date()

        conn.execute("""
            UPDATE borrowing
            SET status='Returned', return_date=?
            WHERE borrow_id=?
        """, (return_date, borrow_id))

        conn.execute("""
            UPDATE books
            SET available_copies = available_copies + 1
            WHERE book_id=?
        """, (record["book_id"],))

        message = "Book returned successfully"

        if returned > due:
            days = (returned - due).days
            amount = days * daily_fine

            fine_id = "FN" + str(
                conn.execute("SELECT COUNT(*) FROM fines").fetchone()[0] + 501
            )

            conn.execute("""
                INSERT INTO fines
                (fine_id, borrow_id, member_id, fine_amount, fine_date)
                VALUES (?, ?, ?, ?, ?)
            """, (fine_id, borrow_id, record["member_id"],
                  amount, return_date))

            message = f"Late return. Fine: {amount}"

        conn.commit()
        return True, message

    except Exception as e:
        conn.rollback()
        return False, str(e)

    finally:
        conn.close()


# Borrowing records
def get_active_borrowings():
    conn = connect()

    rows = conn.execute("""
        SELECT b.borrow_id, b.book_id, bk.title AS book_title,
               b.member_id,
               m.first_name || ' ' || m.last_name AS member_name,
               b.borrow_date, b.due_date, b.status
        FROM borrowing b
        JOIN books bk ON b.book_id=bk.book_id
        JOIN members m ON b.member_id=m.member_id
        WHERE b.status='Issued'
    """).fetchall()

    conn.close()
    return [dict(r) for r in rows]


# Fines
def get_all_fines():
    conn = connect()

    rows = conn.execute("""
        SELECT f.*, m.first_name || ' ' || m.last_name AS member_name
        FROM fines f
        JOIN members m ON f.member_id=m.member_id
        ORDER BY f.fine_id DESC
    """).fetchall()

    conn.close()
    return [dict(r) for r in rows]


def mark_fine_as_paid(fine_id):
    conn = connect()

    fine = conn.execute(
        "SELECT * FROM fines WHERE fine_id=?", (fine_id,)
    ).fetchone()

    if not fine:
        conn.close()
        return False, "Fine not found"

    if fine["payment_status"] == "Paid":
        conn.close()
        return False, "Fine already paid"

    conn.execute("""
        UPDATE fines
        SET payment_status='Paid', payment_date=?
        WHERE fine_id=?
    """, (str(date.today()), fine_id))

    conn.commit()
    conn.close()
    return True, "Fine paid successfully"


# Dashboard
def get_dashboard_stats():
    conn = connect()

    total_books = conn.execute(
        "SELECT COUNT(*) FROM books"
    ).fetchone()[0]

    total_copies = conn.execute(
        "SELECT SUM(total_copies) FROM books"
    ).fetchone()[0] or 0

    available = conn.execute(
        "SELECT SUM(available_copies) FROM books"
    ).fetchone()[0] or 0

    members = conn.execute(
        "SELECT COUNT(*) FROM members WHERE status='Active'"
    ).fetchone()[0]

    borrowed = conn.execute(
        "SELECT COUNT(*) FROM borrowing WHERE status='Issued'"
    ).fetchone()[0]

    fines = conn.execute(
        "SELECT SUM(fine_amount) FROM fines WHERE payment_status='Unpaid'"
    ).fetchone()[0] or 0

    conn.close()

    return {
        "total_titles": total_books,
        "total_copies": total_copies,
        "available_copies": available,
        "active_members": members,
        "currently_issued": borrowed,
        "unpaid_fines": fines
    }
