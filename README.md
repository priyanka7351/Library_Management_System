# Library Management System

Comprehensive Library Management System featuring:
1. **Interactive Full-Stack Web Application & Relational DBMS Engine**: Real-time catalog management, circulation desk (issue/return), patron directory, automated penalty settlement with ACID transactions, foreign keys, and triggers.
2. **Data Analytics & Business Intelligence**: In-depth SQL queries, exploratory data analysis (EDA) using Python/Pandas, and interactive Power BI dashboards for operational insights.

---

## Part 1: Full-Stack Web Application & Relational DBMS

### Overview
A dynamic relational database management web application built with **Python (Flask), SQLite3, HTML5, CSS3, and Vanilla JavaScript**. It provides a real-time responsive dashboard and circulation desk for everyday library operations with strict relational integrity.

### Key Capabilities
* **Live Operational Dashboard**: Real-time metrics for total catalog titles, physical copies, registered patrons, active loans, and pending fines.
* **Book Inventory Management (CRUD)**: Search by title, author, or category; register new titles; manage available vs. total stock; remove discontinued titles.
* **Patron Directory**: Register and manage students and faculty with auto-generated Member IDs and department allocations.
* **Circulation Desk (Issue & Return)**:
  * **Book Checkout**: Atomically validates copy availability, decrements stock count, records loan transaction, and calculates expected due dates.
  * **Book Return**: Automatically checks for overdue returns, calculates daily penalty fees, and updates stock count via ACID transaction.
* **Penalty Management**: Tracks overdue fines and provides one-click penalty settlement.
* **Relational DBMS Guarantees**: SQLite3 database with foreign key constraints, index optimization, and transaction rollback protection.

### Architecture & Technology Stack
* **Frontend**: HTML5, Modern CSS3 (tactile card layout, responsive grids), Vanilla JavaScript (`fetch` API).
* **Backend**: Python 3, Flask REST API.
* **Database**: SQLite3 (`library.db`) with normalized schema, foreign key enforcement, and indexes.

### Project Structure
```text
DBMS_PJT/
├── app.py                  # Flask REST API server and route handlers
├── database.py             # Database initialization, schema setup, and CSV seeding
├── library.db              # SQLite relational database
├── Library_Management_System_DBMS_Presentation.pptx # Project presentation
├── data/                   # Core dataset CSV files
│   ├── books.csv           # Catalog records
│   ├── borrowing.csv       # Loan history and active transactions
│   ├── fines.csv           # Overdue penalties and payment records
│   └── members.csv         # Registered patrons
├── database/               # SQL scripts and schema definitions for analytics
│   ├── 01_create_database.sql
│   ├── 02_create_tables.sql
│   ├── 03_import_data.sql
│   ├── 04_data_validation.sql
│   ├── 05_basic_analysis.sql
│   ├── 06_intermediate_analysis.sql
│   └── 07_advanced_analysis.sql
├── static/
│   ├── script.js           # Client-side dynamic API bindings and UI rendering
│   └── style.css           # Styling, color palette, typography, and layout
├── templates/
│   └── index.html          # Web application user interface
└── README.md               # Project documentation
```

### Quick Start Guide (Web Application)

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Initialize Database (Optional / Automatic)
The database automatically initializes and seeds from the CSV files upon launching `app.py`. To re-seed manually:
```bash
python database.py
```

#### 3. Run the Web Server
```bash
python app.py
```

#### 4. Open Application
Navigate to `http://127.0.0.1:5000` in your web browser.

---

## Part 2: Data Analytics & SQL Insights

### Overview
Data Analytics module designed to analyze historical library operations and extract actionable insights regarding circulation patterns, patron demographics, late returns, and collection performance.

### Analytics Technology Stack
* **Database & Querying**: MySQL / SQLite, Advanced SQL (CTEs, Window Functions, Joins, Aggregations)
* **Data Processing & EDA**: Python, Pandas, NumPy
* **Data Visualization**: Matplotlib, Seaborn
* **Business Intelligence**: Power BI Interactive Dashboards
* **Environment**: Jupyter Notebook

### Core Analytical Inquiries
1. Most frequently borrowed titles and high-demand genres.
2. Patron borrowing velocity across academic departments.
3. Overdue book frequency and fine settlement timelines.
4. Monthly and seasonal borrowing trends.
5. Resource allocation recommendations for inventory expansion.

### Running Analytics Notebooks
```bash
pip install pandas numpy matplotlib seaborn sqlalchemy jupyter
jupyter notebook
```
Open the notebooks located inside the `notebooks/` directory to run exploratory data analysis and export processed tables for Power BI.

---

## Contributing
1. Fork or clone the repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name`.
3. Commit your changes: `git commit -m "feat: description of changes"`.
4. Push to branch: `git push origin feature/your-feature-name`.
5. Open a Pull Request for review.

---

## License
Educational and academic relational database management system project.
