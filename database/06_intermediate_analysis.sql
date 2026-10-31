-- =============================================================================
-- Script 06: Intermediate SQL Analysis
-- Project: Library Management System Analysis Using SQL
-- Description: Aggregated business metrics, trend analysis, circulation rates,
--              overdue patterns, and ranking functions.
-- =============================================================================

USE library_db;

-- -----------------------------------------------------------------------------
-- 1. Monthly Borrowing Velocity and Seasonal Trends
-- -----------------------------------------------------------------------------
SELECT 
    DATE_FORMAT(borrow_date, '%Y-%m') AS year_month,
    YEAR(borrow_date) AS borrow_year,
    MONTHNAME(borrow_date) AS month_name,
    COUNT(borrow_id) AS total_borrowings,
    COUNT(DISTINCT member_id) AS unique_borrowers,
    COUNT(DISTINCT book_id) AS unique_titles_loaned,
    ROUND(COUNT(borrow_id) / COUNT(DISTINCT member_id), 2) AS loans_per_active_borrower
FROM borrowing
GROUP BY DATE_FORMAT(borrow_date, '%Y-%m'), YEAR(borrow_date), MONTHNAME(borrow_date)
ORDER BY year_month ASC;

-- -----------------------------------------------------------------------------
-- 2. Category Circulation Rate & Utilization
-- Circulation rate = total borrowings / total stock volume
-- -----------------------------------------------------------------------------
SELECT 
    bk.category,
    COUNT(b.borrow_id) AS total_loans,
    SUM(bk.total_copies) AS total_category_inventory,
    ROUND(COUNT(b.borrow_id) * 1.0 / NULLIF(SUM(bk.total_copies), 0), 2) AS inventory_turnover_ratio,
    ROUND(AVG(DATEDIFF(COALESCE(b.return_date, CURRENT_DATE()), b.borrow_date)), 1) AS avg_days_checked_out
FROM books bk
LEFT JOIN borrowing b ON bk.book_id = b.book_id
GROUP BY bk.category
ORDER BY total_loans DESC;

-- -----------------------------------------------------------------------------
-- 3. Overdue & Late Return Analysis by Membership Type
-- Identifies behavioral differences between Students, Faculty, and General members.
-- -----------------------------------------------------------------------------
SELECT 
    m.membership_type,
    COUNT(b.borrow_id) AS total_loans,
    SUM(CASE WHEN b.return_date > b.due_date THEN 1 ELSE 0 END) AS late_returns,
    ROUND(SUM(CASE WHEN b.return_date > b.due_date THEN 1 ELSE 0 END) * 100.0 / COUNT(b.borrow_id), 2) AS late_return_rate_pct,
    ROUND(AVG(CASE WHEN b.return_date > b.due_date THEN DATEDIFF(b.return_date, b.due_date) ELSE NULL END), 1) AS avg_days_overdue
FROM members m
JOIN borrowing b ON m.member_id = b.member_id
GROUP BY m.membership_type
ORDER BY late_return_rate_pct DESC;

-- -----------------------------------------------------------------------------
-- 4. Inactive Patron Identification (Zero-Borrow Members)
-- Identifies members who registered but have never checked out a single book.
-- -----------------------------------------------------------------------------
SELECT 
    m.member_id,
    CONCAT(m.first_name, ' ', m.last_name) AS member_name,
    m.email,
    m.membership_type,
    m.registration_date,
    m.status,
    DATEDIFF(CURRENT_DATE(), m.registration_date) AS days_since_registration
FROM members m
LEFT JOIN borrowing b ON m.member_id = b.member_id
WHERE b.borrow_id IS NULL
ORDER BY m.registration_date ASC;

-- -----------------------------------------------------------------------------
-- 5. Fine Settlement Velocity (Days to Pay)
-- Analyzes payment turnaround for members who have been fined.
-- -----------------------------------------------------------------------------
SELECT 
    m.membership_type,
    COUNT(f.fine_id) AS total_fines_issued,
    SUM(CASE WHEN f.payment_status = 'Paid' THEN 1 ELSE 0 END) AS total_fines_cleared,
    ROUND(SUM(CASE WHEN f.payment_status = 'Paid' THEN 1 ELSE 0 END) * 100.0 / COUNT(f.fine_id), 2) AS payment_compliance_pct,
    ROUND(AVG(CASE WHEN f.payment_status = 'Paid' THEN DATEDIFF(f.payment_date, f.fine_date) ELSE NULL END), 1) AS avg_days_to_pay,
    ROUND(SUM(f.fine_amount), 2) AS total_assessed_amount,
    ROUND(SUM(CASE WHEN f.payment_status = 'Paid' THEN f.fine_amount ELSE 0 END), 2) AS total_collected_amount
FROM fines f
JOIN members m ON f.member_id = m.member_id
GROUP BY m.membership_type
ORDER BY payment_compliance_pct DESC;

-- -----------------------------------------------------------------------------
-- 6. Top 3 Most Borrowed Books per Category (Window Functions)
-- Uses DENSE_RANK() to find leading titles within each category partition.
-- -----------------------------------------------------------------------------
WITH ranked_category_books AS (
    SELECT 
        bk.category,
        bk.book_id,
        bk.title,
        bk.author,
        COUNT(b.borrow_id) AS borrow_count,
        DENSE_RANK() OVER (
            PARTITION BY bk.category 
            ORDER BY COUNT(b.borrow_id) DESC
        ) AS rank_in_category
    FROM books bk
    LEFT JOIN borrowing b ON bk.book_id = b.book_id
    GROUP BY bk.category, bk.book_id, bk.title, bk.author
)
SELECT 
    category,
    rank_in_category,
    title,
    author,
    borrow_count
FROM ranked_category_books
WHERE rank_in_category <= 3
ORDER BY category, rank_in_category;

-- -----------------------------------------------------------------------------
-- 7. Author Popularity and Catalog Reach
-- Aggregates performance by author across their entire catalog.
-- -----------------------------------------------------------------------------
SELECT 
    bk.author,
    COUNT(DISTINCT bk.book_id) AS catalog_titles,
    COUNT(b.borrow_id) AS total_borrowings,
    ROUND(COUNT(b.borrow_id) * 1.0 / COUNT(DISTINCT bk.book_id), 2) AS avg_loans_per_title
FROM books bk
LEFT JOIN borrowing b ON bk.book_id = b.book_id
GROUP BY bk.author
ORDER BY total_borrowings DESC
LIMIT 15;
