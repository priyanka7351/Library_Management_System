-- =============================================================================
-- Script 04: Data Validation and Integrity Checks
-- Project: Library Management System Analysis Using SQL
-- Description: Executes audit queries to verify referential integrity,
--              business logic consistency, and data hygiene across all tables.
-- =============================================================================

USE library_db;

-- -----------------------------------------------------------------------------
-- 1. Check Row Counts Across Tables
-- -----------------------------------------------------------------------------
SELECT 'Row Count Audit' AS check_name;
SELECT 
    (SELECT COUNT(*) FROM books) AS total_books,
    (SELECT COUNT(*) FROM members) AS total_members,
    (SELECT COUNT(*) FROM borrowing) AS total_borrowings,
    (SELECT COUNT(*) FROM fines) AS total_fines;

-- -----------------------------------------------------------------------------
-- 2. Audit Orphaned Records (Referential Integrity Check)
-- All results should return 0 rows.
-- -----------------------------------------------------------------------------
-- Borrowings with non-existent books
SELECT 'Orphan Borrowings (Invalid Book ID)' AS issue, b.borrow_id, b.book_id
FROM borrowing b
LEFT JOIN books bk ON b.book_id = bk.book_id
WHERE bk.book_id IS NULL;

-- Borrowings with non-existent members
SELECT 'Orphan Borrowings (Invalid Member ID)' AS issue, b.borrow_id, b.member_id
FROM borrowing b
LEFT JOIN members m ON b.member_id = m.member_id
WHERE m.member_id IS NULL;

-- Fines with non-existent borrowing records
SELECT 'Orphan Fines (Invalid Borrow ID)' AS issue, f.fine_id, f.borrow_id
FROM fines f
LEFT JOIN borrowing b ON f.borrow_id = b.borrow_id
WHERE b.borrow_id IS NULL;

-- Fines with mismatched member records (fine member != borrow member)
SELECT 'Fine Member ID Mismatch' AS issue, f.fine_id, f.member_id AS fine_member, b.member_id AS borrow_member
FROM fines f
JOIN borrowing b ON f.borrow_id = b.borrow_id
WHERE f.member_id <> b.member_id;

-- -----------------------------------------------------------------------------
-- 3. Audit Date Logic and Sequence Integrity
-- Check that due date >= borrow date, and return date >= borrow date.
-- -----------------------------------------------------------------------------
SELECT 'Invalid Due Date (Due before Borrow)' AS issue, borrow_id, borrow_date, due_date
FROM borrowing
WHERE due_date < borrow_date;

SELECT 'Invalid Return Date (Returned before Borrow)' AS issue, borrow_id, borrow_date, return_date
FROM borrowing
WHERE return_date IS NOT NULL AND return_date < borrow_date;

SELECT 'Invalid Fine Payment Date (Paid before Fine Date)' AS issue, fine_id, fine_date, payment_date
FROM fines
WHERE payment_date IS NOT NULL AND payment_date < fine_date;

-- -----------------------------------------------------------------------------
-- 4. Audit Borrowing Status Consistency
-- Verify that 'Returned' status has a return_date, and 'Borrowed'/'Overdue' do not.
-- -----------------------------------------------------------------------------
SELECT 'Returned Without Return Date' AS issue, borrow_id, status, return_date
FROM borrowing
WHERE status = 'Returned' AND return_date IS NULL;

SELECT 'Active Borrowing With Return Date' AS issue, borrow_id, status, return_date
FROM borrowing
WHERE status IN ('Borrowed', 'Overdue') AND return_date IS NOT NULL;

-- -----------------------------------------------------------------------------
-- 5. Audit Book Copy Counts & Inventory Integrity
-- Check total_copies >= available_copies and available_copies >= 0.
-- -----------------------------------------------------------------------------
SELECT 'Available Copies Exceeds Total' AS issue, book_id, title, total_copies, available_copies
FROM books
WHERE available_copies > total_copies OR available_copies < 0;

-- -----------------------------------------------------------------------------
-- 6. Audit Duplicate Identifiers & Unique Constraints
-- -----------------------------------------------------------------------------
SELECT 'Duplicate ISBN' AS issue, isbn, COUNT(*) AS occurrences
FROM books
GROUP BY isbn
HAVING COUNT(*) > 1;

SELECT 'Duplicate Member Email' AS issue, email, COUNT(*) AS occurrences
FROM members
GROUP BY email
HAVING COUNT(*) > 1;
