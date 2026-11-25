# 📚 Library Management System & Data Analytics Platform

A comprehensive end-to-end Library Management System featuring:
1. **Interactive Full-Stack Web Application & Relational DBMS Engine**: Real-time catalog management, circulation desk (issue/return), patron directory, and automated penalty settlement with ACID transactions, foreign keys, and triggers.
2. **Data Analytics, SQL Insights & Power BI**: In-depth SQL queries, automated data cleaning, exploratory data analysis (EDA) using Python/Pandas, and interactive Power BI dashboards for operational insights.

---

## 🛠️ Technology Stack

| Domain | Technologies |
| :--- | :--- |
| **Web Frontend** | HTML5, Modern CSS3 (tactile card layout, responsive grids), Vanilla JavaScript (`fetch` API) |
| **Web Backend** | Python 3, Flask REST API |
| **Database** | SQLite3 (`library.db`) & MySQL (Relational schema, ACID transactions, foreign key enforcement, indexes) |
| **Data Processing & EDA** | Python 3, Pandas, NumPy |
| **Data Visualization** | Matplotlib, Seaborn |
| **Interactive Analytics** | Jupyter Notebook |
| **Business Intelligence** | Microsoft Power BI (DAX, relational modeling, KPI dashboards) |
| **Version Control** | Git & GitHub |

---

## 📁 Project Structure

```text
Library_Management_System/
├── app.py                     # Flask REST API server and route handlers
├── database.py                # Database initialization, schema setup, and CSV seeding
├── library.db                 # SQLite relational database
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
│
├── data/                      # Core dataset CSV files (Web app source)
│   ├── books.csv              # Catalog records
│   ├── borrowing.csv          # Loan history and active transactions
│   ├── fines.csv              # Overdue penalties and payment records
│   └── members.csv            # Registered patrons
│
├── dataset/                   # Analytics datasets
│   ├── raw/                   # Raw source CSV data
│   │   ├── books.csv
│   │   ├── members.csv
│   │   ├── borrowing.csv
│   │   └── fines.csv
│   └── processed/             # Cleaned & standardized CSV data
│       ├── books_cleaned.csv
│       ├── members_cleaned.csv
│       ├── borrowing_cleaned.csv
│       └── fines_cleaned.csv
│
├── database/                  # SQL scripts, schema definitions, and analytical queries
│   ├── 01_create_database.sql
│   ├── 02_create_tables.sql
│   ├── 03_import_data.sql
│   ├── 04_data_validation.sql
│   ├── 05_basic_analysis.sql
│   ├── 06_intermediate_analysis.sql
│   ├── 07_advanced_analysis.sql
│   ├── create_tables.sql
│   └── analysis_queries.sql
│
├── notebooks/                 # Jupyter Notebook for exploratory data analysis
│   └── Library_Analysis.ipynb
│
├── outputs/
│   └── charts/                # Generated data visualizations
│       ├── top_borrowed_books.png
│       ├── popular_categories.png
│       ├── monthly_borrowing_trend.png
│       ├── active_members.png
│       └── fine_analysis.png
│
├── powerbi/                   # Power BI dashboard guide and DAX measures
│   └── README.md
│
├── python/                    # Automation scripts
│   ├── data_cleaning.py       # Automated data cleaning pipeline
│   └── data_analysis.py       # Python statistical analysis and chart generation
│
├── static/                    # Frontend assets
│   ├── script.js              # Client-side dynamic API bindings and UI rendering
│   └── style.css              # Styling, color palette, typography, and layout
│
└── templates/
    └── index.html             # Web application user interface
```

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

### Running the Web Application

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize Database (Optional / Automatic)**:
   The database automatically initializes and seeds from the CSV files upon launching `app.py`. To re-seed manually:
   ```bash
   python database.py
   ```

3. **Run the Web Server**:
   ```bash
   python app.py
   ```

4. **Open Application**:
   Navigate to `http://127.0.0.1:5000` in your web browser.

---

## Part 2: Data Analytics, SQL & Business Intelligence

### 🗄️ Dataset Description
The system consists of 4 relational tables:

1. **Books (`books.csv` / `books_cleaned.csv`)** - 50 titles:
   - `book_id`: Unique identifier (e.g., `B101`)
   - `title`: Book title
   - `author`: Author name
   - `category`: Genre / subject (Fiction, Computer Science, etc.)
   - `isbn`: Unique ISBN code
   - `publication_year`: Year of publication
   - `total_copies`: Total inventory count
   - `available_copies`: Currently available copies on shelf
   - `price`: Unit replacement cost

2. **Members (`members.csv` / `members_cleaned.csv`)** - 50 patrons:
   - `member_id`: Unique patron identifier (e.g., `M101`)
   - `first_name`, `last_name`: Patron full name
   - `email`, `phone`: Contact details
   - `membership_type`: Student, Faculty, General, Premium
   - `registration_date`: Date member joined
   - `status`: Active, Inactive, Suspended

3. **Borrowing (`borrowing.csv` / `borrowing_cleaned.csv`)** - 320 records:
   - `borrow_id`: Unique transaction identifier (e.g., `BR1001`)
   - `book_id`: Foreign key referencing books
   - `member_id`: Foreign key referencing members
   - `borrow_date`: Date book was checked out
   - `due_date`: Expected return date
   - `return_date`: Actual return date
   - `status`: Transaction status (e.g., `Returned`)

4. **Fines (`fines.csv` / `fines_cleaned.csv`)** - 106 records:
   - `fine_id`: Unique fine identifier (e.g., `FN501`)
   - `borrow_id`: Foreign key referencing borrowing
   - `member_id`: Foreign key referencing members
   - `fine_amount`: Dollar penalty levied
   - `fine_date`: Date fine was assessed
   - `payment_status`: Paid or Unpaid
   - `payment_date`: Date penalty was settled (empty if unpaid)

---

### 🧹 Data Cleaning (`python/data_cleaning.py`)
Run the automated cleaning pipeline:
```bash
python python/data_cleaning.py
```
**Pipeline Tasks**:
1. Ingests all 4 raw CSV files and inspects missing values and duplicate records.
2. Strips leading/trailing whitespace across text fields.
3. Standardizes date fields into ISO standard `YYYY-MM-DD`.
4. Handles null `payment_date` values for unpaid fines.
5. Saves clean, validated tables to `dataset/processed/`.

---

### 📊 SQL Analytics (`database/analysis_queries.sql`)
Ten structured analytical queries covering fundamental to advanced SQL techniques (`SELECT`, `WHERE`, `JOIN`, `GROUP BY`, `ORDER BY`, `COUNT`, `SUM`):
1. **Total Catalog Holdings**: Total distinct titles and physical copies.
2. **Member Demographics**: Registered patrons and active patron counts.
3. **Most Borrowed Titles**: Top 5 most borrowed books joining `books` and `borrowing`.
4. **Top Patrons**: Top 5 most active patrons by checkout frequency.
5. **Category Circulation**: Aggregated loans grouped by book genre/category.
6. **Circulation Timeline**: Monthly loan distribution using date aggregation.
7. **Overdue Tracking**: Records where `return_date > due_date`.
8. **Revenue & Penalties**: Paid fines revenue vs. outstanding penalties.
9. **Departmental Breakdown**: Circulation across student and faculty membership tiers.
10. **Zero-Circulation Inventory**: Identifying books with zero loans using `LEFT JOIN` and `IS NULL`.

To execute MySQL scripts:
```sql
SOURCE database/create_tables.sql;
SOURCE database/analysis_queries.sql;
```

---

### 🐍 Python Data Analysis & Charts (`python/data_analysis.py`)
Run Python analysis to generate summary statistics and charts:
```bash
python python/data_analysis.py
```
Generated figures saved to `outputs/charts/`:
* `top_borrowed_books.png`: Top 5 borrowed titles (e.g., *Dune*, *The Republic*).
* `popular_categories.png`: Circulation distribution across genres.
* `monthly_borrowing_trend.png`: Circulation trend line (2023–2025).
* `active_members.png`: Top 5 frequent patrons.
* `fine_analysis.png`: Fine settlement ratio (Paid vs. Outstanding).

---

### 📓 Jupyter Notebook (`notebooks/Library_Analysis.ipynb`)
Launch the interactive notebook:
```bash
jupyter notebook notebooks/Library_Analysis.ipynb
```
Sections included:
1. Project Introduction & Objectives
2. Library Imports (Pandas, NumPy, Matplotlib, Seaborn)
3. Dataset Ingestion & Validation
4. Data Understanding & Profiling
5. Data Cleaning Pipeline
6. Exploratory Data Analysis & Joins
7. Data Visualizations
8. Key Insights & Metrics
9. Strategic Operational Recommendations

---

### 📈 Power BI Dashboard (`powerbi/README.md`)
Includes step-by-step guidance and DAX measures to build an interactive dashboard:
* **KPI Cards**: Total Titles (50), Patrons (50), Borrowings (320), Overdue Loans (106), Total Fines ($1,695.00).
* **Interactive Visuals**: Most Borrowed Books, Category Circulation, Monthly Loan Trends, Membership Breakdown.
* **Slicers**: Year, Book Category, Membership Type.
* See [powerbi/README.md](powerbi/README.md) for full DAX measures and schema diagram.

---

## 💡 Key Findings & Operational Insights

1. **Circulation Concentration**: Titles like *Dune* (15 loans) and *The Republic* (11 loans) experience peak circulation. Procuring additional copies will reduce wait times.
2. **Category Demand**: Fiction (63 borrowings) and Computer Science (50 borrowings) represent the highest circulation categories.
3. **Overdue Risk**: 106 out of 320 transactions (33.1%) were returned late, totaling $1,695.00 in fines.
4. **Fine Recovery**: $1,273.50 (75.1%) has been collected, with $421.50 remaining outstanding.
5. **Operational Recommendation**: Implement automated SMS or email reminders 2 days prior to the due date to minimize late returns.

---

## 🎓 College Viva Questions & Answers

* **Q: Why use relational tables instead of one flat Excel spreadsheet?**  
  * *A: Relational normalization eliminates data redundancy, enforces referential integrity through foreign keys, and prevents update/delete anomalies.*
* **Q: How are overdue books calculated?**  
  * *A: By evaluating the condition `return_date > due_date` in SQL queries or Pandas masks.*
* **Q: Why use a `LEFT JOIN` to identify books never borrowed?**  
  * *A: A `LEFT JOIN` preserves all catalog rows from `books`; filtering for `borrowing.borrow_id IS NULL` identifies records with no transaction history.*
* **Q: How does the web app maintain ACID compliance during book checkout?**  
  * *A: It executes the stock decrement and borrowing record creation within a single database transaction, rolling back if availability drops below 1.*

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
