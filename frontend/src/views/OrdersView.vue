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
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const orders = ref([])
const loading = ref(true)

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
</style>
