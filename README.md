# Kashmiri Heritage

[![BDD Tests](https://img.shields.io/badge/BDD%20Tests-100%25%20Pass-brightgreen)](https://github.com/yourusername/kashmiri-heritage)
[![Tech Stack](https://img.shields.io/badge/Stack-Vue%203%20%7C%20Flask%20%7C%20MySQL-blue)](https://github.com/yourusername/kashmiri-heritage)

A premium, high-performance e-commerce platform dedicated to preserving and showcasing the artisanal excellence of the Kashmir Valley. **Kashmiri Heritage** bridges the gap between traditional Himalayan craftsmanship and the global connoisseur through an immersive, storytelling-driven digital experience.

## 🏺 Project Vision
To provide a world-class storefront for authentic Kashmiri products, ranging from lab-certified Mongra Saffron to hand-embroidered Pashmina shawls. The platform emphasizes:
- **Organic Aesthetics**: A cultural color palette (Walnut, Saffron, Chinar) and artisanal typography.
- **Cultural Integrity**: Humanizing the craft through "Artisan Spotlights" and "Heritage Stories."
- **Trust-Based Commerce**: Implementation of a unique Partial COD payment model to secure commitment for artisanal goods.

## ✨ Key Features
- **Global General Store Model**: Sophisticated catalog supporting weights, dynamic JSON attributes, and product variants (Size, Color, etc.).
- **Psychological Checkout**: An editorial-style single-page checkout featuring trust badges, commitment-based messaging, and a sticky order summary.
- **Partial COD (30/70 Rule)**: Unique payment logic requiring a 30% commitment fee today and 70% balance on delivery.
- **Dynamic Logistics**: Automated shipping calculations with complimentary delivery for local pincodes and flat-fee global shipping.
- **Admin Insights & Inventory**: Shopify-style dashboard for real-time revenue tracking, best-seller analytics, abandoned cart monitoring, and customer inquiry management.
- **Multi-Media Support**: Advanced product galleries with multi-image handling and primary image selection.
- **Customer Engagement**: Persistent Wishlist synchronization, order history tracking, and an immersive contact hub.

## 🛠️ Tech Stack
- **Frontend**: Vue.js 3 (Composition API), Vite, Pinia, Vue Router, Axios.
- **Backend**: Python (Flask), SQLAlchemy (ORM), Flask-Migrate, Bcrypt, PyJWT.
- **Database**: MySQL 8.0+.
- **Messaging**: Twilio/WhatsApp Business API integration for real-time order notifications.
- **Testing**: Comprehensive BDD suite powered by **Behave** and **Playwright** (100% scenario pass rate).

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.12+
- MySQL Server

### 1. Database Setup
```sql
CREATE DATABASE kashmiri_dry_fruits; -- Name retained for internal environment compatibility
```
Run the initialization scripts to prepare the schema and seed data:
```bash
python backend/scripts/update_db_schema.py
python backend/scripts/register_root.py
python backend/scripts/seed_themed_data.py
```

### 2. Backend Installation
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### 3. Frontend Installation
```bash
cd frontend
npm install
npm run dev
```

## 🧪 Quality Assurance
The platform is verified by a rigorous BDD regression suite covering 34+ end-to-end scenarios.
```bash
.\backend\venv\Scripts\behave.exe tests/features
```

## 🌍 Hosting Strategy ($0 Starting Cost)
- **Frontend**: [Vercel](https://vercel.com/) or Netlify.
- **Backend**: [Render](https://render.com/) (Free Tier).
- **Database**: [Aiven](https://aiven.io/) (Free MySQL Plan).

---
*Created with focus on preserving the timeless heritage of the Kashmir Valley.*
