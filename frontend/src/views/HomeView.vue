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

    <!-- Heritage Trust Bar -->
    <div class="trust-bar">
      <div class="container trust-content">
        <div class="trust-item">
          <span class="trust-icon">🏺</span>
          <div class="trust-text">
            <strong>Direct from Artisans</strong>
            <p>Fair trade & direct sourcing</p>
          </div>
        </div>
        <div class="trust-divider"></div>
        <div class="trust-item">
          <span class="trust-icon">🔬</span>
          <div class="trust-text">
            <strong>Lab Certified</strong>
            <p>100% Pure Grade A++ Saffron</p>
          </div>
        </div>
        <div class="trust-divider"></div>
        <div class="trust-item">
          <span class="trust-icon">✈️</span>
          <div class="trust-text">
            <strong>Global Delivery</strong>
            <p>Secure worldwide shipping</p>
          </div>
        </div>
      </div>
    </div>

    <!-- SVG Divider -->
    <svg class="section-divider" viewBox="0 0 1440 100" preserveAspectRatio="none">
      <path d="M0,0 C240,100 480,100 720,50 C960,0 1200,0 1440,100 L1440,100 L0,100 Z"></path>
    </svg>

    <!-- Categories Section -->
    <section id="featured" class="categories-section container">
      <div class="section-header">
        <span class="category-tag">Heritage Collections</span>
        <h2>Curated Treasures</h2>
        <p class="fw-light">Discover the finest artisanal gems from the Kashmir Valley</p>
      </div>
      
      <div class="category-grid">
        <div class="category-card tilla-hover" v-for="cat in categories" :key="cat.name">
          <div class="cat-image" :style="{ backgroundImage: `url(${cat.image})` }"></div>
          <div class="cat-info">
            <h3>{{ cat.name }}</h3>
            <router-link :to="{ name: 'products', query: { category: cat.id } }" class="btn-link">View All Collection →</router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Artisan Spotlight -->
    <section class="artisan-spotlight kashmiri-pattern">
      <div class="container spotlight-grid">
        <div class="spotlight-image-wrapper">
          <div class="spotlight-image"></div>
          <div class="experience-badge">40+ Years of Craft</div>
        </div>
        <div class="spotlight-content">
          <div class="category-tag">The Hands Behind the Heritage</div>
          <h2>Master Weaver: <span class="italic">Abdul Rashid</span></h2>
          <p class="quote">"Each Pashmina I weave is a story of my ancestors, passed down through generations. When you wear our heritage, you carry the soul of Kashmir."</p>
          <div class="spotlight-stats">
            <div class="stat">
              <span class="stat-num">100%</span>
              <span class="stat-label">Hand Spun</span>
            </div>
            <div class="stat">
              <span class="stat-num">6+ Months</span>
              <span class="stat-label">Per Masterpiece</span>
            </div>
          </div>
          <router-link to="/products?category=2" class="btn btn-primary">Meet the Artisans</router-link>
        </div>
      </div>
    </section>

    <!-- Best Sellers -->
    <section class="featured-products">
      <div class="container">
        <div class="section-header">
          <span class="category-tag">Customer Favorites</span>
          <h2>Premium Best Sellers</h2>
          <router-link to="/products" class="btn-link">Shop Entire Store →</router-link>
        </div>
        
        <div class="product-grid">
          <!-- Skeleton Loader -->
          <template v-if="productStore.loading">
            <div class="product-card" v-for="i in 4" :key="i">
              <div class="product-image skeleton"></div>
              <div class="product-info">
                <div class="skeleton" style="height: 10px; width: 40%; margin-bottom: 10px;"></div>
                <div class="skeleton" style="height: 20px; width: 80%; margin-bottom: 15px;"></div>
                <div class="skeleton" style="height: 40px; width: 100%;"></div>
              </div>
            </div>
          </template>

          <div v-else class="product-card card" v-for="product in productStore.products.slice(0, 4)" :key="product.id">
            <router-link :to="'/products/' + product.id" class="product-image">
              <img :src="product.image_url || 'https://via.placeholder.com/300x400'" :alt="product.name" />
              <div class="product-badge" v-if="product.stock > 0">Hand-Selected</div>
            </router-link>
            <div class="product-info">
              <span class="category-tag">Kashmiri Specialty</span>
              <router-link :to="'/products/' + product.id" style="text-decoration: none; display: block; margin: 0.5rem 0;">
                <h4 style="margin: 0;">{{ product.name }}</h4>
              </router-link>
              <div class="price-row" style="margin-bottom: 1rem;">
                <span class="price">₹{{ product.price }}</span>
                <span v-if="product.discount_price" class="old-price">₹{{ product.discount_price }}</span>
              </div>
            </div>
            <div style="padding: 0 1.5rem 1.5rem 1.5rem;">
              <button @click="addToCart(product)" class="btn btn-primary btn-sm btn-block">Add to Cart</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Social Proof / Testimonials -->
    <section class="testimonials-section container">
      <div class="section-header">
        <span class="category-tag">Global Appreciation</span>
        <h2>Heritage in Your Homes</h2>
      </div>
      <div class="testimonial-grid">
        <div class="testimonial-card card">
          <div class="rating">⭐⭐⭐⭐ stars</div>
          <p>"The Saffron quality is unlike anything I've found in Europe. Truly authentic and the packaging is premium."</p>
          <div class="user-info">
            <strong>Sarah J.</strong>
            <span>London, UK</span>
          </div>
        </div>
        <div class="testimonial-card card highlight-testimonial">
          <div class="rating">⭐⭐⭐⭐⭐ stars</div>
          <p>"My Kani shawl is a work of art. You can feel the months of labor in every thread. Excellent service and fast delivery."</p>
          <div class="user-info">
            <strong>Priya M.</strong>
            <span>Mumbai, India</span>
          </div>
        </div>
        <div class="testimonial-card card">
          <div class="rating">⭐⭐⭐⭐⭐ stars</div>
          <p>"The Mamra almonds are so fresh and crunchy. I love knowing they come directly from Kashmiri orchards."</p>
          <div class="user-info">
            <strong>David L.</strong>
            <span>Dubai, UAE</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProductStore } from '../stores/productStore'
import { useCartStore } from '../stores/cartStore'

const productStore = useProductStore()
const cartStore = useCartStore()
const router = useRouter()
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

/* Heritage Trust Bar */
.trust-bar {
  background: white;
  padding: 2.5rem 0;
  border-bottom: 1px solid #eee;
  box-shadow: 0 4px 20px rgba(0,0,0,0.02);
}

.trust-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.trust-item {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.trust-icon {
  font-size: 2rem;
  filter: drop-shadow(0 2px 5px rgba(0,0,0,0.1));
}

.trust-text strong {
  display: block;
  font-size: 1rem;
  color: var(--primary);
  margin-bottom: 0.2rem;
}

.trust-text p {
  font-size: 0.85rem;
  color: #777;
  margin: 0;
}

.trust-divider {
  width: 1px;
  height: 40px;
  background: #eee;
}

/* Artisan Spotlight */
.artisan-spotlight {
  padding: 8rem 0;
  background: #fff;
  overflow: hidden;
}

.spotlight-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 5rem;
  align-items: center;
}

.spotlight-image-wrapper {
  position: relative;
}

.spotlight-image {
  height: 600px;
  background-image: url("https://images.unsplash.com/photo-1590073844006-33379778ae09?auto=format&fit=crop&q=80&w=800");
  background-size: cover;
  background-position: center;
  border-radius: 30px;
  box-shadow: 30px 30px 0 var(--pattern-color, #f4f1ea);
}

.experience-badge {
  position: absolute;
  bottom: 2rem;
  right: -2rem;
  background: var(--primary);
  color: white;
  padding: 1.5rem 2rem;
  border-radius: 15px;
  font-weight: 700;
  box-shadow: var(--shadow);
}

.spotlight-content h2 {
  font-size: 3rem;
  margin: 1.5rem 0;
  color: var(--primary);
}

.quote {
  font-family: 'Playfair Display', serif;
  font-style: italic;
  font-size: 1.5rem;
  color: #555;
  line-height: 1.6;
  margin-bottom: 2.5rem;
  position: relative;
}

.quote::before {
  content: '"';
  position: absolute;
  top: -2rem;
  left: -1rem;
  font-size: 5rem;
  color: var(--secondary);
  opacity: 0.3;
}

.spotlight-stats {
  display: flex;
  gap: 3rem;
  margin-bottom: 3rem;
}

.stat-num {
  display: block;
  font-family: 'Playfair Display', serif;
  font-size: 2.5rem;
  font-weight: 900;
  color: var(--secondary);
}

.stat-label {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #888;
}

/* Testimonials */
.testimonials-section {
  padding: 8rem 0;
}

.testimonial-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

.testimonial-card {
  padding: 3rem 2rem;
  text-align: center;
}

.highlight-testimonial {
  background: var(--primary);
  color: white;
  transform: scale(1.05);
}

.highlight-testimonial p { color: #ccc; }
.highlight-testimonial .rating { color: var(--secondary); }

.rating {
  font-size: 0.8rem;
  margin-bottom: 1.5rem;
  color: var(--tilla-gold);
}

.testimonial-card p {
  font-size: 1.1rem;
  margin-bottom: 2rem;
  font-style: italic;
}

.user-info strong {
  display: block;
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

.user-info span {
  font-size: 0.8rem;
  color: #888;
}

.highlight-testimonial .user-info span { color: #aaa; }

@media (max-width: 768px) {
  .trust-content { flex-direction: column; gap: 2rem; text-align: center; }
  .trust-item { flex-direction: column; gap: 0.5rem; }
  .trust-divider { display: none; }
  .spotlight-grid { grid-template-columns: 1fr; gap: 3rem; }
  .spotlight-image { height: 400px; }
  .experience-badge { right: 1rem; }
  .testimonial-grid { grid-template-columns: 1fr; }
  .highlight-testimonial { transform: none; }
}
</style>
