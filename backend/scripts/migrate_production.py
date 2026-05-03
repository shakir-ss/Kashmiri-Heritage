"""
migrate_production.py
=====================
SAFE production migration script for schema changes introduced in Phase 1-5.

What this does:
  - Adds NEW columns to existing tables using ALTER TABLE IF NOT EXISTS
  - Creates NEW tables using CREATE TABLE IF NOT EXISTS
  - NEVER drops columns, NEVER truncates tables, NEVER overwrites data

What this does NOT do:
  - Does NOT re-run seed_themed_data.py
  - Does NOT delete any customer/product/order data
  - Does NOT modify existing rows

Run this once against your production (Aiven/cloud) MySQL database:
  cd backend
  python scripts/migrate_production.py

You can safely re-run it — all statements use IF NOT EXISTS / IF EXISTS guards.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db

# ─── Columns to add (table, column, definition) ────────────────────────────
NEW_COLUMNS = [
    # Phase 1 — Category image support
    ("categories",  "image_url",         "VARCHAR(255) NULL"),

    # Phase 3 — Order shipment tracking
    ("orders",      "tracking_link",      "VARCHAR(500) NULL"),
    ("orders",      "tracking_number",    "VARCHAR(100) NULL"),
]

# ─── New tables (raw CREATE TABLE IF NOT EXISTS SQL) ───────────────────────
NEW_TABLES_SQL = [
    # Phase 2 — B2B Wholesale Inquiries
    """
    CREATE TABLE IF NOT EXISTS b2b_inquiries (
        id              INT AUTO_INCREMENT PRIMARY KEY,
        company_name    VARCHAR(150) NOT NULL,
        contact_name    VARCHAR(100) NOT NULL,
        email           VARCHAR(120) NOT NULL,
        phone           VARCHAR(20),
        requirements    TEXT NOT NULL,
        status          VARCHAR(20) DEFAULT 'pending',
        created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """,

    # Phase 4 — Customer Reviews (with photo support)
    """
    CREATE TABLE IF NOT EXISTS reviews (
        id          INT AUTO_INCREMENT PRIMARY KEY,
        product_id  INT NOT NULL,
        user_id     INT NULL,
        rating      INT NOT NULL,
        comment     TEXT,
        created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_approved TINYINT(1) DEFAULT 1,
        FOREIGN KEY (product_id) REFERENCES products(id),
        FOREIGN KEY (user_id)    REFERENCES users(id)
    );
    """,

    # Phase 4 — Review Images (UGC photo attachments)
    """
    CREATE TABLE IF NOT EXISTS review_images (
        id          INT AUTO_INCREMENT PRIMARY KEY,
        review_id   INT NOT NULL,
        image_url   VARCHAR(255) NOT NULL,
        FOREIGN KEY (review_id) REFERENCES reviews(id) ON DELETE CASCADE
    );
    """,

    # Phase 5 — Abandoned Cart Recovery
    """
    CREATE TABLE IF NOT EXISTS abandoned_carts (
        id          INT AUTO_INCREMENT PRIMARY KEY,
        email       VARCHAR(120) NOT NULL,
        cart_data   JSON NOT NULL,
        created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
        recovered   TINYINT(1) DEFAULT 0,
        email_sent  TINYINT(1) DEFAULT 0
    );
    """,
]


def column_exists(conn, table, column):
    """Check if a column already exists in a table."""
    result = conn.execute(
        db.text(
            "SELECT COUNT(*) FROM information_schema.COLUMNS "
            "WHERE TABLE_SCHEMA = DATABASE() "
            "AND TABLE_NAME = :table AND COLUMN_NAME = :column"
        ),
        {"table": table, "column": column}
    )
    return result.scalar() > 0


def run_migration():
    app = create_app('dev')   # 'dev' reads your local config.py — override DB_URI via env for cloud
    with app.app_context():
        with db.engine.connect() as conn:
            print("\n" + "=" * 60)
            print("  THE HUNDRED VILLAGES — Production Migration")
            print("=" * 60)

            # ── 1. New columns ─────────────────────────────────────────
            print("\n[1/2] Adding new columns to existing tables...")
            for table, column, definition in NEW_COLUMNS:
                if column_exists(conn, table, column):
                    print(f"  [SKIP]  {table}.{column} already exists")
                else:
                    sql = f"ALTER TABLE `{table}` ADD COLUMN `{column}` {definition};"
                    conn.execute(db.text(sql))
                    conn.commit()
                    print(f"  [ADDED] {table}.{column}")

            # -- 2. New tables -------------------------------------------------
            print("\n[2/2] Creating new tables (if not exist)...")
            for sql in NEW_TABLES_SQL:
                # Extract table name for the log message
                table_name = [line.strip() for line in sql.strip().splitlines()
                              if 'CREATE TABLE' in line][0].split('IF NOT EXISTS')[-1].strip().split('(')[0].strip()
                conn.execute(db.text(sql.strip()))
                conn.commit()
                print(f"  [TABLE] {table_name}")

            print("\n" + "=" * 60)
            print("  Migration complete -- zero data was modified.")
            print("=" * 60 + "\n")


if __name__ == '__main__':
    run_migration()
