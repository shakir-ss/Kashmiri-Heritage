<template>
  <div>
    <!-- Hero Section -->
    <header class="hero">
      <div class="container hero-content">
        <h2>Premium. Organic. Authentic.</h2>
        <p>Bringing the finest flavors of the Valley straight to your doorstep.</p>
        <div class="hero-actions">
          <button class="btn btn-secondary">Shop Dry Fruits</button>
          <button class="btn btn-outline">Explore Shawls</button>
        </div>
      </div>
    </header>

    <!-- Content -->
    <main class="container main-content">
      <section class="placeholder-section">
        <h3>Our Favorites</h3>
        <div class="product-grid">
          <!-- Real Product Card -->
          <div class="product-card" v-for="product in productStore.products.slice(0, 3)" :key="product.id">
            <div class="product-image">
              <img v-if="product.image_url" :src="product.image_url" :alt="product.name" />
            </div>
            <div class="product-info">
              <h4>{{ product.name }}</h4>
              <p class="price">
                ₹{{ product.price }} 
                <span v-if="product.discount_price" class="old-price">₹{{ product.discount_price }}</span>
              </p>
              <button @click="addToCart(product)" class="btn btn-secondary btn-sm">Add to Cart</button>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useProductStore } from '../stores/productStore'
import { useCartStore } from '../stores/cartStore'

const productStore = useProductStore()
const cartStore = useCartStore()

onMounted(() => {
  productStore.fetchProducts()
})

const addToCart = (product) => {
  cartStore.addItem(product)
}
</script>

<style scoped>
.hero {
  background: linear-gradient(rgba(139, 69, 19, 0.4), rgba(139, 69, 19, 0.6)), 
              url('https://images.unsplash.com/photo-1596515101107-111d4d386b1f?q=80&w=2070&auto=format&fit=crop');
  background-size: cover;
  background-position: center;
  height: 500px;
  display: flex;
  align-items: center;
  color: white;
  text-align: center;
}

.hero-content h2 {
  font-size: 3.5rem;
  margin-bottom: 1rem;
}

.hero-content p {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  max-width: 600px;
  margin-inline: auto;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.btn-outline {
  background: transparent;
  border: 2px solid white;
  color: white;
}

.main-content {
  padding: 4rem 0;
}

.placeholder-section h3 {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 3rem;
  color: var(--primary);
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.product-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow);
  transition: transform 0.3s ease;
}

.product-card:hover {
  transform: translateY(-5px);
}

.product-image {
  height: 200px;
  background: #eee;
}

.product-info {
  padding: 1.5rem;
}

.product-info h4 {
  margin-bottom: 0.5rem;
  color: var(--primary);
}

.price {
  font-weight: 700;
  color: var(--accent);
  margin-bottom: 1rem;
}

.old-price {
  text-decoration: line-through;
  color: #999;
  font-size: 0.9rem;
  margin-left: 0.5rem;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  width: 100%;
}
</style>
