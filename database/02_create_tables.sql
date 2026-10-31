-- =============================================================================
-- Script 02: Create Tables
-- Project: Library Management System Analysis Using SQL
-- Description: Creates the 4 core relational tables (books, members, borrowing,
--              fines) with primary keys, foreign keys, check constraints,
--              and optimization indexes.
-- =============================================================================

USE library_db;

-- -----------------------------------------------------------------------------
-- Clean up existing tables in reverse dependency order
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS fines;
DROP TABLE IF EXISTS borrowing;
DROP TABLE IF EXISTS members;
DROP TABLE IF EXISTS books;

-- -----------------------------------------------------------------------------
-- 1. Table: Books
-- Stores library catalog information, availability counts, and pricing.
-- -----------------------------------------------------------------------------
CREATE TABLE books (
    book_id VARCHAR(10) NOT NULL,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(150) NOT NULL,
    category VARCHAR(100) NOT NULL,
    isbn VARCHAR(25) NOT NULL UNIQUE,
    publication_year INT NULL,
    total_copies INT NOT NULL DEFAULT 1,
    available_copies INT NOT NULL DEFAULT 1,
    price DECIMAL(8, 2) NOT NULL DEFAULT 0.00,
    CONSTRAINT pk_books PRIMARY KEY (book_id),
    CONSTRAINT chk_total_copies CHECK (total_copies >= 0),
    CONSTRAINT chk_available_copies CHECK (available_copies >= 0 AND available_copies <= total_copies),
    CONSTRAINT chk_price CHECK (price >= 0.00)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Performance indexes for books
CREATE INDEX idx_books_category ON books(category);
CREATE INDEX idx_books_author ON books(author);
CREATE INDEX idx_books_available ON books(available_copies);

-- -----------------------------------------------------------------------------
-- 2. Table: Members
-- Stores patron accounts, membership classifications, and account lifecycle status.
-- -----------------------------------------------------------------------------
CREATE TABLE members (
    member_id VARCHAR(10) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(25) NOT NULL,
    membership_type VARCHAR(50) NOT NULL,
    registration_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Active',
    CONSTRAINT pk_members PRIMARY KEY (member_id),
    CONSTRAINT chk_membership_type CHECK (membership_type IN ('Student', 'Faculty', 'General', 'Premium')),
    CONSTRAINT chk_member_status CHECK (status IN ('Active', 'Inactive', 'Suspended'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Performance indexes for members
CREATE INDEX idx_members_status ON members(status);
CREATE INDEX idx_members_type ON members(membership_type);

-- -----------------------------------------------------------------------------
-- 3. Table: Borrowing
-- Tracks lending transactions, expected due dates, actual returns, and statuses.
-- -----------------------------------------------------------------------------
CREATE TABLE borrowing (
    borrow_id VARCHAR(10) NOT NULL,
    book_id VARCHAR(10) NOT NULL,
    member_id VARCHAR(10) NOT NULL,
    borrow_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Borrowed',
    CONSTRAINT pk_borrowing PRIMARY KEY (borrow_id),
    CONSTRAINT fk_borrowing_books FOREIGN KEY (book_id)
        REFERENCES books(book_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_borrowing_members FOREIGN KEY (member_id)
        REFERENCES members(member_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT chk_borrow_due_date CHECK (due_date >= borrow_date),
    CONSTRAINT chk_borrow_status CHECK (status IN ('Borrowed', 'Returned', 'Overdue'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Performance indexes for borrowing
CREATE INDEX idx_borrowing_book_id ON borrowing(book_id);
CREATE INDEX idx_borrowing_member_id ON borrowing(member_id);
CREATE INDEX idx_borrowing_dates ON borrowing(borrow_date, due_date, return_date);
CREATE INDEX idx_borrowing_status ON borrowing(status);

-- -----------------------------------------------------------------------------
-- 4. Table: Fines
-- Records overdue penalties, assessment dates, and settlement status.
-- -----------------------------------------------------------------------------
CREATE TABLE fines (
    fine_id VARCHAR(10) NOT NULL,
    borrow_id VARCHAR(10) NOT NULL,
    member_id VARCHAR(10) NOT NULL,
    fine_amount DECIMAL(8, 2) NOT NULL DEFAULT 0.00,
    fine_date DATE NOT NULL,
    payment_status VARCHAR(20) NOT NULL DEFAULT 'Unpaid',
    payment_date DATE NULL,
    CONSTRAINT pk_fines PRIMARY KEY (fine_id),
    CONSTRAINT fk_fines_borrowing FOREIGN KEY (borrow_id)
        REFERENCES borrowing(borrow_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_fines_members FOREIGN KEY (member_id)
        REFERENCES members(member_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT chk_fine_amount CHECK (fine_amount >= 0.00),
    CONSTRAINT chk_fine_payment_status CHECK (payment_status IN ('Paid', 'Unpaid', 'Pending', 'Waived'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Performance indexes for fines
CREATE INDEX idx_fines_borrow_id ON fines(borrow_id);
CREATE INDEX idx_fines_member_id ON fines(member_id);
CREATE INDEX idx_fines_payment_status ON fines(payment_status);
CREATE INDEX idx_fines_date ON fines(fine_date);
