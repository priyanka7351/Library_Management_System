"""Generate useful descriptive statistics for the library datasets."""
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "dataset" / "processed"
if not (DATA_DIR / "books_cleaned.csv").exists():
    DATA_DIR = PROJECT_DIR / "dataset" / "raw"

def main():
    books = pd.read_csv(DATA_DIR / "books_cleaned.csv" if (DATA_DIR / "books_cleaned.csv").exists() else DATA_DIR / "books.csv")
    members = pd.read_csv(DATA_DIR / "members_cleaned.csv" if (DATA_DIR / "members_cleaned.csv").exists() else DATA_DIR / "members.csv")
    borrowing = pd.read_csv(
        DATA_DIR / "borrowing_cleaned.csv" if (DATA_DIR / "borrowing_cleaned.csv").exists() else DATA_DIR / "borrowing.csv",
        parse_dates=["issue_date", "due_date", "return_date"]
    )
    fines = pd.read_csv(DATA_DIR / "fines_cleaned.csv" if (DATA_DIR / "fines_cleaned.csv").exists() else DATA_DIR / "fines.csv")

    print("========== LIBRARY OVERVIEW ==========")
    print("Total books:", len(books))
    print("Total members:", len(members))
    print("Total borrowing transactions:", len(borrowing))
    print("Total fine records:", len(fines))
    print("Total fine amount:", round(fines["fine_amount"].sum(), 2))

    print("\\n========== BOOKS BY CATEGORY ==========")
    print(books.groupby("category")["book_id"].count().sort_values(ascending=False))

    print("\\n========== TOP 10 BORROWED BOOKS ==========")
    top_books = borrowing.merge(books[["book_id", "title"]], on="book_id")
    print(top_books.groupby("title")["borrow_id"].count().nlargest(10))

    print("\\n========== TOP 10 ACTIVE MEMBERS ==========")
    active = borrowing.merge(members[["member_id", "member_name"]], on="member_id")
    print(active.groupby("member_name")["borrow_id"].count().nlargest(10))

    print("\\n========== FINES BY PAYMENT STATUS ==========")
    print(fines.groupby("payment_status")["fine_amount"].agg(["count", "sum"]))

    print("\\n========== MONTHLY BORROWING ==========")
    borrowing["issue_date"] = pd.to_datetime(borrowing["issue_date"])
    monthly = borrowing.groupby(borrowing["issue_date"].dt.to_period("M"))["borrow_id"].count()
    print(monthly)

if __name__ == "__main__":
    main()
