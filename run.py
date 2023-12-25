from app import create_app
import secrets

# Create the Flask application
app = create_app()

# Set the secret key for session management
app.secret_key = secrets.token_hex(16)

if __name__ == '__main__':
    # Run the application
    app.run(debug=True)