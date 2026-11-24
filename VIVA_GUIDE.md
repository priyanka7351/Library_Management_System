# 6-Member Viva & Presentation Guide (DBMS Special Edition)

> **Project Name**: Dynamic Relational Library Management System  
> **Tech Stack**: HTML5, CSS3, JavaScript, Python Flask, SQLite  
> **How to Start**: `python app.py` -> Open `http://127.0.0.1:5000`

---

## 6-Member Role Division (Kaun Kya Explain Karega)

Har member ke paas ek clear topic aur bolne ki simple script hai. Examiner jab pooche, bina dare confidently yeh bolna hai:

---

### Member 1: Project Overview, 3-Tier Architecture & ACID Properties
* **Topic**: System Architecture aur ACID Guarantees.
* **Viva Script**:
  > *"Hamara project ek 3-Tier Architecture par based dynamic Relational Library Management System hai:*
  > *1. Presentation Layer (Frontend): HTML5, CSS3 (Neo-Brutalist Pop UI), Vanilla JavaScript.*
  > *2. Application Layer (Backend): Python Flask REST API.*
  > *3. Database Layer: SQLite Relational Database.*
  > *Humne ACID properties implement ki hain: Atomicity ensure hoti hai kyunki har transaction (issue/return) ya toh poora commit hota hai ya rollback. Consistency ke liye database constraints lagaye hain taaki copies kabhi negative na ho sakein."*
* **File to show**: [app.py](file:///c:/Users/Ashish/OneDrive/Documents/Desktop/DBMS_PJT/app.py) & [README.md](file:///c:/Users/Ashish/OneDrive/Documents/Desktop/DBMS_PJT/README.md).

---

### Member 2: Relational Schema Design, Normalization & Constraints
* **Topic**: Database Schema, 3NF Normalization, Primary/Foreign Keys, aur Domain Constraints.
* **Viva Script**:
  > *"Maine relational schema design ki hai jo 3NF (Third Normal Form) mein normalized hai taaki redundancy na ho:*
  > *1. `books`: book_id (PK), title, author, total_copies, available_copies, price.*
  > *2. `members`: member_id (PK), first_name, email (UNIQUE), status.*
  > *3. `borrowing`: borrow_id (PK), book_id (FK), member_id (FK) with ON UPDATE CASCADE & ON DELETE RESTRICT.*
  > *4. `fines`: fine_id (PK), borrow_id (FK), fine_amount, payment_status.*
  > *Humne CHECK constraints lagaye hain jaise `CHECK(available_copies >= 0)` aur `CHECK(price >= 0.0)`."*
* **File to show**: [database.py](file:///c:/Users/Ashish/OneDrive/Documents/Desktop/DBMS_PJT/database.py) (function `init_db()`).

---

### Member 3: Book Inventory & Member CRUD Operations
* **Topic**: CRUD operations, dynamic stock sync, aur referential protection.
* **Viva Script**:
  > *"Maine Catalog aur Member Management module implement kiya hai:*
  > *Librarian nayi book insert kar sakta hai, live title/author search kar sakta hai, aur member register kar sakta hai.*
  > *Sabse important: Jab nayi book ya member add hota hai, toh dashboard ke saare live metrics, badges aur charts bina reload ke real-time SQL queries se refresh hote hain.*
  > *Agar koi book kisi student ke paas already issued hai, toh database referential constraint us book ko delete hone se block kar deta hai."*
* **File to show**: `add_new_book()`, `delete_book()`, `add_new_member()` in [database.py](file:///c:/Users/Ashish/OneDrive/Documents/Desktop/DBMS_PJT/database.py).

---

### Member 4: Database Triggers & Issue Transaction
* **Topic**: SQL Triggers (`trg_decrement_stock_on_issue`) aur book checkout logic.
* **Viva Script**:
  > *"Maine Database Triggers implement kiye hain jo business logic ko directly database engine level par enforce karte hain.*
  > *Jab librarian book issue karta hai, toh `AFTER INSERT ON borrowing` trigger automatic fire hota hai aur `UPDATE books SET available_copies = available_copies - 1` execute karta hai.*
  > *Iska fayda yeh hai ki application code se galti hone par bhi database kabhi inconsistent nahi hota. Agar available copies 0 hon, toh constraint check transaction ko abort karke rollback kar deta hai."*
* **File to show**: Trigger definition in `init_db()` aur `issue_book()` in [database.py](file:///c:/Users/Ashish/OneDrive/Documents/Desktop/DBMS_PJT/database.py).

---

### Member 5: Return Trigger, Date Calculation & Dynamic Penalties
* **Topic**: Return Trigger (`trg_increment_stock_on_return`) aur late fee engine.
* **Viva Script**:
  > *"Maine Book Return transaction aur fine engine design kiya hai.*
  > *Jab borrowing record update hoke 'Returned' banta hai, toh database trigger automatic fire hota hai aur shelf stock ko +1 restore karta hai.*
  > *Agar Actual Return Date > Due Date hoti hai, toh system `(return_date - due_date) * daily_rate` calculate karke `fines` table mein pending penalty record insert karta hai.*
  > *Saara transaction atomic hota hai."*
* **File to show**: `return_book()` in [database.py](file:///c:/Users/Ashish/OneDrive/Documents/Desktop/DBMS_PJT/database.py) aur API `/api/return`.

---

### Member 6: Database Views, Live Frontend UI & Financial Settlement
* **Topic**: SQL Views (`v_active_borrowings`, `v_unpaid_fines`), Asynchronous UI, aur Penalty Settlement.
* **Viva Script**:
  > *"Maine Database Views aur Frontend UI develop kiya hai.*
  > *Humne complex relational joins ko abstract karne ke liye SQL Views banaye hain jaise `v_active_borrowings` aur `v_unpaid_fines`.*
  > *Frontend mein humne Vanilla JavaScript `fetch()` API use ki hai jo backend ke saath asynchronously communicate karti hai bina page reload kiye.*
  > *Librarian ek click mein pending fines ko settle aur 'Paid' mark kar sakta hai, aur saath hi poora UI Light aur Dark mode mein switch ho sakta hai."*
* **File to show**: [templates/index.html](file:///c:/Users/Ashish/OneDrive/Documents/Desktop/DBMS_PJT/templates/index.html) aur [static/script.js](file:///c:/Users/Ashish/OneDrive/Documents/Desktop/DBMS_PJT/static/script.js).

---

## Top 10 Core DBMS Viva Questions & Direct Answers

#### Q1: "Aapke project mein Normalization ka kaun sa level follow hua hai?"
**Ans**: Project **3NF (Third Normal Form)** mein hai:
1. Har column atomic hai (1NF).
2. Har non-key attribute poori primary key par dependent hai (2NF).
3. Koi transitive dependency nahi hai (3NF) — jaise patron ki details `members` table mein alag hain aur transaction details `borrowing` mein.

#### Q2: "Database Trigger kya hota hai aur aapne kahan use kiya?"
**Ans**: Trigger ek automatic SQL procedure hota hai jo table par INSERT, UPDATE ya DELETE event hone par database engine dwara execute hota hai. Humne 2 triggers lagaye hain:
- `trg_decrement_stock_on_issue`: Jab book issue hoti hai, toh stock automatic -1 ho jaata hai.
- `trg_increment_stock_on_return`: Jab book return hoti hai, toh stock automatic +1 ho jaata hai.

#### Q3: "Database View kya hota hai aur iska kya fayda hai?"
**Ans**: View ek virtual table hoti hai jo kisi SQL SELECT query ke result-set par based hoti hai. Humne `v_active_borrowings` view banaya hai jo books, members aur borrowing tables ko pehle se join karke rakhta hai. Isse security milti hai aur complex queries baar-baar nahi likhni padti.

#### Q4: "ACID properties mein 'A' (Atomicity) kaise guarantee hoti hai?"
**Ans**: Hum SQLite transactions use karte hain (`conn.commit()` aur `conn.rollback()`). Agar book issue karte waqt stock update ho gaya par transaction insert fail ho gaya, toh `ROLLBACK` poore operation ko undo kar deta hai, taaki half-baked data na bache.

#### Q5: "Consistency kaise ensure hoti hai?"
**Ans**: Database schema mein constraints se:
- `CHECK(available_copies >= 0)`: Stock kabhi negative nahi ho sakta.
- `CHECK(price >= 0.0)`: Price invalid negative nahi ho sakti.
- `FOREIGN KEY ON DELETE RESTRICT`: Agar koi book issued hai, toh wo book catalog se delete nahi ho sakti.

#### Q6: "Primary Key aur Foreign Key mein difference kya hai?"
**Ans**: 
- **Primary Key** (`book_id` in books) table ke har record ko uniquely identify karti hai aur kabhi NULL ya duplicate nahi ho sakti.
- **Foreign Key** (`book_id` in borrowing) dusri table ki primary key ko refer karti hai aur referential integrity maintain karti hai.

#### Q7: "Database schema ya live queries kaise verify karte hain?"
**Ans**: *"Sir, terminal me `sqlite3 library.db` open karke `.schema` ya direct SQL queries chala sakte hain, aur frontend ke har UI tab (Books, Members, Circulation, Fines) par REST API ke through direct parameterized SQL queries live execute hoti hain."*

#### Q8: "SQLite serverless database hone ka kya advantage hai?"
**Ans**: SQLite lightweight file-based relational database engine hai. Isme alag se MySQL server install karne, ports open karne ya password match karne ki jarurat nahi hoti. ACID compliant rehta hai aur kisi bhi machine par zero-configuration chalta hai.

#### Q9: "Foreign Keys ko SQLite mein enable kaise karte hain?"
**Ans**: SQLite default mein foreign keys disable rakhta hai backward compatibility ke liye. Isliye connection start hote hi hum `PRAGMA foreign_keys = ON;` execute karte hain.

#### Q10: "Fine calculate karne ka logic application mein hai ya database mein?"
**Ans**: System actual return date aur expected due date ka difference nikal kar days late nikalta hai aur daily rate se multiply karke transactionally `fines` table mein persist karta hai.

#### Q11: "Aapne kaun-kaun se real-world DBMS Corner Cases aur Business Rules handle kiye hain?"
**Ans**: 
1. **Primary Key Collision Protection**: `MAX(CAST(SUBSTR(id, 3) AS INTEGER)) + 1` query se safe monotonic ID generation taaki `COUNT(*)` par gap aane se crash na ho.
2. **Duplicate Active Loans**: Ek member same book ki multiple copies ek saath tab tak check out nahi kar sakta jab tak pehli return na ho.
3. **Quota & Delinquency Guard**: Har member par maximum 5 active loans ki limit hai, aur agar unpaid fines $20 se jyada pending hain toh new book issue block ho jati hai.
4. **Referential Integrity Audit Trail**: `ON DELETE RESTRICT` rule ensure karta hai ki circulation history wali books delete na ho sakein taaki library ka audit log preserve rahe.
5. **Temporal Constraints**: Due date past date nahi ho sakti (`due_date > borrow_date`), aur return date borrow date se pehle nahi ho sakti.
6. **Input Sanitization**: Non-numeric inputs (e.g. text in copies/price) par 500 server crash ke bajaye HTTP 400 clean constraint error message return hota hai.
