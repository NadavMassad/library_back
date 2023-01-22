# This repo is the server side of the Library project.

The first thing we do is create a virtual environment.
If we don't have it install on our pc, we need to install it.
Make sure you are in the prject directory in the terminal.
Use the terminal and write this command:
`python -m pip install --user virtualenv `

To create it write in the terminal this:
`python -m virtualenv env`

To activate write this:
`env\Scripts\activate`

Than you need to install the requirements
use the cmd and write:
`pip install -r requirements.txt`

We import the json package to let us read/write to/from the database
The datetime import (date function) is used to create date objects
Next we import flask packages:
1. the first one, `from flask import Flask, request`,
 is used to initiate the flask app,
 and to let us use diffrent methods on the browser(GET, POST, DELETE, PUT)
2. The second one, `from flask_cors import CORS`, is used to 
give us permission to use the methods(GET, POST, DELETE, PUT) we want besides the default, which is GET.
3. the last one,`from flask_sqlalchemy import SQLAlchemy`, is used to create database,
 and enables us to communicate with the database.


Next comes the we initialize the app, the db and use CORS on the app:

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)


Next we create class for every table we want in the db, and we enherite it from the db.Model object.

The Books table has 6 columns:
1. id - The id of the book (PK).
2. name - The name of the book.
3. author - The name of the author.
4. year_published - The year the book was published.
5. book_type - The type of the book - how lpng it can be loaned.
6. is_active - True/False - determines if the book can be loaned or not.

The Customers table has 5 columns:
1. id - The id of the customer (PK).
2. name - The name of the customer.
3. city - The city of the customer.
4. age - The age og the customer.
5. is_active - True/False - determines if the customer is active or not.

The Loans table has 6 columns:
1. id - The id of the loan (PK).
2. customer_id - The id of the customer(The loaner). FK from the customers table.
3. book_id - The id of the book(The loaned book). FK from the books table.
4. loan_date - The date the book was loaned.
5. return_date - The date the book was retruned.
6. status - Determines the status of the loan - Returned on time/late/ wasn't returned yet.

The next step is to create end-point(URL) for every page, one for each object(each table).
In the Books end-point we have 4 options(methods):
1. GET (read) - Display all the books objects.
2. POST (create) - Create a new book record.
3. DELETE (delete) - It doesn't realy deletes the book, but it deactivates him. We'd never want to delete an record from the db, because it ma effect many tables.
4. PUT (update) - It activates unactive books.
A book that is unactive is not available to be loaned.

Same goes to the Customers table:
1. GET (read) - Display all the customers objects.
2. POST (create) - Create a new customer record.
3. DELETE (delete) - Deactivate customers.
4. PUT (update) - Activates a customer.

And same for the loans table:
1. GET (read) - Display all the loans objects.
2. POST (create) - Create a new customer loan record. 
3. DELETE (delete) - It doesn't realy exists, because we don't want to delete any loan.
4. PUT (update) - It updates the return date fron `Null` to the current date.
It also updates the status of the loan. depending on the `day_delta` - the difference between the `loan_date` and the `return_date`. 


The next end-point it the home page(index.html).
it does't do anything, but it exists so we have a home page


The last part of this script is the entry-point:
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)

the first part makes sure that we are in the app context,
so we can access the database.
the last part enables us to make changes in the code,
without having to stop and run the program to save them.
in the instance folder we have the database.
