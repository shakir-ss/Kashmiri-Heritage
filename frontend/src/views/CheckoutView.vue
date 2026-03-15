<template>
  <div class="checkout-view container">
    <h2 class="section-title">Finalize Your Order</h2>
    
    <div v-if="successOrder" class="success-screen card">
      <div class="success-icon">✓</div>
      <h3>Order Placed Successfully!</h3>
      <p>Thank you for choosing Kashmiri Dry Fruits. Your order #{{ successOrder.id }} is being processed.</p>
      <div class="success-actions">
        <router-link to="/orders" class="btn btn-primary">View My Orders</router-link>
        <router-link to="/" class="btn btn-outline">Continue Shopping</router-link>
      </div>
    </div>

    <div v-else class="checkout-grid">
      <!-- Checkout Form -->
      <div class="checkout-form card">
        <h3>Shipping Information</h3>
        <form @submit.prevent="handleCheckout">
          <div class="form-group">
            <label for="full-name">Full Name</label>
            <input id="full-name" v-model="form.name" type="text" placeholder="Your full name" required />
          </div>
          <div class="form-group">
            <label for="phone">Phone Number</label>
            <input id="phone" v-model="form.phone" type="tel" placeholder="+91 XXXX XXX XXX" required />
          </div>
          <div class="form-group">
            <label for="address">Shipping Address</label>
            <textarea id="address" v-model="form.address" rows="4" placeholder="House/Apt No, Street, City, Pincode" required></textarea>
          </div>

          <div class="payment-section">
            <h4>Payment Method</h4>
            <div class="payment-options">
              <label class="payment-option active">
                <input type="radio" name="payment" checked />
                <span class="option-details">
                  <strong>Secure Online Payment</strong>
                  <small>Razorpay / Stripe / Cards</small>
                </span>
              </label>
            </div>
          </div>

          <button type="submit" class="btn btn-secondary btn-block mt-2" :disabled="loading">
            {{ loading ? 'Processing...' : 'Pay & Place Order' }}
          </button>
        </form>
      </div>

      <!-- Order Summary -->
      <div class="order-summary card">
        <h3>Order Summary</h3>
        <div class="summary-items">
          <div v-for="item in cartStore.items" :key="item.product_id" class="summary-item">
            <router-link :to="'/products/' + item.product_id" class="item-thumb">
              <img :src="item.image_url || 'https://via.placeholder.com/50'" :alt="item.name" />
            </router-link>
            <div class="item-info">
              <router-link :to="'/products/' + item.product_id" class="item-name-link">
                <span class="item-name">{{ item.name }}</span>
              </router-link>
              <span class="item-qty">Qty: {{ item.quantity }}</span>
            </div>
            <span class="item-price">₹{{ item.price * item.quantity }}</span>
          </div>
        </div>
        
        <div class="summary-totals">
          <div class="total-row">
            <span>Subtotal</span>
            <span>₹{{ cartStore.cartTotal }}</span>
          </div>
          <div class="total-row">
            <span>Shipping</span>
            <span class="free">FREE</span>
          </div>
          <hr />
          <div class="total-row grand-total">
            <span>Grand Total</span>
            <span>₹{{ cartStore.cartTotal }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCartStore } from '../stores/cartStore'
import { useAuthStore } from '../stores/authStore'
import axios from 'axios'

const cartStore = useCartStore()
const auth = useAuthStore()
const loading = ref(false)
const successOrder = ref(null)

const form = ref({
  name: auth.user?.name || '',
  address: '',
  phone: ''
})

const handleCheckout = async () => {
  loading.value = true
  try {
    console.log('Initializing Secure Payment Gateway...')
    const res = await axios.post('/api/orders/place', {
      address: form.value.address,
      phone: form.value.phone
    })
    successOrder.value = res.data
    cartStore.clearCart()
  } catch (err) {
    console.error('Checkout error:', err.response?.data || err.message)
    alert(err.response?.data?.message || 'Failed to place order')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.checkout-view {
  padding-top: 4rem;
  padding-bottom: 8rem;
}

.section-title {
  margin-bottom: 3rem;
  color: var(--primary);
  text-align: center;
}

.checkout-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 3rem;
  align-items: start;
}

.checkout-form h3, .order-summary h3 {
  margin-bottom: 2rem;
  font-size: 1.4rem;
  color: var(--primary);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  font-size: 0.85rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: #666;
}

.form-group input, .form-group textarea {
  width: 100%;
  padding: 1rem;
  border: 1px solid #eee;
  background: #f9f9f9;
  border-radius: 10px;
  font-family: inherit;
}

.payment-section {
  margin-top: 3rem;
}

.payment-section h4 {
  font-size: 1rem;
  margin-bottom: 1rem;
}

.payment-option {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  border: 2px solid var(--secondary);
  background: rgba(244, 164, 96, 0.05);
  border-radius: 12px;
  cursor: pointer;
}

.option-details strong {
  display: block;
  color: var(--primary);
}

.option-details small {
  color: #888;
}

.summary-items {
  margin-bottom: 2rem;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid #f5f5f5;
}

.item-thumb img {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: 6px;
}

.item-info {
  flex-grow: 1;
}

.item-name-link {
  text-decoration: none;
  color: inherit;
}

.item-name-link:hover .item-name {
  color: var(--secondary);
}

.item-name {
  display: block;
  font-weight: 600;
  font-size: 0.95rem;
}

.item-qty {
  font-size: 0.8rem;
  color: #888;
}

.summary-totals {
  background: #f9f9f9;
  padding: 1.5rem;
  border-radius: 12px;
}

.total-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
}

.grand-total {
  margin-top: 1rem;
  font-weight: 800;
  font-size: 1.25rem;
  color: var(--primary);
}

.free {
  color: var(--accent);
  font-weight: 700;
}

.success-screen {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
  padding: 4rem;
}

.success-icon {
  width: 80px;
  height: 80px;
  background: var(--accent);
  color: white;
  font-size: 3rem;
  border-radius: 50%;
  line-height: 80px;
  margin: 0 auto 2rem;
}

.success-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.btn-block {
  width: 100%;
}

.mt-2 { margin-top: 2rem; }

@media (max-width: 992px) {
  .checkout-grid {
    grid-template-columns: 1fr;
  }
}
</style>
