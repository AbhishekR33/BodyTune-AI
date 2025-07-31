from app import app
from utils.database import init_db

if __name__ == '__main__':
    with app.app_context():
        init_db(app)
        print("Database initialized successfully!")
        print("You can now run the application with: python app.py")
