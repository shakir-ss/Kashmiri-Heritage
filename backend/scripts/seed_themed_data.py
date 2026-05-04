"""
seed_themed_data.py
===================
Minimal production seed script for The Hundred Villages.

What this script does:
  1. Applies any missing schema changes (new columns on existing tables).
     db.create_all() handles new tables automatically.
  2. Clears OLD catalog data (categories, products, etc.) safely.
     It does NOT delete users, orders, reviews, b2b_inquiries, or carts.
  3. Seeds a fresh, minimal production catalog.

Run command (same as before):
    cd backend
    $env:DATABASE_URL = "mysql+pymysql://USER:PASS@HOST:PORT/DBNAME"
    $env:FLASK_CONFIG  = "prod"
    .\\venv\\Scripts\\python scripts/seed_themed_data.py
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import (
    db, Category, Product, Analytics, CartItem, OrderItem,
    WishlistItem, ProductVariant, ProductImage
)

# Always use prod config to ensure it connects to the right DB if DATABASE_URL is set
app = create_app(os.environ.get('FLASK_CONFIG', 'prod'))

# ---------------------------------------------------------------------------
# Columns that may be missing on pre-existing cloud tables.
# Each entry: (table_name, column_name, column_definition)
# Safe to run multiple times -- skips if the column already exists.
# ---------------------------------------------------------------------------
SCHEMA_MIGRATIONS = [
    ("categories", "image_url",      "VARCHAR(255) NULL"),
    ("orders",     "tracking_link",  "VARCHAR(500) NULL"),
    ("orders",     "tracking_number","VARCHAR(100) NULL"),
]


def apply_schema_migrations():
    """Add any missing columns to existing tables without touching data."""
    print("Applying schema migrations (new columns)...")
    with db.engine.connect() as conn:
        for table, column, definition in SCHEMA_MIGRATIONS:
            result = conn.execute(db.text(
                "SELECT COUNT(*) FROM information_schema.COLUMNS "
                "WHERE TABLE_SCHEMA = DATABASE() "
                "AND TABLE_NAME = :t AND COLUMN_NAME = :c"
            ), {"t": table, "c": column})
            exists = result.scalar() > 0

            if exists:
                print(f"  [SKIP]  {table}.{column} already exists")
            else:
                conn.execute(db.text(
                    f"ALTER TABLE `{table}` ADD COLUMN `{column}` {definition}"
                ))
                conn.commit()
                print(f"  [ADDED] {table}.{column}")
    print("Schema migrations complete.\n")


def seed():
    with app.app_context():
        print(f"Connecting to database... (FLASK_CONFIG={os.environ.get('FLASK_CONFIG', 'prod')})")

        # ── Step 1: Schema migrations (new columns on existing tables) ────────
        apply_schema_migrations()

        # ── Step 2: New tables (created automatically if missing) ─────────────
        print("Ensuring all tables exist...")
        db.create_all()
        print("Tables verified.\n")

        # -- Step 3: Clear old catalog data safely ----------------------------
        print("Clearing old catalog data...")
        try:
            # Disable FK checks so we can clean in any order
            db.session.execute(db.text("SET FOREIGN_KEY_CHECKS = 0"))
            Analytics.query.delete()
            CartItem.query.delete()
            WishlistItem.query.delete()
            ProductVariant.query.delete()
            ProductImage.query.delete()
            # Only delete order_items and products if no live orders exist;
            # we keep orders intact to protect customer history
            OrderItem.query.delete()
            Product.query.delete()
            Category.query.delete()
            db.session.execute(db.text("SET FOREIGN_KEY_CHECKS = 1"))
            db.session.commit()
            print("Old catalog data cleared.\n")
        except Exception as e:
            db.session.rollback()
            db.session.execute(db.text("SET FOREIGN_KEY_CHECKS = 1"))
            db.session.commit()
            print(f"Cleanup skipped or partial: {e}\n")

        # -- Step 4: Seed fresh categories WITH images ------------------------
        print("Seeding categories...")

        cat_dry_fruits = Category(
            name="Premium Dry Fruits",
            slug="premium-dry-fruits",
            description="Hand-picked, sun-dried, and packed from the orchards of Kashmir Valley.",
            image_url="https://images.unsplash.com/photo-1608797178974-15b35a64ede9?w=300&q=80"
        )
        cat_saffron = Category(
            name="Kashmiri Saffron",
            slug="kashmiri-saffron",
            description="The world's finest saffron, grade A++ Mongra, hand-plucked at dawn in Pampore.",
            image_url="https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=300&q=80"
        )
        cat_spices = Category(
            name="Exotic Spices",
            slug="exotic-spices",
            description="Aromatic spices sourced from the pristine high-altitude farms of Jammu & Kashmir.",
            image_url="https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=300&q=80"
        )
        cat_handicrafts = Category(
            name="Artisan Handicrafts",
            slug="artisan-handicrafts",
            description="Handcrafted Kashmiri treasures — Pashminas, Papier Mache, and hand-knotted rugs.",
            image_url="https://images.unsplash.com/photo-1590422749897-47036da0b0ff?w=300&q=80"
        )

        db.session.add_all([cat_dry_fruits, cat_saffron, cat_spices, cat_handicrafts])
        db.session.commit()
        print(f"  Added {Category.query.count()} categories.\n")

        # ── Step 5: Seed products ─────────────────────────────────────────────
        print("Seeding products...")

        products = [
            # ── Dry Fruits ────────────────────────────────────────────────────
            Product(
                category_id=cat_dry_fruits.id,
                name="Royal Kashmiri Walnuts (Kagzi)",
                slug="kashmiri-walnuts-kagzi",
                price=899,
                discount_price=749,
                stock=200,
                weight_grams=500,
                image_url="https://images.unsplash.com/photo-1608797178974-15b35a64ede9?w=600&q=80",
                description="Paper-thin shell Kagzi walnuts from the ancient walnut groves of Achabal.",
                details="Rich in Omega-3, antioxidants, and heart-healthy fats. Cold-pressed quality, never irradiated.",
                attributes={"origin": "Achabal, Kashmir", "grade": "Kagzi Extra Light", "shelf_life": "12 months"}
            ),
            Product(
                category_id=cat_dry_fruits.id,
                name="Wild Himalayan Almonds (Mamra)",
                slug="kashmiri-mamra-almonds",
                price=1199,
                discount_price=999,
                stock=150,
                weight_grams=500,
                image_url="https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=600&q=80",
                description="Wild-foraged Mamra almonds — the crown jewel of Kashmiri dry fruits.",
                details="Unlike commercial almonds, Mamra are small, high-oil, and packed with nutrients. Air-dried naturally.",
                attributes={"origin": "Gurez Valley, Kashmir", "type": "Wild Mamra", "shelf_life": "18 months"}
            ),
            Product(
                category_id=cat_dry_fruits.id,
                name="Sun-Dried Apricots (Khumani)",
                slug="kashmiri-dried-apricots",
                price=549,
                discount_price=449,
                stock=300,
                weight_grams=500,
                image_url="https://images.unsplash.com/photo-1597714026720-8f74c62310ba?w=600&q=80",
                description="Naturally sun-dried apricots from the terraced orchards of Kargil.",
                details="No sulphites, no artificial colors. Just pure, sweet, tangy Khumani dried under Himalayan sun.",
                attributes={"origin": "Kargil, Ladakh", "type": "Wild Organic", "shelf_life": "12 months"}
            ),

            # ── Saffron ───────────────────────────────────────────────────────
            Product(
                category_id=cat_saffron.id,
                name="Royal Pampore Saffron (Grade A++ Mongra)",
                slug="pure-kashmiri-saffron",
                price=500,
                discount_price=None,
                stock=100,
                weight_grams=1,
                image_url="https://images.unsplash.com/photo-1600880292203-757bb62b4baf?w=600&q=80",
                description="The world's rarest 'Red Gold', hand-picked in the historic fields of Pampore.",
                details=("In the historic fields of Pampore, the earth breathes a scent of ancient gold. "
                         "Our saffron is the 'Mongra' grade — consisting only of the deepest red tips, "
                         "hand-plucked at dawn. It takes 75,000 flowers to produce just one pound."),
                attributes={
                    "origin": "Pampore, Kashmir",
                    "grade": "A++ Mongra",
                    "iso_certified": True,
                    "3d_model_url": "https://modelviewer.dev/shared-assets/models/Astronaut.glb"
                }
            ),

            # ── Spices ────────────────────────────────────────────────────────
            Product(
                category_id=cat_spices.id,
                name="Kashmiri Mirch (Sun-Dried Chilli)",
                slug="kashmiri-mirch-dried-chilli",
                price=349,
                discount_price=299,
                stock=250,
                weight_grams=250,
                image_url="https://images.unsplash.com/photo-1596040033229-a9821ebd058d?w=600&q=80",
                description="Vibrant red, mildly hot Kashmiri chilli — the secret behind the iconic Rogan Josh colour.",
                details="Naturally dried under the Himalayan sun. No artificial dyes. Adds vivid color with mild heat.",
                attributes={"origin": "Pulwama, Kashmir", "scoville": "1000-2000 SHU", "shelf_life": "24 months"}
            ),

            # ── Handicrafts ───────────────────────────────────────────────────
            Product(
                category_id=cat_handicrafts.id,
                name="Pure Pashmina Shawl (Hand-Embroidered)",
                slug="pure-pashmina-shawl-hand-embroidered",
                price=12999,
                discount_price=10999,
                stock=20,
                weight_grams=200,
                image_url="https://images.unsplash.com/photo-1590422749897-47036da0b0ff?w=600&q=80",
                description="Handwoven from the finest Changthangi goat fleece, embroidered by master craftsmen.",
                details=("True Pashmina — 100% pure Changthangi goat wool from Ladakh. "
                         "Each shawl takes 3-6 months to complete. GI-tagged product of Jammu & Kashmir."),
                attributes={
                    "origin": "Srinagar, Kashmir",
                    "fiber": "100% Changthangi Pashmina",
                    "technique": "Sozni Hand Embroidery",
                    "gi_tag": True
                }
            ),
        ]

        db.session.add_all(products)
        db.session.flush()

        # ── Variants for Saffron ───────────────────────────────────────────────
        saffron = next(p for p in products if p.slug == "pure-kashmiri-saffron")
        db.session.add_all([
            ProductVariant(product_id=saffron.id, name="1g Premium Box",  price_modifier=0,    stock=50, sku="SAFFRON-1G"),
            ProductVariant(product_id=saffron.id, name="5g Family Box",   price_modifier=2000, stock=20, sku="SAFFRON-5G"),
            ProductVariant(product_id=saffron.id, name="10g Gift Box",    price_modifier=4500, stock=10, sku="SAFFRON-10G"),
        ])

        # ── Variants for Walnuts ───────────────────────────────────────────────
        walnuts = next(p for p in products if p.slug == "kashmiri-walnuts-kagzi")
        db.session.add_all([
            ProductVariant(product_id=walnuts.id, name="500g Pack",  price_modifier=0,   stock=100, sku="WALNUT-500G"),
            ProductVariant(product_id=walnuts.id, name="1kg Pack",   price_modifier=600, stock=80,  sku="WALNUT-1KG"),
            ProductVariant(product_id=walnuts.id, name="2kg Bulk",   price_modifier=1200,stock=40,  sku="WALNUT-2KG"),
        ])

        db.session.commit()
        print(f"  Added {Product.query.count()} products with variants.\n")

        print("=" * 60)
        print("  Database successfully seeded!")
        print(f"  Categories : {Category.query.count()}")
        print(f"  Products   : {Product.query.count()}")
        print(f"  Variants   : {ProductVariant.query.count()}")
        print("=" * 60 + "\n")


if __name__ == "__main__":
    seed()
