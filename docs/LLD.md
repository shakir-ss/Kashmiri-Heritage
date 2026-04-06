# Low-Level Design (LLD): Technical Specifications

## 1. Data Model Deep Dive
### Product & Variants
Products are modeled with a base price. Flexible options are handled via the `ProductVariant` table:
*   `price_modifier`: A float value added to the base product price.
*   `stock`: Unique inventory count for each variant.
*   `SKU`: Unique identifier for logistics and tracking.

### Orders & Payments
To support Partial COD and Razorpay integration, the `Order` model includes:
*   `total_amount`: The grand total including shipping.
*   `prepaid_amount`: The amount paid upfront (Full for UPI/Card, 30% for COD).
*   `balance_on_delivery`: The remaining 70% for COD orders.
*   `status`: Initialized as `pending` during the handshake. Transitions to `paid` or `partial_paid` only after the `/verify` endpoint confirms the payment signature.

## 2. Key Algorithms & Logic
### Shipping Calculation
Implemented in `backend/routes/orders.py` and mirrored in `CheckoutView.vue` for real-time UI updates:
```python
LOCAL_PINCODES = [...] # Pincodes maintained for Kashmiri heritage radius
if pincode in LOCAL_PINCODES:
    shipping = 0.0
else:
    shipping = 50.0
```

### Stock Management
Stock is handled via **Deferred Deduction**. During `place_order`, stock is verified but not deducted. Actual deduction occurs only during the `verify_payment` phase to ensure inventory is only reduced for successful transactions:
```python
# During /api/orders/verify
for item in order.items:
    item.product.stock -= item.quantity
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
