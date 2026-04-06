import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './authStore'
import { useWishlistStore } from './wishlistStore'
import { API_URL } from '../config'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: JSON.parse(localStorage.getItem('cart_items')) || [],
    loading: false
  }),

  getters: {
    cartCount: (state) => state.items.reduce((total, item) => total + item.quantity, 0),
    cartTotal: (state) => state.items.reduce((total, item) => {
      // Only include items that are in stock in the total
      if (item.stock > 0) {
        return total + (item.price * item.quantity)
      }
      return total
    }, 0),
    isInCart: (state) => (productId) => state.items.some(item => item.product_id === productId)
  },

  actions: {
    async addItem(product, quantity = 1) {
      const auth = useAuthStore()
      const existing = this.items.find(i => i.product_id === product.id)
      
      if (existing) {
        if (existing.quantity + quantity > product.stock) {
          alert(`Only ${product.stock} items available in total.`)
          return
        }
        existing.quantity += quantity
      } else {
        if (quantity > product.stock) {
          alert(`Only ${product.stock} items available.`)
          return
        }
        this.items.push({
          product_id: product.id,
          name: product.name,
          price: product.discount_price || product.price,
          quantity: quantity,
          image_url: product.image_url,
          stock: product.stock // Store current known stock
        })
      }
      this.persist()

      if (auth.isAuthenticated) {
        await axios.post('/api/cart/add', { product_id: product.id, quantity })
        await this.syncWithBackend()
      }
    },

    async updateQuantity(productId, quantity) {
      const auth = useAuthStore()
      const item = this.items.find(i => i.product_id === productId)
      if (item) {
        if (quantity > item.stock) {
          alert(`Only ${item.stock} items available.`)
          return
        }
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

    async removeItem(productId) {
      const auth = useAuthStore()
      this.items = this.items.filter(i => i.product_id !== productId)
      this.persist()

      if (auth.isAuthenticated) {
        await axios.delete(`/api/cart/remove/${productId}`)
      }
    },

    async moveToWishlist(productId) {
      const auth = useAuthStore()
      const wishlist = useWishlistStore()
      
      if (!auth.isAuthenticated) {
        alert('Please login to save items to your wishlist.')
        return
      }

      const item = this.items.find(i => i.product_id === productId)
      if (item) {
        // Mock product object for wishlist toggle
        const productObj = { id: productId, name: item.name, price: item.price, image_url: item.image_url }
        await wishlist.toggleWishlist(productObj)
        await this.removeItem(productId)
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
