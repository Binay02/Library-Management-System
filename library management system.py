import mysql.connector

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",  
        database="library_db"
    )

# Dataset Ex
initial_books = [
    ("To Kill a Mockingbird", "Harper Lee", "9780060935467"),
    ("1984", "George Orwell", "9780451524935"),
    ("The Great Gatsby", "F. Scott Fitzgerald", "9780743273565")
]

initial_members = [
    ("Binay",),
    ("Himanshu",)
]


#Setup Functions 
def setup_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS library_db")
    cursor.execute("USE library_db")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255),
            author VARCHAR(255),
            isbn VARCHAR(50),
            issued_to INT DEFAULT NULL,
            FOREIGN KEY (issued_to) REFERENCES members(id) ON DELETE SET NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS issuance (
            id INT AUTO_INCREMENT PRIMARY KEY,
            book_id INT,
            member_id INT,
            issue_date DATE,
            return_date DATE,
            FOREIGN KEY (book_id) REFERENCES books(id),
            FOREIGN KEY (member_id) REFERENCES members(id)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def populate_dataset():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executemany("INSERT INTO books (title, author, isbn) VALUES (%s, %s, %s)", initial_books)
    cursor.executemany("INSERT INTO members (name) VALUES (%s)", initial_members)
    conn.commit()
    cursor.close()
    conn.close()

# CRUD Operations

def add_book(title, author, isbn):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, isbn) VALUES (%s, %s, %s)", (title, author, isbn))
    conn.commit()
    cursor.close()
    conn.close()
    print("Book added!")

def update_book(book_id, title, author, isbn):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title=%s, author=%s, isbn=%s WHERE id=%s", (title, author, isbn, book_id))
    conn.commit()
    cursor.close()
    conn.close()
    print("Book updated!")

def delete_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id=%s", (book_id,))
    conn.commit()
    cursor.close()
    conn.close()
    print("Book deleted!")

def search_books(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, isbn, issued_to FROM books WHERE title LIKE %s OR author LIKE %s", (f"%{query}%", f"%{query}%"))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    print("Books found:")
    for row in results:
        print(row)

def add_member(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO members (name) VALUES (%s)", (name,))
    conn.commit()
    cursor.close()
    conn.close()
    print("Member added!")

def update_member(member_id, name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE members SET name=%s WHERE id=%s", (name, member_id))
    conn.commit()
    cursor.close()
    conn.close()
    print("Member updated!")

def delete_member(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM members WHERE id=%s", (member_id,))
    conn.commit()
    cursor.close()
    conn.close()
    print("Member deleted!")

def issue_book(book_id, member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET issued_to=%s WHERE id=%s AND issued_to IS NULL", (member_id, book_id))
    if cursor.rowcount == 0:
        print("Book already issued or not found!")
    else:
        cursor.execute("INSERT INTO issuance (book_id, member_id, issue_date) VALUES (%s, %s, NOW())", (book_id, member_id))
        conn.commit()
        print("Book issued!")
    cursor.close()
    conn.close()

def return_book(book_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT issued_to FROM books WHERE id=%s", (book_id,))
    issued_to = cursor.fetchone()
    if issued_to and issued_to[0]:
        cursor.execute("UPDATE books SET issued_to=NULL WHERE id=%s", (book_id,))
        cursor.execute("UPDATE issuance SET return_date=NOW() WHERE book_id=%s AND return_date IS NULL", (book_id,))
        conn.commit()
        print("Book returned!")
    else:
        print("Book not issued!")
    cursor.close()
    conn.close()

def list_issued_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.title, m.name, i.issue_date, i.return_date
        FROM issuance i
        JOIN books b ON i.book_id = b.id
        JOIN members m ON i.member_id = m.id
        WHERE i.return_date IS NULL
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    print("Issued books:")
    for row in results:
        print(row)

# Main Menu 
def main():
    setup_database()
    try:
        populate_dataset()
    except:
        pass  # Ignore duplicate entry errors

    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Update Book")
        print("3. Delete Book")
        print("4. Search Books")
        print("5. Add Member")
        print("6. Update Member")
        print("7. Delete Member")
        print("8. Issue Book")
        print("9. Return Book")
        print("10. List Issued Books")
        print("0. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            t = input("Title: ")
            a = input("Author: ")
            i = input("ISBN: ")
            add_book(t, a, i)
        elif choice == "2":
            book_id = int(input("Book ID: "))
            t = input("Title: ")
            a = input("Author: ")
            i = input("ISBN: ")
            update_book(book_id, t, a, i)
        elif choice == "3":
            book_id = int(input("Book ID: "))
            delete_book(book_id)
        elif choice == "4":
            q = input("Search query (title/author): ")
            search_books(q)
        elif choice == "5":
            n = input("Member Name: ")
            add_member(n)
        elif choice == "6":
            member_id = int(input("Member ID: "))
            n = input("Member Name: ")
            update_member(member_id, n)
        elif choice == "7":
            member_id = int(input("Member ID: "))
            delete_member(member_id)
        elif choice == "8":
            book_id = int(input("Book ID: "))
            member_id = int(input("Member ID: "))
            issue_book(book_id, member_id)
        elif choice == "9":
            book_id = int(input("Book ID: "))
            return_book(book_id)
        elif choice == "10":
            list_issued_books()
        elif choice == "0":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
