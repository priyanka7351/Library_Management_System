"""Create charts from the processed library datasets."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = PROJECT_DIR / "dataset" / "processed"
RAW_DIR = PROJECT_DIR / "dataset" / "raw"
OUTPUT_DIR = PROJECT_DIR / "outputs" / "python_charts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def read_dataset(clean_name, raw_name, **kwargs):
    path = PROCESSED_DIR / clean_name
    if not path.exists():
        path = RAW_DIR / raw_name
    return pd.read_csv(path, **kwargs)

def main():
    books = read_dataset("books_cleaned.csv", "books.csv")
    members = read_dataset("members_cleaned.csv", "members.csv")
    borrowing = read_dataset(
        "borrowing_cleaned.csv", "borrowing.csv",
        parse_dates=["borrow_date", "due_date", "return_date"]
    )
    fines = read_dataset("fines_cleaned.csv", "fines.csv")

    sns.set_theme()

    # 1. Number of books in each category.
    category_counts = books.groupby("category")["book_id"].count().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=category_counts.index, y=category_counts.values)
    plt.title("Number of Books by Category")
    plt.xlabel("Category")
    plt.ylabel("Number of Books")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "books_by_category.png", dpi=300)
    plt.close()

    # 2. Monthly borrowing trend.
    borrowing["issue_date"] = pd.to_datetime(borrowing["borrow_date"])
    monthly = borrowing.groupby(borrowing["borrow_date"].dt.to_period("M"))["borrow_id"].count()
    monthly.index = monthly.index.astype(str)
    plt.figure(figsize=(12, 6))
    sns.lineplot(x=monthly.index, y=monthly.values, marker="o")
    plt.title("Monthly Borrowing Trend")
    plt.xlabel("Month")
    plt.ylabel("Number of Borrowings")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "monthly_borrowing_trend.png", dpi=300)
    plt.close()

    # 3. Top 10 borrowed books.
    book_activity = borrowing.merge(books[["book_id", "title"]], on="book_id")
    top_books = book_activity.groupby("title")["borrow_id"].count().nlargest(10).sort_values()
    plt.figure(figsize=(10, 7))
    sns.barplot(x=top_books.values, y=top_books.index)
    plt.title("Top 10 Most Borrowed Books")
    plt.xlabel("Borrowing Count")
    plt.ylabel("Book")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "top_10_books.png", dpi=300)
    plt.close()

    # 4. Fine amount by payment status.
    fine_summary = fines.groupby("payment_status")["fine_amount"].sum().sort_values(ascending=False)
    plt.figure(figsize=(8, 5))
    sns.barplot(x=fine_summary.index, y=fine_summary.values)
    plt.title("Fine Amount by Payment Status")
    plt.xlabel("Payment Status")
    plt.ylabel("Fine Amount")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "fines_by_status.png", dpi=300)
    plt.close()

    print(f"Charts saved in: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
