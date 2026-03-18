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
        
        try:
            # Create product_images table
            db.session.execute(db.text("""
                CREATE TABLE IF NOT EXISTS product_images (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id INT,
                    image_url VARCHAR(255) NOT NULL,
                    is_primary BOOLEAN DEFAULT FALSE,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
                )
            """))
            print("Created 'product_images' table.")
        except Exception as e:
            print(f"Error creating 'product_images' table: {e}")
        
        try:
            # Check if order columns exist
            cols = db.session.execute(db.text("SHOW COLUMNS FROM orders")).fetchall()
            col_names = [c[0] for c in cols]
            
            if 'prepaid_amount' not in col_names:
                db.session.execute(db.text("ALTER TABLE orders ADD COLUMN prepaid_amount FLOAT DEFAULT 0.0"))
                print("Added 'prepaid_amount' column.")
            
            if 'balance_on_delivery' not in col_names:
                db.session.execute(db.text("ALTER TABLE orders ADD COLUMN balance_on_delivery FLOAT DEFAULT 0.0"))
                print("Added 'balance_on_delivery' column.")

            if 'city' not in col_names:
                db.session.execute(db.text("ALTER TABLE orders ADD COLUMN city VARCHAR(100)"))
                print("Added 'city' column.")

            if 'state' not in col_names:
                db.session.execute(db.text("ALTER TABLE orders ADD COLUMN state VARCHAR(100)"))
                print("Added 'state' column.")

            if 'country' not in col_names:
                db.session.execute(db.text("ALTER TABLE orders ADD COLUMN country VARCHAR(100) DEFAULT 'India'"))
                print("Added 'country' column.")

            if 'pincode' not in col_names:
                db.session.execute(db.text("ALTER TABLE orders ADD COLUMN pincode VARCHAR(20)"))
                print("Added 'pincode' column.")
                
        except Exception as e:
            print(f"Error updating 'orders' table: {e}")

        try:
            # Check if columns exist first
            cols = db.session.execute(db.text("SHOW COLUMNS FROM products")).fetchall()
            col_names = [c[0] for c in cols]
            
            if 'weight_grams' not in col_names:
                db.session.execute(db.text("ALTER TABLE products ADD COLUMN weight_grams INT DEFAULT 0"))
                print("Added 'weight_grams' column.")
            
            if 'attributes' not in col_names:
                db.session.execute(db.text("ALTER TABLE products ADD COLUMN attributes JSON"))
                print("Added 'attributes' column.")
                
        except Exception as e:
            print(f"Error updating 'products' table: {e}")

        try:
            # Create product_variants table
            db.session.execute(db.text("""
                CREATE TABLE IF NOT EXISTS product_variants (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    product_id INT,
                    name VARCHAR(50) NOT NULL,
                    price_modifier FLOAT DEFAULT 0.0,
                    stock INT DEFAULT 0,
                    sku VARCHAR(50) UNIQUE,
                    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
                )
            """))
            print("Created 'product_variants' table.")
        except Exception as e:
            print(f"Error creating 'product_variants' table: {e}")

        try:
            # Create contact_inquiries table
            db.session.execute(db.text("""
                CREATE TABLE IF NOT EXISTS contact_inquiries (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(120) NOT NULL,
                    phone VARCHAR(20),
                    subject VARCHAR(200),
                    message TEXT NOT NULL,
                    status VARCHAR(20) DEFAULT 'pending',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """))
            print("Created 'contact_inquiries' table.")
        except Exception as e:
            print(f"Error creating 'contact_inquiries' table: {e}")
        
        db.session.commit()
        print("Schema update complete.")

if __name__ == "__main__":
    update_schema()
