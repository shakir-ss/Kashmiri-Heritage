# Comprehensive E-commerce & UAT Audit: "The Hundred Villages"

## Objective
To elevate the platform from a "6.5/10" to a "9.5/10" by identifying and fixing bugs, UX friction, and mobile-specific issues across the entire user journey. This audit will act as an "expert swarm" to simulate new users and an e-commerce specialist.

## Key Files & Context
- **Discovery:** `frontend/src/views/HomeView.vue`, `ProductsView.vue`, `ProductDetailView.vue`
- **Cart & Checkout:** `frontend/src/views/CartView.vue`, `CheckoutView.vue`, `frontend/src/stores/cartStore.js`
- **User Management:** `frontend/src/views/LoginView.vue`, `RegisterView.vue`, `OrdersView.vue`
- **Admin:** `frontend/src/views/AdminDashboard.vue`
- **Mobile Experience:** `frontend/src/assets/style.css`, `frontend/src/App.vue` (Responsive navigation)

## Phased Audit & Implementation Plan

### Phase 1: The "New User" Swarm (Auditing)
Use sub-agents to simulate three distinct personas and report on friction points.
1.  **Persona A (The High-End Shopper):** Focuses on "Artisanal Storytelling," image quality, and trust markers.
2.  **Persona B (The Mobile-First Commuter):** Focuses on navigation, button sizes, and responsiveness on small screens.
3.  **Persona C (The Practical Buyer):** Focuses on the Cart, quantity updates, "Partial COD" clarity, and shipping rules.

### Phase 2: Bug Hunting (Cart & Checkout)
- **Cart Logic:** Check for issues when updating quantities (e.g., negative numbers, exceeding stock).
- **Checkout Friction:** Verify validation error messages (are they "Artisanal" or "Broken"?).
- **Session Persistence:** Check if the cart survives a page refresh or login/logout.

### Phase 3: Mobile & UX Refinement
- **Sticky Navigation:** Ensure the header doesn't hide content on mobile.
- **Touch Targets:** Verify all "Add to Cart" and "Shop Now" buttons are easy to tap.
- **Hero Polish:** Final check on the "Shikara-Smooth" transition across different devices.

### Phase 4: Expert E-commerce Recommendation Report
- **Conversion Optimization:** Suggest "Cross-Sells" or "Frequently Bought Together" logic.
- **Trust Elements:** Verify SSL badges, secure payment icons, and "Hand-Inspected" markers.
- **Performance:** Review bundle size and lazy-loading opportunities.

## Verification & Testing
- **Lighthouse Pass:** Target 95+ in all categories.
- **BDD Regression:** Run the full `behave` suite to ensure no new bugs are introduced.
- **Manual "Blind" Walkthrough:** Final test by an agent simulating a first-time purchase.

---
*Next Action: Activate sub-agents for the "New User" Swarm Audit.*
