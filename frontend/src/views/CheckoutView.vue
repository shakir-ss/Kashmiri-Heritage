<template>
  <div class="checkout-view container">
    <h2 class="section-title editorial">Complete Your Acquisition</h2>
    
    <div v-if="successOrder" class="success-screen card artisan-border">
      <div class="success-icon">✓</div>
      <h2>Order Secured Successfully!</h2>
      <p>Thank you for choosing Kashmiri treasures. Your commitment is our pride.</p>
      <div class="order-id">Transaction Reference: #{{ successOrder }}</div>
      <router-link to="/orders" class="btn btn-secondary mt-2">Track Your Heritage</router-link>
    </div>

    <div v-else class="checkout-grid">
      <!-- Checkout Form -->
      <div class="checkout-sections">
        <section class="checkout-form card">
          <h3 class="subsection-title">1. Shipping Destination</h3>
          <div class="form-body">
            <div class="form-group">
              <label for="full-name">Full Name</label>
              <input id="full-name" v-model="form.name" type="text" placeholder="Recipient's Name" required />
            </div>
            <div class="form-group">
              <label for="phone">Phone Number</label>
              <input id="phone" v-model="form.phone" type="tel" placeholder="+91 XXXX XXX XXX" required />
            </div>
            <div class="form-row">
              <div class="form-group flex-2">
                <label for="address">Shipping Address</label>
                <input id="address" v-model="form.address" placeholder="House/Apt No, Street, Landmark" required />
              </div>
              <div class="form-group flex-1">
                <label for="pincode">Area Pincode</label>
                <input id="pincode" v-model="form.pincode" type="text" placeholder="190001" required @input="updateShipping" />
              </div>
            </div>

          </div>
        </section>

        <section class="checkout-form card mt-2">
          <h3 class="subsection-title">2. Secure Payment Gateway</h3>
          <div class="payment-methods">
            <label class="payment-option" :class="{ selected: form.payment_mode === 'upi' }">
              <input type="radio" v-model="form.payment_mode" value="upi" name="payment" />
              <div class="opt-content">
                <span class="opt-label">Instant Confirmation (UPI)</span>
                <small>Secure your order immediately via PhonePe, GPay, or Paytm.</small>
              </div>
            </label>
            
            <label class="payment-option" :class="{ selected: form.payment_mode === 'cod' }">
              <input type="radio" v-model="form.payment_mode" value="cod" name="payment" />
              <div class="opt-content">
                <span class="opt-label">Partial COD (Trust & Commitment)</span>
                <small>Pay 30% now to initiate shipping, and the remaining 70% at your doorstep.</small>
              </div>
            </label>

            <label class="payment-option" :class="{ selected: form.payment_mode === 'card' }">
              <input type="radio" v-model="form.payment_mode" value="card" name="payment" />
              <div class="opt-content">
                <span class="opt-label">Debit / Credit Card</span>
                <small>Full secure payment via global banking networks.</small>
              </div>
            </label>
          </div>

          <!-- Psychological commitment message -->
          <div v-if="form.payment_mode === 'cod'" class="commitment-info">
            <div class="info-icon">💡</div>
            <div class="info-text">
              <strong>Smart Choice!</strong> By paying a small 30% commitment fee today (₹{{ prepaidAmount.toFixed(0) }}), you help us ensure these artisanal products are handled with priority care.
            </div>
          </div>

          <button @click="handleCheckout" class="btn btn-primary btn-block mt-2" :disabled="loading || cartStore.items.length === 0">
            <span v-if="!loading">
              {{ form.payment_mode === 'cod' ? `Confirm Order (Pay ₹${prepaidAmount.toFixed(0)} Now)` : 'Authorize Full Payment' }}
            </span>
            <span v-else>Securing Transaction...</span>
          </button>
        </section>
      </div>

      <!-- Order Summary Sidebar -->
      <aside class="order-summary-sidebar">
        <div class="order-summary card sticky-top">
          <h3 class="subsection-title">Order Summary</h3>
          <div class="summary-items">
            <div v-for="item in cartStore.items" :key="item.product_id" class="summary-item">
              <img :src="item.image_url || 'https://via.placeholder.com/50'" class="item-thumb" />
              <div class="item-info">
                <span class="item-name">{{ item.name }}</span>
                <span class="item-qty">Qty: {{ item.quantity }}</span>
              </div>
              <span class="item-price">₹{{ item.price * item.quantity }}</span>
            </div>
          </div>

          <div class="summary-totals">
            <div class="summary-row">
              <span>Merchandise Subtotal</span>
              <span>₹{{ subtotal }}</span>
            </div>
            <div class="summary-row">
              <span>Logistics & Handling</span>
              <span :class="{ 'free-shipping': deliveryCharge === 0 }">
                {{ deliveryCharge === 0 ? 'COMPLIMENTARY' : '₹' + deliveryCharge }}
              </span>
            </div>
            <div class="summary-row total-row">
              <span>Consolidated Total</span>
              <span>₹{{ total }}</span>
            </div>

            <!-- Breakdown for Partial COD -->
            <div v-if="form.payment_mode === 'cod'" class="payment-breakdown mt-2">
              <div class="breakdown-row highlight">
                <span>Due Today (30%)</span>
                <span>₹{{ prepaidAmount.toFixed(0) }}</span>
              </div>
              <div class="breakdown-row">
                <span>Pay on Arrival (70%)</span>
                <span>₹{{ balanceAmount.toFixed(0) }}</span>
              </div>
            </div>
          </div>
          
          <div class="trust-badges mt-2">
            <span>🛡️ SSL Secure</span>
            <span>📦 Priority Shipping</span>
            <span>✅ Hand-Inspected</span>
          </div>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCartStore } from '../stores/cartStore'
import { LOCAL_PINCODES } from '../config'
import axios from 'axios'

const cartStore = useCartStore()
const loading = ref(false)
const successOrder = ref(null)

const form = ref({
  name: '',
  phone: '',
  address: '',
  pincode: '',
  payment_mode: 'upi'
})

const subtotal = computed(() => {
  return cartStore.items.reduce((sum, item) => sum + (item.price * item.quantity), 0)
})

const deliveryCharge = ref(0)

const updateShipping = () => {
  if (form.value.pincode.length >= 6) {
    if (LOCAL_PINCODES.includes(form.value.pincode)) {
      deliveryCharge.value = 0
    } else {
      deliveryCharge.value = 50
    }
  }
}

const total = computed(() => subtotal.value + deliveryCharge.value)

// Partial COD Calculations
const prepaidAmount = computed(() => {
  if (form.value.payment_mode === 'cod') {
    return total.value * 0.30
  }
  return total.value
})

const balanceAmount = computed(() => {
  if (form.value.payment_mode === 'cod') {
    return total.value * 0.70
  }
  return 0
})

const handleCheckout = async () => {
  if (cartStore.items.length === 0) return
  if (!form.value.name || !form.value.address || !form.value.pincode) {
    alert('Please complete all shipping fields.')
    return
  }
  
  loading.value = true
  try {
    const res = await axios.post('/api/orders/place', {
      name: form.value.name,
      address: form.value.address,
      pincode: form.value.pincode,
      phone: form.value.phone,
      payment_mode: form.value.payment_mode
    })
    successOrder.value = res.data.order_id
    cartStore.clearCart()
  } catch (err) {
    alert(err.response?.data?.message || 'Transaction could not be completed.')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.checkout-view {
  padding-top: 3rem;
  padding-bottom: 6rem;
  background-color: #fbfbfb;
}

.editorial {
  font-family: 'Playfair Display', serif;
  font-size: 2.5rem;
  margin-bottom: 2.5rem;
  text-align: center;
  color: var(--primary);
}

.checkout-grid {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 3rem;
  align-items: start;
}

.subsection-title {
  font-size: 1.1rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--primary);
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 0.75rem;
}

.form-body {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.payment-methods {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.payment-option {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.25rem;
  border: 1px solid #eee;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: white;
}

.payment-option:hover {
  border-color: var(--secondary);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.payment-option.selected {
  border-color: var(--secondary);
  background: #fdfaf5;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.payment-option input {
  margin-top: 0.25rem;
}

.opt-content {
  display: flex;
  flex-direction: column;
}

.opt-label {
  font-weight: 700;
  color: var(--text-dark);
  font-size: 1rem;
}

.opt-content small {
  color: #777;
  margin-top: 0.25rem;
}

.commitment-info {
  margin-top: 1.5rem;
  padding: 1.25rem;
  background: #fff9f0;
  border-left: 4px solid var(--secondary);
  border-radius: 0 8px 8px 0;
  display: flex;
  gap: 1rem;
  align-items: center;
}

.info-icon { font-size: 1.5rem; }
.info-text { font-size: 0.9rem; color: #856404; line-height: 1.5; }

.order-summary {
  position: sticky;
  top: 2rem;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 0;
  border-bottom: 1px solid #f5f5f5;
}

.item-thumb {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid #eee;
}

.item-info { flex-grow: 1; }
.item-name { font-weight: 700; font-size: 0.95rem; color: var(--primary); }
.item-qty { font-size: 0.8rem; color: #888; }
.item-price { font-weight: 700; color: var(--text-dark); }

.summary-totals {
  margin-top: 1.5rem;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.75rem;
  font-weight: 600;
  color: #666;
  font-size: 0.9rem;
}

.total-row {
  font-size: 1.3rem;
  font-weight: 900;
  color: var(--primary);
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 2px solid var(--primary);
}

.free-shipping { color: #1e7e34; font-weight: 800; }

.payment-breakdown {
  background: #f8f9fa;
  padding: 1.25rem;
  border-radius: 8px;
}

.breakdown-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
}

.breakdown-row.highlight {
  color: var(--secondary);
  font-weight: 800;
  font-size: 1rem;
}

.trust-badges {
  display: flex;
  justify-content: space-between;
  font-size: 0.7rem;
  color: #aaa;
  font-weight: 700;
  text-transform: uppercase;
}

.artisan-border {
  border-top: 5px solid var(--secondary);
}

.success-screen { text-align: center; padding: 5rem 2rem; }
.success-icon { font-size: 5rem; color: #1e7e34; margin-bottom: 2rem; }

@media (max-width: 1024px) {
  .checkout-grid { grid-template-columns: 1fr; }
}
</style>
