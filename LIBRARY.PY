"""
Library Management System
A simple command-line app to manage books using Python + SQLite.
Run with: python library.py
"""

import sqlite3

# ---------- 1. Connect to the database (creates library.db if it doesn't exist) ----------
conn = sqlite3.connect("library.db")
cursor = conn.cursor()

# ---------- 2. Create the books table if it doesn't already exist ----------
cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    is_issued INTEGER DEFAULT 0,
    issued_to TEXT
)
""")
conn.commit()


# ---------- 3. Functions for each menu option ----------

def add_book():
    title = input("Enter book title: ")
    author = input("Enter author name: ")
    cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
    print(f"'{title}' added successfully!\n")


def view_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    if not books:
        print("No books in the library yet.\n")
        return
    print("\n%-4s %-25s %-20s %-10s %-15s" % ("ID", "Title", "Author", "Status", "Issued To"))
    print("-" * 80)
    for book in books:
        book_id, title, author, is_issued, issued_to = book
        status = "Issued" if is_issued else "Available"
        print("%-4s %-25s %-20s %-10s %-15s" % (book_id, title, author, status, issued_to or "-"))
    print()


def search_book():
    keyword = input("Enter title keyword to search: ")
    cursor.execute("SELECT * FROM books WHERE title LIKE ?", ('%' + keyword + '%',))
    results = cursor.fetchall()
    if not results:
        print("No matching books found.\n")
        return
    for book in results:
        book_id, title, author, is_issued, issued_to = book
        status = "Issued" if is_issued else "Available"
        print(f"[{book_id}] {title} by {author} - {status}")
    print()


def issue_book():
    book_id = input("Enter book ID to issue: ")
    member = input("Enter member name: ")
    cursor.execute("SELECT is_issued FROM books WHERE id = ?", (book_id,))
    row = cursor.fetchone()
    if row is None:
        print("Book not found.\n")
        return
    if row[0] == 1:
        print("This book is already issued.\n")
        return
    cursor.execute("UPDATE books SET is_issued = 1, issued_to = ? WHERE id = ?", (member, book_id))
    conn.commit()
    print(f"Book issued to {member}.\n")


def return_book():
    book_id = input("Enter book ID to return: ")
    cursor.execute("SELECT is_issued FROM books WHERE id = ?", (book_id,))
    row = cursor.fetchone()
    if row is None:
        print("Book not found.\n")
        return
    if row[0] == 0:
        print("This book was not issued.\n")
        return
    cursor.execute("UPDATE books SET is_issued = 0, issued_to = NULL WHERE id = ?", (book_id,))
    conn.commit()
    print("Book returned successfully.\n")


def delete_book():
    book_id = input("Enter book ID to delete: ")
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    print("Book deleted (if it existed).\n")


# ---------- 4. The main menu loop ----------

def main():
    while True:
        print("===== LIBRARY MANAGEMENT SYSTEM =====")
        print("1. Add a book")
        print("2. View all books")
        print("3. Search for a book")
        print("4. Issue a book")
        print("5. Return a book")
        print("6. Delete a book")
        print("7. Exit")
        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            add_book()
        elif choice == "2":
            view_books()
        elif choice == "3":
            search_book()
        elif choice == "4":
            issue_book()
        elif choice == "5":
            return_book()
        elif choice == "6":
            delete_book()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.\n")

    conn.close()


if __name__ == "__main__":
    main()