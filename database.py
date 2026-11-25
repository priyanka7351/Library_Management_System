import sqlite3
import os
import pandas as pd
from datetime import datetime, date

DB_NAME = "library.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    # Enforce foreign key constraints at database engine level
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Books Table with Domain and Integrity Constraints
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        book_id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        category TEXT NOT NULL,
        isbn TEXT NOT NULL,
        publication_year INTEGER CHECK(publication_year >= 1500),
        total_copies INTEGER NOT NULL CHECK(total_copies >= 0),
        available_copies INTEGER NOT NULL CHECK(available_copies >= 0),
        price REAL NOT NULL CHECK(price >= 0.0)
    );
    """)

    # 2. Members Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS members (
        member_id TEXT PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT,
        membership_type TEXT DEFAULT 'Student' CHECK(membership_type IN ('Student', 'Faculty', 'General', 'Premium')),
        registration_date TEXT NOT NULL,
        status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive', 'Suspended'))
    );
    """)

    # 3. Borrowing Table (Transactions with Foreign Keys)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS borrowing (
        borrow_id TEXT PRIMARY KEY,
        book_id TEXT NOT NULL,
        member_id TEXT NOT NULL,
        borrow_date TEXT NOT NULL,
        due_date TEXT NOT NULL,
        return_date TEXT,
        status TEXT DEFAULT 'Issued' CHECK(status IN ('Issued', 'Returned')),
        FOREIGN KEY (book_id) REFERENCES books(book_id) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (member_id) REFERENCES members(member_id) ON UPDATE CASCADE ON DELETE RESTRICT
    );
    """)

    # 4. Fines Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fines (
        fine_id TEXT PRIMARY KEY,
        borrow_id TEXT NOT NULL,
        member_id TEXT NOT NULL,
        fine_amount REAL NOT NULL CHECK(fine_amount >= 0.0),
        fine_date TEXT NOT NULL,
        payment_status TEXT DEFAULT 'Unpaid' CHECK(payment_status IN ('Unpaid', 'Paid')),
        payment_date TEXT,
        FOREIGN KEY (borrow_id) REFERENCES borrowing(borrow_id) ON DELETE CASCADE,
        FOREIGN KEY (member_id) REFERENCES members(member_id) ON DELETE RESTRICT
    );
    """)

    # 5. DBMS Relational Views
    cursor.execute("""
    CREATE VIEW IF NOT EXISTS v_active_borrowings AS
    SELECT 
        b.borrow_id, 
        b.borrow_date, 
        b.due_date, 
        bk.book_id,
        bk.title AS book_title, 
        (m.first_name || ' ' || m.last_name) AS member_name,
        m.email AS member_email
    FROM borrowing b
    JOIN books bk ON b.book_id = bk.book_id
    JOIN members m ON b.member_id = m.member_id
    WHERE b.status = 'Issued'
    ORDER BY b.due_date ASC;
    """)

    cursor.execute("""
    CREATE VIEW IF NOT EXISTS v_unpaid_fines AS
    SELECT 
        f.fine_id, 
        f.borrow_id, 
        (m.first_name || ' ' || m.last_name) AS member_name,
        f.fine_amount, 
        f.fine_date,
        b.due_date
    FROM fines f
    JOIN members m ON f.member_id = m.member_id
    JOIN borrowing b ON f.borrow_id = b.borrow_id
    WHERE f.payment_status = 'Unpaid';
    """)

    # 6. Database Triggers (DBMS Logic at Database Level)
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS trg_decrement_stock_on_issue
    AFTER INSERT ON borrowing
    WHEN NEW.status = 'Issued'
    BEGIN
        UPDATE books 
        SET available_copies = available_copies - 1
        WHERE book_id = NEW.book_id;
    END;
    """)

    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS trg_increment_stock_on_return
    AFTER UPDATE OF status ON borrowing
    WHEN NEW.status = 'Returned' AND OLD.status != 'Returned'
    BEGIN
        UPDATE books 
        SET available_copies = available_copies + 1
        WHERE book_id = NEW.book_id;
    END;
    """)

    conn.commit()

    # Seed data if empty
    cursor.execute("SELECT COUNT(*) FROM books")
    if cursor.fetchone()[0] == 0:
        seed_data(conn)

    conn.close()

def seed_data(conn):
    data_dir = "data"
    
    books_path = os.path.join(data_dir, "books.csv")
    if os.path.exists(books_path):
        df_books = pd.read_csv(books_path)
        df_books.to_sql("books", conn, if_exists="append", index=False)

    members_path = os.path.join(data_dir, "members.csv")
    if os.path.exists(members_path):
        df_members = pd.read_csv(members_path)
        df_members.to_sql("members", conn, if_exists="append", index=False)

    borrowing_path = os.path.join(data_dir, "borrowing.csv")
    if os.path.exists(borrowing_path):
        df_borrow = pd.read_csv(borrowing_path)
        df_borrow.to_sql("borrowing", conn, if_exists="append", index=False)

    fines_path = os.path.join(data_dir, "fines.csv")
    if os.path.exists(fines_path):
        df_fines = pd.read_csv(fines_path)
        df_fines.to_sql("fines", conn, if_exists="append", index=False)

# ---------------- Book Functions (CRUD) ----------------

def get_all_books(search=""):
    conn = get_connection()
    cursor = conn.cursor()
    if search:
        query = """
        SELECT * FROM books 
        WHERE title LIKE ? OR author LIKE ? OR category LIKE ? OR book_id LIKE ?
        ORDER BY title ASC
        """
        term = f"%{search}%"
        cursor.execute(query, (term, term, term, term))
    else:
        cursor.execute("SELECT * FROM books ORDER BY title ASC")
    
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def add_new_book(book_id, title, author, category, isbn, year, copies, price):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT book_id FROM books WHERE book_id = ?", (book_id,))
        if cursor.fetchone():
            return False, f"Duplicate Key: Book ID '{book_id}' already exists in catalog."
        cursor.execute("SELECT book_id, title FROM books WHERE isbn = ?", (isbn,))
        existing_isbn = cursor.fetchone()
        if existing_isbn:
            return False, f"Unique Constraint: ISBN '{isbn}' is already registered to '{existing_isbn['title']}'."

        cursor.execute("""
        INSERT INTO books (book_id, title, author, category, isbn, publication_year, total_copies, available_copies, price)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (book_id, title, author, category, isbn, year, copies, copies, price))
        conn.commit()
        return True, f"Book '{title}' added successfully!"
    except sqlite3.IntegrityError as e:
        return False, f"Integrity Constraint Violation: {str(e)}"
    finally:
        conn.close()

def delete_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Check if currently issued
    cursor.execute("SELECT COUNT(*) FROM borrowing WHERE book_id = ? AND status = 'Issued'", (book_id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return False, "Referential Integrity: Cannot delete a book that is currently issued to active borrower(s)."

    # 2. Check if past loan history exists (Referential Integrity & Audit Trail)
    cursor.execute("SELECT COUNT(*) FROM borrowing WHERE book_id = ?", (book_id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return False, "Referential Integrity (ON DELETE RESTRICT): Book has historical borrowing records and cannot be deleted to preserve the library audit log."

    try:
        cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
        conn.commit()
        return True, "Book deleted successfully."
    except sqlite3.IntegrityError as e:
        return False, f"Referential Integrity Constraint Failed: {str(e)}"
    finally:
        conn.close()

# ---------------- Member Functions ----------------

def get_all_members():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members ORDER BY member_id DESC")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def add_new_member(member_id, first_name, last_name, email, phone, membership_type):
    conn = get_connection()
    cursor = conn.cursor()
    today = date.today().strftime("%Y-%m-%d")
    try:
        cursor.execute("SELECT member_id FROM members WHERE member_id = ?", (member_id,))
        if cursor.fetchone():
            return False, f"Duplicate Key: Member ID '{member_id}' already exists."
        cursor.execute("SELECT member_id FROM members WHERE email = ?", (email,))
        if cursor.fetchone():
            return False, f"Unique Constraint: Email '{email}' is already registered."

        cursor.execute("""
        INSERT INTO members (member_id, first_name, last_name, email, phone, membership_type, registration_date, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'Active')
        """, (member_id, first_name, last_name, email, phone, membership_type, today))
        conn.commit()
        return True, f"Member '{first_name} {last_name}' registered successfully!"
    except sqlite3.IntegrityError as e:
        return False, f"Integrity Constraint Violation: {str(e)}"
    finally:
        conn.close()

# ---------------- ACID Circulation Logic (Issue & Return) ----------------

def issue_book(book_id, member_id, due_date):
    """
    ACID Transaction for Book Issue:
    1. Validates available stock > 0.
    2. Validates temporal constraints (due_date > today).
    3. Prevents duplicate active loan of the same book to the same patron.
    4. Enforces patron borrowing quota (max 5 active books).
    5. Blocks borrowing if patron has overdue unpaid fines > $20.00.
    6. Uses safe monotonic MAX() ID generation to prevent PK collisions.
    7. Trigger automatically decrements available_copies in books table.
    8. Commits transaction atomically or rolls back on any error.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Check stock availability
        cursor.execute("SELECT available_copies, title FROM books WHERE book_id = ?", (book_id,))
        book = cursor.fetchone()
        if not book:
            return False, "Book ID not found in database."
        if book["available_copies"] <= 0:
            return False, f"Integrity Constraint: '{book['title']}' is currently out of stock."

        # Check member status
        cursor.execute("SELECT status, first_name, last_name FROM members WHERE member_id = ?", (member_id,))
        member = cursor.fetchone()
        if not member:
            return False, "Member ID not found in database."
        if member["status"] != "Active":
            return False, f"Patron status is '{member['status']}'. Only active patrons can borrow books."

        # Temporal Constraint: Due date cannot be in the past or earlier than today
        borrow_date_obj = date.today()
        borrow_date = borrow_date_obj.strftime("%Y-%m-%d")
        try:
            due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
        except ValueError:
            return False, "Invalid due date format. Expected YYYY-MM-DD."

        if due_date_obj < borrow_date_obj:
            return False, "Temporal Constraint: Due date cannot be earlier than issue date."
        
        if (due_date_obj - borrow_date_obj).days > 365:
            return False, "Policy Constraint: Maximum loan period cannot exceed 365 days (1 year)."

        # Duplicate loan check: Member cannot have 2 active issues of the same title
        cursor.execute("""
        SELECT COUNT(*) FROM borrowing 
        WHERE member_id = ? AND book_id = ? AND status = 'Issued'
        """, (member_id, book_id))
        if cursor.fetchone()[0] > 0:
            return False, f"Duplicate Active Loan: Member already has a copy of '{book['title']}' currently checked out."

        # Patron quota check: Max 5 active loans
        cursor.execute("SELECT COUNT(*) FROM borrowing WHERE member_id = ? AND status = 'Issued'", (member_id,))
        active_loans = cursor.fetchone()[0]
        if active_loans >= 5:
            return False, "Borrowing Quota Exceeded: Patron already has 5 active borrowed books. Return previous books first."

        # Unpaid overdue fines check: Block borrowing if patron owes > $20.00
        cursor.execute("SELECT SUM(fine_amount) FROM fines WHERE member_id = ? AND payment_status = 'Unpaid'", (member_id,))
        unpaid_fines = cursor.fetchone()[0] or 0.0
        if unpaid_fines > 20.0:
            return False, f"Circulation Blocked: Patron has ${unpaid_fines:.2f} in unpaid overdue fines. Please clear fines before borrowing."

        # Safe monotonic Borrow ID generation
        cursor.execute("SELECT MAX(CAST(SUBSTR(borrow_id, 3) AS INTEGER)) FROM borrowing")
        max_id = cursor.fetchone()[0]
        next_num = (max_id + 1) if max_id else 1001
        borrow_id = f"BR{next_num}"

        # Execute insertion (Trigger automatically decrements available_copies)
        cursor.execute("""
        INSERT INTO borrowing (borrow_id, book_id, member_id, borrow_date, due_date, status)
        VALUES (?, ?, ?, ?, ?, 'Issued')
        """, (borrow_id, book_id, member_id, borrow_date, due_date))

        conn.commit()
        return True, f"Transaction committed successfully! Borrow ID: {borrow_id}"
    except Exception as e:
        conn.rollback()
        return False, f"Transaction Aborted (Rollback): {str(e)}"
    finally:
        conn.close()

def return_book(borrow_id, return_date=None, daily_fine=2.0):
    """
    ACID Transaction for Book Return & Late Fee Calculation:
    1. Updates borrowing record to 'Returned'.
    2. Trigger automatically increments available_copies in books table.
    3. If returned late, generates penalty in fines table with safe ID.
    4. Commits transaction atomically.
    """
    conn = get_connection()
    cursor = conn.cursor()

    if not return_date:
        return_date = date.today().strftime("%Y-%m-%d")

    try:
        cursor.execute("SELECT * FROM borrowing WHERE borrow_id = ?", (borrow_id,))
        record = cursor.fetchone()
        if not record:
            return False, "Borrow record not found."
        if record["status"] == "Returned":
            return False, "Idempotency Check: This book has already been returned."

        member_id = record["member_id"]
        try:
            due_date = datetime.strptime(record["due_date"], "%Y-%m-%d").date()
            borrow_date = datetime.strptime(record["borrow_date"], "%Y-%m-%d").date()
            ret_date = datetime.strptime(return_date, "%Y-%m-%d").date()
        except ValueError:
            return False, "Invalid return date format. Expected YYYY-MM-DD."

        if ret_date < borrow_date:
            return False, "Temporal Constraint: Return date cannot be earlier than borrow date."

        # Update borrowing status (Trigger will automatically restore stock +1)
        cursor.execute("""
        UPDATE borrowing 
        SET return_date = ?, status = 'Returned' 
        WHERE borrow_id = ?
        """, (return_date, borrow_id))

        msg = "Book returned on schedule. Stock restored."

        # Calculate late penalty
        if ret_date > due_date:
            days_late = (ret_date - due_date).days
            amount = round(days_late * daily_fine, 2)

            cursor.execute("SELECT MAX(CAST(SUBSTR(fine_id, 3) AS INTEGER)) FROM fines")
            max_fine = cursor.fetchone()[0]
            next_fnum = (max_fine + 1) if max_fine else 501
            fine_id = f"FN{next_fnum}"

            cursor.execute("""
            INSERT INTO fines (fine_id, borrow_id, member_id, fine_amount, fine_date, payment_status)
            VALUES (?, ?, ?, ?, ?, 'Unpaid')
            """, (fine_id, borrow_id, member_id, amount, return_date))

            msg = f"Overdue by {days_late} day(s). Penalty of ${amount:.2f} assessed (Fine ID: {fine_id})."

        conn.commit()
        return True, msg
    except Exception as e:
        conn.rollback()
        return False, f"Transaction Aborted (Rollback): {str(e)}"
    finally:
        conn.close()

def get_active_borrowings():
    """Queries the SQL View v_active_borrowings."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM v_active_borrowings")
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

# ---------------- Fine Functions ----------------

def get_all_fines():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT f.fine_id, f.borrow_id, 
           (m.first_name || ' ' || m.last_name) AS member_name,
           f.fine_amount, f.fine_date, f.payment_status, f.payment_date
    FROM fines f
    JOIN members m ON f.member_id = m.member_id
    ORDER BY f.fine_id DESC
    """)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def mark_fine_as_paid(fine_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT payment_status, fine_amount FROM fines WHERE fine_id = ?", (fine_id,))
        fine = cursor.fetchone()
        if not fine:
            return False, "Fine record not found."
        if fine["payment_status"] == "Paid":
            return False, "Idempotency Check: This fine has already been paid and settled."

        today = date.today().strftime("%Y-%m-%d")
        cursor.execute("""
        UPDATE fines 
        SET payment_status = 'Paid', payment_date = ? 
        WHERE fine_id = ?
        """, (today, fine_id))
        conn.commit()
        return True, f"Fine {fine_id} of ${fine['fine_amount']:.2f} marked as Paid."
    finally:
        conn.close()

# ---------------- Dashboard Stats ----------------

def get_dashboard_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*), SUM(total_copies), SUM(available_copies) FROM books")
    b_count, b_total, b_avail = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) FROM members WHERE status = 'Active'")
    m_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM borrowing WHERE status = 'Issued'")
    issued_count = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(fine_amount) FROM fines WHERE payment_status = 'Unpaid'")
    unpaid = cursor.fetchone()[0] or 0.0

    conn.close()
    return {
        "total_titles": b_count or 0,
        "total_copies": b_total or 0,
        "available_copies": b_avail or 0,
        "active_members": m_count or 0,
        "currently_issued": issued_count or 0,
        "unpaid_fines": round(unpaid, 2)
    }
