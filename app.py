from flask import Flask, render_template, request, jsonify
import database

app = Flask(__name__)
database.init_db()


@app.route("/")
def home():
    return render_template("index.html")


# Dashboard
@app.route("/api/stats")
def stats():
    return jsonify(database.get_dashboard_stats())


# Books
@app.route("/api/books")
def books():
    search = request.args.get("search", "")
    return jsonify(database.get_all_books(search))


@app.route("/api/books", methods=["POST"])
def add_book():
    data = request.json

    result, message = database.add_new_book(
        data["book_id"],
        data["title"],
        data["author"],
        data.get("category", "General"),
        data.get("isbn", ""),
        int(data.get("publication_year", 2024)),
        int(data.get("total_copies", 1)),
        float(data.get("price", 0))
    )

    return jsonify({"message": message}), 200 if result else 400


@app.route("/api/books/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    result, message = database.delete_book(book_id)
    return jsonify({"message": message}), 200 if result else 400


# Members
@app.route("/api/members")
def members():
    return jsonify(database.get_all_members())


@app.route("/api/members", methods=["POST"])
def add_member():
    data = request.json

    result, message = database.add_new_member(
        data["member_id"],
        data["first_name"],
        data.get("last_name", ""),
        data["email"],
        data.get("phone", ""),
        data.get("membership_type", "Student")
    )

    return jsonify({"message": message}), 200 if result else 400


# Issue and return
@app.route("/api/issue", methods=["POST"])
def issue():
    data = request.json

    result, message = database.issue_book(
        data["book_id"],
        data["member_id"],
        data["due_date"]
    )

    return jsonify({"message": message}), 200 if result else 400


@app.route("/api/return", methods=["POST"])
def return_book():
    data = request.json

    result, message = database.return_book(
        data["borrow_id"],
        data.get("return_date"),
        float(data.get("daily_fine", 2))
    )

    return jsonify({"message": message}), 200 if result else 400


@app.route("/api/borrowings")
def borrowings():
    return jsonify(database.get_active_borrowings())


# Fines
@app.route("/api/fines")
def fines():
    return jsonify(database.get_all_fines())


@app.route("/api/fines/<fine_id>/pay", methods=["POST"])
def pay_fine(fine_id):
    result, message = database.mark_fine_as_paid(fine_id)
    return jsonify({"message": message}), 200 if result else 400


if __name__ == "__main__":
    app.run(debug=True)
