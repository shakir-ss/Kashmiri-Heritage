import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('token') || null,
    loading: false,
    error: null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.role === 'admin'
  },
  
  actions: {
  init() {
    if (this.token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
    }
  },
  async login(email, password) {
    this.loading = true
    this.error = null
    try {
      const response = await axios.post('/api/auth/login', { email, password })
      this.token = response.data.token
      this.user = response.data.user

      localStorage.setItem('token', this.token)
      localStorage.setItem('user', JSON.stringify(this.user))

      // CRITICAL: Set the header for all subsequent requests
      axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`

      return true
    } catch (err) {
      this.error = err.response?.data?.message || 'Login failed'
      return false
    } finally {
      this.loading = false
    }
  },    
    async register(name, email, password) {
      this.loading = true
      this.error = null
      try {
        await axios.post('/api/auth/register', { name, email, password })
        return true
      } catch (err) {
        this.error = err.response?.data?.message || 'Registration failed'
        return false
      } finally {
        this.loading = false
      }
    },
    
    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      delete axios.defaults.headers.common['Authorization']
    }
  }
})
