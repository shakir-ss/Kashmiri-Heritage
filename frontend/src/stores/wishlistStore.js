import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './authStore'

export const useWishlistStore = defineStore('wishlist', {
  state: () => ({
    items: [],
    loading: false
  }),

  actions: {
    async fetchWishlist() {
      const auth = useAuthStore()
      if (!auth.isAuthenticated) return
      
      this.loading = true
      try {
        const res = await axios.get('/api/wishlist/')
        this.items = res.data
      } catch (err) {
        console.error('Failed to fetch wishlist:', err)
      } finally {
        this.loading = false
      }
    },

    async toggleWishlist(product) {
      const auth = useAuthStore()
      if (!auth.isAuthenticated) {
        alert('Please login to use wishlist')
        return
      }

      const index = this.items.findIndex(item => item.product_id === product.id)
      if (index > -1) {
        // Remove
        try {
          await axios.delete(`/api/wishlist/remove/${product.id}`)
          this.items.splice(index, 1)
        } catch (err) {
          console.error('Failed to remove from wishlist:', err)
        }
      } else {
        // Add
        try {
          await axios.post('/api/wishlist/add', { product_id: product.id })
          this.items.push({
            product_id: product.id,
            name: product.name,
            price: product.price,
            image_url: product.image_url,
            slug: product.slug
          })
        } catch (err) {
          console.error('Failed to add to wishlist:', err)
        }
      }
    },

    isInWishlist(productId) {
      return this.items.some(item => item.product_id === productId)
    }
  }
})
