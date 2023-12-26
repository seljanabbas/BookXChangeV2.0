from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

from .helpers import apology, login_required, lookup, usd


main_bp = Blueprint('main', __name__)

# SQLite database file
database_file = 'books.db'
user_database_file = 'users.db'

# Configure session to use filesystem (you can choose other options)
main_bp.config = {}
main_bp.config['SESSION_PERMANENT'] = False
main_bp.config['SESSION_TYPE'] = 'filesystem'
Session(main_bp)

@main_bp.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@main_bp.route('/')
def index():
    if request.method == 'GET':
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                title,
                authors,
                average_rating
            FROM books
            ORDER BY publication_date DESC LIMIT 50
        ''')
        
        books = cursor.fetchall()

        conn.close()

        return render_template('index.html', books=books)
    

@main_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form.get('first_name')
        email = request.form.get('email')
        password = request.form.get('pwd')
        password_confirm = request.form.get('pwd-2')

        # Validate form data (add your validation logic)
        if not username:
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        if password != password_confirm:
            return apology("passwords do not match", 400)

        # Connect to the database and create a cursor
        conn = sqlite3.connect(user_database_file)
        db = conn.cursor()

        # Query database for username
        user_rows = db.execute("SELECT * FROM users WHERE username = ?", (username,))

        # Ensure username does not exist
        if len(list(user_rows)):
            return apology("username in use, please select another", 400)

        # Generate hashed password and insert the new user
        hash_password = generate_password_hash(
            password, method="pbkdf2:sha256", salt_length=8
        )
        db.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", (username, email, hash_password)
        )

        # Commit changes and close the connection
        conn.commit()
        conn.close()

        # Remember which user has logged in and redirect to home page
        # Query database for username
        conn = sqlite3.connect(user_database_file)
        db = conn.cursor()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (request.form.get("first_name"),)
        ).fetchone()

        session["user_id"] = user[0]

        return apology("Registered successfully", 200)
    else:
        return render_template("signup.html")



@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('pwd')

        # Connect to the SQLite users database
        conn = sqlite3.connect(user_database_file)
        cursor = conn.cursor()

        # Retrieve user information based on the provided username
        cursor.execute('''
            SELECT id, username, password_hash FROM users WHERE username = ?
        ''', (username,))

        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            # If the username and password are correct, set up the user session
            session['user_id'] = user[0]
            flash('Login successful!', 'success')
            # Close the database connection
            conn.close()
            return redirect(url_for('main.index'))
        else:
            # Close the database connection
            conn.close()
            # Flash an error message if login fails
            return apology('Login not successful', 400)


    return render_template('login.html')

@main_bp.route('/logout')
@login_required
def logout():
    # Clear the user session
    session.clear()
    flash('Logout successful!', 'success')
    return redirect(url_for('main.index'))

def get_book_info(book_name):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT
            book_id,
            title,
            authors,
            average_rating,
            language_code,
            num_pages,
            ratings_count,
            publication_date,
            publisher
        FROM books
        WHERE title = ?
    ''', (book_name,))

    detailed_book_info = cursor.fetchone()

    conn.close()

    return detailed_book_info

@main_bp.route('/list_book', methods=['GET', 'POST'])
@login_required
def list_book():
    # Handle listing books logic
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        description = request.form.get('description')
        state = request.form.get('state')
        rating = request.form.get('rating')
        num_pages = request.form.get('num_pages')
        publication_date = request.form.get('publication_date')
        publisher = request.form.get('publisher')

        if not title:
            return apology('please enter a valid title', 400)
        elif not author:
            return apology('please enter a valid author(s)', 400)
        
        conn = sqlite3.connect(database_file)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO books (title, authors, average_rating, language_code, num_pages, ratings_count, publication_date, publisher)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, author, rating, 'en', num_pages, 1, publication_date, publisher))
        
        conn.commit()
        conn.close()
        
        book = get_book_info(title)
        return render_template('book_details.html', book=book)

    else:
        return render_template('listbook.html')
        

@main_bp.route('/book/<book_name>', methods=['GET'])
def book_details(book_name):
    # Fetch detailed book information
    print(book_name)
    book = get_book_info(book_name)

    if book:
        return render_template('book_details.html', book=book)
    else:
        # Handle the case where the book is not found
        return render_template('error.html', message='Book not found'), 404

@main_bp.route('/add_to_my_books/<int:book_id>', methods=['POST'])
@login_required
def add_to_my_books(book_id):
    if request.method == 'POST':
        # Get the user_id from the session
        user_id = session['user_id']

        # Connect to the SQLite users database
        conn = sqlite3.connect(user_database_file)
        cursor = conn.cursor()

        # Add the book to the user's collection
        cursor.execute("INSERT INTO user_books (user_id, book_id) VALUES (?, ?)", (user_id, book_id))
        conn.commit()
        flash('Book added to your collection successfully', 'success')

        # Close the database connection
        conn.close()

        return redirect(url_for('main.my_books'))

@main_bp.route('/my_books', methods=['GET'])
@login_required
def my_books():
    # Get the user_id from the session
    user_id = session['user_id']

    # Connect to the SQLite users database
    conn_users = sqlite3.connect(user_database_file)
    cursor_users = conn_users.cursor()

    # Fetch book IDs for the user
    cursor_users.execute('''
        SELECT book_id FROM user_books WHERE user_id = ?
    ''', (user_id,))

    book_ids = cursor_users.fetchall()

    # Close the connection to the users database
    conn_users.close()

    # Connect to the SQLite books database
    conn_books = sqlite3.connect(database_file)
    cursor_books = conn_books.cursor()

    # Fetch book details based on book IDs
    user_books = []
    for book_id in book_ids:
        cursor_books.execute('''
            SELECT book_id, title, authors, average_rating, language_code, num_pages, ratings_count, publication_date, publisher
            FROM books
            WHERE book_id = ?
        ''', (book_id[0],))
        book_details = cursor_books.fetchone()
        user_books.append(book_details)

    # Close the connection to the books database
    conn_books.close()    
    return render_template('mybooks.html', user_books=user_books)

@main_bp.route('/remove_book/<int:book_id>', methods=['POST'])
@login_required
def remove_book(book_id):
    # Get the user_id from the session
    user_id = session['user_id']

    # Connect to the SQLite users database
    conn = sqlite3.connect(user_database_file)
    cursor = conn.cursor()

    # Remove the book from the user's books
    cursor.execute("DELETE FROM user_books WHERE user_id = ? AND book_id = ?", (user_id, book_id))
    conn.commit()
    flash('Book removed from your collection successfully', 'success')

    # Close the database connection
    conn.close()

    return redirect(url_for('main.my_books'))
