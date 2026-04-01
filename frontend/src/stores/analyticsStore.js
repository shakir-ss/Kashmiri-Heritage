import { defineStore } from 'pinia'
import axios from 'axios'
import { API_URL } from '../config'

export const useAnalyticsStore = defineStore('analytics', {
  state: () => ({
    stats: {
      revenue: 0,
      total_orders: 0,
      popular_items: [],
      best_sellers: [],
      abandoned_carts: 0
    },
    loading: false,
    error: null
  }),

  actions: {
    async fetchStats() {
      this.loading = true
      try {
        const res = await axios.get(`${API_URL}/api/analytics/stats`)
        this.stats = res.data
      } catch (err) {
        this.error = 'Failed to fetch analytics data'
      } finally {
        this.loading = false
      }
    },

    async trackProductView(productId) {
      try {
        await axios.post(`${API_URL}/api/analytics/view/${productId}`)
      } catch (err) {
        // Silent error for tracking failure
        console.warn('Tracking failed for product:', productId)
      }
    }
  }
})
