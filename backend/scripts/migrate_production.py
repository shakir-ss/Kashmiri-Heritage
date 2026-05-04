"""
migrate_production.py
=====================
SAFE production migration script for schema changes introduced in Phase 1-5.

What this does:
  - Adds NEW columns to existing tables using ALTER TABLE IF NOT EXISTS
  - Creates NEW tables using CREATE TABLE IF NOT EXISTS
  - NEVER drops columns, NEVER truncates tables, NEVER overwrites data

HOW TO RUN:
  Local DB (default):
    cd backend
    .\\venv\\Scripts\\python scripts/migrate_production.py

  TiDB Cloud / Production:
    cd backend
    $env:DATABASE_URL = "mysql+pymysql://USER:PASS@HOST:PORT/DBNAME"
    .\\venv\\Scripts\\python scripts/migrate_production.py
"""

import sys
import os
import ssl
import re

# -- Path setup (must stay before local imports) ------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# -- Columns to add (table, column, SQL type) ---------------------------------
NEW_COLUMNS = [
    # Phase 1 -- Category image support
    ("categories", "image_url",      "VARCHAR(255) NULL"),
    # Phase 3 -- Order shipment tracking
    ("orders",     "tracking_link",   "VARCHAR(500) NULL"),
    ("orders",     "tracking_number", "VARCHAR(100) NULL"),
]

# -- New tables (raw CREATE TABLE IF NOT EXISTS SQL) --------------------------
NEW_TABLES_SQL = [
    # Phase 2 -- B2B Wholesale Inquiries
    """CREATE TABLE IF NOT EXISTS b2b_inquiries (
        id           INT AUTO_INCREMENT PRIMARY KEY,
        company_name VARCHAR(150) NOT NULL,
        contact_name VARCHAR(100) NOT NULL,
        email        VARCHAR(120) NOT NULL,
        phone        VARCHAR(20),
        requirements TEXT NOT NULL,
        status       VARCHAR(20) DEFAULT 'pending',
        created_at   DATETIME DEFAULT CURRENT_TIMESTAMP
    )""",

    # Phase 4 -- Customer Reviews (with photo support)
    """CREATE TABLE IF NOT EXISTS reviews (
        id          INT AUTO_INCREMENT PRIMARY KEY,
        product_id  INT NOT NULL,
        user_id     INT NULL,
        rating      INT NOT NULL,
        comment     TEXT,
        created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_approved TINYINT(1) DEFAULT 1,
        FOREIGN KEY (product_id) REFERENCES products(id),
        FOREIGN KEY (user_id)    REFERENCES users(id)
    )""",

    # Phase 4 -- Review image attachments (UGC)
    """CREATE TABLE IF NOT EXISTS review_images (
        id        INT AUTO_INCREMENT PRIMARY KEY,
        review_id INT NOT NULL,
        image_url VARCHAR(255) NOT NULL,
        FOREIGN KEY (review_id) REFERENCES reviews(id) ON DELETE CASCADE
    )""",

    # Phase 5 -- Abandoned Cart Recovery
    """CREATE TABLE IF NOT EXISTS abandoned_carts (
        id         INT AUTO_INCREMENT PRIMARY KEY,
        email      VARCHAR(120) NOT NULL,
        cart_data  JSON NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        recovered  TINYINT(1) DEFAULT 0,
        email_sent TINYINT(1) DEFAULT 0
    )""",
]


def parse_db_url(url):
    """Parse mysql+pymysql://user:pass@host:port/db into a dict."""
    url = "".join(url.split())
    url = re.sub(r'^mysql(\+\w+)?://', '', url)
    url = url.split('?')[0]
    user_pass, rest = url.split('@', 1)
    user, password  = user_pass.split(':', 1)
    host_port, db   = rest.split('/', 1)
    if ':' in host_port:
        host, port = host_port.rsplit(':', 1)
        port = int(port)
    else:
        host, port = host_port, 3306
    return dict(host=host, port=port, user=user, password=password, database=db)


def get_connection():
    """Return a raw pymysql connection -- with SSL for cloud, plain for local."""
    import pymysql

    raw_url = os.environ.get('DATABASE_URL', '')
    is_cloud = bool(raw_url) and 'localhost' not in raw_url and '127.0.0.1' not in raw_url

    if is_cloud:
        params = parse_db_url(raw_url)
        # Build an SSL context that works on Windows without a CA cert file.
        # TiDB Cloud accepts connections with CERT_NONE (encryption is still active,
        # we just skip certificate chain verification -- acceptable for admin scripts).
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode   = ssl.CERT_NONE
        params['ssl'] = ctx
        print(f"  Connecting (TiDB Cloud SSL) -> {params['host']}:{params['port']}/{params['database']}")
        return pymysql.connect(**params), True
    else:
        # Local: read from config.py / local .env
        from app import create_app
        from models import db as sa_db
        flask_app = create_app(os.environ.get('FLASK_CONFIG', 'dev'))
        flask_app.app_context().push()
        engine = sa_db.engine
        raw_conn = engine.raw_connection()
        print(f"  Connecting (local) -> {engine.url.host}/{engine.url.database}")
        return raw_conn, False


def column_exists(cursor, table, column):
    cursor.execute(
        "SELECT COUNT(*) FROM information_schema.COLUMNS "
        "WHERE TABLE_SCHEMA = DATABASE() "
        "AND TABLE_NAME = %s AND COLUMN_NAME = %s",
        (table, column)
    )
    return cursor.fetchone()[0] > 0


def run_migration():
    print("\n" + "=" * 60)
    print("  THE HUNDRED VILLAGES -- Production Migration")
    print("=" * 60)

    conn, is_cloud = get_connection()
    cursor = conn.cursor()

    try:
        # -- 1. New columns ---------------------------------------------------
        print("\n[1/2] Adding new columns to existing tables...")
        for table, column, definition in NEW_COLUMNS:
            if column_exists(cursor, table, column):
                print(f"  [SKIP]  {table}.{column} already exists")
            else:
                cursor.execute(f"ALTER TABLE `{table}` ADD COLUMN `{column}` {definition}")
                conn.commit()
                print(f"  [ADDED] {table}.{column}")

        # -- 2. New tables ----------------------------------------------------
        print("\n[2/2] Creating new tables (if not exist)...")
        for sql in NEW_TABLES_SQL:
            match = re.search(r'CREATE TABLE IF NOT EXISTS\s+(\w+)', sql)
            table_name = match.group(1) if match else "unknown"
            cursor.execute(sql)
            conn.commit()
            print(f"  [TABLE] {table_name}")

        print("\n" + "=" * 60)
        print("  Migration complete -- zero data was modified.")
        print("=" * 60 + "\n")

    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    run_migration()
