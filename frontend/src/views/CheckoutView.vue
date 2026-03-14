<template>
  <div class="checkout-view container">
    <h2 class="section-title">Finalize Your Order</h2>
    
    <div v-if="successOrder" class="success-screen">
      <div class="success-icon">✓</div>
      <h2>Order Placed Successfully!</h2>
      <p>A confirmation message has been sent to your WhatsApp.</p>
      <p>Order ID: #{{ successOrder }}</p>
      <router-link to="/products" class="btn btn-secondary mt-2">Continue Shopping</router-link>
    </div>

    <div v-else class="checkout-layout">
      <!-- Shipping Form -->
      <div class="shipping-info card">
        <h3>Shipping Details</h3>
        <form @submit.prevent="handleCheckout" class="checkout-form">
          <div class="form-group">
            <label>Full Address</label>
            <textarea v-model="form.address" placeholder="House/Apt No, Street, City, Pincode" required></textarea>
          </div>
          
          <div class="form-group">
            <label>WhatsApp Number</label>
            <input v-model="form.phone" type="tel" placeholder="+91 XXXX XXX XXX" required />
            <small>We'll send your order confirmation here.</small>
          </div>

          <div class="payment-method">
            <h3>Payment Method</h3>
            <div class="payment-option active">
              <input type="radio" checked />
              <label>Secured Payment Gateway (Razorpay/Stripe)</label>
            </div>
          </div>

          <button type="submit" class="btn btn-secondary btn-block" :disabled="loading">
            {{ loading ? 'Processing Payment...' : 'Pay & Place Order' }}
          </button>
        </form>
      </div>

      <!-- Summary -->
      <div class="order-preview card">
        <h3>Order Preview</h3>
        <div v-for="item in cartStore.items" :key="item.product_id" class="preview-item">
          <span>{{ item.quantity }}x {{ item.name }}</span>
          <span>₹{{ item.price * item.quantity }}</span>
        </div>
        <hr />
        <div class="total-row">
          <span>Total Amount</span>
          <span>₹{{ cartStore.cartTotal }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCartStore } from '../stores/cartStore'
import { useRouter } from 'vue-router'
import axios from 'axios'

const cartStore = useCartStore()
const router = useRouter()
const loading = ref(false)
const successOrder = ref(null)

const form = ref({
  address: '',
  phone: ''
})

const handleCheckout = async () => {
  loading.value = true
  try {
    // 1. Mock Payment (Simulation)
    console.log("Initializing Secure Payment Gateway...")
    await new Promise(resolve => setTimeout(resolve, 1500))

    // 2. Place Order in Backend
    const res = await axios.post('/api/orders/place', {
      address: form.value.address,
      phone: form.value.phone,
      payment_id: 'PAY_' + Math.random().toString(36).substr(2, 9)
    })

    // 3. Success handling
    successOrder.value = res.data.order_id
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
  padding-top: 3rem;
  max-width: 900px;
}

.section-title {
  margin-bottom: 2rem;
  color: var(--primary);
}

.checkout-layout {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: 2rem;
}

.card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: var(--shadow);
}

.card h3 {
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
  color: var(--primary);
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  font-size: 0.9rem;
}

.form-group textarea, .form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  outline: none;
}

.payment-method {
  margin: 2rem 0;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.payment-option {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #fdfaf5;
  border: 2px solid var(--secondary);
  border-radius: 8px;
}

.preview-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  font-size: 0.9rem;
}

.total-row {
  display: flex;
  justify-content: space-between;
  font-weight: 800;
  font-size: 1.2rem;
  color: var(--primary);
  margin-top: 1rem;
}

.success-screen {
  text-align: center;
  padding: 5rem 0;
  background: white;
  border-radius: 12px;
  box-shadow: var(--shadow);
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

.btn-block {
  width: 100%;
}

.mt-2 { margin-top: 2rem; }
</style>
