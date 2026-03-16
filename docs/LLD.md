# Low-Level Design (LLD): Technical Specifications

## 1. Data Model Deep Dive
### Product & Variants
Products are modeled with a base price. Flexible options are handled via the `ProductVariant` table:
*   `price_modifier`: A float value added to the base product price.
*   `stock`: Unique inventory count for each variant.
*   `SKU`: Unique identifier for logistics and tracking.

### Orders & Payments
To support Partial COD, the `Order` model includes:
*   `total_amount`: The grand total including shipping.
*   `prepaid_amount`: Calculated as `total * 0.30` during checkout.
*   `balance_on_delivery`: Calculated as `total * 0.70`.
*   `status`: Initialized as `partial_paid` for COD orders.

## 2. Key Algorithms & Logic
### Shipping Calculation
Implemented in `backend/routes/orders.py` and mirrored in `CheckoutView.vue` for real-time UI updates:
```python
LOCAL_PINCODES = [...] # List maintained in config.js/backend constants
if pincode in LOCAL_PINCODES:
    shipping = 0.0
else:
    shipping = 50.0
```

### Stock Management
The backend implements **Atomic Deductions**. During `place_order`, stock is checked and deducted within a database transaction to prevent overselling:
```python
if product.stock < item.quantity:
    return error
product.stock -= item.quantity
```

## 3. API Contract Patterns
*   **Response Format:** Standardized JSON objects with `message` and data payload.
*   **Status Codes:** 
    *   `201`: Successful creation (Product, Cart Item, User).
    *   `200`: Successful fetch or update.
    *   `400/404`: Client-side data or existence error.
    *   `401/403`: Authentication or Authorization failures.

## 4. Frontend State Orchestration
Using **Pinia**, the application maintains multiple synchronized stores:
*   `authStore`: Manages JWT persistence and user role metadata.
*   `cartStore`: Handles `localStorage` persistence and automatic backend synchronization upon item addition.
*   `productStore`: Buffers the catalog and category lists to reduce redundant API calls.
