<template>
  <div class="home-wrapper">
    <!-- Hero Section -->
    <header class="hero" :class="{ 'hero-walnut': showWalnutBanner }">
      <div class="hero-overlay"></div>
      <div class="container hero-content">
        <template v-if="showWalnutBanner">
          <div class="hero-badge">Special Harvest</div>
          <h1>Premium Kashmiri <span>Walnuts</span></h1>
          <p>Sourced from the sun-drenched orchards of Ganderbal. Organic, crunchy, and packed with the goodness of nature.</p>
          <div class="hero-actions">
            <router-link to="/products?search=Walnut" class="btn btn-secondary">Shop Walnuts</router-link>
            <button @click="showWalnutBanner = false" class="btn btn-outline-white">Discover More</button>
          </div>
        </template>
        <template v-else>
          <div class="hero-badge">Authentic & Handcrafted</div>
          <h1>Bringing the Heart of <span>Kashmir</span> to Your Home</h1>
          <p>Premium dry fruits, exquisite Pashminas, and timeless handicrafts sourced directly from the valleys of Kashmir.</p>
          <div class="hero-actions">
            <router-link to="/products" class="btn btn-secondary">Shop Collection</router-link>
            <button @click="showWalnutBanner = true" class="btn btn-outline-white">Special Offers</button>
          </div>
        </template>
      </div>
    </header>

    <!-- Categories Section -->
    <section id="featured" class="categories-section container">
      <div class="section-header">
        <h2>Curated Collections</h2>
        <p>Discover the finest artisanal treasures from the Valley</p>
      </div>
      
      <div class="category-grid">
        <div class="category-card" v-for="cat in categories" :key="cat.name">
          <div class="cat-image" :style="{ backgroundImage: `url(${cat.image})` }"></div>
          <div class="cat-info">
            <h3>{{ cat.name }}</h3>
            <router-link :to="{ name: 'products', query: { category: cat.id } }" class="btn-link">View All →</router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Best Sellers -->
    <section class="featured-products kashmiri-pattern">
      <div class="container">
        <div class="section-header">
          <h2>Premium Best Sellers</h2>
          <router-link to="/products" class="btn-link">View All Collection →</router-link>
        </div>
        
        <div class="product-grid">
          <div class="product-card" v-for="product in productStore.products.slice(0, 4)" :key="product.id">
            <div class="product-image">
              <img :src="product.image_url || 'https://via.placeholder.com/300x400'" :alt="product.name" />
              <div class="product-badge" v-if="product.stock > 0">In Stock</div>
            </div>
            <div class="product-info">
              <span class="category-tag">Kashmiri Specialty</span>
              <h4>{{ product.name }}</h4>
              <div class="price-row">
                <span class="price">₹{{ product.price }}</span>
                <span v-if="product.discount_price" class="old-price">₹{{ product.discount_price }}</span>
              </div>
              <button @click="addToCart(product)" class="btn btn-primary btn-sm btn-block">Add to Cart</button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useProductStore } from '../stores/productStore'
import { useCartStore } from '../stores/cartStore'

const productStore = useProductStore()
const cartStore = useCartStore()
const showWalnutBanner = ref(false)

const b64_img = (color_hex) => `data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='600'%3E%3Crect width='800' height='600' fill='%23${color_hex}'/%3E%3C/svg%3E`

const categories = [
  { id: 1, name: 'Premium Dry Fruits', image: b64_img('4a2c2a') },
  { id: 2, name: 'Pashmina & Kani', image: b64_img('2d5a27') },
  { id: 3, name: 'Artistic Papier Mâché', image: b64_img('d4af37') }
]

onMounted(() => {
  productStore.fetchProducts()
})

const addToCart = (product) => {
  cartStore.addItem(product)
}
</script>

<style scoped>
.hero {
  height: 90vh;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='1920' height='1080'%3E%3Crect width='1920' height='1080' fill='%234a2c2a'/%3E%3Ctext x='50%25' y='50%25' fill='white' font-size='80' font-family='serif' text-anchor='middle'%3E%3C/text%3E%3C/svg%3E");
  background-size: cover;
  background-position: center;
  position: relative;
  display: flex;
  align-items: center;
  color: white;
  margin-top: -80px; /* Offset for transparent navbar if needed */
  transition: background-image 0.5s ease-in-out;
}

.hero-walnut {
  /* background-image: url("https://www.canva.com/M/MAHECykVWjc/AZzzB21pfRSDZxl9GnQK8A-AZzzB21pywOtcsTb1wVr7g.jpg"); 
  /* Using the @ alias which points to src */
  background-image: url("@/assets/wallnuts/walnut-banner.jpg");
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to right, rgba(0,0,0,0.7), rgba(0,0,0,0.2));
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 800px;
}

.hero-badge {
  display: inline-block;
  background: var(--secondary);
  padding: 0.5rem 1.2rem;
  border-radius: 50px;
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 1.5rem;
}

.hero h1 {
  font-size: 4.5rem;
  line-height: 1.1;
  margin-bottom: 1.5rem;
}

.hero h1 span {
  color: var(--secondary);
}

.hero p {
  font-size: 1.25rem;
  margin-bottom: 2.5rem;
  opacity: 0.9;
  font-weight: 300;
}

.hero-actions {
  display: flex;
  gap: 1.5rem;
}

.btn-outline-white {
  background: transparent;
  border: 2px solid white;
  color: white;
}

.section-header {
  text-align: center;
  margin-bottom: 4rem;
}

.section-header h2 {
  font-size: 2.5rem;
  color: var(--primary);
  margin-bottom: 1rem;
}

.categories-section {
  padding: 8rem 0;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.category-card {
  position: relative;
  height: 450px;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: var(--shadow);
}

.cat-image {
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  transition: transform 0.6s ease;
}

.category-card:hover .cat-image {
  transform: scale(1.1);
}

.cat-info {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  padding: 2rem;
  background: linear-gradient(transparent, rgba(0,0,0,0.8));
  color: white;
}

.cat-info h3 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.featured-products {
  padding: 8rem 0;
  background-color: #f9f6f2;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2.5rem;
}

.product-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: var(--shadow);
  transition: all 0.3s ease;
}

.product-image {
  height: 350px;
  position: relative;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.product-card:hover img {
  transform: scale(1.05);
}

.product-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(255,255,255,0.9);
  padding: 0.4rem 0.8rem;
  border-radius: 50px;
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--accent);
}

.product-info {
  padding: 1.5rem;
}

.category-tag {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--secondary);
  letter-spacing: 1px;
}

.product-info h4 {
  font-size: 1.25rem;
  margin: 0.5rem 0;
  color: var(--primary);
}

.price-row {
  margin-bottom: 1.5rem;
}

.price {
  font-weight: 800;
  font-size: 1.2rem;
  color: var(--text-dark);
}

.old-price {
  text-decoration: line-through;
  color: #999;
  font-size: 0.9rem;
  margin-left: 0.75rem;
}

.btn-link {
  color: var(--secondary);
  text-decoration: none;
  font-weight: 700;
  font-size: 0.9rem;
}

.btn-block {
  width: 100%;
}
</style>
