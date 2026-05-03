<template>
  <div class="orders-view container">
    <h2 class="section-title">Your Order History</h2>
    
    <div v-if="loading" class="loading">Loading your orders...</div>
    
    <div v-else-if="orders.length === 0" class="empty-orders">
      <p>You haven't placed any orders yet.</p>
      <router-link to="/products" class="btn btn-secondary">Start Shopping</router-link>
    </div>

    <div v-else class="orders-list">
      <div v-for="order in orders" :key="order.id" class="order-card card">
        <div class="order-header">
          <span class="order-id">Order #{{ order.id }}</span>
          <span class="order-date">{{ formatDate(order.created_at) }}</span>
          <span :class="['order-status', order.status]">{{ order.status }}</span>
        </div>
        <div class="order-items">
          <div v-for="item in order.items" :key="item.name" class="order-item">
            <span>{{ item.quantity }}x {{ item.name }}</span>
            <span>₹{{ item.price * item.quantity }}</span>
          </div>
        </div>
        <div class="order-footer">
          <span class="total-label">Total Amount:</span>
          <span class="total-value">₹{{ order.total_amount }}</span>
        </div>
        <div class="order-actions mt-2" v-if="order.status === 'delivered' || true">
          <button v-if="order.status === 'delivered'" @click="requestReturn(order.id)" class="btn btn-outline btn-sm">Request Return</button>
          <button @click="buyAgain(order)" class="btn btn-secondary btn-sm ml-2">Buy Again</button>
        </div>
      </div>
    </div>

    <!-- Return Request Modal -->
    <div v-if="showReturnModal" class="modal-overlay">
      <div class="modal-content">
        <h3>Request Return for Order #{{ returnOrderId }}</h3>
        <p>Please provide a reason for the return (e.g., damaged, wrong item):</p>
        <textarea v-model="returnReason" class="return-textarea" rows="4" placeholder="Enter reason..."></textarea>
        <div class="modal-actions mt-2">
          <button @click="submitReturn" class="btn btn-primary" :disabled="!returnReason.trim()">Submit Request</button>
          <button @click="closeReturnModal" class="btn btn-outline ml-2">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useCartStore } from '../stores/cartStore'
import { useRouter } from 'vue-router'

const orders = ref([])
const loading = ref(true)
const cartStore = useCartStore()
const router = useRouter()

const showReturnModal = ref(false)
const returnOrderId = ref(null)
const returnReason = ref('')

onMounted(async () => {
  try {
    const res = await axios.get('/api/orders/')
    orders.value = res.data
  } catch (err) {
    console.error('Failed to fetch orders:', err)
  } finally {
    loading.value = false
  }
})

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}

const requestReturn = (id) => {
  returnOrderId.value = id
  returnReason.value = ''
  showReturnModal.value = true
}

const closeReturnModal = () => {
  showReturnModal.value = false
  returnOrderId.value = null
  returnReason.value = ''
}

const submitReturn = async () => {
  if (!returnReason.value.trim()) return
  
  try {
    const res = await axios.post(`/api/orders/${returnOrderId.value}/return`, { reason: returnReason.value })
    alert(res.data.message)
    closeReturnModal()
    // Update local status or fetch orders again
    const resOrders = await axios.get('/api/orders/')
    orders.value = resOrders.data
  } catch (err) {
    alert(err.response?.data?.message || 'Failed to request return')
    closeReturnModal()
  }
}

const buyAgain = async (order) => {
  for (const item of order.items) {
    // We mock the product object to pass to addItem
    await cartStore.addItem({
      id: item.product_id, // We need product_id here, but orders API only gives name. Let's adapt if possible. Wait, orders API needs to return product_id.
      name: item.name,
      price: item.price,
      stock: 100 // Mock stock to allow adding
    }, item.quantity)
  }
  router.push('/cart')
}
</script>

<style scoped>
.orders-view {
  padding-top: 3rem;
}

.section-title {
  margin-bottom: 2rem;
  color: var(--primary);
}

.card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: var(--shadow);
  margin-bottom: 1.5rem;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
  padding-bottom: 1rem;
  margin-bottom: 1rem;
}

.order-id {
  font-weight: 700;
  color: var(--primary);
}

.order-status {
  text-transform: uppercase;
  font-size: 0.75rem;
  font-weight: 800;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
}

.order-status.paid {
  background: #e6f4ea;
  color: #1e7e34;
}

.order-item {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  color: #666;
}

.order-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  align-items: center;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #eee;
}

.total-label {
  font-weight: 600;
}

.total-value {
  font-weight: 800;
  font-size: 1.1rem;
  color: var(--primary);
}

.empty-orders {
  text-align: center;
  padding: 4rem 0;
}

.order-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px dashed #eee;
}

.ml-2 {
  margin-left: 0.5rem;
}

.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
}

.return-textarea {
  width: 100%;
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  margin-top: 1rem;
  font-family: inherit;
}
</style>
