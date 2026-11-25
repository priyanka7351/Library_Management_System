from flask import Flask, render_template, request, jsonify
import database

app = Flask(__name__)

# Initialize database tables on server startup
database.init_db()

@app.route("/")
def home():
    return render_template("index.html")

# ---------------- Dashboard Route ----------------

@app.route("/api/stats", methods=["GET"])
def get_stats():
    stats = database.get_dashboard_stats()
    return jsonify(stats)

# ---------------- Books Routes ----------------

@app.route("/api/books", methods=["GET"])
def get_books():
    search = request.args.get("search", "").strip()
    books = database.get_all_books(search)
    return jsonify(books)

@app.route("/api/books", methods=["POST"])
def add_book():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided."}), 400
    
    book_id = str(data.get("book_id", "")).strip()
    title = str(data.get("title", "")).strip()
    author = str(data.get("author", "")).strip()
    category = str(data.get("category", "General")).strip()
    isbn = str(data.get("isbn", "")).strip()

    if not book_id or not title or not author:
        return jsonify({"success": False, "message": "Book ID, Title, and Author are required fields."}), 400

    if not isbn:
        isbn = f"978-{book_id}"

    try:
        raw_year = data.get("publication_year")
        year = int(raw_year) if raw_year is not None and str(raw_year).strip() != "" else 2024
        
        raw_copies = data.get("total_copies")
        copies = int(raw_copies) if raw_copies is not None and str(raw_copies).strip() != "" else 1
        
        raw_price = data.get("price")
        price = float(raw_price) if raw_price is not None and str(raw_price).strip() != "" else 0.0
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Publication year, total copies, and price must be valid numbers."}), 400

    if copies <= 0:
        return jsonify({"success": False, "message": "Total copies must be at least 1."}), 400

    if price < 0.0:
        return jsonify({"success": False, "message": "Price cannot be negative."}), 400

    if year < 1500 or year > 2030:
        return jsonify({"success": False, "message": "Publication year must be between 1500 and 2030."}), 400

    success, message = database.add_new_book(book_id, title, author, category, isbn, year, copies, price)
    status_code = 200 if success else 400
    return jsonify({"success": success, "message": message}), status_code

@app.route("/api/books/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    success, message = database.delete_book(book_id)
    status_code = 200 if success else 400
    return jsonify({"success": success, "message": message}), status_code

# ---------------- Members Routes ----------------

@app.route("/api/members", methods=["GET"])
def get_members():
    members = database.get_all_members()
    return jsonify(members)

@app.route("/api/members", methods=["POST"])
def add_member():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided."}), 400
    
    member_id = str(data.get("member_id", "")).strip()
    first_name = str(data.get("first_name", "")).strip()
    last_name = str(data.get("last_name", "")).strip()
    email = str(data.get("email", "")).strip()
    phone = str(data.get("phone", "")).strip()
    m_type = str(data.get("membership_type", "Student")).strip()

    if not member_id or not first_name or not email:
        return jsonify({"success": False, "message": "Member ID, First Name, and Email are required fields."}), 400

    if "@" not in email or "." not in email:
        return jsonify({"success": False, "message": "Invalid email address format."}), 400

    success, message = database.add_new_member(member_id, first_name, last_name, email, phone, m_type)
    status_code = 200 if success else 400
    return jsonify({"success": success, "message": message}), status_code

# ---------------- Circulation Routes ----------------

@app.route("/api/borrowings", methods=["GET"])
def get_borrowings():
    loans = database.get_active_borrowings()
    return jsonify(loans)

@app.route("/api/issue", methods=["POST"])
def issue_book():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided."}), 400

    book_id = str(data.get("book_id", "")).strip()
    member_id = str(data.get("member_id", "")).strip()
    due_date = str(data.get("due_date", "")).strip()

    if not book_id or not member_id or not due_date:
        return jsonify({"success": False, "message": "Book ID, Member ID, and Due Date are required."}), 400

    success, message = database.issue_book(book_id, member_id, due_date)
    status_code = 200 if success else 400
    return jsonify({"success": success, "message": message}), status_code

@app.route("/api/return", methods=["POST"])
def return_book():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data provided."}), 400

    borrow_id = str(data.get("borrow_id", "")).strip()
    return_date = str(data.get("return_date", "")).strip() or None
    
    try:
        raw_fine = data.get("daily_fine", 2.0)
        daily_fine = float(raw_fine) if raw_fine is not None else 2.0
        if daily_fine < 0.0:
            daily_fine = 2.0
    except (ValueError, TypeError):
        daily_fine = 2.0

    if not borrow_id:
        return jsonify({"success": False, "message": "Borrow ID is required."}), 400

    success, message = database.return_book(borrow_id, return_date, daily_fine)
    status_code = 200 if success else 400
    return jsonify({"success": success, "message": message}), status_code

# ---------------- Fines Routes ----------------

@app.route("/api/fines", methods=["GET"])
def get_fines():
    fines = database.get_all_fines()
    return jsonify(fines)

@app.route("/api/fines/<fine_id>/pay", methods=["POST"])
def pay_fine(fine_id):
    success, message = database.mark_fine_as_paid(fine_id)
    status_code = 200 if success else 400
    return jsonify({"success": success, "message": message}), status_code

if __name__ == "__main__":
    print("Starting Library Management System on http://127.0.0.1:5000 ...")
    app.run(host="127.0.0.1", port=5000, debug=False)
