<template>
  <component :is="AnalyticsComponent" v-if="analyticsEnabled" />
  <div class="app-wrapper">
    <!-- Top Bar -->
    <div class="top-bar">
      <div class="container top-bar-content">
        <span>Authentic Kashmiri Treasures Delivered Worldwide</span>
        <div class="top-links">
          <router-link to="/orders" v-if="auth.isAuthenticated">My Orders</router-link>
          <a href="#">Track Shipping</a>
        </div>
      </div>
    </div>

    <!-- Navbar -->
    <nav class="navbar" :class="{ 'nav-scrolled': scrolly > 50 }">
      <div class="container nav-content">
        <router-link to="/" class="logo">The Hundred <span>Villages</span></router-link>
        
        <div class="nav-links">
          <router-link to="/products">Products</router-link>
          
          <div class="nav-actions">
            <router-link to="/wishlist" class="nav-icon-link" title="Wishlist">
              <span class="icon">🤍</span>
            </router-link>
            <router-link to="/cart" class="cart-link">
              <span class="cart-icon">🛒</span>
              <span v-if="cartStore.cartCount > 0" class="cart-badge">{{ cartStore.cartCount }}</span>
            </router-link>

            <template v-if="!auth.isAuthenticated">
              <router-link to="/login" class="btn btn-outline btn-nav">Login</router-link>
            </template>
            <template v-else>
              <router-link to="/admin" v-if="auth.isAdmin" class="admin-tag">Admin</router-link>
              <button @click="handleLogout" class="btn-text">Logout</button>
            </template>
          </div>
        </div>
      </div>
    </nav>

    <!-- Page Content -->
    <router-view></router-view>

    <!-- Footer -->
    <footer class="footer">
      <div class="container footer-grid">
        <div class="footer-brand">
          <router-link to="/" class="logo white">The Hundred <span>Villages</span></router-link>
          <p>Preserving the heritage of the Valley through authentic products and artisanal crafts. Sourced with care, delivered with love.</p>
        </div>
        <div class="footer-links">
          <h4>Quick Links</h4>
          <router-link to="/products">All Products</router-link>
          <router-link to="/about">Our Story</router-link>
          <router-link to="/contact">Contact Us</router-link>
        </div>
        <div class="footer-contact">
          <h4>Newsletter</h4>
          <p>Subscribe for updates on new arrivals and seasonal harvest.</p>
          <div class="subscribe-form">
            <input type="email" placeholder="Your Email" />
            <button class="btn btn-secondary btn-sm">Join</button>
          </div>
        </div>
      </div>
      <div class="container footer-bottom">
        <p>© 2026 The Hundred Villages. Artisanal Quality from the Heart of the Valley.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, defineAsyncComponent } from 'vue'
import { useAuthStore } from './stores/authStore'
import { useCartStore } from './stores/cartStore'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const cartStore = useCartStore()
const router = useRouter()
const scrolly = ref(0)

// Conditional Analytics for Local Dev
const analyticsEnabled = import.meta.env.VITE_VERCEL_ANALYTICS === 'true'
const AnalyticsComponent = analyticsEnabled 
  ? defineAsyncComponent(() => import(/* @vite-ignore */ '@vercel/analytics/vue').then(m => m.Analytics))
  : null

const handleScroll = () => {
  scrolly.value = window.scrollY
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

const handleLogout = () => {
  auth.logout()
  router.push('/')
}
</script>

<style scoped>
.app-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.top-bar {
  background: var(--primary);
  color: white;
  padding: 0.5rem 0;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 1px;
}

.top-bar-content {
  display: flex;
  justify-content: space-between;
}

.top-links {
  display: flex;
  gap: 1.5rem;
}

.top-links a {
  color: white;
  text-decoration: none;
}

.navbar {
  transition: all 0.3s ease;
}

.nav-scrolled {
  padding: 0.5rem 0;
  box-shadow: var(--shadow);
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.cart-link {
  position: relative;
  text-decoration: none;
}

.cart-icon {
  font-size: 1.2rem;
}

.cart-badge {
  position: absolute;
  top: -8px;
  right: -10px;
  background: var(--secondary);
  color: white;
  font-size: 0.6rem;
  font-weight: 800;
  padding: 2px 6px;
  border-radius: 10px;
  border: 2px solid white;
}

.admin-tag {
  background: #eee;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--primary);
  text-decoration: none;
}

.btn-nav {
  padding: 0.5rem 1.5rem;
}

.logo.white {
  color: white;
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1.5fr;
  gap: 4rem;
}

.footer-brand p {
  margin-top: 1.5rem;
  opacity: 0.7;
  font-size: 0.9rem;
  line-height: 1.8;
}

.footer h4 {
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
  letter-spacing: 1px;
}

.footer-links {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.footer-links a {
  color: white;
  text-decoration: none;
  opacity: 0.7;
  font-size: 0.9rem;
  transition: opacity 0.2s;
}

.footer-links a:hover {
  opacity: 1;
  color: var(--secondary);
}

.subscribe-form {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
}

.subscribe-form input {
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.2);
  padding: 0.75rem;
  border-radius: 8px;
  color: white;
  flex-grow: 1;
}

.footer-bottom {
  margin-top: 4rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(255,255,255,0.1);
  text-align: center;
  font-size: 0.8rem;
  opacity: 0.5;
}

.btn-text {
  background: none;
  border: none;
  color: var(--text-dark);
  font-weight: 600;
  cursor: pointer;
}

@media (max-width: 768px) {
  .footer-grid {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }
}
</style>
