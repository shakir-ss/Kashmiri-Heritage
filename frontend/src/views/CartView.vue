<template>
  <div class="cart-view container">
    <h2 class="cart-title">Your Shopping Cart</h2>
    
    <div v-if="cartStore.items.length === 0" class="empty-cart">
      <p>Your cart is empty. The finest Kashmiri dry fruits are waiting for you!</p>
      <router-link to="/products" class="btn btn-secondary">Start Shopping</router-link>
    </div>

    <div v-else class="cart-layout">
      <!-- Cart Items -->
      <div class="cart-items">
        <div v-for="item in cartStore.items" :key="item.product_id" class="cart-item">
          <img :src="item.image_url || 'https://via.placeholder.com/80'" :alt="item.name" />
          <div class="item-details">
            <h4>{{ item.name }}</h4>
            <p class="price">₹{{ item.price }}</p>
          </div>
          <div class="quantity-controls">
            <button @click="cartStore.updateQuantity(item.product_id, item.quantity - 1)" class="btn-qty">-</button>
            <span>{{ item.quantity }}</span>
            <button @click="cartStore.updateQuantity(item.product_id, item.quantity + 1)" class="btn-qty">+</button>
          </div>
          <div class="item-total">
            ₹{{ item.price * item.quantity }}
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

const proceedToCheckout = () => {
  router.push('/checkout')
}
</script>

<style scoped>
.cart-view {
  padding-top: 3rem;
}

.cart-title {
  margin-bottom: 2rem;
  color: var(--primary);
}

.empty-cart {
  text-align: center;
  padding: 5rem 0;
  background: white;
  border-radius: 12px;
  box-shadow: var(--shadow);
}

.empty-cart p {
  margin-bottom: 2rem;
  color: #666;
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
  padding: 1rem;
  border-radius: 12px;
  margin-bottom: 1rem;
  box-shadow: var(--shadow);
}

.cart-item img {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
  margin-right: 1.5rem;
}

.item-details {
  flex-grow: 1;
}

.item-details h4 {
  color: var(--primary);
  margin-bottom: 0.25rem;
}

.quantity-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-right: 2rem;
}

.btn-qty {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1px solid #ddd;
  background: white;
  cursor: pointer;
}

.btn-qty:hover {
  border-color: var(--secondary);
  color: var(--secondary);
}

.item-total {
  font-weight: 800;
  width: 100px;
  text-align: right;
  color: var(--accent);
}

.summary {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: var(--shadow);
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.summary-row.total {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--primary);
  margin-top: 1rem;
}

.free {
  color: var(--accent);
  font-weight: 700;
}

.btn-block {
  width: 100%;
  margin-top: 2rem;
}
</style>
