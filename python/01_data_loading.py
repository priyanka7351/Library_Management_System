"""Load the four raw library CSV datasets."""
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_DIR / "dataset" / "raw"

def load_data():
    books = pd.read_csv(RAW_DIR / "books.csv")
    members = pd.read_csv(RAW_DIR / "members.csv")
    borrowing = pd.read_csv(RAW_DIR / "borrowing.csv", parse_dates=["issue_date", "due_date", "return_date"])
    fines = pd.read_csv(RAW_DIR / "fines.csv", parse_dates=["fine_date"])

    print("DATASET SHAPES")
    for name, df in {
        "Books": books, "Members": members,
        "Borrowing": borrowing, "Fines": fines
    }.items():
        print(f"{name}: {df.shape[0]} rows, {df.shape[1]} columns")

    print("\\nBOOKS PREVIEW")
    print(books.head())
    return books, members, borrowing, fines

if __name__ == "__main__":
    load_data()
