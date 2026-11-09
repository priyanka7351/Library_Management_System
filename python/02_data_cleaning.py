"""Clean library CSV data and save processed versions."""
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_DIR / "dataset" / "raw"
PROCESSED_DIR = PROJECT_DIR / "dataset" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def clean_data():
    books = pd.read_csv(RAW_DIR / "books.csv")
    members = pd.read_csv(RAW_DIR / "members.csv")
    borrowing = pd.read_csv(
        RAW_DIR / "borrowing.csv",
        parse_dates=["borrow_date", "due_date", "return_date"]
    )
    fines = pd.read_csv(RAW_DIR / "fines.csv", parse_dates=["fine_date"])

    # Remove exact duplicate rows.
    books = books.drop_duplicates()
    members = members.drop_duplicates()
    borrowing = borrowing.drop_duplicates()
    fines = fines.drop_duplicates()

    # Standardize text columns.
    for df in (books, members, fines):
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].astype("string").str.strip()

    # Normalize email addresses.
    members["email"] = members["email"].str.lower()

    # Convert numeric columns safely.
    for col in ["publication_year", "available_copies", "total_copies"]:
        books[col] = pd.to_numeric(books[col], errors="coerce")
    fines["fine_amount"] = pd.to_numeric(fines["fine_amount"], errors="coerce")

    # Validate basic inventory values.
    books = books[
        books["book_id"].notna()
        & books["available_copies"].ge(0)
        & books["total_copies"].ge(0)
        & books["available_copies"].le(books["total_copies"])
    ].copy()

    # Keep only rows with essential identifiers and dates.
    borrowing = borrowing[
        borrowing["borrow_id"].notna()
        & borrowing["member_id"].notna()
        & borrowing["book_id"].notna()
        & borrowing["borrow_date"].notna()
        & borrowing["due_date"].notna()
    ].copy()

    members = members[members["member_id"].notna() & members["email"].notna()].copy()
    fines = fines[
        fines["fine_id"].notna()
        & fines["borrow_id"].notna()
        & fines["fine_amount"].ge(0)
    ].copy()

    outputs = {
        "books_cleaned.csv": books,
        "members_cleaned.csv": members,
        "borrowing_cleaned.csv": borrowing,
        "fines_cleaned.csv": fines,
    }
    for filename, df in outputs.items():
        df.to_csv(PROCESSED_DIR / filename, index=False)
        print(f"Saved {filename}: {len(df)} rows")

    print("\\nCleaning completed.")
    return books, members, borrowing, fines

if __name__ == "__main__":
    clean_data()
