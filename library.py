import os
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv

load_dotenv()

class Library:
    def __init__(self):
        """initializing a connection to the database"""
        self.connect_to_db()

    def connect_to_db(self):
        """function that creates a connection with the database"""
        try:
            self.connection = psycopg2.connect(
                dbname=os.getenv("dbname"),
                user=os.getenv("user"),
                password=os.getenv("password"),
                host=os.getenv("host"),
                port=os.getenv("port")
            )
            print(" Successfully Connected")
            return self.connection
        except OperationalError as e:
            print(f" The error {e} occured")
            return None
        
    def add_book(self,title,author,year):
        """ function to add a new book"""
        cur = self.connection.cursor()
        cur.execute("INSERT INTO books (title,author,year_pub) VALUES (%s,%s,%s)", (title,author,year))
        self.connection.commit()
        cur.close()
        print(f'{title} by {author} has been added.')
        
    def search_book(self,search_item):
        """function to search for a book"""
        cur = self.connection.cursor()
        cur.execute("SELECT title, author from books WHERE title = %s OR author = %s ", (search_item,search_item))
        results = cur.fetchall()

        for title,author in results:
            print(f"{title} , {author}")

    def display_books(self):
        """function to display all books in the library"""
        cur = self.connection.cursor()
        cur.execute('SELECT * FROM books')
        books = cur.fetchall()
        print('\n ====== All books in the library ======')
        for i, (id,title,author,year) in enumerate(books,start=1):
            print(f'{i}.  {title} by {author}')

    def remove_book(self,title,author):
        """function to remove a book from the library"""
        cur = self.connection.cursor()
        cur.execute("DELETE FROM books WHERE title = %s AND author = %s", (title,author))

        if cur.rowcount == 0:
            print(f" No book with the title {title} by {author}")
        else:
            self.connection.commit()
            print(f" {title} by {author} has been removed")
        cur.close()


def main():

    library = Library()

    while True:
        print("\nLibrary System\n 1. Add Book\n 2. Find Book\n 3. Display All Books\n 4. Remove Book\n 5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            title = input("Enter the book title: ")
            author = input("Enter the book author: ")
            year = input("Enter the year of publishing: ")
            library.add_book(title, author,year)
        elif choice == '2':
            search_item = input("Enter the book title or author to search: ")
            library.search_book(search_item)
        elif choice == '3':
            library.display_books()
        elif choice == '4':
            title = input("Enter the book title to remove: ")
            author = input("Enter the book author to remove: ")
            library.remove_book(title,author)
        elif choice == '5':
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()

