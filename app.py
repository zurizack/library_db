from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
from dal import *

app = Flask(__name__)
CORS(app)

# Create the database schema
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Author TEXT NOT NULL,
        YearPublished INTEGER NOT NULL,
        Type INTEGER NOT NULL
    )
''')

# Create Customers table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Family TEXT NOT NULL,
        City TEXT NOT NULL,
        Age INTEGER NOT NULL
    )
''')

# Create Loans table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Loans (
        CustID INTEGER,
        BookID INTEGER,
        LoanDate TEXT NOT NULL,
        ReturnDate TEXT NOT NULL,
        FOREIGN KEY (CustID) REFERENCES Customers(Id),
        FOREIGN KEY (BookID) REFERENCES Books(Id)
    )
''')

conn.commit()
conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/show_books')
def show_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Books')
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('show_books.html', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        try:
            data = request.get_json()
            name = data['name']
            author = data['author']
            year_published = data['yearPublished']
            book_type = data['bookType']

            book = Book(name, author, year_published, book_type)

            if book.existing():
                # Book already exists in the database
                return jsonify({'message': 'Book already exists'})

            book.save()

            return jsonify({'message': 'Book added successfully', 'name': book.name, 'author': book.author,
                            'yearPublished': book.year_published, 'bookType': book.book_type})
        except Exception as e:
            print("Error:", e)
            return jsonify({'error': 'An error occurred'}), 500
    else:
        return render_template('add_book.html')

@app.route('/find_book')
def find_book():
    search_name = request.args.get('name')
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Books WHERE Name = ?', (search_name,))
    book = cursor.fetchone()
    cursor.close()
    conn.close()

    if book:
        return render_template('find_book.html', book=book)
    else:
        return render_template('find_book.html', error='Book not found')

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        try:
            data = request.get_json()
            name = data['name']
            family = data['family']
            city = data['city']
            age = data['age']
            print("name:",name,"family:",family,"city:",city,"age:",age)
            customer = Customer(name, family, city, age)

            if customer.existing():
                # Customer already exists in the database
                return jsonify({'message': 'Customer already exists'})

            customer = Customer(name, family, city, age)
            customer.save()

            return jsonify({'message': 'Customer added successfully', 'name': customer.name, 'family': customer.family, 'city': customer.city,
                            'age': customer.age})
        except Exception as e:
            print("Error:", e)
            return jsonify({'error': 'An error occurred'}), 500
    else:
        return render_template('add_customer.html')

@app.route('/show_customers')
def show_customers():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Customers')
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('show_customers.html', customers=customers)

@app.route('/find_customer')
def find_customer():
    search_name = request.args.get('name')
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Customers WHERE Name = ?', (search_name,))
    customer = cursor.fetchone()
    cursor.close()
    conn.close()

    if customer:
        return render_template('find_customer.html', customer=customer)
    else:
        return render_template('find_customer.html', error='Customer not found')

@app.route('/delete_book', methods=['GET','POST'])
def delete_book():
    if request.method == 'POST':
        try:
            data = request.get_json()
            name = data['name']
            author = data['author']
            book = Book(name,author,0,0)
            if book.existing():
                book.delete()
                return jsonify({'message': 'Book removed successfully'})
            else:
                return jsonify({'message': 'Book not found'})


        except Exception as e:
            print("Error:", e)
            return jsonify({'error': 'An error occurred'}), 500

    else:
        return render_template('delete_book.html')
    
@app.route('/delete_customer', methods=['GET', 'POST'])
def delete_customer():
    if request.method == 'POST':
        try:
            data = request.get_json()
            name = data['name']
            family = data['family']
            city = data['city']
            age = data['age']

            customer = Customer(name, family, city, age)

            if customer.existing():
                customer.delete()
                return jsonify({'message': 'Customer removed successfully'})
            else:
                return jsonify({'message': 'Customer not found'})

        except Exception as e:
            print("Error:", e)
            return jsonify({'error': 'An error occurred'}), 500

    else:
        return render_template('delete_customer.html')





if __name__ == '__main__':
    app.run(debug=True)