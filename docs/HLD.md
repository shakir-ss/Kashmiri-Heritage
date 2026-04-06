# High-Level Design (HLD): Kashmiri General Store

## 1. System Overview
The platform is a premium e-commerce application designed for global reach and high performance. It utilizes a **Hybrid Cloud Architecture** to maximize scalability while maintaining zero initial overhead.

## 2. Technology Stack
*   **Frontend:** Vue.js 3 (Composition API) with Pinia for state management and Vite for build orchestration.
*   **Backend:** Python Flask with a RESTful Blueprint-based architecture.
*   **Database:** MySQL 8.0 (Managed via Aiven/RDS) for transactional integrity and complex relationship modeling.
*   **Testing:** BDD (Behavior-Driven Development) using Behave and Playwright.

## 3. Core Architectural Pillars
### A. Hybrid Cloud Strategy
*   **Vercel (Frontend):** Blazing fast global delivery of the Vue application via Edge network.
*   **Render (Backend):** Scalable hosting for the Flask API.
*   **Aiven (Database):** High-availability MySQL hosting with automated backups.

### B. Security & Identity
*   **JWT Authentication:** Stateless authentication using JSON Web Tokens.
*   **RBAC (Role-Based Access Control):** Clear separation between 'Customer' and 'Admin' privileges.
*   **Bcrypt:** Industry-standard password hashing.

### C. The Artisan Analytics Engine
A custom-built analytics suite that tracks:
*   **Conversion Funnel:** Abandoned cart tracking for items older than 24 hours.
*   **Traffic Intelligence:** Product view counters and popularity heatmaps.
*   **Revenue Metrics:** Real-time calculation of total revenue from verified (paid) orders.

### D. Enhanced Data Model
*   **Multimedia Integration:** Support for multiple high-resolution images per product, with a primary image identification system.
*   **Variants & Weights:** Support for weight-based pricing (grams) and arbitrary product variants (size, color, material) to accommodate both dry fruits and handicrafts.

## 4. Integration Layer
*   **Logistics:** Pincode-based shipping calculator. Local radius patrons receive **COMPLIMENTARY** shipping, while all other destinations are charged a flat ₹50 fee.
*   **Communication:** Twilio/WhatsApp integration for real-time customer transactional alerts.
