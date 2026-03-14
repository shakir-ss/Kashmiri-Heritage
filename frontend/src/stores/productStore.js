import { defineStore } from 'pinia'
import axios from 'axios'

export const useProductStore = defineStore('products', {
  state: () => ({
    products: [],
    categories: [],
    loading: false,
    error: null
  }),
  
  actions: {
    async fetchCategories() {
      try {
        const res = await axios.get('/api/products/categories')
        this.categories = res.data
      } catch (err) {
        this.error = 'Failed to fetch categories'
      }
    },

    async fetchProducts(query = {}) {
      this.loading = true
      try {
        const res = await axios.get('/api/products/', { params: query })
        this.products = res.data
      } catch (err) {
        this.error = 'Failed to fetch products'
      } finally {
        this.loading = false
      }
    },

    async fetchProductById(id) {
      this.loading = true
      try {
        const res = await axios.get(`/api/products/${id}`)
        return res.data
      } catch (err) {
        this.error = 'Failed to fetch product details'
        return null
      } finally {
        this.loading = false
      }
    },

    async addProduct(productData) {
      try {
        await axios.post('/api/products/', productData)
        await this.fetchProducts()
        return true
      } catch (err) {
        this.error = err.response?.data?.message || 'Failed to add product'
        return false
      }
    },

    async updateProduct(id, productData) {
      try {
        await axios.put(`/api/products/${id}`, productData)
        await this.fetchProducts()
        return true
      } catch (err) {
        this.error = 'Failed to update product'
        return false
      }
    },

    async deleteProduct(id) {
      if (!confirm('Are you sure you want to delete this product?')) return
      try {
        await axios.delete(`/api/products/${id}`)
        await this.fetchProducts()
      } catch (err) {
        this.error = 'Failed to delete product'
      }
    }
  }
})
