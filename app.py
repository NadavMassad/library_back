import json
from datetime import date
from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


"""
This module is the server for the library website.
We use flask fraework to use python and sqlalchemy as our db.
The CORS is used to let us use diffent methods in the browser.
Every Class in this file Defines a table (check in the class doc).
We have app.route to every page in the website (check desc in the route doc).
"""


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)

# The model of the Books table in the db
class Books(db.Model):
    """
    This class defines the Books table in the sqlite db.
    this table has 6 columns:
    1. id - The id of the book (PK).
    2. name - The name of the book.
    3. author - The name of the author.
    4. year_published - The year the book was published.
    5. book_type - The type of the book - how lpng it can be loaned.
    6. is_active - True/False - determines if the book can be loaned or not.
    """
    id = db.Column('book_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(50))
    year_published = db.Column(db.Integer)
    book_type = db.Column(db.Integer)
    is_active = db.Column(db.String(10))
    loaned = db.relationship('Loans', backref='book')

    def __init__(self, name, author, year_published, book_type, is_active='true'):
        self.name = name
        self.author = author
        self.year_published = year_published
        self.book_type = book_type
        self.is_active = is_active

# The model of the Customers table in the db
class Customers(db.Model):
    """
    This class defines the Customers table in the sqlite db.
    This table has 5 columns:
    1. id - The id of the customer (PK).
    2. name - The name of the customer.
    3. city - The city of the customer.
    4. age - The age og the customer.
    5. is_active - True/False - determines if the customer is active or not.
    """
    id = db.Column('customer_id', db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    age = db.Column(db.Integer)
    is_active = db.Column(db.String(10))
    loans = db.relationship('Loans', backref='customer')

    def __init__(self, name, city, age, is_active='true'):
        self.name = name
        self.city = city
        self.age = age
        self.is_active = is_active

# The model of the Loans table in the db
class Loans(db.Model):
    """
    This class defines the Loans table in the sqlite db.
    This table has 6 columns:
    1. id - The id of the loan (PK).
    2. customer_id - The id of the customer(The loaner). FK from the customers table.
    3. book_id - The id of the book(The loaned book). FK from the books table.
    4. loan_date - The date the book was loaned.
    5. return_date - The date the book was retruned.
    6. status - Determines the status of the loan - Returned on time/late/ wasn't returned yet.
    """
    loan_id = db.Column('loan_id', db.Integer, primary_key = True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    loan_date = db.Column(db.Date)
    return_date = db.Column(db.String(50))
    status = db.Column(db.String(50))

    def __init__(self, customer, book, loan_date, return_date, status):
        self.customer_id = customer
        self.book_id = book
        self.loan_date = loan_date
        self.return_date = return_date
        self.status = status

# The end point for the books actions
@app.route('/books/<book_id>', methods = ['GET', 'POST', 'DELETE', 'PUT'])
@app.route('/books/', methods = ['GET', 'POST', 'DELETE', 'PUT'])
def books_crud(book_id=-1):
    """
    The route for the books page
    """
    if request.method == "GET":
        # Display all books
        res = []
        for book in Books.query.all():
            res.append({'id': book.id,
                        'name': book.name,
                        'author': book.author,
                        'year_published': book.year_published,
                        "book_type": book.book_type,
                        'is_active': book.is_active})
        return json.dumps(res)
    if request.method == "POST":
        # Add new book
        request_data = request.get_json()
        name = request_data['name']
        author = request_data['author']
        year_published = request_data['year_published']
        book_type = request_data['book_type']
        new_book = Books(name, author, year_published, book_type, is_active='true')
        db.session.add(new_book)
        db.session.commit()
        return 'New Book Was Added'
    if request.method == "DELETE":
        # Remove book
        del_book = Books.query.get(book_id)
        del_book.is_active = 'false'
        db.session.commit()
        return 'Book Removed'
    if request.method == "PUT":
        update_book = Books.query.get(book_id)
        is_active = request.json['is_active']
        update_book.is_active = is_active
        db.session.commit()
        return 'A Book Was Activated'

# The end point for the customers actions
@app.route('/customers/<customer_id>', methods = ['GET', 'POST', 'DELETE', 'PUT'])
@app.route('/customers/', methods = ['GET', 'POST', 'DELETE', 'PUT'])
def customers_crud(customer_id=-1):
    """
    The route for the customers page.
    """
    if request.method == "GET":
        # Display the customers
        res = []
        for customer in Customers.query.all():
            res.append({'id': customer.id,
                        'name': customer.name,
                        'city': customer.city,
                        'age': customer.age,
                        'is_active': customer.is_active})
        return json.dumps(res)
    if request.method == "POST":
        # Add new customer
        request_data = request.get_json()
        name = request_data['name']
        city = request_data['city']
        age = request_data['age']
        new_customer = Customers(name, city, age, is_active='true')
        db.session.add(new_customer)
        db.session.commit()
        return 'New Customer Was Added'
    if request.method == "DELETE":
        # Remove customer
        del_customer = Customers.query.get(customer_id)
        del_customer.is_active = "false"
        db.session.commit()
        return 'Customer Removed'
    if request.method == "PUT":
        update_customer = Customers.query.get(customer_id)
        is_active = request.json['is_active']
        update_customer.is_active = is_active
        db.session.commit()
        return 'A Customer Has Returned'

def get_difference(date1, date2):
    """ Deals with days difference
    date1 - The day the book was loaned
    date2 - The day the book was retured
     """
    delta = date2 - date1
    return delta.days

# The end point for the loans actions
@app.route('/loans/<loan_id>', methods = ['GET', 'POST', 'DELETE', 'PUT'])
@app.route('/loans/', methods = ['GET', 'POST', 'DELETE', 'PUT'])
def loans_crud(loan_id=-1):
    """
    The route for the loans page.
    """
    if request.method == "GET":
        # Display all loans
        res = []
        customer_list=[]
        book_list = []
        # Create list of customers object, to access the customer's name by id
        for customer in Customers.query.all():
            customer_list.append({'id': customer.id,
                                  'name': customer.name,
                                  'city': customer.city,
                                  'age': customer.age})
        # Create list of books object, to access the book's name by id
        for book in Books.query.all():
            book_list.append({'id': book.id,
                              'name': book.name,
                              'author': book.author,
                              'year_published': book.year_published,
                              'book_type': book.book_type})
        # Get the loans with the book_name and customer_name by the id of them in their tables.
        for loan in Loans.query.all():
            customer_name = ""
            book_name = ""
            book_type = 0
            for customer in customer_list:
                if loan.customer_id == customer['id']:
                    customer_name = customer['name']
            for book in book_list:
                if loan.book_id == book['id']:
                    book_name = book['name']
                    book_type = book['book_type']

            res.append({'id': loan.loan_id,
                        'customer_name': customer_name,
                        'book_name': book_name,
                        'book_type': book_type,
                        'loan_date': str(loan.loan_date),
                        'return_date': loan.return_date,
                        'status': loan.status})
        return json.dumps(res)
    if request.method == "POST":
        # Loan a book
        request_data = request.get_json()
        customer_list=[]
        book_list = []

        # Create list of customers object, to access the customer's name by id
        for customer in Customers.query.all():
            customer_list.append({'id': customer.id,
                                  'name': customer.name,
                                  'city': customer.city,
                                  'age': customer.age})
        # Create list of books object, to access the book's name by id
        for book in Books.query.all():
            book_list.append({'id': book.id,
                              'name': book.name,
                              'author': book.author,
                              'year_published': book.year_published,
                              'book_type': book.book_type})

        for customer in customer_list:
            if request_data["customer_name"] == customer['name']:
                customer_id = customer['id']

        for book in book_list:
            if request_data["book_name"] == book['name']:
                book_id = book['id']

        loan_date = date.today()
        new_loan = Loans(customer_id, book_id, loan_date, return_date="Null", status="Pending")
        db.session.add(new_loan)
        db.session.commit()
        return 'Book Was Loaned'
    if request.method == "DELETE":
        pass
    if request.method == "PUT":
        # Return a book
        # Edit the row because when he loaned it, he didn't have the return date yet.
        update_loan = Loans.query.get(loan_id)
        return_date = date.today()

        day_delta = get_difference(update_loan.loan_date, return_date)
        if Books.query.get(update_loan.book_id).book_type == 1:
            if day_delta > 10:
                update_loan.status = "Late"
            else:
                update_loan.status = "onTime"
        elif Books.query.get(update_loan.book_id).book_type == 2:
            if day_delta > 5:
                update_loan.status = "Late"
            else:
                update_loan.status = "onTime"
        elif Books.query.get(update_loan.book_id).book_type == 3:
            if day_delta > 2:
                update_loan.status = "Late"
            else:
                update_loan.status = "onTime"

        update_loan.return_date = return_date
        db.session.commit()
        return 'A Book Was Returned'

@app.route('/')
def hello():
    """
    The route for the home page (index.html)
    """
    return "Home Page"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)
