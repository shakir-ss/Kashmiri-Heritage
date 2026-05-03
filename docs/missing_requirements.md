# Category-Based Gap Analysis & Missing Requirements
**Project:** The Hundred Villages - Kashmiri Heritage Platform
**Date:** May 2026
**Analysis Basis:** 2025 Google Doc Roadmap vs. Current Codebase (v1.4)

## Overview
Following a comprehensive audit of the current Vue 3/Flask codebase and cross-referencing it with 2025 industry best practices for premium D2C e-commerce, several critical gaps have been identified. While the foundation (Partial COD, Variants, Basic Checkout) is solid, the platform requires advanced trust-building, personalization, and operational features to compete as a premium heritage brand.

Below is the category-by-category breakdown of the missing important features, prioritized using the MoSCoW framework.

---

### 1. Storefront & Navigation
*Current State:* Basic routing and static `HomeView.vue`. No advanced navigation structures.
*Industry Standard:* Premium brands utilize highly visual, predictive navigation to guide users instantly to niche products.

| ID | Missing Feature | Priority | Business Value |
|---|---|---|---|
| SN-01 | **Visual Mega-Menu:** Dropdown navigation displaying category images and featured artisanal products (not just text links). | Should-Have | Increases discoverability and reinforces the premium aesthetic immediately upon interaction. |
| SN-02 | **IP-Based Geolocation Personalization:** Automatically detect if a user is in a "Local Pincode" zone and display a banner for "Complimentary Shipping Available". | Could-Have | Drives urgency and localization without requiring the user to reach the checkout phase. |

### 2. Product Discovery (PLP & Search)
*Current State:* Basic `ProductsView.vue` with standard listing. No intelligent search.
*Industry Standard:* 2025 platforms use NLP (Natural Language Processing) for search and highly granular faceted filtering.

| ID | Missing Feature | Priority | Business Value |
|---|---|---|---|
| PD-01 | **Agentic AI / Predictive Search Engine:** Type-ahead search that understands synonyms (e.g., "Kesar" = "Saffron") and corrects typos natively. | Must-Have | Direct impact on conversion; users who use search are 2-3x more likely to convert if they find relevant results. |
| PD-02 | **Advanced Faceted Filtering:** Allow users to filter products by `weight_grams` (for food) or `attributes` like material/artisan origin simultaneously. | Must-Have | Essential for navigating complex variant catalogs without user frustration. |

### 3. Product Presentation (PDP)
*Current State:* Excellent "Heritage Story" section and basic variant switching. Missing social proof and advanced media.
*Industry Standard:* PDPs are landing pages. They require intense social proof and immersive visual capabilities.

| ID | Missing Feature | Priority | Business Value |
|---|---|---|---|
| PP-01 | **Customer Reviews & Ratings Engine:** A verified review system (Database model missing) allowing image uploads (UGC) for received products. | Must-Have | The #1 trust signal for high-ticket artisanal items. Crucial for the D2C trust bridge. |
| PP-02 | **Frequently Bought Together (Cross-sell):** Algorithmically or manually linked products (e.g., suggesting Almonds when viewing Saffron). | Must-Have | The most effective method for increasing Average Order Value (AOV). |
| PP-03 | **3D/AR Viewer for Handicrafts:** `.glb`/`.gltf` integration for non-food items (like Papier Mache boxes) allowing spatial visualization. | Should-Have | Aligns with the 2025 AR roadmap; drastically reduces return rates for high-ticket decor. |

### 4. Transactional Flow (Cart & Checkout)
*Current State:* `CheckoutView.vue` excellently handles Partial COD (30/70 split). However, it relies on manual data entry.
*Industry Standard:* Frictionless checkout with 1-click wallets and address auto-completion.

| ID | Missing Feature | Priority | Business Value |
|---|---|---|---|
| TF-01 | **Address Auto-Complete API (Google Places):** Real-time address validation in the checkout form. | Must-Have | Reduces "type-time" and drastically lowers the rate of Return-To-Origin (RTO) due to bad addresses. |
| TF-02 | **Promo Code & Discount Engine:** Logic for percentage or fixed-amount coupons applied at checkout (Database model missing). | Must-Have | Necessary for marketing campaigns, influencer collaborations, and abandoned cart recovery. |
| TF-03 | **Guest Cart to Auth Sync:** Logic ensuring that if a user adds items as a guest and *then* logs in, their localStorage cart merges with the database `cart_items`. | Must-Have | Prevents the frustrating experience of "losing" items upon registration. |

### 5. Customer Lifecycle & Account
*Current State:* Basic `LoginView.vue` and `OrdersView.vue`. No robust profile management.
*Industry Standard:* Self-service portals that reduce customer support overhead.

| ID | Missing Feature | Priority | Business Value |
|---|---|---|---|
| CL-01 | **Customer Address Book:** Ability to save multiple shipping addresses to the user profile for 1-click selection at checkout. | Must-Have | Streamlines repeat purchases and increases Customer Lifetime Value (CLV). |
| CL-02 | **1-Click Reorder:** A button in the `OrdersView.vue` that instantly repopulates the cart with a past order's items. | Should-Have | Drives recurring revenue, especially for consumable items like Dry Fruits. |
| CL-03 | **Artisan Loyalty Program:** Point accrual system based on purchase value, redeemable on future orders. | Could-Have | Incentivizes long-term brand loyalty over purchasing from generic marketplaces. |

### 6. Post-Purchase & Logistics
*Current State:* `Order` model tracks status.
*Industry Standard:* Proactive communication and self-service returns.

| ID | Missing Feature | Priority | Business Value |
|---|---|---|---|
| PL-01 | **Automated WhatsApp/SMS Tracking (Twilio):** Trigger transactional messages upon status changes (`Shipped`, `Out for Delivery`). | Must-Have | Standard for 2025; reduces WISMO ("Where Is My Order") support tickets by 80%. |
| PL-02 | **Self-Service RMA (Return Merchandise Authorization):** A workflow in the user dashboard to request a return/refund with automated label generation. | Should-Have | Builds pre-purchase trust (knowing returns are easy) and streamlines reverse logistics. |

### 7. Admin Governance & Operations
*Current State:* `AdminDashboard.vue` exists but lacks granular operational tools.
*Industry Standard:* Centralized hub for multi-role operations.

| ID | Missing Feature | Priority | Business Value |
|---|---|---|---|
| AG-01 | **Low Stock / Inventory Alert Dashboard:** Automated visual warnings when `product_variants.stock` falls below a defined threshold. | Must-Have | Prevents revenue loss from out-of-stock high-velocity items. |
| AG-02 | **Partial COD Reconciliation Interface:** A specific view for admins to mark the "70% Balance on Delivery" as collected by the logistics partner. | Must-Have | Critical for the financial auditing of the unique business model. |
| AG-03 | **Role-Based Admin Permissions (RBAC UI):** Interface to restrict junior staff (e.g., Customer Support) from altering prices or editing product data. | Should-Have | Protects enterprise data integrity as the operational team scales. |
