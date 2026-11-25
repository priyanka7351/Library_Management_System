USE library_db;

SELECT * FROM books;

SELECT * FROM members;

SELECT * FROM borrowing;

SELECT * FROM fines;

-- Check duplicate emails
SELECT email, COUNT(*)
FROM members
GROUP BY email
HAVING COUNT(*) > 1;

-- Check available copies
SELECT *
FROM books
WHERE available_copies > total_copies;

-- Check missing books
SELECT *
FROM books
WHERE title IS NULL;

-- Check invalid borrowing records
SELECT *
FROM borrowing
WHERE book_id NOT IN (SELECT book_id FROM books);
