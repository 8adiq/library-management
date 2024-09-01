from flask import Flask,jsonify,request
import psycopg2,os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# connecting to database
def db_connect():
    """"""
    try:
        connection = psycopg2.connect(
            dbname=os.getenv("dbname"),
                    user=os.getenv("user"),
                    password=os.getenv("password"),
                    host=os.getenv("host"),
                    port=os.getenv("port")
        )
        print('message : connected to database')
        return connection
    except (Exception,psycopg2.Error) as e:
        print(f'error: {e} occured')

# adding a book
@app.route('/add-book',methods=['POST'])
def add_book():
    """"""
    try:
        data = request.get_json()
        author = data.get('author')
        title = data.get('title')
        year_pub = data.get('year_pub')

        if not author or not title or not year_pub:
            return jsonify({'Error':'Author, Title or Year of Publication can not be empty'}),400
        
        conn = db_connect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM books WHERE author =%s and title=%s and year_pub =%s',(author,title,year_pub))
        exits = cur.fetchone()

        if exits:
            return jsonify({'message':'Book already in the library'})
        else:
            cur.execute('INSERT INTO books (author,title,year_pub) VALUES (%s,%s,%s)',(author,title,year_pub))
            conn.commit()
            return jsonify({'Message':f'{title} by {author} has been added'})
        
    except (Exception,psycopg2.Error) as e:
        return jsonify({'Error':str(e)})
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
    


# update book
@app.route('/update-book/<int:id>',methods=['PUT'])
def update_book(id):
    """"""
    try:
        data = request.get_json()
        author = data.get('author')
        title = data.get('title')
        year_pub = data.get('year_pub')

        if not author and not title and not year_pub:
            return jsonify({'Error': 'At least one of Author, Title, or Year of Publication must be provided'}), 400

        conn = db_connect()
        cur = conn.cursor()

        update_fields = []
        params = []

        if author:
            update_fields.append('author = %s')
            params.append(author)
        if title:
            update_fields.append('title = %s')
            params.append(title)
        if year_pub:
            update_fields.append('year_pub = %s')
            params.append(year_pub)

        if not update_fields:
            return jsonify({'Error': 'No fields to update'}), 400

        query = 'UPDATE books SET ' + ', '.join(update_fields) + ' WHERE id = %s'
        params.append(id)

        cur.execute(query, tuple(params))
        conn.commit()

        if cur.rowcount == 0:
            return jsonify({'Error': f'No book with ID {id} found'}), 404

        return jsonify({'message': f'Book with ID {id} updated successfully'}), 200

    except (Exception, psycopg2.Error) as e:
        return jsonify({'Error': str(e)}), 500
    finally:
            cur.close()
            conn.close()


# show books
@app.route('/show-books',methods=['GET'])
def show_books():
    """"""
    try:
        conn = db_connect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM books')
        books = cur.fetchall()

        if not books:
            return jsonify({'Error': 'No books found'}), 404

        books_list = []
        for book in books:
            book_dict = {
                'book_id': book[0],
                'author': book[1],
                'title': book[2],
                'year_pub': book[3]
            }
            books_list.append(book_dict)

        return jsonify({'Books': books_list}), 200

    except (Exception, psycopg2.Error) as e:
        return jsonify({'Error': str(e)}), 500
    finally:
        cur.close()
        conn.close()


# delete a book
@app.route('/delete-book/<int:id>', methods=['DELETE'])
def remove_book(id):
    """"""
    try:
        conn = db_connect()
        cur = conn.cursor()
        cur.execute('DELETE FROM books WHERE id = %s', (id,))
        conn.commit()

        if cur.rowcount == 0:
            return jsonify({'Error': f'No book with ID {id} found'}), 404

        return jsonify({'message': f'Book with ID {id} deleted successfully'}), 200

    except (Exception, psycopg2.Error) as e:
        return jsonify({'Error': str(e)}), 500
    finally:
            cur.close()
            conn.close()
