import os
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv

load_dotenv()

class Library:
    def __init__(self):
        self.connect_to_db()

    def connect_to_db(self):
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
        cur = self.connection.cursor()
        cur.execute("INSERT INTO books (title,author,year_pub) VALUES (%s,%s,%s)", (title,author,year))
        self.connection.commit()
        cur.close()

        
    def search_book(self,search_item):
        cur = self.connection.cursor()
        cur.execute("SELECT title, author from books WHERE title = %s OR author = %s ", (search_item,search_item))
        results = cur.fetchall()

        for title,author in results:
            print(f"{title} , {author}")

    def remove_book(self,title):
        cur = self.connection.cursor()
        cur.execute("DELETE FROM books WHERE title = %s", (title,))

        if cur.rowcount == 0:
            print(f" No book with the title {title}")
        else:
            self.connection.commit()
            print(f" {title} has been removed")
        cur.close()




library = Library()
# library.connect_to_db()
library.add_book('title1','author1',1952)
library.add_book('title2','author2',2000)
library.add_book('title3','author3',1996)

library.search_book("title1")
