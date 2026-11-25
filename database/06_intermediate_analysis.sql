USE library_db;

-- Monthly borrowing
SELECT MONTH(borrow_date) AS month,
       COUNT(*) AS total
FROM borrowing
GROUP BY MONTH(borrow_date);

-- Borrowing by member
SELECT member_id, COUNT(*) AS total_books
FROM borrowing
GROUP BY member_id
ORDER BY total_books DESC;

-- Late returns
SELECT *
FROM borrowing
WHERE return_date > due_date;

-- Books with the lowest availability
SELECT title, available_copies
FROM books
ORDER BY available_copies ASC;

-- Members who never borrowed books
SELECT name
FROM members
WHERE member_id NOT IN (
    SELECT member_id FROM borrowing
);

-- Fine totals by member
SELECT member_id, SUM(fine_amount) AS total_fines
FROM fines
GROUP BY member_id;
