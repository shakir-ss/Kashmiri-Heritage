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

## DATABASE SCHEMA (V1.2)
- **`users`**: `id`, `name`, `email`, `password_hash`, `role` (admin/customer).
- **`categories`**: `id`, `name`, `slug`, `description`.
- **`products`**: `id`, `category_id`, `name`, `slug`, `price`, `discount_price`, `stock`, `is_active`.
- **`orders`**: `id`, `user_id`, `total_amount`, `status`, `address`, `phone`, `payment_id`.
- **`order_items`**: `id`, `order_id`, `product_id`, `quantity`, `price_at_purchase`.
- **`cart_items`**: `id`, `user_id`, `product_id`, `quantity`, `updated_at`.
- **`analytics`**: `id`, `product_id`, `view_count`, `last_viewed_at`.

## MAJOR DECISIONS
- [2026-03-13]: Chose Flask for backend for its simplicity and flexibility.
- [2026-03-13]: Selected Vue.js for a reactive, mobile-responsive UI.
- [2026-03-13]: Opted for MySQL to handle structured e-commerce data efficiently.
- [2026-03-13]: **HOSTING STRATEGY**: Hybrid Cloud (Vercel for Frontend, Render for Backend, Aiven for MySQL) for a $0 starting cost.
- [2026-03-13]: **ANALYTICS**: Implemented custom tracking to avoid heavy 3rd-party scripts and maintain "premium" performance.
- [2026-03-13]: **MESSAGING**: Selected WhatsApp (Twilio) as the primary notification channel to align with regional user behavior.

## TECH STACK SUMMARY
- **Backend**: Flask, SQLAlchemy, Bcrypt, PyJWT, Flask-CORS, Twilio.
- **Frontend**: Vue 3, Pinia, Vue-Router, Axios.
- **Database**: MySQL 8.0.
