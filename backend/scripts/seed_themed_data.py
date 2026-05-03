import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db, Category, Product, Analytics, CartItem, OrderItem, WishlistItem, ProductVariant, ProductImage

# Always use prod config to ensure it connects to the right DB if DATABASE_URL is set
app = create_app(os.environ.get('FLASK_CONFIG', 'prod'))

def seed():
    with app.app_context():
        print(f"Connecting to database... (FLASK_CONFIG={os.environ.get('FLASK_CONFIG')})")
        print("Ensuring all tables exist (including new Phase 5 tables)...")
        db.create_all()
        
        print("Cleaning up old catalog data...")
        try:
            # Note: We do NOT delete Users or Orders to protect user accounts,
            # but deleting Products might fail if they are tied to existing orders.
            Analytics.query.delete()
            CartItem.query.delete()
            OrderItem.query.delete()
            WishlistItem.query.delete()
            ProductVariant.query.delete()
            ProductImage.query.delete()
            Product.query.delete()
            Category.query.delete()
            db.session.commit()
            print("Old catalog data cleared.")
        except Exception as e:
            db.session.rollback()
            print(f"Cleanup skipped or failed (likely due to existing orders): {e}")

        print("Adding Minimal Production Category...")
        cat_organic = Category(
            name="Kashmiri Heritage", 
            slug="kashmiri-heritage", 
            description="Pure, raw, and artisanal treasures from the pristine high-altitude farms of the Kashmir Valley."
        )
        db.session.add(cat_organic)
        db.session.commit()

        print("Adding Minimal Production Product with 3D AR Attributes...")
        
        saffron = Product(
            category_id=cat_organic.id,
            name="Royal Pampore Saffron (Grade A++ Mongra)",
            slug="pure-kashmiri-saffron",
            price=500,
            stock=100,
            weight_grams=1,
            description="The world's rarest 'Red Gold', hand-picked in the historic fields of Pampore.",
            details="""In the historic fields of Pampore, the earth breathes a scent of ancient gold. Our saffron is the 'Mongra' 
            grade—consisting only of the deepest red tips of the Crocus sativus, hand-plucked at dawn. It takes 
            75,000 flowers to produce just one pound of this spice. Each strand is a concentrated burst of 
            sun-drenched flavor, powerful antioxidants, and a mesmerizing aroma that defines Kashmiri royalty.""",
            attributes={
                "3d_model_url": "https://modelviewer.dev/shared-assets/models/Astronaut.glb", # Placeholder 3D model
                "origin": "Pampore, Kashmir",
                "grade": "A++ Mongra"
            }
        )
        db.session.add(saffron)
        db.session.flush()

        db.session.add(ProductVariant(
            product_id=saffron.id,
            name="1g Premium Box",
            price_modifier=0,
            stock=50,
            sku="SAFFRON-1G"
        ))
        
        db.session.add(ProductVariant(
            product_id=saffron.id,
            name="5g Family Box",
            price_modifier=2000,
            stock=20,
            sku="SAFFRON-5G"
        ))

        db.session.commit()
        print("Database successfully seeded with minimal data!")

if __name__ == "__main__":
    seed()
