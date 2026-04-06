<template>
  <div class="cart-view container">
    <h2 class="cart-title">Your Shopping Cart</h2>
    
    <div v-if="cartStore.items.length === 0" class="empty-cart">
      <p>Your cart is empty. The finest The Hundred Villages treasures are waiting for you!</p>
      <router-link to="/products" class="btn btn-secondary">Start Shopping</router-link>
    </div>

    <div v-else class="cart-layout">
      <!-- Cart Items -->
      <div class="cart-items">
        <div 
          v-for="item in cartStore.items" 
          :key="item.product_id" 
          class="cart-item"
          :class="{ 'out-of-stock-item': item.stock <= 0 }"
        >
          <router-link :to="'/products/' + item.product_id" class="item-link">
            <img :src="item.image_url || 'https://via.placeholder.com/80'" :alt="item.name" />
          </router-link>
          <div class="item-details">
            <router-link :to="'/products/' + item.product_id" class="item-name-link">
              <h4>{{ item.name }}</h4>
            </router-link>
            <p class="price">₹{{ item.price }}</p>
            <div class="stock-status-msg">
              <p v-if="item.stock > 0" class="stock-info" :class="{ 'low-stock': item.stock <= 5 }">
                {{ item.stock }} available
              </p>
              <p v-else class="stock-info out-of-stock-text">
                ⚠️ Currently Out of Stock
              </p>
            </div>
            <div class="cart-item-actions">
              <button @click="cartStore.moveToWishlist(item.product_id)" class="btn-text">Save to Wishlist</button>
              <span class="divider">|</span>
              <button @click="handleQuantityUpdate(item.product_id, 0)" class="btn-text remove">Remove</button>
            </div>
          </div>
          <div class="quantity-controls" :class="{ disabled: item.stock <= 0 }">
            <button 
              @click="handleQuantityUpdate(item.product_id, item.quantity - 1)" 
              class="btn-qty"
              :disabled="item.stock <= 0"
              aria-label="Decrease quantity"
            >
              <span v-if="item.quantity > 1">-</span>
              <span v-else class="delete-icon">🗑️</span>
            </button>
            <span class="qty-display">{{ item.quantity }}</span>
            <button 
              @click="handleQuantityUpdate(item.product_id, item.quantity + 1)" 
              class="btn-qty"
              :disabled="item.quantity >= item.stock || item.stock <= 0"
              aria-label="Increase quantity"
            >+</button>
          </div>
          <div class="item-total">
            <span v-if="item.stock > 0">₹{{ item.price * item.quantity }}</span>
            <span v-else class="unavailable">Unavailable</span>
          </div>
        </div>
      </div>

      <!-- Order Summary -->
      <aside class="summary">
        <h3>Order Summary</h3>
        <div class="summary-row">
          <span>Subtotal</span>
          <span>₹{{ cartStore.cartTotal }}</span>
        </div>
        <div class="summary-row">
          <span>Delivery</span>
          <span class="free">FREE</span>
        </div>
        <hr />
        <div class="summary-row total">
          <span>Total</span>
          <span>₹{{ cartStore.cartTotal }}</span>
        </div>
        
        <button @click="proceedToCheckout" class="btn btn-secondary btn-block">
          Proceed to Checkout
        </button>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { useCartStore } from '../stores/cartStore'
import { useRouter } from 'vue-router'

const cartStore = useCartStore()
const router = useRouter()

const handleQuantityUpdate = (productId, newQuantity) => {
  if (newQuantity <= 0) {
    if (confirm('Are you sure you want to remove this Kashmiri treasure from your cart?')) {
      cartStore.updateQuantity(productId, 0)
    }
  } else {
    cartStore.updateQuantity(productId, newQuantity)
  }
}

const proceedToCheckout = () => {
  router.push('/checkout')
}
</script>

<style scoped>
.cart-view {
  padding-top: 3rem;
  padding-bottom: 5rem;
}

.cart-title {
  font-family: 'Playfair Display', serif;
  font-size: 2.5rem;
  margin-bottom: 2rem;
  color: var(--primary);
  text-align: center;
}

.empty-cart {
  text-align: center;
  padding: 5rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: var(--shadow);
  max-width: 600px;
  margin: 0 auto;
}

.empty-cart p {
  margin-bottom: 2rem;
  color: #666;
  font-size: 1.1rem;
}

.cart-layout {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 2rem;
  align-items: start;
}

.cart-item {
  display: flex;
  align-items: center;
  background: white;
  padding: 1.25rem;
  border-radius: 12px;
  margin-bottom: 1rem;
  box-shadow: var(--shadow);
  transition: transform 0.2s;
}

.cart-item:hover {
  transform: translateX(5px);
}

.cart-item img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 10px;
  margin-right: 1.5rem;
  border: 1px solid #f0f0f0;
}

.item-details {
  flex-grow: 1;
}

.item-details h4 {
  font-family: 'Playfair Display', serif;
  font-size: 1.2rem;
  color: var(--primary);
  margin-bottom: 0.5rem;
}

.item-name-link {
  text-decoration: none;
}

.item-name-link:hover h4 {
  color: var(--secondary);
}

.price {
  font-weight: 700;
  color: var(--text-dark);
}

.stock-info {
  font-size: 0.75rem;
  color: #888;
  margin-top: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.stock-info.low-stock {
  color: #d00;
  font-weight: 800;
}

.cart-item-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 0.75rem;
}

.btn-text {
  background: none;
  border: none;
  padding: 0;
  font-size: 0.8rem;
  font-weight: 700;
  color: #888;
  cursor: pointer;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  transition: color 0.2s;
}

.btn-text:hover {
  color: var(--secondary);
}

.btn-text.remove:hover {
  color: #d00;
}

.divider {
  color: #eee;
  font-size: 0.8rem;
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-right: 2rem;
}

.qty-display {
  font-weight: 800;
  font-size: 1.1rem;
  min-width: 30px;
  text-align: center;
}

.btn-qty {
  width: 44px; /* Standard Touch Target Size */
  height: 44px;
  border-radius: 50%;
  border: 2px solid #eee;
  background: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1.2rem;
  transition: all 0.2s;
}

.btn-qty:hover:not(:disabled) {
  border-color: var(--secondary);
  color: var(--secondary);
  background: #fffcf5;
}

.btn-qty:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.delete-icon {
  font-size: 1rem;
}

.item-total {
  font-weight: 900;
  font-size: 1.1rem;
  width: 120px;
  text-align: right;
  color: var(--primary);
}

.item-total .unavailable {
  color: #d00;
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
}

/* Out of Stock Handling */
.out-of-stock-item {
  opacity: 0.6;
  background: #fdfdfd;
  filter: grayscale(0.5);
}

.out-of-stock-text {
  color: #d00 !important;
  font-weight: 800;
}

.quantity-controls.disabled {
  pointer-events: none;
  opacity: 0.5;
}

.summary {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: var(--shadow);
  border-top: 4px solid var(--secondary);
}

.summary h3 {
  font-family: 'Playfair Display', serif;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #f0f0f0;
  padding-bottom: 0.75rem;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1.25rem;
  font-weight: 600;
}

.summary-row.total {
  font-size: 1.5rem;
  font-weight: 900;
  color: var(--primary);
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 2px solid var(--primary);
}

.free {
  color: var(--accent);
  font-weight: 800;
}

.btn-block {
  width: 100%;
  padding: 1rem;
  font-size: 1rem;
}

@media (max-width: 768px) {
  .cart-layout {
    grid-template-columns: 1fr;
  }
  
  .cart-item {
    flex-direction: column;
    text-align: center;
    gap: 1.25rem;
    padding: 1.5rem;
  }

  .cart-item img {
    margin-right: 0;
    width: 150px;
    height: 150px;
  }

  .quantity-controls {
    margin-right: 0;
    justify-content: center;
    background: #fbfbfb;
    padding: 0.5rem;
    border-radius: 50px;
    width: 100%;
  }

  .item-total {
    width: 100%;
    text-align: center;
    border-top: 1px solid #f0f0f0;
    padding-top: 1rem;
    font-size: 1.3rem;
  }

  .summary {
    margin-top: 1rem;
  }
}
</style>
