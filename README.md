# Library-Management-System

# 📚 Library Management System

This is a Python-based **Library Management System** developed as part of the BBM103: Introduction to Programming Laboratory I course at Hacettepe University.

It simulates the core operations of a university library using file-based data and enforces borrowing rules for students. The system reads and updates book records, manages borrow/return actions, and outputs updated files representing the final library state.

---

## 🧠 Features

- ✅ Load existing books and new book additions
- ✅ Track book availability and student borrows
- ✅ Borrow and return operations with rule enforcement:
  - No student can borrow more than 3 books at once
- ✅ Detect and prevent invalid actions
- ✅ Output result files:
  - `library.txt`: Full book list
  - `available_books.txt`: Available books
  - `on_loan_books.txt`: Borrowed books

---

## 📁 Input Files

- `existing_books.txt`: Initial book records
- `new_books.txt`: New books to be added
- `existing_student_borrows.txt`: Existing borrow status
- `borrow_and_return_data.txt`: Student actions (borrow / return)

> 🧪 Test versions of input files (`test_existing_books.txt`, etc.) are also supported for validation and debugging.

---

## 🛠 Technologies Used

- Python 3.9.18
- File I/O
- Core data structures: `list`, `tuple`, `set`, `dict`
- Modular function-based architecture

---

## 🚀 How to Run

```bash
python main.py
