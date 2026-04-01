<template>
  <div class="admin-dashboard container">
    <header class="admin-header">
      <h1>Admin Insights & Inventory</h1>
      <div class="header-actions">
        <button @click="refreshAllData" class="btn btn-outline btn-sm">Refresh Stats</button>
        <button id="add-product-btn" @click="showAddModal = true" class="btn btn-secondary">+ Add New Product</button>
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

    <!-- Orders Management -->
    <section class="admin-section">
      <h2 class="section-title">Recent Customer Orders</h2>
      <div class="admin-table-container">
        <table class="admin-table">
          <thead>
            <tr>
              <th>Order ID</th>
              <th>Customer</th>
              <th>Date</th>
              <th>Amount</th>
              <th>Status</th>
              <th>Details</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="order in orders" :key="order.id">
              <td>#{{ order.id }}</td>
              <td>
                <div class="cust-info">
                  <strong>{{ order.user }}</strong>
                  <small>{{ order.user_email }}</small>
                </div>
              </td>
              <td>{{ formatDate(order.created_at) }}</td>
              <td><strong>₹{{ order.total_amount }}</strong></td>
              <td>
                <span class="status-badge" :class="order.status">
                  {{ order.status }}
                </span>
              </td>
              <td>
                <button @click="viewOrderDetails(order)" class="btn-text">View Items</button>
              </td>
            </tr>
            <tr v-if="orders && orders.length === 0">
              <td colspan="6" class="text-center">No orders placed yet.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <hr class="divider" />

    <!-- Category Management -->
    <section class="admin-section">
      <div class="section-header">
        <h2 class="section-title">Categories</h2>
        <button @click="openCategoryModal()" class="btn btn-primary btn-sm">+ New Category</button>
      </div>
      <div class="admin-table-container">
        <table class="admin-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Slug</th>
              <th>Description</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="cat in productStore.categories" :key="cat.id">
              <td><strong>{{ cat.name }}</strong></td>
              <td>{{ cat.slug }}</td>
              <td>{{ truncate(cat.description || '', 50) }}</td>
              <td class="actions">
                <button @click="openCategoryModal(cat)" class="btn-text">Edit</button>
                <button @click="productStore.deleteCategory(cat.id)" class="btn-text delete">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <hr class="divider" />

    <!-- Customer Inquiries -->
    <section class="admin-section">
      <h2 class="section-title">Customer Inquiries</h2>
      <div class="admin-table-container">
        <table class="admin-table">
          <thead>
            <tr>
              <th>From</th>
              <th>Subject</th>
              <th>Date</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="inquiry in inquiries" :key="inquiry.id">
              <td>
                <div class="cust-info">
                  <strong>{{ inquiry.name }}</strong>
                  <small>{{ inquiry.email }}</small>
                  <small v-if="inquiry.phone">{{ inquiry.phone }}</small>
                </div>
              </td>
              <td>
                <div class="subject-info">
                  <strong>{{ inquiry.subject }}</strong>
                  <p class="mini-message">{{ truncate(inquiry.message, 60) }}</p>
                </div>
              </td>
              <td>{{ formatDate(inquiry.created_at) }}</td>
              <td>
                <span class="status-badge" :class="inquiry.status">
                  {{ inquiry.status }}
                </span>
              </td>
              <td class="actions">
                <button @click="viewInquiry(inquiry)" class="btn-text">View</button>
                <select @change="updateInquiryStatus(inquiry.id, $event.target.value)" :value="inquiry.status" class="status-select">
                  <option value="pending">Pending</option>
                  <option value="responded">Responded</option>
                  <option value="closed">Closed</option>
                </select>
              </td>
            </tr>
            <tr v-if="inquiries && inquiries.length === 0">
              <td colspan="5" class="text-center">No inquiries yet.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <hr class="divider" />

    <!-- Inventory Management -->
    <h2 class="section-title">Product Inventory</h2>
    <div class="admin-table-container" v-if="!productStore.loading">
      <table class="admin-table" id="inventory-table">
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
          <tr v-for="product in productStore.products" :key="product.id" :class="{'row-out-of-stock': product.stock <= 0, 'row-low-stock': product.stock > 0 && product.stock <= 5}">
            <td>
              <router-link :to="'/products/' + product.id" class="product-cell-link">
                <div class="product-cell">
                  <img :src="product.image_url || 'https://via.placeholder.com/40'" class="mini-thumb" />
                  <strong>{{ product.name }}</strong>
                </div>
              </router-link>
            </td>
            <td><span class="category-pill">{{ product.category }}</span></td>
            <td>₹{{ product.price }}</td>
            <td>{{ product.discount_price ? '₹' + product.discount_price : '-' }}</td>
            <td>
              <div class="stock-badge" :class="{'out-of-stock': product.stock <= 0, 'low-stock': product.stock > 0 && product.stock <= 5}">
                {{ product.stock }} {{ product.stock <= 0 ? '(Empty)' : 'units' }}
              </div>
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
          <tr v-if="productStore.products && productStore.products.length === 0">
              <td colspan="7" class="text-center">No products in inventory.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add/Edit Modal (Global Store Ready) -->
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
              <label for="prod-price">Base Price (₹)</label>
              <input id="prod-price" v-model.number="form.price" type="number" required />
            </div>
            <div class="form-group">
              <label for="prod-discount">Discount Price (Optional)</label>
              <input id="prod-discount" v-model.number="form.discount_price" type="number" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="prod-stock">Total Stock</label>
              <input id="prod-stock" v-model.number="form.stock" type="number" required />
            </div>
            <div class="form-group">
              <label for="prod-weight">Weight (grams)</label>
              <input id="prod-weight" v-model.number="form.weight_grams" type="number" placeholder="e.g. 500" />
            </div>
          </div>
          <div class="form-group">
            <label for="prod-category">Category</label>
            <select id="prod-category" v-model="form.category_id" required>
              <option v-for="cat in productStore.categories" :key="cat.id" :value="cat.id">
                {{ cat.name }}
              </option>
            </select>
          </div>

          <div class="form-group checkbox-group">
            <input type="checkbox" id="prod-active" v-model="form.is_active" />
            <label for="prod-active">Show on Website (Active)</label>
          </div>
          
          <!-- Variants Section -->
          <div class="form-group">
            <label>Product Variants (Size, Color, etc.)</label>
            <div v-for="(v, idx) in form.variants" :key="idx" class="variant-input-row">
              <input v-model="v.name" placeholder="Variant Name" class="flex-2" />
              <input v-model.number="v.price_modifier" type="number" placeholder="+₹" class="flex-1" />
              <input v-model.number="v.stock" type="number" placeholder="Stock" class="flex-1" />
              <button type="button" @click="removeVariantField(idx)" class="btn-text delete">×</button>
            </div>
            <button type="button" @click="addVariantField" class="btn-text">+ Add Variant</button>
          </div>

          <div class="form-group">
            <label for="prod-desc">Short Description</label>
            <textarea id="prod-desc" v-model="form.description" rows="2"></textarea>
          </div>
          <div class="form-group">
            <label for="prod-details">Detailed Product Story (Optional)</label>
            <textarea id="prod-details" v-model="form.details" rows="5" placeholder="Tell the story of this product, its origin, and craft..."></textarea>
          </div>
          <div class="form-group">
            <label for="prod-image">Main Image URL</label>
            <div class="image-input-group">
              <input id="prod-image" v-model="form.image_url" placeholder="https://..." />
              <button type="button" @click="openUploadWidget" class="btn btn-secondary btn-sm">Upload from Cloud</button>
            </div>
            <div v-if="form.image_url" class="image-preview mt-2">
              <img :src="form.image_url" alt="Preview" style="max-height: 100px; border-radius: 8px;" />
            </div>
          </div>

          <div class="form-group">
            <label>Additional Images (Optional)</label>
            <div v-for="(img, index) in form.additional_images" :key="index" class="image-input-row">
              <input v-model="form.additional_images[index]" placeholder="https://..." />
              <button type="button" @click="removeImageField(index)" class="btn-text delete">Remove</button>
            </div>
            <button type="button" @click="addImageField" class="btn-text">+ Add Another Image</button>
          </div>
          <div class="modal-actions">
            <button type="button" @click="closeModal" class="btn btn-outline">Cancel</button>
            <button type="submit" class="btn btn-secondary">Save Product</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Category Modal -->
    <div v-if="showCategoryModal" class="modal-overlay">
      <div class="modal-content">
        <h2>{{ editingCatId ? 'Edit Category' : 'New Category' }}</h2>
        <form @submit.prevent="saveCategory" class="modal-form">
          <div class="form-group">
            <label for="cat-name">Category Name</label>
            <input id="cat-name" v-model="catForm.name" required />
          </div>
          <div class="form-group">
            <label for="cat-desc">Description</label>
            <textarea id="cat-desc" v-model="catForm.description" rows="3"></textarea>
          </div>
          <div class="modal-actions">
            <button type="button" @click="closeCategoryModal" class="btn btn-outline">Cancel</button>
            <button type="submit" class="btn btn-secondary">Save Category</button>
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
import axios from 'axios'

const productStore = useProductStore()
const analyticsStore = useAnalyticsStore()
const showAddModal = ref(false)
const showCategoryModal = ref(false)
const editingId = ref(null)
const editingCatId = ref(null)
const orders = ref([])
const inquiries = ref([])

const form = ref({
  name: '',
  price: 0,
  discount_price: null,
  stock: 0,
  category_id: null,
  description: '',
  image_url: '',
  additional_images: [],
  weight_grams: 0,
  variants: []
})

const catForm = ref({
  name: '',
  description: ''
})

onMounted(() => {
  productStore.fetchProducts()
  productStore.fetchCategories()
  analyticsStore.fetchStats()
  fetchOrders()
  fetchInquiries()
})

const fetchInquiries = async () => {
  try {
    const res = await axios.get('/api/contact/')
    inquiries.value = res.data
  } catch (err) {
    console.error('Failed to fetch inquiries:', err)
  }
}

const viewInquiry = (inquiry) => {
  alert(`Inquiry from ${inquiry.name}\nSubject: ${inquiry.subject}\n\nMessage:\n${inquiry.message}\n\nContact:\nEmail: ${inquiry.email}\nPhone: ${inquiry.phone || 'N/A'}`)
}

const openUploadWidget = () => {
  // Check if cloudinary is loaded
  if (!window.cloudinary) {
    alert("Cloudinary script not loaded yet. Please refresh the page.")
    return
  }

  const widget = window.cloudinary.createUploadWidget(
    {
      cloudName: 'dghwqmarz', // Replace with your Cloudinary Cloud Name
      uploadPreset: 'hundred_villages_preset', // Replace with your Unsigned Upload Preset
      sources: ['local', 'url', 'camera'],
      multiple: false,
      cropping: true,
      showSkipCropButton: false,
      croppingAspectRatio: 0.75, // 3:4 Portrait for premium look
      clientAllowedFormats: ['png', 'jpeg', 'jpg', 'webp'],
      styles: {
        palette: {
          window: "#FFFFFF",
          windowBorder: "#90A0B3",
          tabIcon: "#4a2c2a",
          menuIcons: "#5A616A",
          textDark: "#000000",
          textLight: "#FFFFFF",
          link: "#4a2c2a",
          action: "#4a2c2a",
          inactiveTabIcon: "#0E2F5A",
          error: "#F44235",
          inProgress: "#0078FF",
          complete: "#20B832",
          sourceBg: "#E4EBF1"
        }
      }
    },
    (error, result) => {
      if (!error && result && result.event === "success") {
        console.log("Done! Here is the image info: ", result.info)
        form.value.image_url = result.info.secure_url
      }
    }
  )
  widget.open()
}

const updateInquiryStatus = async (id, newStatus) => {
  try {
    await axios.put(`/api/contact/${id}/status`, { status: newStatus })
    await fetchInquiries()
  } catch (err) {
    alert('Failed to update status')
  }
}

const truncate = (text, length) => {
  return text.length > length ? text.substring(0, length) + '...' : text
}

const addImageField = () => {
  form.value.additional_images.push('')
}

const removeImageField = (index) => {
  form.value.additional_images.splice(index, 1)
}

const addVariantField = () => {
  form.value.variants.push({ name: '', price_modifier: 0, stock: 0 })
}

const removeVariantField = (index) => {
  form.value.variants.splice(index, 1)
}

const openCategoryModal = (cat = null) => {
  if (cat) {
    editingCatId.value = cat.id
    catForm.value = { name: cat.name, description: cat.description }
  } else {
    editingCatId.value = null
    catForm.value = { name: '', description: '' }
  }
  showCategoryModal.value = true
}

const closeCategoryModal = () => {
  showCategoryModal.value = false
  editingCatId.value = null
}

const saveCategory = async () => {
  let success
  if (editingCatId.value) {
    success = await productStore.updateCategory(editingCatId.value, catForm.value)
  } else {
    success = await productStore.addCategory(catForm.value)
  }
  if (success) closeCategoryModal()
}

const refreshAllData = () => {
  analyticsStore.fetchStats()
  fetchOrders()
  productStore.fetchProducts()
  productStore.fetchCategories()
}

const fetchOrders = async () => {
  try {
    const res = await axios.get('/api/orders/admin')
    orders.value = res.data
  } catch (err) {
    console.error('Failed to fetch admin orders:', err)
  }
}

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleString('en-IN', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const viewOrderDetails = (order) => {
  const itemsList = order.items.map(i => `${i.quantity}x ${i.name}`).join('\n')
  alert(`Order #${order.id} Details:\n\nItems:\n${itemsList}\n\nAddress:\n${order.address}\n\nPhone: ${order.phone}`)
}

const editProduct = (product) => {
  editingId.value = product.id
  form.value = { 
    ...product,
    additional_images: product.images ? [...product.images] : [],
    variants: product.variants ? [...product.variants] : [],
    is_active: product.is_active // Ensure this is captured
  }
  showAddModal.value = true
}

const saveProduct = async () => {
  // Ensure stock is a number
  form.value.stock = Number(form.value.stock)
  form.value.price = Number(form.value.price)
  if (form.value.discount_price) form.value.discount_price = Number(form.value.discount_price)
  
  let success
  if (editingId.value) {
    success = await productStore.updateProduct(editingId.value, form.value)
  } else {
    // New products are active by default if not specified
    if (form.value.is_active === undefined) form.value.is_active = true
    success = await productStore.addProduct(form.value)
  }
  
  if (success) closeModal()
}

const closeModal = () => {
  showAddModal.value = false
  editingId.value = null
  form.value = { 
    name: '', 
    price: 0, 
    discount_price: null, 
    stock: 0, 
    category_id: null, 
    description: '', 
    image_url: '', 
    additional_images: [],
    weight_grams: 0,
    variants: [],
    is_active: true // Reset to default
  }
}
</script>

<style scoped>
.admin-dashboard {
  padding-top: 2rem;
  padding-bottom: 5rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.image-input-row, .variant-input-row {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.image-input-row input, .variant-input-row input {
  flex-grow: 1;
}

.flex-2 { flex: 2; }
.flex-1 { flex: 1; }

.modal-form input, .modal-form select, .modal-form textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  font-weight: 700;
  font-size: 0.85rem;
  margin-bottom: 0.5rem;
  color: #555;
}

/* Enhanced Table Styles */
.product-cell {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.product-cell-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.product-cell-link:hover .product-cell strong {
  color: var(--secondary);
}

.mini-thumb {
  width: 40px;
  height: 40px;
  border-radius: 6px;
  object-fit: cover;
  border: 1px solid #eee;
}

.category-pill {
  background: #f0f4f8;
  color: #4a5568;
  padding: 0.25rem 0.75rem;
  border-radius: 50px;
  font-size: 0.75rem;
  font-weight: 600;
}

.stock-badge {
  display: inline-block;
  padding: 0.35rem 0.75rem;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 700;
  background: #ebf8ff;
  color: #2b6cb0;
}

.stock-badge.low-stock {
  background: #fffaf0;
  color: #b7791f;
}

.stock-badge.out-of-stock {
  background: #fff5f5;
  color: #c53030;
}

/* Row Highlighting */
.admin-table tr.row-out-of-stock {
  background-color: rgba(255, 0, 0, 0.03);
  box-shadow: inset 4px 0 0 #e53e3e;
}

.admin-table tr.row-low-stock {
  background-color: rgba(255, 165, 0, 0.02);
  box-shadow: inset 4px 0 0 #ed8936;
}

.admin-table tr:hover {
  background-color: #fcfcfc;
}

.text-center { text-align: center; }

/* Status Badges */
.status-badge {
  padding: 0.25rem 0.6rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-badge.active { background: #e6fffa; color: #2c7a7b; }
.status-badge.inactive { background: #fff0f0; color: #d00; }

.cust-info {
  display: flex;
  flex-direction: column;
}

.cust-info small {
  color: #888;
}

/* Modal and layout fixes */
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
.section-title { margin-bottom: 1.5rem; color: var(--primary); font-size: 1.5rem; }

.admin-table-container {
  background: white;
  border-radius: 12px;
  box-shadow: var(--shadow);
  overflow: hidden;
  margin-bottom: 2rem;
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
  font-weight: 700;
}

.btn-text {
  background: none;
  border: none;
  color: var(--secondary);
  font-weight: 600;
  cursor: pointer;
  margin-right: 1rem;
}

.btn-text.delete { color: #d00; }

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
  max-height: 90vh;
  overflow-y: auto;
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
