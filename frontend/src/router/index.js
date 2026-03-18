import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/products',
      name: 'products',
      component: () => import('../views/ProductsView.vue')
    },
    {
      path: '/cart',
      name: 'cart',
      component: () => import('../views/CartView.vue')
    },
    {
      path: '/products/:id',
      name: 'product-detail',
      component: () => import('../views/ProductDetailView.vue')
    },
    {
      path: '/wishlist',
      name: 'wishlist',
      component: () => import('../views/WishlistView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/checkout',
      name: 'checkout',
      component: () => import('../views/CheckoutView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/orders',
      name: 'orders',
      component: () => import('../views/OrdersView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/AdminDashboard.vue'),
      meta: { requiresAdmin: true }
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/contact',
      name: 'contact',
      component: () => import('../views/ContactView.vue')
    }
  ]
})

// Navigation Guard
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  
  if (to.meta.requiresAdmin && !auth.isAdmin) {
    next({ name: 'login' })
  } else if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next({ name: 'login' })
  } else if (auth.isAuthenticated && (to.name === 'login' || to.name === 'register')) {
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router
