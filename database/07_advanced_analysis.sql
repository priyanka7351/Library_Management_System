-- =============================================================================
-- Script 07: Advanced SQL Analysis
-- Project: Library Management System Analysis Using SQL
-- Description: Advanced analytical queries utilizing window functions, Common
--              Table Expressions (CTEs), cumulative aggregations, member risk
--              segmentation, operational views, and stored procedures.
-- =============================================================================

USE library_db;

-- -----------------------------------------------------------------------------
-- 1. Month-over-Month (MoM) Borrowing Growth Rate
-- Uses LAG() window function to calculate growth rate compared to prior month.
-- -----------------------------------------------------------------------------
WITH monthly_volume AS (
    SELECT 
        DATE_FORMAT(borrow_date, '%Y-%m') AS period,
        COUNT(borrow_id) AS current_month_loans
    FROM borrowing
    GROUP BY DATE_FORMAT(borrow_date, '%Y-%m')
)
SELECT 
    period,
    current_month_loans,
    LAG(current_month_loans, 1) OVER (ORDER BY period) AS previous_month_loans,
    current_month_loans - LAG(current_month_loans, 1) OVER (ORDER BY period) AS net_growth_count,
    ROUND(
        (current_month_loans - LAG(current_month_loans, 1) OVER (ORDER BY period)) * 100.0 /
        NULLIF(LAG(current_month_loans, 1) OVER (ORDER BY period), 0),
        2
    ) AS mom_growth_pct
FROM monthly_volume
ORDER BY period;

-- -----------------------------------------------------------------------------
-- 2. Running Total of Financial Realization (Cumulative Fines)
-- Calculates cumulative revenue collection trajectory over calendar quarters.
-- -----------------------------------------------------------------------------
SELECT 
    DATE_FORMAT(fine_date, '%Y-%m') AS year_month,
    ROUND(SUM(fine_amount), 2) AS monthly_fines_assessed,
    ROUND(SUM(CASE WHEN payment_status = 'Paid' THEN fine_amount ELSE 0 END), 2) AS monthly_fines_collected,
    ROUND(SUM(SUM(fine_amount)) OVER (ORDER BY DATE_FORMAT(fine_date, '%Y-%m')), 2) AS cumulative_fines_assessed,
    ROUND(SUM(SUM(CASE WHEN payment_status = 'Paid' THEN fine_amount ELSE 0 END)) OVER (ORDER BY DATE_FORMAT(fine_date, '%Y-%m')), 2) AS cumulative_fines_collected
FROM fines
GROUP BY DATE_FORMAT(fine_date, '%Y-%m')
ORDER BY year_month;

-- -----------------------------------------------------------------------------
-- 3. Comprehensive Patron Delinquency & Risk Profiling Matrix
-- Segments members into risk tiers based on late returns and unpaid fines.
-- -----------------------------------------------------------------------------
WITH member_stats AS (
    SELECT 
        m.member_id,
        CONCAT(m.first_name, ' ', m.last_name) AS member_name,
        m.membership_type,
        m.status,
        COUNT(b.borrow_id) AS total_borrowed,
        SUM(CASE WHEN b.return_date > b.due_date OR b.status = 'Overdue' THEN 1 ELSE 0 END) AS total_delinquencies,
        COALESCE(SUM(f.fine_amount), 0.00) AS total_fines_assessed,
        COALESCE(SUM(CASE WHEN f.payment_status IN ('Unpaid', 'Pending') THEN f.fine_amount ELSE 0 END), 0.00) AS outstanding_balance
    FROM members m
    LEFT JOIN borrowing b ON m.member_id = b.member_id
    LEFT JOIN fines f ON b.borrow_id = f.borrow_id
    GROUP BY m.member_id, m.first_name, m.last_name, m.membership_type, m.status
)
SELECT 
    member_id,
    member_name,
    membership_type,
    status,
    total_borrowed,
    total_delinquencies,
    ROUND(total_delinquencies * 100.0 / NULLIF(total_borrowed, 0), 1) AS delinquency_rate_pct,
    total_fines_assessed,
    outstanding_balance,
    CASE 
        WHEN outstanding_balance > 30.00 OR (total_borrowed > 5 AND (total_delinquencies * 1.0 / total_borrowed) >= 0.5) THEN 'High Risk / Action Required'
        WHEN outstanding_balance > 0.00 OR total_delinquencies >= 2 THEN 'Moderate Risk / Follow-up'
        WHEN total_borrowed > 0 THEN 'Good Standing'
        ELSE 'Inactive Patron'
    END AS risk_tier
FROM member_stats
ORDER BY outstanding_balance DESC, total_delinquencies DESC;

-- -----------------------------------------------------------------------------
-- 4. Inventory Optimization: High Demand vs Underutilized Titles
-- Identifies titles where available stock is low relative to borrowing velocity.
-- -----------------------------------------------------------------------------
SELECT 
    bk.book_id,
    bk.title,
    bk.category,
    bk.total_copies,
    bk.available_copies,
    COUNT(b.borrow_id) AS lifetime_borrows,
    ROUND(COUNT(b.borrow_id) * 1.0 / bk.total_copies, 2) AS demand_per_copy_index,
    CASE 
        WHEN bk.available_copies = 0 THEN 'Stock Depleted - Procure Additional Copies'
        WHEN bk.available_copies <= 2 AND (COUNT(b.borrow_id) * 1.0 / bk.total_copies) > 3.0 THEN 'High Demand - Low Buffer'
        WHEN COUNT(b.borrow_id) = 0 THEN 'Zero Circulation - Review Placement'
        ELSE 'Adequately Stocked'
    END AS inventory_recommendation
FROM books bk
LEFT JOIN borrowing b ON bk.book_id = b.book_id
GROUP BY bk.book_id, bk.title, bk.category, bk.total_copies, bk.available_copies
ORDER BY demand_per_copy_index DESC;

-- -----------------------------------------------------------------------------
-- 5. Operational View: Active and Overdue Loans Dashboard
-- -----------------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_active_overdue_rentals AS
SELECT 
    b.borrow_id,
    b.borrow_date,
    b.due_date,
    b.status AS loan_status,
    bk.book_id,
    bk.title AS book_title,
    bk.category,
    m.member_id,
    CONCAT(m.first_name, ' ', m.last_name) AS borrower_name,
    m.email AS borrower_email,
    m.phone AS borrower_phone,
    DATEDIFF(CURRENT_DATE(), b.due_date) AS days_elapsed_past_due,
    CASE 
        WHEN CURRENT_DATE() > b.due_date THEN 'Overdue Action Needed'
        WHEN DATEDIFF(b.due_date, CURRENT_DATE()) <= 2 THEN 'Due Soon'
        ELSE 'Current'
    END AS urgency_level
FROM borrowing b
JOIN books bk ON b.book_id = bk.book_id
JOIN members m ON b.member_id = m.member_id
WHERE b.return_date IS NULL;

-- Query the operational view
SELECT * FROM vw_active_overdue_rentals ORDER BY days_elapsed_past_due DESC;

-- -----------------------------------------------------------------------------
-- 6. Stored Procedure: Patron 360-Degree Historical Report
-- -----------------------------------------------------------------------------
DROP PROCEDURE IF EXISTS sp_member_borrowing_profile;

DELIMITER $$
CREATE PROCEDURE sp_member_borrowing_profile(IN p_member_id VARCHAR(10))
BEGIN
    -- 1. Patron Demographic and Account Summary
    SELECT 
        member_id,
        CONCAT(first_name, ' ', last_name) AS full_name,
        email,
        phone,
        membership_type,
        registration_date,
        status AS account_status
    FROM members
    WHERE member_id = p_member_id;

    -- 2. Borrowing Activity Record
    SELECT 
        b.borrow_id,
        bk.title AS book_title,
        bk.category,
        b.borrow_date,
        b.due_date,
        b.return_date,
        b.status,
        CASE 
            WHEN b.return_date IS NOT NULL AND b.return_date > b.due_date THEN DATEDIFF(b.return_date, b.due_date)
            WHEN b.return_date IS NULL AND CURRENT_DATE() > b.due_date THEN DATEDIFF(CURRENT_DATE(), b.due_date)
            ELSE 0 
        END AS days_overdue
    FROM borrowing b
    JOIN books bk ON b.book_id = bk.book_id
    WHERE b.member_id = p_member_id
    ORDER BY b.borrow_date DESC;

    -- 3. Fine & Penalty Ledger
    SELECT 
        fine_id,
        borrow_id,
        fine_amount,
        fine_date,
        payment_status,
        payment_date
    FROM fines
    WHERE member_id = p_member_id
    ORDER BY fine_date DESC;
END$$
DELIMITER ;

-- Test stored procedure for Member M101
-- CALL sp_member_borrowing_profile('M101');
