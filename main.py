import os # This line imports the 'os' module, which allows us to interact with the opwrating system.


# This function reads books from a file and stores them in a list.
# Each line in the file should contain four parts: ISBN, title, author, and year.
def read_books(file_path):
    books = []

    with open(file_path,"r",encoding="cp1254") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) == 4:
                isbn,title,author,year = parts
                books.append((isbn,(title,author,year)))
    print(f"[OK] {len(books)} book read: {os.path.basename(file_path)}")

    return books

# This function add a book to the library.
# If the book already exists (by ISBN) it doesnt add again.
def add_book(isbn,book,library):
    if isbn in library:
        return False
    library[isbn] = book
    return True

# This function merges two book lists one.
# It avoids adding duplicate books and counts how many new books added.
def merge_books(existing,new):
    library = {}
    added_count = 0

    for isbn,book in existing:
        library[isbn] = book

    for isbn,book in new:
        if add_book(isbn,book,library):
            added_count += 1

    print(f"[OK] new books added: {added_count}")
    return library

# This function reads which books are borrowed now.
# It returns both the list of loans and the set of available books.
def process_borrow_status(file_path,library):
    loans = {}
    borrowed = set()

    with open(file_path,"r",encoding="cp1254") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) == 2:
                student,isbn = parts
                isbn = isbn.strip()
                if isbn:
                    loans[isbn] = student
                    borrowed.add(isbn)
    print(f"[OK] number of books borrowed: {len(borrowed)}")

    available = set(library.keys()) - borrowed
    return loans,available

# This function lets a student borrow a book.
# Checks if the book is available and if the student borrowed less than three books.
def borrow_book(isbn,student,available,loans,student_loans):
    if isbn not in available:
        return False

    current_loans = student_loans.get(student, set())
    if len(current_loans) >= 3:
        return False

    available.remove(isbn)
    loans[isbn] = student
    current_loans.add(isbn)
    student_loans[student] = current_loans
    return True

# This function lets a student return a borrowed book.
# Checks if the student borrowed the book before.
def return_book(isbn,student,available,loans,student_loans):
    if isbn not in loans or loans[isbn] != student:
        return False

    del loans[isbn]
    available.add(isbn)
    student_loans[student].remove(isbn)
    return True

# This function processes a list of actions (borrow or return).
# Updates the current loan and availability status for each book.
def process_actions(file_path,library,loans,available):
    student_loans = {}

    for isbn,student in loans.items():
        student_loans.setdefault(student, set()).add(isbn)

    with open(file_path,"r",encoding="cp1254") as file:
        for i, line in enumerate(file, 1):
            parts = line.strip().split(",")
            if len(parts) == 3:
                student,action,isbn = parts
                isbn = isbn.strip()

                if action == "borrow":
                    if borrow_book(isbn,student,available,loans,student_loans):
                        print(f"[{i}] {student} -> {isbn} borrowed")
                    else:
                        print(f"[{i}] {student} -> {isbn} couldn't borrow")
                elif action == "return":
                    if return_book(isbn,student,available,loans,student_loans):
                        print(f"[{i}] {student} -> {isbn} returned")
                    else:
                        print(f"[{i}] {student} -> {isbn} couldn't return")

    return loans,available

# This function writes the final state of the library to thre output files:
# 1-All books, 2-Available books, 3-Borrowed books.
def write_outputs(output_dir,library,available,loans):

    with open(os.path.join(output_dir,"library.txt"),"w",encoding="cp1254") as f:
        for isbn in sorted(library):
            book = library[isbn]
            f.write(f"{isbn},{book[0]},{book[1]},{book[2]}\n")
    print(f"[OK] library.txt file written ({len(library)} book)")

    with open(os.path.join(output_dir,"available_books.txt"),"w",encoding="cp1254") as f:
        for isbn in sorted(available):
            f.write(f"{isbn}\n")
    print(f"[OK] available_books.txt file written ({len(available)} book)")


    with open(os.path.join(output_dir,"on_loan_books.txt"),"w",encoding="cp1254") as f:
        for isbn in sorted(loans):
            f.write(f"{isbn},{loans[isbn]}\n")
    print(f"[OK] on_loan_books.txt file written ({len(loans)} book)")

    return True

# This is the main function. It run the library system step by step.
def main():
    print("Launching Library Management System...\n")
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # File paths for existing books, new books, borrow records, and actions
    existing_books_path = os.path.join(base_dir,"existing_books.txt")
    new_books_path = os.path.join(base_dir,"new_books.txt")
    borrows_path = os.path.join(base_dir,"existing_student_borrows.txt")
    actions_path = os.path.join(base_dir,"borrow_and_return_data.txt")

    # Read and process data
    existing_books = read_books(existing_books_path)
    new_books = read_books(new_books_path)
    library = merge_books(existing_books,new_books)

    loans,available = process_borrow_status(borrows_path,library)
    loans,available = process_actions(actions_path,library,loans,available)

    # Write outputs to files
    write_outputs(base_dir,library,available,loans)

# If this file is run directly start the program.
if __name__ == "__main__":
    main()
