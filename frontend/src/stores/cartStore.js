import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './authStore'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: JSON.parse(localStorage.getItem('cart_items')) || [],
    loading: false
  }),

  getters: {
    cartCount: (state) => state.items.reduce((total, item) => total + item.quantity, 0),
    cartTotal: (state) => state.items.reduce((total, item) => total + (item.price * item.quantity), 0)
  },

  actions: {
    async addItem(product) {
      const auth = useAuthStore()
      const existing = this.items.find(i => i.product_id === product.id)
      
      if (existing) {
        existing.quantity += 1
      } else {
        this.items.push({
          product_id: product.id,
          name: product.name,
          price: product.discount_price || product.price,
          quantity: 1,
          image_url: product.image_url
        })
      }
      this.persist()

      if (auth.isAuthenticated) {
        await axios.post('/api/cart/add', { product_id: product.id, quantity: 1 })
      }
    },

    async updateQuantity(productId, quantity) {
      const auth = useAuthStore()
      const item = this.items.find(i => i.product_id === productId)
      if (item) {
        item.quantity = quantity
        if (item.quantity <= 0) {
          this.items = this.items.filter(i => i.product_id !== productId)
        }
      }
      this.persist()

      if (auth.isAuthenticated) {
        await axios.put('/api/cart/update', { product_id: productId, quantity })
      }
    },

    async syncWithBackend() {
      const auth = useAuthStore()
      if (!auth.isAuthenticated) return

      try {
        const res = await axios.get('/api/cart/')
        // Simple merge strategy: Backend wins
        if (res.data.length > 0) {
          this.items = res.data
          this.persist()
        }
      } catch (err) {
        console.error('Cart sync failed')
      }
    },

    persist() {
      localStorage.setItem('cart_items', JSON.stringify(this.items))
    },

    clearCart() {
      this.items = []
      this.persist()
    }
  }
})
