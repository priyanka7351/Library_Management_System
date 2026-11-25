# 📚 Library Management System

A Library Management System developed to manage books, members, borrowing records, and fines. This project combines a simple web application with SQL-based data analysis.

The project has two main parts:
- **Library Web Application** – Manage books, members, book issues, returns, and fines.
- **SQL Data Analysis** – Analyze library data using SQL queries.

---

## 🚀 Project Features

### 1. Library Web Application
- **Dashboard:** Displays library statistics.
- **Book Management:** Add, search, and delete books.
- **Member Management:** Add and view library members.
- **Issue Books:** Issue books to registered members.
- **Return Books:** Record book returns.
- **Fine Management:** Manage overdue fines.

### 2. SQL Data Analysis
- Analyze book borrowing patterns.
- Find the most borrowed books.
- Analyze member activity.
- Identify late returns.
- Analyze unpaid fines.
- Study borrowing trends.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| SQLite | Web application database |
| MySQL | SQL data analysis |
| SQL | Database queries and analysis |
| HTML | Web page structure |
| CSS | Web page design |
| JavaScript | Website functionality |
| CSV | Sample dataset |

---

## 📁 Project Structure

```text
Library_Management_System/
│
├── app.py
├── database.py
├── library.db
│
├── data/
│   ├── books.csv
│   ├── members.csv
│   ├── borrowing.csv
│   └── fines.csv
│
├── SQL/
│   ├── 01_create_database.sql
│   ├── 02_create_tables.sql
│   ├── 03_import_data.sql
│   ├── 04_data_validation.sql
│   ├── 05_basic_analysis.sql
│   ├── 06_intermediate_analysis.sql
│   └── 07_advanced_analysis.sql
│
├── static/
│   ├── script.js
│   └── style.css
│
├── templates/
│   └── index.html
│
├── requirements.txt
└── README.md
```

---

## 🗄️ Database Design

The project uses four main database tables.

### 1. Books
Stores information about books available in the library.

- Book ID
- Title
- Author
- Category
- Total Copies
- Available Copies

### 2. Members
Stores information about library members.

- Member ID
- Name
- Email
- Membership Type

### 3. Borrowing
Stores information about book borrowing and returning.

- Borrow ID
- Book ID
- Member ID
- Borrow Date
- Due Date
- Return Date
- Status

### 4. Fines
Stores fine-related information.

- Fine ID
- Member ID
- Borrow ID
- Fine Amount
- Payment Status

---

## 🔗 Database Relationships

- One book can appear in multiple borrowing records.
- One member can have multiple borrowing records.
- Borrowing records can be associated with fines.

The database uses **Primary Keys (PK)** and **Foreign Keys (FK)** to connect the tables.

---

## 📊 SQL Analysis

The project contains SQL queries divided into three levels.

### Basic SQL Analysis
- Find total books.
- Calculate total book copies.
- Find available book copies.
- Count total members.
- Analyze books by category.
- Count borrowing records.
- Calculate unpaid fines.
- Find the most borrowed books.

### Intermediate SQL Analysis
- Analyze monthly borrowing.
- Analyze borrowing activity by member.
- Identify late returns.
- Find books with low availability.
- Find members who never borrowed books.
- Calculate total fines by member.

### Advanced SQL Analysis
- Find the top three most borrowed books.
- Find members with unpaid fines.
- Analyze borrowing status.
- Analyze book demand.
- Identify active borrowing records.

---

## 📂 Dataset

The project uses CSV files to store sample data.

| File | Description |
|---|---|
| `books.csv` | Book information |
| `members.csv` | Member information |
| `borrowing.csv` | Borrowing and returning records |
| `fines.csv` | Fine information |

These datasets are imported into MySQL tables for SQL-based analysis.

---

## 🧹 Data Validation

The project includes SQL queries for checking data quality.

- Check duplicate member emails.
- Check book availability.
- Check missing book titles.
- Check invalid book IDs.
- Check invalid member IDs.

---

## ▶️ How to Run the Web Application

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/Library_Management_System.git
```

### Step 2: Open the Project Folder

```bash
cd Library_Management_System
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Initialize the Database

```bash
python database.py
```

### Step 5: Run the Application

```bash
python app.py
```

### Step 6: Open in Browser

```text
http://127.0.0.1:5000
```

---

## 🐬 How to Run SQL Analysis

### Step 1: Open MySQL

Open MySQL Workbench or your MySQL terminal.

### Step 2: Create the Database

Run:

```sql
01_create_database.sql
```

### Step 3: Create Tables

Run:

```sql
02_create_tables.sql
```

### Step 4: Import CSV Data

Run:

```sql
03_import_data.sql
```

### Step 5: Validate Data

Run:

```sql
04_data_validation.sql
```

### Step 6: Perform Analysis

Run the following SQL files:

- `05_basic_analysis.sql`
- `06_intermediate_analysis.sql`
- `07_advanced_analysis.sql`

---

## 🎯 Project Objectives

- Manage library books and members.
- Record borrowing and returning activities.
- Manage fine records.
- Design a relational database.
- Implement Primary Keys and Foreign Keys.
- Import and validate datasets.
- Perform SQL-based data analysis.
- Understand real-world database management.

---

## 🔮 Future Improvements

- Add user authentication.
- Improve the dashboard design.
- Add book search filters.
- Automate fine calculation.
- Add more SQL analysis queries.
- Add more functionality to the web application.

---

## 👥 Team Project

This project was developed as a team project of six members.

Work was divided among:
- Database design
- Dataset preparation
- Data import
- Data validation
- Basic SQL analysis
- Intermediate SQL analysis
- Advanced SQL analysis
- Documentation

---

## 🏁 Conclusion

The Library Management System is designed to manage library records and analyze library activities. It combines a web application with SQL-based analysis to provide practical experience in Python, Flask, SQLite, MySQL, SQL, database design, and data management.

---

**Developed as an academic project.**
