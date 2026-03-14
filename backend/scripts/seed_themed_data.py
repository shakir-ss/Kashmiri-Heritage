import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db, Category, Product, Analytics, CartItem, OrderItem

app = create_app('dev')

def seed():
    with app.app_context():
        print("Cleaning up old data...")
        # Clear child tables first
        Analytics.query.delete()
        CartItem.query.delete()
        OrderItem.query.delete()
        # Now clear parent tables
        Product.query.delete()
        Category.query.delete()
        
        print("Seeding Categories...")
        categories = [
            Category(name="Premium Dry Fruits", slug="dry-fruits", description="Organic and sun-dried fruits from the orchards of Kashmir."),
            Category(name="Pashmina & Kani", slug="pashmina-shawls", description="Authentic handcrafted Pashmina shawls with intricate Kani and Sozni work."),
            Category(name="Artistic Papier Mâché", slug="papier-mache", description="Timeless handcrafted decor items with traditional motifs."),
            Category(name="Pure Saffron & Spices", slug="saffron-spices", description="The world's finest saffron and organic mountain spices.")
        ]
        db.session.add_all(categories)
        db.session.commit()

        # Base64 placeholders (1x1 or small colored blocks)
        def b64_img(color_hex):
            return f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='300'%3E%3Crect width='400' height='300' fill='%23{color_hex}'/%3E%3C/svg%3E"

        print("Seeding Products...")
        products = [
            # Dry Fruits
            Product(
                name="Premium Mamra Almonds", slug="mamra-almonds", category_id=categories[0].id,
                description="The richest variety of almonds, grown organically in the high altitudes of Kashmir.",
                price=1800, discount_price=1650, stock=50,
                image_url=b64_img("4a2c2a"), is_active=True,
                details="""Our Mamra Almonds are sourced from the high-altitude orchards of Ganderbal. Unlike regular almonds, Mamra is characterized by its concave shape and higher oil content.
                
- 100% Organic & Preservative Free
- Rich in Omega-3 and Vitamin E
- Traditional sun-drying process preserves natural crunch
- Perfect for boosting brain health and immunity."""
            ),
            Product(
                name="Kashmiri Walnut Kernels (Snow White)", slug="walnut-kernels", category_id=categories[0].id,
                description="Extra light, 'Snow White' quality walnut kernels.",
                price=1200, discount_price=950, stock=100,
                image_url=b64_img("4a2c2a"), is_active=True,
                details="""Known as the 'Brain Food', our Snow White Walnut Kernels are hand-shelled to ensure the largest possible 'halves'. 
                
Grown in the cold climate of Kupwara, these walnuts have a buttery texture and zero bitterness. They are vacuum-packed to retain freshness and prevent oxidation of the healthy fats."""
            ),
            # Saffron
            Product(
                name="Pure Mongra Saffron (Grade A++)", slug="pure-mongra-saffron", category_id=categories[3].id,
                description="World-renowned Lacha Saffron from Pampore.",
                price=650, discount_price=499, stock=200,
                image_url=b64_img("f4a460"), is_active=True,
                details="""Harvested from the plateau of Pampore during the short autumn bloom, our Mongra Saffron consists only of the deep red stigmas of the Crocus sativus flower.
                
- Lab-tested for high Crocin content (Color)
- Intense aroma and distinct flavor
- Essential for traditional Wazwan, Kahwa, and skincare
- Sourced directly from farmer cooperatives."""
            ),
            # Pashmina
            Product(
                name="Hand-Embroidered Sozni Pashmina", slug="sozni-pashmina-shawl", category_id=categories[1].id,
                description="Exquisite pure Pashmina shawl featuring intricate Sozni hand-embroidery.",
                price=15000, discount_price=12500, stock=5,
                image_url=b64_img("2d5a27"), is_active=True,
                details="""A labor of love that takes over 6 months to complete. This shawl is made from the finest 'Changthangi' wool, hand-spun by women in Srinagar and hand-woven on traditional looms.
                
The Sozni embroidery is a delicate needlework craft passed down through generations. Each motif is inspired by the flora of the Valley—Chinar leaves, almonds, and lotuses. A true heirloom piece."""
            ),
            # Papier Mache
            Product(
                name="Gold-Leaf Papier Mâché Trinket Box", slug="gold-papier-mache-box", category_id=categories[2].id,
                description="Hand-painted trinket box featuring traditional 'Naqashi' work.",
                price=2500, discount_price=1850, stock=15,
                image_url=b64_img("d4af37"), is_active=True,
                details="""This decorative box is a masterpiece of 'Naqashi'. The base is created from recycled paper pulp, hardened and smoothed to a wood-like finish.
                
Artisans then use fine brushes made of goat hair to paint intricate Persian-inspired patterns. The finishing touch is the application of real 24K gold leaf, giving it a regal and timeless glow."""
            )
        ]
        db.session.add_all(products)
        db.session.commit()
        print("Database seeded with Kashmiri themed data!")

if __name__ == "__main__":
    seed()
