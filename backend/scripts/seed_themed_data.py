import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db, Category, Product, Analytics, CartItem, OrderItem, WishlistItem, ProductVariant, ProductImage

app = create_app('prod')

def seed():
    with app.app_context():
        print("Ensuring tables exist...")
        db.create_all()
        
        print("Cleaning up old data...")
        try:
            Analytics.query.delete()
            CartItem.query.delete()
            OrderItem.query.delete()
            WishlistItem.query.delete()
            ProductVariant.query.delete()
            ProductImage.query.delete()
            Product.query.delete()
            Category.query.delete()
            db.session.commit()
            print("Old data cleared.")
        except Exception as e:
            db.session.rollback()
            print(f"Cleanup skipped or failed: {e}")

        print("Adding Production Categories...")
        cat_organic = Category(
            name="Organic Staples", 
            slug="organic-staples", 
            description="Pure, raw, and medicinal-grade staples harvested from the pristine high-altitude farms of the Kashmir Valley."
        )
        cat_dry_fruits = Category(
            name="Premium Dry Fruits", 
            slug="dry-fruits", 
            description="Sun-dried treasures from ancient Kashmiri orchards, known globally for their superior oil content and nutritional density."
        )
        
        db.session.add_all([cat_organic, cat_dry_fruits])
        db.session.commit()

        print("Adding Production Products with Artisanal Stories...")
        
        # 1. Pure Kashmiri Honey
        honey = Product(
            category_id=cat_organic.id,
            name="Wild Himalayan White Honey",
            slug="pure-kashmiri-honey",
            price=800,
            stock=50,
            weight_grams=500,
            description="Raw, unpasteurized forest nectar from the high-altitude meadows.",
            details="""Gathered from the high-altitude meadows of the Himalayas, our honey is a symphony of wild forest nectar. 
            Unlike commercial honey, it is never heated or ultra-filtered, preserving the live enzymes and delicate pollens 
            that make Kashmiri honey a legendary healing elixir. It has a creamy texture and a floral finish that reflects 
            the biodiversity of the valley."""
        )
        db.session.add(honey)
        db.session.flush()
        
        db.session.add(ProductVariant(
            product_id=honey.id,
            name="1000g (1kg) Artisanal Jar",
            price_modifier=700,
            stock=30,
            sku="HONEY-1KG"
        ))

        # 2. Pure Kashmiri Saffron
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
            sun-drenched flavor, powerful antioxidants, and a mesmerizing aroma that defines Kashmiri royalty."""
        )
        db.session.add(saffron)

        # 3. Pure Kashmiri Almonds
        almonds = Product(
            category_id=cat_dry_fruits.id,
            name="Kashmiri Mamra Almonds",
            slug="pure-kashmiri-almonds",
            price=250,
            stock=60,
            weight_grams=500,
            description="Small in size, mighty in nutrition. The highest oil content almonds in the world.",
            details="""Our Kashmiri Mamra almonds are the rarest in the world. Grown in organic orchards fed by glacial 
            streams, they are smaller in size but contain significantly higher oil content than Californian 
            varieties. Known as 'Brain Food' in the valley, these almonds are sweet, crunchy, and packed with 
            Vitamin E and healthy fats. They are sun-dried to preserve their natural oils and crunch."""
        )
        db.session.add(almonds)
        db.session.flush()

        db.session.add(ProductVariant(
            product_id=almonds.id,
            name="1000g (1kg) Family Pack",
            price_modifier=150,
            stock=40,
            sku="ALMOND-1KG"
        ))

        # 4. Pure Kashmiri Walnuts (New)
        walnuts = Product(
            category_id=cat_dry_fruits.id,
            name="Snow-Fed Kashmiri Walnuts",
            slug="pure-kashmiri-walnuts",
            price=300, # Placeholder base price
            stock=80,
            weight_grams=500,
            description="Premium heart-healthy walnuts from the cool mountain slopes of the Himalayas.",
            details="""The pride of Kashmiri orchards. These walnuts are nurtured by the cool mountain air and rich 
            alluvial soil of the valley. Known for their light color and butterfly-shaped kernels, they are 
            harvested with care to ensure the highest quality. Rich in Omega-3 fatty acids, they are nature's 
            ultimate heart and brain food. Our walnuts are 100% organic and free from any chemical processing."""
        )
        db.session.add(walnuts)
        db.session.flush()

        db.session.add_all([
            ProductVariant(
                product_id=walnuts.id,
                name="With Shell (Whole Nut)",
                price_modifier=0,
                stock=40,
                sku="WALNUT-SHELL"
            ),
            ProductVariant(
                product_id=walnuts.id,
                name="Without Shell (Golden Kernels)",
                price_modifier=200, # Example modifier
                stock=40,
                sku="WALNUT-KERNEL"
            )
        ])

        db.session.commit()
        print("Database successfully seeded with enhanced production data and Walnut variants!")

if __name__ == "__main__":
    seed()
