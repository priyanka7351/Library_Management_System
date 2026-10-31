-- =============================================================================
-- Script 03: Import Data
-- Project: Library Management System Analysis Using SQL
-- Description: Ingests raw CSV data into MySQL tables using LOAD DATA LOCAL INFILE.
--              Handles empty date fields by transforming them into NULL values.
-- =============================================================================

USE library_db;

-- Enable local infile on server session (if allowed by server configuration)
SET GLOBAL local_infile = 1;

-- -----------------------------------------------------------------------------
-- 1. Import Books
-- Path convention: adjust path to match your environment if needed
-- -----------------------------------------------------------------------------
LOAD DATA LOCAL INFILE '../dataset/raw/books.csv'
INTO TABLE books
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(book_id, title, author, category, isbn, @pub_year, total_copies, available_copies, price)
SET 
    publication_year = NULLIF(TRIM(@pub_year), '');

-- -----------------------------------------------------------------------------
-- 2. Import Members
-- -----------------------------------------------------------------------------
LOAD DATA LOCAL INFILE '../dataset/raw/members.csv'
INTO TABLE members
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(member_id, first_name, last_name, email, phone, membership_type, registration_date, status);

-- -----------------------------------------------------------------------------
-- 3. Import Borrowing
-- Maps empty return_date strings ('') to SQL NULL
-- -----------------------------------------------------------------------------
LOAD DATA LOCAL INFILE '../dataset/raw/borrowing.csv'
INTO TABLE borrowing
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(borrow_id, book_id, member_id, borrow_date, due_date, @return_date, status)
SET 
    return_date = NULLIF(TRIM(@return_date), '');

-- -----------------------------------------------------------------------------
-- 4. Import Fines
-- Maps empty payment_date strings ('') to SQL NULL
-- -----------------------------------------------------------------------------
LOAD DATA LOCAL INFILE '../dataset/raw/fines.csv'
INTO TABLE fines
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(fine_id, borrow_id, member_id, fine_amount, fine_date, payment_status, @payment_date)
SET 
    payment_date = NULLIF(TRIM(@payment_date), '');

-- -----------------------------------------------------------------------------
-- Verify import counts
-- -----------------------------------------------------------------------------
SELECT 'books' AS table_name, COUNT(*) AS total_rows FROM books
UNION ALL
SELECT 'members', COUNT(*) FROM members
UNION ALL
SELECT 'borrowing', COUNT(*) FROM borrowing
UNION ALL
SELECT 'fines', COUNT(*) FROM fines;
