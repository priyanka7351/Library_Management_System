USE library_db;

CREATE TABLE books (
    book_id INT PRIMARY KEY,
    title VARCHAR(100),
    author VARCHAR(100),
    category VARCHAR(50),
    total_copies INT,
    available_copies INT
);

CREATE TABLE members (
    member_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    membership_type VARCHAR(50)
);

CREATE TABLE borrowing (
    borrow_id INT PRIMARY KEY,
    book_id INT,
    member_id INT,
    borrow_date DATE,
    due_date DATE,
    return_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);

CREATE TABLE fines (
    fine_id INT PRIMARY KEY,
    member_id INT,
    borrow_id INT,
    fine_amount DECIMAL(10,2),
    payment_status VARCHAR(20),
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (borrow_id) REFERENCES borrowing(borrow_id)
);
