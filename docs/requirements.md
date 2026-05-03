# Business Requirements Document (BRD)
**Project:** The Hundred Villages - Kashmiri Heritage Platform
**Date:** May 2026
**Version:** 1.0

### Executive Strategy
The Hundred Villages is designed as a premium, scalable, and high-performance D2C/B2C e-commerce platform specializing in authentic Kashmiri products, including dry fruits and handicrafts. The architectural paradigm emphasizes performance, robust security, and an organic aesthetic (Walnut Brown, Saffron Orange, Forest Green). Crucially, the platform bridges the trust deficit between artisanal sellers and global consumers through a unique Partial COD model (30% commitment fee, 70% balance on delivery). By leveraging a modern tech stack (Vue 3, Flask, MySQL) and adhering to 2025 market standards—including AI-driven personalization, rich Schema.org metadata, and omnichannel awareness—this ecosystem is engineered to maximize conversion rates while maintaining sustainable operational margins.

### Identity and Access Management (IAM)
The IAM module governs the secure onboarding and lifecycle management of both consumers and administrators. It prioritizes low-friction entry for buyers while maintaining stringent security protocols.

| ID | Requirement | Priority | Business Value |
|---|---|---|---|
| IAM-01 | **Guest Checkout & Low-Friction Onboarding:** Allow checkout without mandatory account creation. Post-purchase, offer seamless account creation using the provided email. | Must-Have | Reduces cart abandonment by minimizing "type-time" and onboarding friction for first-time buyers. |
| IAM-02 | **Role-Based Access Control (RBAC):** Implement strict roles in MySQL (`users.role` ENUM) for Customers, Admins, and potentially Artisans, restricting API endpoint access via JWT scopes. | Must-Have | Ensures administrative governance and prevents unauthorized data manipulation. |
| IAM-03 | **JWT-Based Authentication:** Utilize secure, HttpOnly, short-lived JWTs for session management with a robust refresh token rotation strategy. | Must-Have | Modern, stateless security standard aligning with the Vue/Flask architecture. |
| IAM-04 | **Password Management Workflow:** Secure password resets via encrypted email tokens (Bcrypt hashed passwords in DB). | Must-Have | Reduces customer support overhead and maintains security compliance. |
| IAM-05 | **Social SSO (Google/Apple):** Integrate OAuth 2.0/OpenID Connect for 1-click registration and login. | Should-Have | Increases registration rates and captures first-party data seamlessly. |

### Product Discovery & Product Information Management (PIM)
This module handles the presentation, categorization, and discoverability of the diverse product catalog (food items via weight, handicrafts via variants).

| ID | Requirement | Priority | Business Value |
|---|---|---|---|
| PIM-01 | **Variant & Weight Matrix:** Support a unified `products` table with dynamic JSON `attributes` and a `product_variants` table handling SKU, price modifiers, and distinct stock levels for weights (e.g., 250g, 500g) and non-food variants. | Must-Have | Essential for accurately representing the complex inventory of agricultural and artisanal goods. |
| PIM-02 | **Faceted Filtering & Predictive Search:** Enable real-time filtering by category, price, weight, and artisan origin. Implement predictive search (type-ahead) for rapid discovery. | Must-Have | Drastically improves the speed at which consumers locate niche products, boosting conversion. |
| PIM-03 | **Schema.org Structured Data:** Embed JSON-LD product markup (aggregateRating, offers, shippingDetails) on all Product Detail Pages (PDPs). | Must-Have | Optimizes search engine visibility and enables rich snippets in Google search results. |
| PIM-04 | **Dynamic SEO Metadata:** Auto-generate SEO-friendly URLs (`slug`), meta titles, and descriptions based on product attributes and category hierarchies. | Must-Have | Drives organic acquisition by aligning with Google's mobile-first indexing standards. |
| PIM-05 | **Immersive Media Support:** Support high-resolution imagery and WebP formats, with lazy-loading for organic aesthetics without sacrificing performance. | Should-Have | Enhances the "premium" perception critical to the D2C brand narrative. |

### Transactional Core (Cart, Checkout & Payment)
The transactional engine is heavily customized to support the unique logistical and psychological requirements of the Kashmiri heritage market.

| ID | Requirement | Priority | Business Value |
|---|---|---|---|
| TRX-01 | **Persistent Shopping Cart:** Cart state managed via Pinia on the frontend and persisted to localStorage (guest) or database (logged-in user) to survive session drops. | Must-Have | Recovers revenue from multi-device browsing behavior. |
| TRX-02 | **Partial COD Payment Orchestration:** Implement a specialized checkout flow requiring a 30% prepaid commitment fee via UPI/Card, with the remaining 70% logged as `balance_on_delivery`. | Must-Have | The core business model; minimizes return-to-origin (RTO) losses and artisanal risk. |
| TRX-03 | **Dynamic Shipping Engine:** Calculate shipping at checkout: ₹0 for defined local pincodes (loaded from `config.js`), and a flat ₹50 fee for all non-local destinations. | Must-Have | Ensures transparent pricing and automates local promotional logistics. |
| TRX-04 | **Psychological Checkout UI:** Editorial-style checkout interface featuring trust badges, secure connection icons, and commitment-based messaging to reassure buyers. | Must-Have | Builds the necessary trust to facilitate the 30% upfront payment. |
| TRX-05 | **Payment Gateway Integration:** API-first integration with a primary payment gateway (e.g., Razorpay/Stripe) supporting UPI, Credit/Debit, and net banking for the prepaid portion. | Must-Have | Enables secure and diverse financial transaction capture. |

### Order Management & Logistics
This module orchestrates the post-purchase lifecycle, synchronizing real-time notifications and inventory adjustments.

| ID | Requirement | Priority | Business Value |
|---|---|---|---|
| OMS-01 | **Atomic Inventory Decrement:** Real-time database transaction reducing `product_variants.stock` instantly upon payment authorization to prevent overselling. | Must-Have | Maintains inventory integrity for scarce artisanal goods. |
| OMS-02 | **WhatsApp Business API (Twilio):** Trigger real-time, automated transactional messages (Order Confirmation, Dispatch, Out for Delivery) directly to the user's phone number. | Must-Have | Aligns with regional communication preferences, drastically reducing "where is my order" queries. |
| OMS-03 | **Order Status State Machine:** Robust backend tracking of order lifecycle: `Pending` -> `Partially Paid` -> `Processing` -> `Shipped` -> `Delivered` -> `Completed`. | Must-Have | Provides a unified truth for fulfillment operations and customer tracking. |

### Administrative Governance
The secure back-office portal enabling internal teams to manage the ecosystem without developer intervention.

| ID | Requirement | Priority | Business Value |
|---|---|---|---|
| ADM-01 | **Centralized Dashboard:** Real-time overview of revenue, pending orders requiring dispatch, and low-stock alerts for variants. | Must-Have | Enables rapid decision-making for fulfillment and inventory replenishment. |
| ADM-02 | **Custom Analytics Engine:** Internal tracking of KPIs (AOV, Conversion Rate, Abandoned Carts) without heavy third-party scripts. | Must-Have | Maintains premium frontend performance while delivering actionable business intelligence. |
| ADM-03 | **Product & Category CRUD:** Intuitive Vue-based interfaces to add, edit, or deactivate categories, products, and variant pricing/stock. | Must-Have | Empowers business users to manage the catalog dynamically. |
| ADM-04 | **Order Fulfillment Workflow:** Interface to update order statuses, input tracking numbers, and manage the 70% COD collection reconciliation upon delivery. | Must-Have | Streamlines logistics and financial auditing. |

### 2025 Technological Integrations
Advanced features positioning the platform ahead of standard ecommerce implementations.

| ID | Requirement | Priority | Business Value |
|---|---|---|---|
| T25-01 | **Agentic AI Search Recommendations:** Utilize backend ML/AI (or LLM APIs) to analyze browsing patterns and suggest complementary products (e.g., matching Saffron with specific Dry Fruits). | Could-Have | Increases Average Order Value (AOV) by 5-15% through hyper-personalization. |
| T25-02 | **Omnichannel / Local Pickup (BOPIS):** Allow local customers (based on pincode) to opt for "Pick Up at Store" instead of complimentary shipping. | Could-Have | Drives foot traffic to physical retail locations and reduces logistical overhead. |

### Non-Functional Standards
The underlying architectural and compliance requirements ensuring a robust, enterprise-grade system.

| ID | Requirement | Priority | Business Value |
|---|---|---|---|
| NFS-01 | **Hybrid Cloud Scalability:** Frontend deployed on Vercel (Edge CDN for global speed), Backend on Render, Database on Aiven MySQL 8.0. | Must-Have | Ensures cost-effective scaling (starting at $0) while maintaining high availability. |
| NFS-02 | **Frontend Performance Profile:** Lighthouse scores >90 for Performance, Accessibility, and SEO. Implementation of aggressive caching and Vue Suspense. | Must-Have | Direct correlation to lower bounce rates and higher organic search rankings. |
| NFS-03 | **Data Privacy & Compliance:** Secure handling of PII, Bcrypt password hashing, and compliance with regional data protection standards. | Must-Have | Mitigates legal risk and builds consumer trust. |
| NFS-04 | **API-First Architecture:** Strict decoupling of the Vue.js frontend and Flask backend via RESTful APIs with comprehensive CORS configuration. | Must-Have | Enables future omnichannel expansion (e.g., native mobile apps) without rewriting core logic. |
| NFS-05 | **Test Isolation & BDD:** Automated testing pipelines that proactively replenish stock and clear state before runs to ensure reliable deployment verification. | Must-Have | Prevents regressions and accelerates the CI/CD deployment lifecycle. |
