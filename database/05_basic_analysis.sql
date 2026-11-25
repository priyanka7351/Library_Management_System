USE library_db;

-- Total books
SELECT COUNT(*) AS total_books FROM books;

-- Total book copies
SELECT SUM(total_copies) AS total_copies FROM books;

-- Available books
SELECT SUM(available_copies) AS available_books FROM books;

-- Total members
SELECT COUNT(*) AS total_members FROM members;

-- Books by category
SELECT category, COUNT(*) AS count
FROM books
GROUP BY category;

-- Borrowing records
SELECT COUNT(*) AS total_borrowing
FROM borrowing;

-- Unpaid fines
SELECT SUM(fine_amount) AS unpaid_fines
FROM fines
WHERE payment_status = 'Unpaid';

-- Most borrowed books
SELECT book_id, COUNT(*) AS borrow_count
FROM borrowing
GROUP BY book_id
ORDER BY borrow_count DESC
LIMIT 5;
