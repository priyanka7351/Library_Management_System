USE library_db;

-- Top 3 most borrowed books
SELECT book_id, COUNT(*) AS borrow_count
FROM borrowing
GROUP BY book_id
ORDER BY borrow_count DESC
LIMIT 3;

-- Members with unpaid fines
SELECT member_id, SUM(fine_amount) AS total_fine
FROM fines
WHERE payment_status = 'Unpaid'
GROUP BY member_id
ORDER BY total_fine DESC;

-- Borrowing status
SELECT status, COUNT(*) AS total
FROM borrowing
GROUP BY status;

-- Book demand
SELECT b.title, COUNT(br.borrow_id) AS demand
FROM books b
LEFT JOIN borrowing br ON b.book_id = br.book_id
GROUP BY b.book_id, b.title
ORDER BY demand DESC;

-- Active borrowing records
SELECT *
FROM borrowing
WHERE status = 'Borrowed';
