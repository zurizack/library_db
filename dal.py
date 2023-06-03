import sqlite3

class Book:
    def __init__(self, name, author, year_published, book_type):
        self.name = name
        self.author = author
        self.year_published = year_published
        self.book_type = book_type

    def save(self):
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO Books (Name, Author, YearPublished, Type)
            VALUES (?, ?, ?, ?)
        ''', (self.name, self.author, self.year_published, self.book_type))


        conn.commit()
        cursor.close()
        conn.close()
    
    def existing(self):
            conn = sqlite3.connect('library.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Books WHERE Name = ? AND Author = ?', (self.name, self.author))
            existing_book = cursor.fetchone()
            cursor.close()
            conn.close()
            return existing_book is not None

    def delete(self):
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM Books WHERE Name = ? AND Author = ?', (self.name, self.author))

        conn.commit()
        conn.close() 
    

    

class Customer:
    def __init__(self, name,family,city, age):
        self.name = name
        self.family = family
        self.city = city
        self.age = age

    def save(self):
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO Customers (Name ,family ,City, Age)
            VALUES (?, ?, ?, ?)
        ''', (self.name, self.family, self.city, self.age))

        conn.commit()
        cursor.close()
        conn.close()

    def existing(self):
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Customers WHERE Name = ? AND Family = ? AND City = ? AND Age = ?', (self.name, self.family, self.city, self.age))
        existing_customer = cursor.fetchone()
        cursor.close()
        conn.close()
        return existing_customer is not None

    def delete(self):
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM Customers WHERE Name = ? AND Family = ? AND City = ? AND Age = ?', (self.name, self.family, self.city, self.age))

        conn.commit()
        conn.close()

   

class Loan:
    def __init__(self, cust_id, book_id, loan_date, return_date):
        self.cust_id = cust_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.return_date = return_date

    def save(self):
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO Loans (CustID, BookID, LoanDate, ReturnDate)
            VALUES (?, ?, ?, ?)
        ''', (self.cust_id, self.book_id, self.loan_date, self.return_date))

        conn.commit()
        conn.close()
