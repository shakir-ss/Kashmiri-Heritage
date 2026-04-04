import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db, User

app = create_app('dev')

def create_admin_user():
    with app.app_context():
        print("Ensuring tables exist...")
        db.create_all()
        print("Registering root admin user...")
        # Check if user already exists
        email = "root@thehundredvillages.com"
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"User with email {email} already exists.")
            return

        try:
            admin_user = User(
                name="Root Admin",
                email=email,
                role="admin"
            )
            admin_user.set_password("root123")
            db.session.add(admin_user)
            db.session.commit()
            print(f"Admin user registered successfully! Email: {email}, Password: root123")
        except Exception as e:
            print(f"Error registering admin user: {e}")

if __name__ == "__main__":
    create_admin_user()
