-- =============================================================================
-- Script 01: Create Database
-- Project: Library Management System Analysis Using SQL
-- Description: Initializes the library database with UTF-8 character encoding.
-- =============================================================================

-- Drop database if it already exists (useful for clean reinstalls)
DROP DATABASE IF EXISTS library_db;

-- Create database with full Unicode UTF-8 support
CREATE DATABASE library_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Switch to the newly created database
USE library_db;

-- Display database creation confirmation
SELECT 
    SCHEMA_NAME AS database_name,
    DEFAULT_CHARACTER_SET_NAME AS charset,
    DEFAULT_COLLATION_NAME AS collation
FROM information_schema.SCHEMATA
WHERE SCHEMA_NAME = 'library_db';
