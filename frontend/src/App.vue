<template>
  <component :is="AnalyticsComponent" v-if="analyticsEnabled" />
  <div class="app-wrapper">
    <!-- Top Bar -->
    <div class="top-bar">
      <div class="container top-bar-content">
        <span>Authentic Kashmiri Treasures Delivered Worldwide</span>
        <div class="top-links">
          <router-link to="/orders" v-if="auth.isAuthenticated">My Orders</router-link>
          <router-link to="/track">Track Shipping</router-link>
        </div>
      </div>
    </div>

    <!-- Navbar -->
    <nav class="navbar" :class="{ 'nav-scrolled': scrolly > 50 }">
      <div class="container nav-content">
        <router-link @click="closeMenu" to="/" class="logo">The Hundred <span>Villages</span></router-link>
        
        <!-- Hamburger Menu Toggle -->
        <button class="mobile-menu-toggle" @click="isMenuOpen = !isMenuOpen" :class="{ 'active': isMenuOpen }" aria-label="Toggle Menu">
          <span class="bar"></span>
          <span class="bar"></span>
          <span class="bar"></span>
        </button>

        <!-- Mobile Overlay -->
        <div class="nav-overlay" :class="{ 'active': isMenuOpen }" @click="closeMenu"></div>

        <div class="nav-links" :class="{ 'mobile-active': isMenuOpen }">
          <!-- Mega Menu Trigger -->
          <div class="mega-menu-wrapper" @mouseenter="megaOpen = true" @mouseleave="megaOpen = false">
            <router-link @click="closeMenu" to="/products" class="mega-trigger">Products ▾</router-link>
            <transition name="mega-fade">
              <div class="mega-menu" v-if="megaOpen">
                <div class="mega-inner container">
                  <div class="mega-search">
                    <input
                      v-model="megaSearch"
                      @input="debounceMegaSearch"
                      placeholder="Search products…"
                      @keyup.enter="goToSearch"
                    />
                    <div class="mega-suggestions" v-if="megaSuggestions.length">
                      <router-link
                        v-for="s in megaSuggestions"
                        :key="s.id"
                        :to="`/products/${s.id}`"
                        class="suggestion-item"
                        @click="closeMega"
                      >
                        <img :src="s.image_url" :alt="s.name" class="suggestion-img" />
                        <span>{{ s.name }}</span>
                        <strong>₹{{ s.discount_price || s.price }}</strong>
                      </router-link>
                    </div>
                  </div>
                  <div class="mega-categories">
                    <router-link
                      v-for="cat in categories"
                      :key="cat.id"
                      :to="`/products?category=${cat.slug}`"
                      class="mega-cat-card"
                      @click="closeMega"
                    >
                      <span v-if="cat.image_url" class="mega-cat-img">
                        <img :src="cat.image_url" :alt="cat.name" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%;" />
                      </span>
                      <span v-else class="mega-cat-icon">{{ cat.icon || '🌿' }}</span>
                      <span class="mega-cat-name">{{ cat.name }}</span>
                    </router-link>
                    <router-link to="/products" class="mega-cat-card all-link" @click="closeMega">
                      <span class="mega-cat-icon">🛍️</span>
                      <span class="mega-cat-name">All Products</span>
                    </router-link>
                  </div>
                </div>
              </div>
            </transition>
          </div>
          <router-link @click="closeMenu" to="/wholesale">Wholesale</router-link>
          
          <div class="nav-actions">
            <router-link @click="closeMenu" to="/wishlist" class="nav-icon-link" title="Wishlist">
              <span class="icon">🤍</span>
              <span class="mobile-only-text">Wishlist</span>
            </router-link>
            <router-link @click="closeMenu" to="/cart" class="cart-link">
              <span class="cart-icon">🛒</span>
              <span v-if="cartStore.cartCount > 0" class="cart-badge">{{ cartStore.cartCount }}</span>
              <span class="mobile-only-text">Cart</span>
            </router-link>

            <template v-if="!auth.isAuthenticated">
              <router-link @click="closeMenu" to="/login" class="btn btn-outline btn-nav">Login</router-link>
            </template>
            <template v-else>
              <router-link @click="closeMenu" to="/admin" v-if="auth.isAdmin" class="admin-tag">Admin</router-link>
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
          <router-link to="/wholesale">B2B Wholesale</router-link>
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

    <!-- Floating Artisan Support -->
    <div class="floating-support">
      <div class="support-bubble">Talk to an Artisan</div>
      <a href="https://wa.me/917889527508" target="_blank" class="btn-support" aria-label="WhatsApp Support">
        <span>💬</span>
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, defineAsyncComponent } from 'vue'
import { useAuthStore } from './stores/authStore'
import { useCartStore } from './stores/cartStore'
import { useRouter } from 'vue-router'
import axios from 'axios'

const auth = useAuthStore()
const cartStore = useCartStore()
const router = useRouter()
const scrolly = ref(0)
const isMenuOpen = ref(false)
const megaOpen = ref(false)
const megaSearch = ref('')
const megaSuggestions = ref([])
const categories = ref([])

const closeMenu = () => {
  isMenuOpen.value = false
}

const closeMega = () => {
  megaOpen.value = false
  megaSearch.value = ''
  megaSuggestions.value = []
}

let megaTimer;
const debounceMegaSearch = () => {
  clearTimeout(megaTimer)
  if (!megaSearch.value.trim()) { megaSuggestions.value = []; return }
  megaTimer = setTimeout(async () => {
    try {
      const res = await axios.get('/api/products/', { params: { q: megaSearch.value } })
      megaSuggestions.value = res.data.slice(0, 5)
    } catch {}
  }, 250)
}

const goToSearch = () => {
  if (megaSearch.value.trim()) {
    router.push(`/products?search=${encodeURIComponent(megaSearch.value)}`)
    closeMega()
  }
}

// Conditional Analytics for Local Dev
const analyticsEnabled = import.meta.env.VITE_VERCEL_ANALYTICS === 'true'
const AnalyticsComponent = analyticsEnabled 
  ? defineAsyncComponent(() => import(/* @vite-ignore */ '@vercel/analytics/vue').then(m => m.Analytics))
  : null

const handleScroll = () => {
  scrolly.value = window.scrollY
}

onMounted(async () => {
  window.addEventListener('scroll', handleScroll)
  
  // Load categories for mega menu
  try {
    const res = await axios.get('/api/products/categories')
    categories.value = res.data
  } catch {}

  // Silent ping to wake up the Render backend (Free Tier)
  axios.get('/health').catch(() => {
    console.log("Waking up the artisanal servers...");
  });
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

/* Mobile Menu Styles */
.mobile-menu-toggle {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  z-index: 1001;
}

.mobile-menu-toggle .bar {
  width: 25px;
  height: 3px;
  background-color: var(--primary);
  border-radius: 2px;
  transition: all 0.3s ease;
}

.mobile-only-text {
  display: none;
}

/* Mobile Menu Styles */
.nav-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  z-index: 999;
  opacity: 0;
  visibility: hidden;
  transition: all 0.4s ease;
}

.nav-overlay.active {
  opacity: 1;
  visibility: visible;
}

.mobile-menu-toggle {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  z-index: 1001;
  padding: 10px;
  margin-right: -10px;
}

.mobile-menu-toggle .bar {
  width: 25px;
  height: 3px;
  background-color: var(--primary);
  border-radius: 2px;
  transition: all 0.3s ease;
}

@media (max-width: 768px) {
  .mobile-menu-toggle {
    display: flex;
  }

  /* Hamburger Animation */
  .mobile-menu-toggle.active .bar:nth-child(1) { transform: translateY(8px) rotate(45deg); }
  .mobile-menu-toggle.active .bar:nth-child(2) { opacity: 0; }
  .mobile-menu-toggle.active .bar:nth-child(3) { transform: translateY(-8px) rotate(-45deg); }

  .nav-links {
    position: fixed;
    top: 0;
    right: 0;
    width: 80%;
    max-width: 300px;
    height: 100vh;
    background: white;
    flex-direction: column;
    align-items: flex-start;
    padding: 6rem 2rem;
    gap: 2rem;
    transform: translateX(100%);
    visibility: hidden;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: -10px 0 30px rgba(0,0,0,0.1);
    z-index: 1000;
  }

  .nav-links.mobile-active {
    transform: translateX(0);
    visibility: visible;
  }

  .nav-actions {
    flex-direction: column;
    align-items: flex-start;
    width: 100%;
    gap: 2rem;
  }

  .nav-icon-link, .cart-link {
    display: flex;
    align-items: center;
    gap: 1rem;
    font-weight: 600;
    color: var(--text-dark);
    text-decoration: none;
  }

  .mobile-only-text {
    display: inline;
    font-size: 1rem;
  }

  .cart-badge {
    position: static;
    margin-left: 0.5rem;
  }

  .btn-nav {
    width: 100%;
  }
}

@media (max-width: 768px) {
  .footer-grid {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }
}

/* ===== MEGA MENU ===== */
.mega-menu-wrapper {
  position: relative;
}

.mega-trigger {
  text-decoration: none;
  font-weight: 600;
  color: var(--text-dark);
  transition: color 0.2s;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.mega-trigger:hover { color: var(--secondary); }

.mega-menu {
  position: fixed;
  top: 80px;
  left: 0;
  right: 0;
  background: white;
  box-shadow: 0 20px 60px rgba(0,0,0,0.12);
  z-index: 900;
  border-top: 3px solid var(--secondary);
}

.mega-inner {
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 3rem;
  padding: 2.5rem 0;
}

/* Search pane */
.mega-search {
  position: relative;
}

.mega-search input {
  width: 100%;
  padding: 0.85rem 1.2rem;
  border: 2px solid #eee;
  border-radius: 10px;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.2s;
}

.mega-search input:focus { border-color: var(--secondary); }

.mega-suggestions {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  right: 0;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.12);
  z-index: 10;
  overflow: hidden;
}

.suggestion-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.8rem 1rem;
  text-decoration: none;
  color: var(--text-dark);
  transition: background 0.15s;
  border-bottom: 1px solid #f0f0f0;
}

.suggestion-item:last-child { border-bottom: none; }
.suggestion-item:hover { background: #fdfaf5; }

.suggestion-img {
  width: 42px;
  height: 42px;
  object-fit: cover;
  border-radius: 6px;
  flex-shrink: 0;
}

.suggestion-item span { flex: 1; font-size: 0.9rem; }
.suggestion-item strong { color: var(--secondary); font-size: 0.9rem; }

/* Category grid pane */
.mega-categories {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
  gap: 1rem;
  align-content: start;
}

.mega-cat-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1.2rem 0.75rem;
  border-radius: 12px;
  border: 2px solid #f0ede8;
  text-decoration: none;
  color: var(--primary);
  transition: all 0.2s;
  background: #fdfaf5;
}

.mega-cat-card:hover {
  border-color: var(--secondary);
  background: #fff8ee;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}

.mega-cat-icon { font-size: 2rem; }
.mega-cat-name { font-size: 0.8rem; font-weight: 700; text-align: center; }

.all-link { border-color: var(--secondary); }

/* Transition */
.mega-fade-enter-active,
.mega-fade-leave-active { transition: opacity 0.2s, transform 0.2s; }
.mega-fade-enter-from,
.mega-fade-leave-to { opacity: 0; transform: translateY(-8px); }

@media (max-width: 768px) {
  .mega-menu-wrapper { width: 100%; }
  .mega-menu { top: 0; position: static; box-shadow: none; border: none; }
  .mega-inner { grid-template-columns: 1fr; gap: 1.5rem; }
}
</style>
