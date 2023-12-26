# BookXChange Application

BookXChange is a platform dedicated to facilitating the exchange of books among users. Users can explore, list, and manage their book collections with a focus on sharing and trading books with others.

## Functionalities

### 1. Home Page
- **Route:** `/`
- **Description:** Displays a list of the latest 50 books ordered by publication date.

### 2. User Registration
- **Route:** `/signup`
- **Description:** Allows users to create a new account by providing a username, email, and password.

### 3. User Login
- **Route:** `/login`
- **Description:** Allows users to log in using their username and password.

### 4. User Logout
- **Route:** `/logout`
- **Description:** Logs out the currently authenticated user.

### 5. Book Listing
- **Route:** `/list_book`
- **Description:** Allows authenticated users to list new books by providing details such as title, author, description, state, rating, number of pages, publication date, and publisher.

### 6. Book Details
- **Route:** `/book/<book_name>`
- **Description:** Displays detailed information about a specific book identified by its title.

### 7. Add to My Books
- **Route:** `/add_to_my_books/<int:book_id>`
- **Description:** Allows authenticated users to add a specific book to their collection.

### 8. My Books
- **Route:** `/my_books`
- **Description:** Displays a list of books in the user's collection, emphasizing books available for exchange.

### 9. Remove Book
- **Route:** `/remove_book/<int:book_id>`
- **Description:** Allows authenticated users to remove a specific book from their collection.

## Technologies Used
- Flask
- SQLite
- Bootstrap
- Jinja templating
- Werkzeug (for password hashing)

## Getting Started
1. Clone the repository.
2. Install the required dependencies: `pip install -r requirements.txt`.
3. Run the application: `python app.py`.
4. Access the application in your web browser at `http://localhost:5000`.

## Contributing
Contributions are welcome! Please follow the contribution guidelines in the `CONTRIBUTING.md` file.

## License
This project is licensed under the MIT License - see the `LICENSE.md` file for details.
