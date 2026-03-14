<template>
  <div class="app-wrapper">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="container nav-content">
        <router-link to="/" class="logo">Kashmiri <span>Dry Fruits</span></router-link>
        <div class="nav-links">
          <router-link to="/products">Products</router-link>
          <router-link to="/products">Handicrafts</router-link>
          <router-link to="/cart" class="cart-link">
            Cart <span v-if="cartStore.cartCount > 0" class="cart-badge">{{ cartStore.cartCount }}</span>
          </router-link>
          
          <template v-if="!authStore.isAuthenticated">
            <router-link to="/login" class="btn btn-primary btn-nav">Login</router-link>
          </template>
          
          <template v-else>
            <div class="user-menu">
              <router-link v-if="authStore.isAdmin" to="/admin" class="admin-link">Dashboard</router-link>
              <span>Salam, {{ authStore.user?.name.split(' ')[0] }}</span>
              <button @click="handleLogout" class="btn btn-outline btn-sm">Logout</button>
            </div>
          </template>
        </div>
      </div>
    </nav>

    <!-- Page Content -->
    <router-view />

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <p>&copy; 2026 Kashmiri Dry Fruits. All Rights Reserved.</p>
        <p class="premium-tag">Premium Quality from the Heart of the Valley</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { onMounted, watch } from 'vue'
import { useAuthStore } from './stores/authStore'
import { useCartStore } from './stores/cartStore'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const cartStore = useCartStore()
const router = useRouter()

onMounted(() => {
  if (authStore.isAuthenticated) {
    cartStore.syncWithBackend()
  }
})

// Sync cart on login
watch(() => authStore.isAuthenticated, (newVal) => {
  if (newVal) cartStore.syncWithBackend()
})

const handleLogout = () => {
  authStore.logout()
  cartStore.clearCart()
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  height: 80px;
  background: var(--white);
  box-shadow: var(--shadow);
  display: flex;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  color: var(--primary);
  font-weight: 800;
  text-decoration: none;
}

.logo span {
  color: var(--secondary);
}

.nav-links {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav-links a {
  text-decoration: none;
  color: var(--text);
  font-weight: 500;
  transition: color 0.2s;
}

.nav-links a:hover {
  color: var(--secondary);
}

.cart-link {
  position: relative;
}

.cart-badge {
  background: var(--secondary);
  color: white;
  font-size: 0.7rem;
  padding: 2px 6px;
  border-radius: 10px;
  position: absolute;
  top: -12px;
  right: -10px;
  font-weight: 800;
}

.btn-nav {
  padding: 0.5rem 1.5rem;
  text-decoration: none;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-weight: 600;
  color: var(--primary);
}

.admin-link {
  color: var(--secondary);
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 1px;
  margin-right: 0.5rem;
}

.btn-sm {
  padding: 0.4rem 0.8rem;
  font-size: 0.8rem;
  border: 1px solid var(--primary);
  background: transparent;
  color: var(--primary);
}

.btn-sm:hover {
  background: var(--primary);
  color: white;
}

.footer {
  padding: 3rem 0;
  text-align: center;
  background: #2c1810;
  color: #fff;
  margin-top: 4rem;
}

.premium-tag {
  color: var(--secondary);
  font-size: 0.8rem;
  margin-top: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}
</style>
