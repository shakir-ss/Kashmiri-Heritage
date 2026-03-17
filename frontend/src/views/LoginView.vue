<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2 class="auth-title">Welcome Back</h2>
      <p class="auth-subtitle">Login to your Kashmiri Heritage account</p>
      
      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label>Email Address</label>
          <input v-model="email" type="email" placeholder="Enter your email" required />
        </div>
        
        <div class="form-group">
          <label>Password</label>
          <input v-model="password" type="password" placeholder="Enter your password" required />
        </div>
        
        <div v-if="authStore.error" class="error-message">
          {{ authStore.error }}
        </div>
        
        <button type="submit" class="btn btn-secondary btn-block" :disabled="authStore.loading">
          {{ authStore.loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>
      
      <p class="auth-footer">
        Don't have an account? <router-link to="/register">Register here</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const authStore = useAuthStore()
const router = useRouter()

const handleLogin = async () => {
  const success = await authStore.login(email.value, password.value)
  if (success) {
    router.push('/')
  }
}
</script>

<style scoped>
.auth-container {
  min-height: calc(100vh - 80px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: #fdfaf5;
}

.auth-card {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.05);
  width: 100%;
  max-width: 400px;
}

.auth-title {
  color: var(--primary);
  margin-bottom: 0.5rem;
  text-align: center;
}

.auth-subtitle {
  color: #666;
  text-align: center;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  font-size: 0.9rem;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  outline: none;
}

.form-group input:focus {
  border-color: var(--secondary);
}

.error-message {
  background: #fff0f0;
  color: #d00;
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 0.85rem;
  text-align: center;
}

.btn-block {
  width: 100%;
  margin-top: 1rem;
}

.auth-footer {
  text-align: center;
  margin-top: 1.5rem;
  font-size: 0.9rem;
}

.auth-footer a {
  color: var(--secondary);
  text-decoration: none;
  font-weight: 600;
}
</style>
