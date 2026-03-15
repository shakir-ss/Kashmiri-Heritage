<template>
  <div class="product-detail container" v-if="product">
    <div class="breadcrumb">
      <router-link to="/">Home</router-link> / 
      <router-link to="/products">Products</router-link> / 
      <span>{{ product.name }}</span>
    </div>

    <div class="detail-grid">
      <!-- Product Image Gallery -->
      <div class="product-visuals">
        <div class="main-image-container card">
          <img :src="activeImage || 'https://via.placeholder.com/600x800?text=Kashmiri+Product'" :alt="product.name" />
          <button @click="wishlistStore.toggleWishlist(product)" class="wishlist-btn" :class="{ active: wishlistStore.isInWishlist(product.id) }">
            {{ wishlistStore.isInWishlist(product.id) ? '❤️' : '🤍' }}
          </button>
        </div>
        
        <!-- Thumbnails -->
        <div v-if="allImages.length > 1" class="thumbnail-gallery">
          <div 
            v-for="(img, index) in allImages" 
            :key="index" 
            class="thumb-card card" 
            :class="{ active: activeImage === img }"
            @click="activeImage = img"
          >
            <img :src="img" :alt="product.name + ' thumbnail ' + index" />
          </div>
        </div>
      </div>

      <!-- Product Info -->
      <div class="product-info-panel">
        <span class="category-label">{{ product.category }}</span>
        <h1>{{ product.name }}</h1>
        
        <div class="price-section">
          <span class="current-price">₹{{ product.discount_price || product.price }}</span>
          <span v-if="product.discount_price" class="original-price">₹{{ product.price }}</span>
          <span v-if="product.discount_price" class="save-tag">Save ₹{{ product.price - product.discount_price }}</span>
        </div>

        <p class="short-desc">{{ product.description }}</p>

        <div class="inventory-status" :class="{ 'out-of-stock': product.stock <= 0 }">
          {{ product.stock > 0 ? `In Stock (${product.stock} available)` : 'Currently Out of Stock' }}
        </div>

        <div class="action-buttons">
          <div class="quantity-selector">
            <button @click="quantity > 1 ? quantity-- : null">-</button>
            <input type="number" v-model.number="quantity" min="1" :max="product.stock" />
            <button @click="quantity < product.stock ? quantity++ : null">+</button>
          </div>
          
          <button @click="addToCart" class="btn btn-primary btn-lg" :disabled="product.stock <= 0">Add to Cart</button>
          <button @click="buyNow" class="btn btn-secondary btn-lg" :disabled="product.stock <= 0">Buy It Now</button>
        </div>

        <div class="trust-badges">
          <div class="badge-item"><span>🚚</span> Free Worldwide Shipping</div>
          <div class="badge-item"><span>🛡️</span> 100% Authentic Kashmiri</div>
          <div class="badge-item"><span>✨</span> Handcrafted with Love</div>
        </div>
      </div>
    </div>

    <!-- Detailed Information Section -->
    <div class="product-extended-details mt-4" v-if="product.details">
      <h2 class="section-title">The Story & Details</h2>
      <div class="details-content card kashmiri-pattern" v-html="formattedDetails"></div>
    </div>
  </div>
  <div v-else-if="loading" class="container loading-state">
    <p>Discovering Kashmiri treasures...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProductStore } from '../stores/productStore'
import { useCartStore } from '../stores/cartStore'
import { useWishlistStore } from '../stores/wishlistStore'

const route = useRoute()
const router = useRouter()
const productStore = useProductStore()
const cartStore = useCartStore()
const wishlistStore = useWishlistStore()

const product = ref(null)
const loading = ref(true)
const quantity = ref(1)
const activeImage = ref(null)

onMounted(async () => {
  product.value = await productStore.fetchProductById(route.params.id)
  if (product.value) {
    activeImage.value = product.value.image_url
  }
  loading.value = false
  wishlistStore.fetchWishlist()
})

const allImages = computed(() => {
  if (!product.value) return []
  const images = []
  if (product.value.image_url) images.push(product.value.image_url)
  if (product.value.images && product.value.images.length > 0) {
    images.push(...product.value.images)
  }
  return images
})

const formattedDetails = computed(() => {
  if (!product.value?.details) return ''
  // Basic newline to <br> for simple formatting
  return product.value.details.replace(/\n/g, '<br>')
})

const addToCart = () => {
  cartStore.addItem(product.value, quantity.value)
}

const buyNow = () => {
  cartStore.addItem(product.value, quantity.value)
  router.push('/checkout')
}
</script>

<style scoped>
.product-detail {
  padding-top: 2rem;
  padding-bottom: 8rem;
}

.breadcrumb {
  font-size: 0.85rem;
  color: #888;
  margin-bottom: 2.5rem;
}

.breadcrumb a {
  color: var(--primary);
  text-decoration: none;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: start;
}

.main-image-container {
  padding: 0;
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  height: 650px;
}

.main-image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumbnail-gallery {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
}

.thumb-card {
  width: 80px;
  height: 80px;
  min-width: 80px;
  padding: 0;
  cursor: pointer;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid transparent;
  transition: all 0.2s;
}

.thumb-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumb-card:hover { transform: translateY(-3px); }
.thumb-card.active { border-color: var(--secondary); box-shadow: 0 4px 10px rgba(0,0,0,0.1); }

.wishlist-btn {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  background: white;
  border: none;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  cursor: pointer;
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s;
}

.wishlist-btn:hover { transform: scale(1.1); }
.wishlist-btn.active { background: #fff0f0; }

.category-label {
  text-transform: uppercase;
  font-size: 0.75rem;
  font-weight: 800;
  color: var(--secondary);
  letter-spacing: 2px;
}

.product-info-panel h1 {
  font-size: 3rem;
  margin: 1rem 0;
  color: var(--primary);
}

.price-section {
  margin: 2rem 0;
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.current-price {
  font-size: 2rem;
  font-weight: 800;
  color: var(--text-dark);
}

.original-price {
  font-size: 1.25rem;
  text-decoration: line-through;
  color: #bbb;
}

.save-tag {
  background: var(--accent);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 700;
}

.short-desc {
  font-size: 1.1rem;
  line-height: 1.8;
  color: #555;
  margin-bottom: 2rem;
}

.inventory-status {
  font-weight: 700;
  font-size: 0.9rem;
  color: #1e7e34;
  margin-bottom: 2rem;
}

.inventory-status.out-of-stock {
  color: #d00;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-bottom: 3rem;
}

.quantity-selector {
  display: flex;
  border: 2px solid #eee;
  border-radius: 50px;
  overflow: hidden;
}

.quantity-selector button {
  background: none;
  border: none;
  width: 40px;
  cursor: pointer;
  font-size: 1.2rem;
}

.quantity-selector input {
  width: 50px;
  text-align: center;
  border: none;
  font-weight: 700;
  background: #f9f9f9;
}

.trust-badges {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  padding-top: 2rem;
  border-top: 1px solid #eee;
}

.badge-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: #666;
}

.section-title {
  margin: 4rem 0 2rem;
  color: var(--primary);
  font-size: 2rem;
}

.details-content {
  padding: 3rem;
  line-height: 2;
  color: #444;
  font-size: 1.05rem;
}

.mt-4 { margin-top: 4rem; }

@media (max-width: 992px) {
  .detail-grid { grid-template-columns: 1fr; gap: 2rem; }
  .main-image-container { height: 450px; }
  .action-buttons { flex-direction: column; }
  .quantity-selector { width: 100%; justify-content: center; }
}
</style>
