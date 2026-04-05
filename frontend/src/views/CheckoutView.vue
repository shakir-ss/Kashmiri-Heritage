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
            <div class="form-row">
              <div class="form-group flex-1">
                <label for="full-name">Full Name</label>
                <div class="input-wrapper" :class="{ 'error': errors.name }">
                  <span class="input-icon">👤</span>
                  <input id="full-name" v-model="form.name" type="text" placeholder="Recipient's Name" @blur="validateField('name')" />
                </div>
                <span class="error-text" v-if="errors.name">{{ errors.name }}</span>
              </div>
              <div class="form-group flex-1">
                <label for="phone">Phone Number</label>
                <div class="input-wrapper" :class="{ 'error': errors.phone }">
                  <span class="input-icon">📞</span>
                  <input id="phone" v-model="form.phone" type="tel" placeholder="+91XXXXXXXXXX" @blur="validateField('phone')" />
                </div>
                <span class="error-text" v-if="errors.phone">{{ errors.phone }}</span>
              </div>
            </div>

            <div class="form-group">
              <label for="address">Street Address</label>
              <div class="input-wrapper" :class="{ 'error': errors.address }">
                <span class="input-icon">🏠</span>
                <input id="address" v-model="form.address" placeholder="House/Apt No, Street, Landmark" @blur="validateField('address')" />
              </div>
              <span class="error-text" v-if="errors.address">{{ errors.address }}</span>
            </div>

            <div class="form-row">
              <div class="form-group flex-1">
                <label for="country">Country</label>
                <div class="input-wrapper">
                  <span class="input-icon">🌍</span>
                  <select id="country" v-model="form.country" @change="validateField('country')">
                    <option v-for="c in countries" :key="c" :value="c">{{ c }}</option>
                  </select>
                </div>
              </div>
              <div class="form-group flex-1">
                <label for="state">State / Province</label>
                <div class="input-wrapper" :class="{ 'error': errors.state }">
                  <span class="input-icon">🏛️</span>
                  <select v-if="form.country === 'India'" id="state" v-model="form.state">
                    <option v-for="s in indianStates" :key="s" :value="s">{{ s }}</option>
                  </select>
                  <input v-else id="state" v-model="form.state" placeholder="State/Province" @blur="validateField('state')" />
                </div>
                <span class="error-text" v-if="errors.state">{{ errors.state }}</span>
              </div>
            </div>

            <div class="form-row">
              <div class="form-group flex-1">
                <label for="city">City</label>
                <div class="input-wrapper" :class="{ 'error': errors.city }">
                  <span class="input-icon">🏙️</span>
                  <input id="city" v-model="form.city" placeholder="City" @blur="validateField('city')" />
                </div>
                <span class="error-text" v-if="errors.city">{{ errors.city }}</span>
              </div>
              <div class="form-group flex-1">
                <label for="pincode">Area Pincode</label>
                <div class="input-wrapper" :class="{ 'error': errors.pincode }">
                  <span class="input-icon">📮</span>
                  <input id="pincode" v-model="form.pincode" type="text" placeholder="190001" @input="updateShipping" @blur="validateField('pincode')" />
                </div>
                <span class="error-text" v-if="errors.pincode">{{ errors.pincode }}</span>
                <small class="hint-text" v-if="form.pincode.length >= 6 && deliveryCharge === 0">✨ Local Pincode Detected: Complimentary Shipping Applied</small>
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

            <!-- Development Only: Mock Payment Bypass -->
            <label 
              v-if="showMockPayment"
              class="payment-option mock-test-option" 
              :class="{ selected: form.payment_mode === 'mock' }"
              style="border: 2px dashed #ff4757; background: #fff5f6;"
            >
              <input type="radio" v-model="form.payment_mode" value="mock" name="payment" />
              <div class="opt-content">
                <span class="opt-label" style="color: #ff4757;">⚠️ QA Mock Payment (Test Only)</span>
                <small>Instantly bypass gateway for regression testing.</small>
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

          <div class="form-group mt-2">
            <label class="checkbox-container">
              <input type="checkbox" v-model="form.agreed" />
              <span class="checkmark"></span>
              <span class="checkbox-label">I agree to the Terms of Service and acknowledge the 30% commitment fee for Partial COD.</span>
            </label>
            <span class="error-text" v-if="errors.agreed">{{ errors.agreed }}</span>
          </div>

          <div class="payment-trust-footer mt-2">
            <div class="payment-icons">
              <img v-show="false" src="https://upload.wikimedia.org/wikipedia/commons/5/5e/Visa_Inc._logo.svg" alt="Visa" />
              <img v-show="false" src="https://upload.wikimedia.org/wikipedia/commons/2/2a/Mastercard-logo.svg" alt="Mastercard" />
              <img src="https://upload.wikimedia.org/wikipedia/commons/b/b5/PayPal.svg" alt="PayPal" />
              <img src="https://upload.wikimedia.org/wikipedia/commons/f/f2/Google_Pay_Logo.svg" alt="Google Pay" />
              <img src="https://upload.wikimedia.org/wikipedia/commons/9/98/Phonepe.svg" alt="PhonePe" />
              <img src="https://upload.wikimedia.org/wikipedia/commons/e/e1/UPI-Logo-vector.svg" alt="UPI" />
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

            <!-- Estimated Delivery -->
            <div class="estimated-delivery mt-2">
              <div class="est-label">📅 Estimated Arrival</div>
              <div class="est-date">{{ estimatedDate }}</div>
              <small class="est-hint">Via Priority Artisan Logistics</small>
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
import { ref, computed, onMounted } from 'vue'
import { useCartStore } from '../stores/cartStore'
import { useAuthStore } from '../stores/authStore'
import { LOCAL_PINCODES } from '../config'
import axios from 'axios'

const cartStore = useCartStore()
const authStore = useAuthStore()
const loading = ref(false)
const successOrder = ref(null)
// const isDev = import.meta.env.DEV
const showMockPayment = import.meta.env.DEV || import.meta.env.VITE_ENABLE_MOCK_PAYMENT === 'true';

const countries = ['India', 'United States', 'United Kingdom', 'United Arab Emirates', 'Canada', 'Australia']
const indianStates = [
  'Jammu & Kashmir', 'Delhi', 'Maharashtra', 'Karnataka', 'Punjab', 'Kerala', 'Ladakh'
]

const form = ref({
  name: '',
  phone: '',
  address: '',
  city: '',
  state: 'Jammu & Kashmir',
  country: 'India',
  pincode: '',
  payment_mode: 'upi',
  agreed: false
})

const errors = ref({
  name: '',
  phone: '',
  address: '',
  city: '',
  state: '',
  pincode: '',
  agreed: ''
})

// Auto-fill from user profile
onMounted(() => {
  if (authStore.isAuthenticated && authStore.user) {
    form.value.name = authStore.user.name || ''
  }
})

const validateField = (field) => {
  errors.value[field] = ''
  
  if (field === 'name' && !form.value.name) errors.value.name = 'Full name is required'
  if (field === 'phone') {
    const phoneRegex = /^[0-9+\s]{10,20}$/
    if (!form.value.phone) errors.value.phone = 'Phone number is required'
    else if (!phoneRegex.test(form.value.phone)) errors.value.phone = 'Invalid phone format'
  }
  if (field === 'address' && !form.value.address) errors.value.address = 'Street address is required'
  if (field === 'city' && !form.value.city) errors.value.city = 'City is required'
  if (field === 'pincode') {
    if (!form.value.pincode) errors.value.pincode = 'Pincode is required'
    else if (form.value.pincode.length < 5) errors.value.pincode = 'Pincode too short'
  }
  if (field === 'agreed' && !form.value.agreed) errors.value.agreed = 'Please agree to terms'
}

const validateAll = () => {
  validateField('name')
  validateField('phone')
  validateField('address')
  validateField('city')
  validateField('pincode')
  validateField('agreed')
  return !Object.values(errors.value).some(e => e !== '')
}

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

const estimatedDate = computed(() => {
  const today = new Date()
  const startDays = deliveryCharge.value === 0 ? 2 : 5
  const endDays = deliveryCharge.value === 0 ? 4 : 8
  
  const startDate = new Date(today)
  startDate.setDate(today.getDate() + startDays)
  
  const endDate = new Date(today)
  endDate.setDate(today.getDate() + endDays)
  
  const options = { month: 'short', day: 'numeric' }
  return `${startDate.toLocaleDateString('en-IN', options)} - ${endDate.toLocaleDateString('en-IN', options)}`
})

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
  if (!validateAll()) return
  
  loading.value = true
  try {
    // 1. Create Order & Handshake with Backend
    const res = await axios.post('/api/orders/place', {
      name: form.value.name,
      address: form.value.address,
      city: form.value.city,
      state: form.value.state,
      country: form.value.country,
      pincode: form.value.pincode,
      phone: form.value.phone,
      payment_mode: form.value.payment_mode
    })

    const orderData = res.data;

    // --- MOCK PAYMENT BYPASS (Dev Only) ---
    if (form.value.payment_mode === 'mock') {
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate delay
      const verifyRes = await axios.post('/api/orders/verify', {
        razorpay_order_id: orderData.razorpay_order_id || 'mock_order_id',
        razorpay_payment_id: 'mock_payment_' + Date.now(),
        razorpay_signature: 'mock_signature',
        order_id: orderData.order_id
      });
      successOrder.value = verifyRes.data.order_id;
      cartStore.clearCart();
      return;
    }

    // 2. Configure Razorpay Options
    const options = {
      key: orderData.key,
      amount: Math.round(orderData.amount * 100),
      currency: "INR",
      name: "The Hundred Villages",
      description: "Premium Kashmiri Acquisition",
      order_id: orderData.razorpay_order_id,
      handler: async function (response) {
        // 3. Verify Payment with Backend (Final Handshake)
        try {
          const verifyRes = await axios.post('/api/orders/verify', {
            razorpay_order_id: response.razorpay_order_id,
            razorpay_payment_id: response.razorpay_payment_id,
            razorpay_signature: response.razorpay_signature,
            order_id: orderData.order_id
          });
          successOrder.value = verifyRes.data.order_id;
          cartStore.clearCart();
        } catch (err) {
          alert("Payment verification failed. Please contact support.");
        }
      },
      prefill: {
        name: form.value.name,
        contact: form.value.phone
      },
      theme: {
        color: "#3d2b1f" // Walnut Brown
      }
    };

    const rzp = new window.Razorpay(options);
    rzp.open();

  } catch (err) {
    const msg = err.response?.data?.message || err.message;
    successOrder.value = 'DEBUG_ERROR: ' + msg;
    console.error("CHECKOUT_ERROR:", msg);
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
  gap: 1.5rem;
}

.form-row {
  display: flex;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.flex-2 { flex: 2; }
.flex-1 { flex: 1; }

.form-group label {
  display: block;
  font-weight: 700;
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
  color: #555;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1rem;
  font-size: 1.1rem;
  color: #aaa;
  pointer-events: none;
}

.input-wrapper input, .input-wrapper select {
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
  border: 2px solid #eee;
  border-radius: 12px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
}

.input-wrapper select {
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' fill='%23aaa' viewBox='0 0 16 16'%3E%3Cpath d='M7.247 11.14 2.451 5.658C1.885 5.013 2.345 4 3.204 4h9.592a1 1 0 0 1 .753 1.659l-4.796 5.48a1 1 0 0 1-1.506 0z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
}

.input-wrapper.error input {
  border-color: #d00;
}

.input-wrapper input:focus, .input-wrapper select:focus {
  border-color: var(--secondary);
  outline: none;
  box-shadow: 0 0 0 4px rgba(244, 196, 48, 0.1);
}

.error-text {
  color: #d00;
  font-size: 0.75rem;
  font-weight: 700;
  margin-top: 0.4rem;
}

.hint-text {
  display: block;
  margin-top: 0.5rem;
  color: #1e7e34;
  font-weight: 700;
  font-size: 0.8rem;
}

/* Checkbox Styles */
.checkbox-container {
  display: flex;
  align-items: flex-start;
  position: relative;
  padding-left: 35px;
  cursor: pointer;
  font-size: 0.9rem;
  user-select: none;
}

.checkbox-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  position: absolute;
  top: 0;
  left: 0;
  height: 22px;
  width: 22px;
  background-color: #eee;
  border-radius: 6px;
  transition: all 0.2s;
}

.checkbox-container:hover input ~ .checkmark {
  background-color: #ccc;
}

.checkbox-container input:checked ~ .checkmark {
  background-color: var(--secondary);
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

.checkbox-container input:checked ~ .checkmark:after {
  display: block;
}

.checkbox-container .checkmark:after {
  left: 8px;
  top: 4px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 3px 3px 0;
  transform: rotate(45deg);
}

.checkbox-label {
  line-height: 1.4;
  color: #666;
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
  accent-color: var(--secondary);
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

.payment-trust-footer {
  text-align: center;
  border-top: 1px solid #f0f0f0;
  padding-top: 1.5rem;
}

.payment-icons {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
  opacity: 0.6;
}

.payment-icons img {
  height: 24px;
}

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

.estimated-delivery {
  background: #f0f7ff;
  padding: 1.25rem;
  border-radius: 12px;
  margin-top: 1.5rem;
  border: 1px solid #cfe2ff;
}

.est-label {
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  color: #0056b3;
  margin-bottom: 0.25rem;
}

.est-date {
  font-size: 1.1rem;
  font-weight: 800;
  color: var(--primary);
}

.est-hint {
  font-size: 0.7rem;
  color: #6c757d;
  display: block;
  margin-top: 0.25rem;
}

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
  .checkout-grid { grid-template-columns: 1fr; gap: 2rem; }
  .form-row { flex-direction: column; gap: 1.25rem; }
}
</style>
