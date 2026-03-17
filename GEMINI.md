# Kashmiri Dry Fruits - Project Documentation

## PROJECT VISION
A premium, scalable, and high-performance e-commerce platform specializing in Kashmiri products (Dry Fruits & Handicrafts). The architecture focuses on performance, security, and organic aesthetics.

## ARCHITECTURE OVERVIEW
- **Backend**: Python (Flask) with RESTful APIs, organized into Blueprints.
- **Frontend**: Vue.js 3 (Composition API) + Vite + Pinia for state management.
- **Database**: MySQL 8.0+ (Relational, ACID compliant).
- **Security**: JWT-based Authentication with Role-Based Access Control (RBAC).
- **Analytics**: Custom internal engine for revenue, popular items, and abandoned cart tracking.
- **Messaging**: Twilio/WhatsApp Business API for real-time order notifications.
- **Styling**: Premium "Organic" CSS (Walnut Brown, Saffron Orange, Forest Green).

## DATABASE SCHEMA (V1.4)
- **`users`**: `id`, `name`, `email`, `password_hash`, `role`.
- **`categories`**: `id`, `name`, `slug`, `description`.
- **`products`**: `id`, `category_id`, `name`, `slug`, `price`, `discount_price`, `stock`, `is_active`, `details`, `weight_grams`, `attributes` (JSON).
- **`product_variants`**: `id`, `product_id`, `name`, `price_modifier`, `stock`, `sku`.
- **`orders`**: `id`, `user_id`, `total_amount`, `prepaid_amount`, `balance_on_delivery`, `status`, `address`, `phone`, `payment_id`.

## SHIPPING & LOGISTICS
- **Local Radius**: Specified list of Pincodes (defined in `frontend/src/config.js`) receive **COMPLIMENTARY** shipping.
- **Standard Shipping**: Minimal flat fee of ₹50 applied to all non-local destinations.
- **Psychological Checkout**: Editorial-style UI with trust badges and commitment-based messaging.

## PAYMENT ARCHITECTURE
- **Modes**: UPI, Card, and Partial COD.
- **Partial COD Rule**: 30% Commitment Fee paid today; 70% Balance on Delivery. This reduces cart abandonment and ensures artisanal handling priority.

## MAJOR DECISIONS
- [2026-03-13]: Chose Flask for backend for its simplicity and flexibility.
- [2026-03-13]: Selected Vue.js for a reactive, mobile-responsive UI.
- [2026-03-13]: Opted for MySQL to handle structured e-commerce data efficiently.
- [2026-03-13]: **HOSTING STRATEGY**: Hybrid Cloud (Vercel for Frontend, Render for Backend, Aiven for MySQL) for a $0 starting cost.
- [2026-03-13]: **ANALYTICS**: Implemented custom tracking to avoid heavy 3rd-party scripts and maintain "premium" performance.
- [2026-03-13]: **MESSAGING**: Selected WhatsApp (Twilio) as the primary notification channel to align with regional user behavior.
- [2026-03-16]: **GENERAL STORE PIVOT**: Expanded schema to support weights and variants for non-food items.
- [2026-03-16]: **PARTIAL COD**: Implemented 30/70 split payment logic to bridge trust between artisanal sellers and global customers.
- [2026-03-16]: **TEST ISOLATION**: Updated BDD steps to proactively replenish stock and clear state before runs.

## TECH STACK SUMMARY
- **Backend**: Flask, SQLAlchemy, Bcrypt, PyJWT, Flask-CORS, Twilio.
- **Frontend**: Vue 3, Pinia, Vue-Router, Axios.
- **Database**: MySQL 8.0.
