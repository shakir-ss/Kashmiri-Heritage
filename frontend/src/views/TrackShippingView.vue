<template>
  <div class="track-shipping container">
    <h2 class="section-title text-center">Track Your Order</h2>
    
    <div class="track-form-container card">
      <form @submit.prevent="trackOrder">
        <div class="form-group">
          <label>Order Reference Number</label>
          <input v-model="orderId" type="number" required placeholder="e.g. 1024" class="form-control" />
        </div>
        <div class="form-group">
          <label>Email Address</label>
          <input v-model="email" type="email" required placeholder="Email used during checkout" class="form-control" />
        </div>
        <button type="submit" class="btn btn-primary w-100 mt-3" :disabled="loading">
          {{ loading ? 'Locating...' : 'Track Package' }}
        </button>
      </form>
    </div>

    <div v-if="error" class="alert alert-danger mt-4 text-center">
      {{ error }}
    </div>

    <div v-if="orderInfo" class="track-results card mt-4">
      <h3>Order #{{ orderInfo.id }}</h3>
      <p><strong>Status:</strong> <span class="status-badge" :class="orderInfo.status">{{ orderInfo.status.replace('_', ' ').toUpperCase() }}</span></p>
      
      <div v-if="orderInfo.status === 'shipped' || orderInfo.status === 'out_for_delivery' || orderInfo.status === 'delivered'">
        <p v-if="orderInfo.tracking_number"><strong>Tracking Number:</strong> {{ orderInfo.tracking_number }}</p>
        <a v-if="orderInfo.tracking_link" :href="orderInfo.tracking_link" target="_blank" class="btn btn-secondary mt-2">
          Track on Courier Website
        </a>
      </div>
      <div v-else class="text-muted mt-2">
        <p>Your order is currently being processed by our artisans. Tracking details will appear here once dispatched.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const orderId = ref('')
const email = ref('')
const loading = ref(false)
const orderInfo = ref(null)
const error = ref('')

const trackOrder = async () => {
  loading.value = true
  error.value = ''
  orderInfo.value = null
  
  try {
    const res = await axios.get('/api/orders/track', {
      params: { order_id: orderId.value, email: email.value }
    })
    orderInfo.value = res.data
  } catch (err) {
    error.value = err.response?.data?.message || 'Unable to track order. Please check details.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.track-shipping {
  max-width: 600px;
  margin: 4rem auto;
}
.track-form-container {
  padding: 2rem;
}
.form-group {
  margin-bottom: 1.5rem;
}
.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 0.5rem;
}
.form-control {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-weight: bold;
  background: #e9ecef;
}
.status-badge.shipped { background: #cce5ff; color: #004085; }
.status-badge.delivered { background: #d4edda; color: #155724; }
</style>
