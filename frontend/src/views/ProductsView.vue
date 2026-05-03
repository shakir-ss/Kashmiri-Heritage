<template>
  <div class="products-view container">
    <nav class="breadcrumb-nav full-width">
      <router-link to="/">Home</router-link>
      <span class="sep">
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 18L15 12L9 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </span>
      <span class="current">Heritage Catalog</span>
    </nav>

    <!-- Sidebar Filters -->
    <aside class="filters">
      <h3>Categories</h3>
      <div class="filter-list">
        <button 
          @click="selectCategory(null)" 
          :class="{ active: !selectedCategory }"
        >All Products</button>
        <button 
          v-for="cat in productStore.categories" 
          :key="cat.id"
          @click="selectCategory(cat.slug)"
          :class="{ active: selectedCategory == cat.slug || selectedCategory == cat.id }"
        >{{ cat.name }}</button>
      </div>

      <div class="price-filter mt-4">
        <h3>Price Range</h3>
        <div class="price-inputs">
          <div class="price-input-wrap">
            <span>₹</span>
            <input type="number" v-model="minPrice" placeholder="Min" @input="handleSearch" />
          </div>
          <span class="price-dash">—</span>
          <div class="price-input-wrap">
            <span>₹</span>
            <input type="number" v-model="maxPrice" placeholder="Max" @input="handleSearch" />
          </div>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="content">
      <!-- Toolbar: Search + Result count + View toggle -->
      <div class="toolbar">
        <div class="search-bar">
          <span class="search-icon">🔍</span>
          <input 
            v-model="searchQuery" 
            @input="handleSearch"
            type="text" 
            placeholder="Search for Saffron, Walnuts, Shawls..." 
          />
        </div>
        <div class="toolbar-right">
          <span class="result-count" v-if="!productStore.loading">
            {{ productStore.products.length }} product{{ productStore.products.length !== 1 ? 's' : '' }}
          </span>
          <div class="view-toggle" role="group" aria-label="View mode">
            <button 
              @click="viewMode = 'grid'" 
              :class="{ active: viewMode === 'grid' }"
              title="Grid view"
              aria-label="Grid view"
            >
              <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <rect x="0" y="0" width="6" height="6" rx="1"/>
                <rect x="10" y="0" width="6" height="6" rx="1"/>
                <rect x="0" y="10" width="6" height="6" rx="1"/>
                <rect x="10" y="10" width="6" height="6" rx="1"/>
              </svg>
            </button>
            <button 
              @click="viewMode = 'list'" 
              :class="{ active: viewMode === 'list' }"
              title="List view"
              aria-label="List view"
            >
              <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                <rect x="0" y="0" width="16" height="3" rx="1"/>
                <rect x="0" y="6" width="16" height="3" rx="1"/>
                <rect x="0" y="12" width="16" height="3" rx="1"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <div v-if="productStore.loading" class="loading">
        <div class="loading-spinner"></div>
        <p>Searching the Valley for the finest products...</p>
      </div>

      <div v-else-if="productStore.products.length === 0" class="no-results">
        <span class="no-results-icon">🌿</span>
        <p>No products found matching your search.</p>
        <button @click="clearFilters" class="btn btn-outline">Clear Filters</button>
      </div>

      <div v-else :class="['products-container', viewMode === 'list' ? 'product-list' : 'product-grid']">
        <ProductCard 
          v-for="product in productStore.products" 
          :key="product.id" 
          :product="product"
          :list-view="viewMode === 'list'"
          @add-to-cart="addToCart"
        />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useProductStore } from '../stores/productStore'
import { useCartStore } from '../stores/cartStore'
import { useAnalyticsStore } from '../stores/analyticsStore'
import ProductCard from '../components/ProductCard.vue'

const productStore = useProductStore()
const cartStore = useCartStore()
const analyticsStore = useAnalyticsStore()
const route = useRoute()

const selectedCategory = ref(null)
const searchQuery = ref('')
const minPrice = ref(null)
const maxPrice = ref(null)
const viewMode = ref('grid') // 'grid' | 'list'

const syncFiltersFromRoute = () => {
  const cat = route.query.category || null
  const search = route.query.search || ''
  
  selectedCategory.value = cat
  searchQuery.value = search
  
  productStore.fetchProducts({ category: cat, q: search, min_price: minPrice.value, max_price: maxPrice.value })
}

onMounted(async () => {
  await productStore.fetchCategories()
  syncFiltersFromRoute()
})

watch(() => route.query, () => {
  syncFiltersFromRoute()
}, { deep: true })

const selectCategory = (slugOrId) => {
  selectedCategory.value = slugOrId
  handleSearch()
}

let searchTimeout;
const handleSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    productStore.fetchProducts({ 
      category: selectedCategory.value, 
      q: searchQuery.value,
      min_price: minPrice.value,
      max_price: maxPrice.value
    })
  }, 300)
}

const clearFilters = () => {
  selectedCategory.value = null
  searchQuery.value = ''
  minPrice.value = null
  maxPrice.value = null
  productStore.fetchProducts({})
}

const addToCart = (product) => {
  cartStore.addItem(product)
  analyticsStore.trackProductView(product.id)
}
</script>

<style scoped>
.products-view {
  display: grid;
  grid-template-columns: 220px 1fr;
  gap: 2.5rem;
  padding-top: 2.5rem;
  padding-bottom: 4rem;
  align-items: start;
}

.breadcrumb-nav.full-width {
  grid-column: 1 / -1;
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #a0aec0;
}

.breadcrumb-nav.full-width a {
  color: #718096;
  text-decoration: none;
  transition: color 0.2s;
}
.breadcrumb-nav.full-width a:hover { color: var(--secondary); }
.breadcrumb-nav.full-width .current { color: var(--primary); }
.breadcrumb-nav.full-width .sep { color: #cbd5e0; display: flex; }

/* ===== SIDEBAR ===== */
.filters {
  position: sticky;
  top: 90px;
  background: white;
  border-radius: 16px;
  padding: 1.75rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.05);
  border: 1px solid #f0ede8;
}

.filters h3 {
  margin-bottom: 1rem;
  font-size: 0.75rem;
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--primary);
}

.filter-list {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.filter-list button {
  background: none;
  border: none;
  text-align: left;
  padding: 0.6rem 0.85rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.9rem;
  transition: all 0.15s;
  color: #555;
}

.filter-list button:hover { background: rgba(139,69,19,0.05); color: var(--primary); }
.filter-list button.active { background: var(--primary); color: white; font-weight: 700; }

.price-filter { margin-top: 1.5rem; }

.price-inputs {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.price-input-wrap {
  display: flex;
  align-items: center;
  background: #faf9f6;
  border: 1px solid #e0dbd5;
  border-radius: 8px;
  padding: 0 0.5rem;
  gap: 0.25rem;
  flex: 1;
}

.price-input-wrap span { font-size: 0.85rem; color: #888; font-weight: 700; }

.price-input-wrap input {
  width: 100%;
  border: none;
  background: transparent;
  padding: 0.5rem 0.25rem;
  font-size: 0.9rem;
  outline: none;
}

.price-dash { color: #ccc; font-size: 1.2rem; }

/* ===== TOOLBAR ===== */
.toolbar {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  background: white;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.04);
  border: 1px solid #f0ede8;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
  background: #faf9f6;
  border: 1.5px solid #e0dbd5;
  border-radius: 9px;
  padding: 0.6rem 1rem;
  transition: border-color 0.2s;
}

.search-bar:focus-within { border-color: var(--secondary); }

.search-icon { font-size: 0.9rem; opacity: 0.6; }

.search-bar input {
  border: none;
  background: transparent;
  outline: none;
  font-size: 0.95rem;
  width: 100%;
  color: var(--text-dark);
}

.toolbar-right {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-shrink: 0;
}

.result-count {
  font-size: 0.8rem;
  color: #888;
  white-space: nowrap;
}

.view-toggle {
  display: flex;
  background: #f0ede8;
  border-radius: 8px;
  padding: 3px;
  gap: 2px;
}

.view-toggle button {
  background: none;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #888;
  transition: all 0.15s;
}

.view-toggle button.active {
  background: white;
  color: var(--primary);
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
}

/* ===== PRODUCT GRID ===== */
.product-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

/* ===== PRODUCT LIST ===== */
.product-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* ===== LOADING ===== */
.loading {
  text-align: center;
  padding: 5rem 2rem;
  color: #888;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f0ede8;
  border-top-color: var(--secondary);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  margin: 0 auto 1.5rem;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* ===== NO RESULTS ===== */
.no-results {
  text-align: center;
  padding: 5rem 2rem;
  color: #888;
}

.no-results-icon { font-size: 3rem; display: block; margin-bottom: 1rem; }

/* ===== RESPONSIVE ===== */
@media (max-width: 1100px) {
  .product-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 768px) {
  .products-view {
    grid-template-columns: 1fr;
    gap: 1.25rem;
    padding-top: 1.5rem;
  }

  .filters {
    position: static;
    padding: 1rem;
    border-radius: 10px;
  }

  .filter-list {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .filter-list button {
    padding: 0.4rem 1rem;
    font-size: 0.8rem;
    background: #f0f0f0;
    border-radius: 20px;
  }

  .price-filter { display: none; }

  .product-grid { grid-template-columns: repeat(2, 1fr); gap: 1rem; }
}

@media (max-width: 420px) {
  .product-grid { grid-template-columns: 1fr; }
  .view-toggle { display: none; }
}
</style>
