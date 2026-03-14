import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db

app = create_app('dev')

with app.app_context():
    print("Initializing Database...")
    try:
        db.create_all()
        print("All tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
        print("\nMake sure your MySQL server is running and the database 'kashmiri_dry_fruits' exists.")
        print("You can run the SQL script in backend/scripts/setup_db.sql manually.")
