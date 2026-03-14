<template>
  <div class="admin-dashboard container">
    <header class="admin-header">
      <h1>Admin Insights & Inventory</h1>
      <div class="header-actions">
        <button @click="analyticsStore.fetchStats()" class="btn btn-outline btn-sm">Refresh Stats</button>
        <button @click="showAddModal = true" class="btn btn-secondary">+ Add New Product</button>
      </div>
    </header>

    <!-- Analytics Dashboard -->
    <div class="analytics-grid">
      <div class="stat-card revenue">
        <h3>Total Revenue</h3>
        <p>₹{{ analyticsStore.stats.revenue }}</p>
      </div>
      <div class="stat-card orders">
        <h3>Paid Orders</h3>
        <p>{{ analyticsStore.stats.total_orders }}</p>
      </div>
      <div class="stat-card abandoned">
        <h3>Abandoned Carts</h3>
        <p>{{ analyticsStore.stats.abandoned_carts }}</p>
        <small>Carts > 24h old</small>
      </div>
    </div>

    <div class="insights-row">
      <!-- Popular Items -->
      <div class="insight-table card">
        <h3>Most Viewed Products</h3>
        <table>
          <tr v-for="item in analyticsStore.stats.popular_items" :key="item.name">
            <td>{{ item.name }}</td>
            <td class="text-right"><strong>{{ item.views }} views</strong></td>
          </tr>
        </table>
      </div>

      <!-- Best Sellers -->
      <div class="insight-table card">
        <h3>Best Sellers</h3>
        <table>
          <tr v-for="item in analyticsStore.stats.best_sellers" :key="item.name">
            <td>{{ item.name }}</td>
            <td class="text-right"><strong>{{ item.sold }} sold</strong></td>
          </tr>
        </table>
      </div>
    </div>

    <hr class="divider" />

    <!-- Inventory Management -->
    <h2 class="section-title">Product Inventory</h2>
    <div class="admin-table-container">
      <table class="admin-table">
        <thead>
          <tr>
            <th>Product</th>
            <th>Category</th>
            <th>Price</th>
            <th>Discount Price</th>
            <th>Stock</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in productStore.products" :key="product.id">
            <td><strong>{{ product.name }}</strong></td>
            <td>{{ product.category }}</td>
            <td>₹{{ product.price }}</td>
            <td>{{ product.discount_price ? '₹' + product.discount_price : '-' }}</td>
            <td>
              <span :class="{'out-of-stock': product.stock <= 0}">{{ product.stock }}</span>
            </td>
            <td>
              <span class="status-badge" :class="product.is_active ? 'active' : 'inactive'">
                {{ product.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td class="actions">
              <button @click="editProduct(product)" class="btn-text">Edit</button>
              <button @click="productStore.deleteProduct(product.id)" class="btn-text delete">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add/Edit Modal (Simplified for prototype) -->
    <div v-if="showAddModal" class="modal-overlay">
      <div class="modal-content">
        <h2>{{ editingId ? 'Edit Product' : 'Add New Product' }}</h2>
        <form @submit.prevent="saveProduct" class="modal-form">
          <div class="form-group">
            <label for="prod-name">Product Name</label>
            <input id="prod-name" v-model="form.name" required />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="prod-price">Price (₹)</label>
              <input id="prod-price" v-model.number="form.price" type="number" required />
            </div>
            <div class="form-group">
              <label for="prod-discount">Discount Price (Optional)</label>
              <input id="prod-discount" v-model.number="form.discount_price" type="number" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="prod-stock">Stock</label>
              <input id="prod-stock" v-model.number="form.stock" type="number" required />
            </div>
            <div class="form-group">
              <label for="prod-category">Category</label>
              <select id="prod-category" v-model="form.category_id" required>
                <option v-for="cat in productStore.categories" :key="cat.id" :value="cat.id">
                  {{ cat.name }}
                </option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label for="prod-desc">Description</label>
            <textarea id="prod-desc" v-model="form.description"></textarea>
          </div>
          <div class="modal-actions">
            <button type="button" @click="closeModal" class="btn btn-outline">Cancel</button>
            <button type="submit" class="btn btn-secondary">Save Product</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useProductStore } from '../stores/productStore'
import { useAnalyticsStore } from '../stores/analyticsStore'

const productStore = useProductStore()
const analyticsStore = useAnalyticsStore()
const showAddModal = ref(false)
const editingId = ref(null)

const form = ref({
  name: '',
  price: 0,
  discount_price: null,
  stock: 0,
  category_id: null,
  description: '',
  image_url: 'https://via.placeholder.com/150'
})

onMounted(() => {
  productStore.fetchProducts()
  productStore.fetchCategories()
  analyticsStore.fetchStats()
})

const editProduct = (product) => {
  editingId.value = product.id
  form.value = { ...product }
  showAddModal.value = true
}

const saveProduct = async () => {
  let success
  if (editingId.value) {
    success = await productStore.updateProduct(editingId.value, form.value)
  } else {
    success = await productStore.addProduct(form.value)
  }
  
  if (success) closeModal()
}

const closeModal = () => {
  showAddModal.value = false
  editingId.value = null
  form.value = { name: '', price: 0, discount_price: null, stock: 0, category_id: null, description: '', image_url: '' }
}
</script>

<style scoped>
.admin-dashboard {
  padding-top: 2rem;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.analytics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: var(--shadow);
  text-align: center;
  border-bottom: 4px solid #eee;
}

.stat-card.revenue { border-color: var(--accent); }
.stat-card.orders { border-color: var(--secondary); }
.stat-card.abandoned { border-color: #d00; }

.stat-card h3 { font-size: 0.9rem; color: #666; margin-bottom: 0.5rem; }
.stat-card p { font-size: 2.2rem; font-weight: 800; color: var(--primary); }

.insights-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.insight-table {
  padding: 1.5rem;
}

.insight-table h3 { margin-bottom: 1rem; font-size: 1rem; color: var(--primary); }
.insight-table table { width: 100%; border-collapse: collapse; }
.insight-table td { padding: 0.75rem 0; border-bottom: 1px solid #f5f5f5; font-size: 0.9rem; }
.text-right { text-align: right; }

.divider { margin: 3rem 0; border: 0; border-top: 1px solid #eee; }
.section-title { margin-bottom: 1.5rem; color: var(--primary); }

.admin-table-container {
  background: white;
  border-radius: 12px;
  box-shadow: var(--shadow);
  overflow: hidden;
}

.admin-table {
  width: 100%;
  border-collapse: collapse;
}

.admin-table th, .admin-table td {
  padding: 1rem 1.5rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.admin-table th {
  background: #f9f9f9;
  font-size: 0.85rem;
  text-transform: uppercase;
  color: #666;
}

.status-badge {
  padding: 0.25rem 0.6rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-badge.active { background: #e6fffa; color: #2c7a7b; }
.status-badge.inactive { background: #fff0f0; color: #d00; }

.out-of-stock { color: #d00; font-weight: 700; }

.btn-text {
  background: none;
  border: none;
  color: var(--secondary);
  font-weight: 600;
  cursor: pointer;
  margin-right: 1rem;
}

.btn-text.delete { color: #d00; }

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
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
  max-width: 600px;
}

.form-row {
  display: flex;
  gap: 1rem;
}

.form-row .form-group {
  flex: 1;
}

.modal-form select, .modal-form textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}
</style>
