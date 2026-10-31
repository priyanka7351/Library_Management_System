-- =============================================================================
-- Script 05: Basic SQL Analysis
-- Project: Library Management System Analysis Using SQL
-- Description: Core summary and descriptive statistics queries providing
--              immediate operational visibility into the library system.
-- =============================================================================

USE library_db;

-- -----------------------------------------------------------------------------
-- 1. Executive Summary KPI Snapshot
-- -----------------------------------------------------------------------------
SELECT 
    (SELECT COUNT(*) FROM books) AS total_unique_titles,
    (SELECT SUM(total_copies) FROM books) AS total_inventory_volume,
    (SELECT SUM(available_copies) FROM books) AS currently_available_books,
    (SELECT COUNT(*) FROM members WHERE status = 'Active') AS active_members,
    (SELECT COUNT(*) FROM borrowing) AS total_borrowing_transactions,
    (SELECT COUNT(*) FROM borrowing WHERE status IN ('Borrowed', 'Overdue')) AS active_rentals,
    (SELECT ROUND(SUM(fine_amount), 2) FROM fines) AS total_fines_levied,
    (SELECT ROUND(SUM(fine_amount), 2) FROM fines WHERE payment_status = 'Paid') AS total_fines_collected;

-- -----------------------------------------------------------------------------
-- 2. Top 10 Most Frequently Borrowed Books
-- -----------------------------------------------------------------------------
SELECT 
    bk.book_id,
    bk.title,
    bk.author,
    bk.category,
    COUNT(b.borrow_id) AS borrow_count
FROM books bk
JOIN borrowing b ON bk.book_id = b.book_id
GROUP BY bk.book_id, bk.title, bk.author, bk.category
ORDER BY borrow_count DESC
LIMIT 10;

-- -----------------------------------------------------------------------------
-- 3. Book Distribution and Catalog Breakdown by Category
-- -----------------------------------------------------------------------------
SELECT 
    category,
    COUNT(book_id) AS total_titles,
    SUM(total_copies) AS total_copies,
    SUM(available_copies) AS available_copies,
    ROUND(AVG(price), 2) AS average_price,
    ROUND(SUM(total_copies * price), 2) AS total_category_asset_value
FROM books
GROUP BY category
ORDER BY total_copies DESC;

-- -----------------------------------------------------------------------------
-- 4. Member Composition by Membership Tier and Status
-- -----------------------------------------------------------------------------
SELECT 
    membership_type,
    status,
    COUNT(member_id) AS member_count,
    ROUND(COUNT(member_id) * 100.0 / (SELECT COUNT(*) FROM members), 2) AS percentage_of_total
FROM members
GROUP BY membership_type, status
ORDER BY membership_type, status;

-- -----------------------------------------------------------------------------
-- 5. Borrowing Lifecycle Status Breakdown
-- -----------------------------------------------------------------------------
SELECT 
    status,
    COUNT(borrow_id) AS total_records,
    ROUND(COUNT(borrow_id) * 100.0 / (SELECT COUNT(*) FROM borrowing), 2) AS percentage
FROM borrowing
GROUP BY status;

-- -----------------------------------------------------------------------------
-- 6. Financial Overview: Fine Realization & Outstanding Penalties
-- -----------------------------------------------------------------------------
SELECT 
    payment_status,
    COUNT(fine_id) AS fine_records,
    ROUND(SUM(fine_amount), 2) AS total_amount,
    ROUND(AVG(fine_amount), 2) AS average_fine
FROM fines
GROUP BY payment_status
ORDER BY total_amount DESC;

-- -----------------------------------------------------------------------------
-- 7. Top 10 Most Active Patrons by Volume of Borrowings
-- -----------------------------------------------------------------------------
SELECT 
    m.member_id,
    CONCAT(m.first_name, ' ', m.last_name) AS member_name,
    m.membership_type,
    m.status AS account_status,
    COUNT(b.borrow_id) AS total_books_borrowed
FROM members m
JOIN borrowing b ON m.member_id = b.member_id
GROUP BY m.member_id, m.first_name, m.last_name, m.membership_type, m.status
ORDER BY total_books_borrowed DESC
LIMIT 10;

-- -----------------------------------------------------------------------------
-- 8. Current Active Loans (Borrowed or Overdue)
-- -----------------------------------------------------------------------------
SELECT 
    b.borrow_id,
    bk.title,
    CONCAT(m.first_name, ' ', m.last_name) AS member_name,
    b.borrow_date,
    b.due_date,
    b.status,
    DATEDIFF(CURRENT_DATE(), b.due_date) AS days_overdue
FROM borrowing b
JOIN books bk ON b.book_id = bk.book_id
JOIN members m ON b.member_id = m.member_id
WHERE b.status IN ('Borrowed', 'Overdue')
ORDER BY b.due_date ASC;
