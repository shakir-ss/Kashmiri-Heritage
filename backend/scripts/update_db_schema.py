import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db

app = create_app('dev')

def update_schema():
    with app.app_context():
        print("Updating database schema...")
        try:
            # Add details column to products
            db.session.execute(db.text("ALTER TABLE products ADD COLUMN details TEXT AFTER created_at"))
            print("Added 'details' column to 'products' table.")
        except Exception as e:
            print(f"Note: Could not add 'details' column (it might already exist): {e}")

        try:
            # Create wishlist_items table
            db.session.execute(db.text("""
                CREATE TABLE IF NOT EXISTS wishlist_items (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    product_id INT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )
            """))
            print("Created 'wishlist_items' table.")
        except Exception as e:
            print(f"Error creating 'wishlist_items' table: {e}")
        
        db.session.commit()
        print("Schema update complete.")

if __name__ == "__main__":
    update_schema()
