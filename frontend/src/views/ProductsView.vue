<template>
  <div class="products-view container">
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
    </aside>

    <!-- Main Content -->
    <main class="content">
      <div class="search-bar">
        <input 
          v-model="searchQuery" 
          @input="handleSearch"
          type="text" 
          placeholder="Search for Saffron, Walnuts, Shawls..." 
        />
      </div>

      <div v-if="productStore.loading" class="loading">
        Searching the Valley for the finest products...
      </div>

      <div v-else-if="productStore.products.length === 0" class="no-results">
        No products found matching your search.
      </div>

      <div v-else class="product-grid">
        <ProductCard 
          v-for="product in productStore.products" 
          :key="product.id" 
          :product="product"
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

const syncFiltersFromRoute = () => {
  const cat = route.query.category || null
  const search = route.query.search || ''
  
  selectedCategory.value = cat
  searchQuery.value = search
  
  productStore.fetchProducts({ category: cat, search: search })
}

onMounted(async () => {
  await productStore.fetchCategories()
  syncFiltersFromRoute()
})

// Watch for route changes (e.g. clicking different categories in header/footer)
watch(() => route.query, () => {
  syncFiltersFromRoute()
}, { deep: true })

const selectCategory = (slugOrId) => {
  selectedCategory.value = slugOrId
  productStore.fetchProducts({ category: slugOrId, search: searchQuery.value })
}

const handleSearch = () => {
  productStore.fetchProducts({ category: selectedCategory.value, search: searchQuery.value })
}

const addToCart = (product) => {
  cartStore.addItem(product)
  analyticsStore.trackProductView(product.id) // Track view on 'interest'
}
</script>

<style scoped>
.products-view {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 3rem;
  padding-top: 3rem;
}

.filters h3 {
  margin-bottom: 1.5rem;
  font-size: 1.25rem;
  color: var(--primary);
}

.filter-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.filter-list button {
  background: none;
  border: none;
  text-align: left;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.filter-list button:hover {
  background: rgba(139, 69, 19, 0.05);
}

.filter-list button.active {
  background: var(--primary);
  color: white;
}

.search-bar {
  margin-bottom: 2rem;
}

.search-bar input {
  width: 100%;
  padding: 1rem 1.5rem;
  border: 1px solid #ddd;
  border-radius: 12px;
  font-size: 1rem;
  outline: none;
  box-shadow: var(--shadow);
}

.search-bar input:focus {
  border-color: var(--secondary);
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2rem;
}

.loading, .no-results {
  text-align: center;
  padding: 4rem;
  color: #666;
}

@media (max-width: 768px) {
  .products-view {
    grid-template-columns: 1fr;
  }
  
  .filters {
    display: none; /* Hide filters on mobile for prototype, or convert to dropdown */
  }
}
</style>
