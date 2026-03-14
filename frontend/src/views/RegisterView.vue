<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2 class="auth-title">Create Account</h2>
      <p class="auth-subtitle">Join us to shop the finest Kashmiri products</p>
      
      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="form-group">
          <label>Full Name</label>
          <input v-model="name" type="text" placeholder="Enter your full name" required />
        </div>

        <div class="form-group">
          <label>Email Address</label>
          <input v-model="email" type="email" placeholder="Enter your email" required />
        </div>
        
        <div class="form-group">
          <label>Password</label>
          <input v-model="password" type="password" placeholder="Create a password" required />
        </div>
        
        <div v-if="authStore.error" class="error-message">
          {{ authStore.error }}
        </div>

        <div v-if="successMessage" class="success-message">
          {{ successMessage }}
        </div>
        
        <button type="submit" class="btn btn-secondary btn-block" :disabled="authStore.loading">
          {{ authStore.loading ? 'Creating account...' : 'Register' }}
        </button>
      </form>
      
      <p class="auth-footer">
        Already have an account? <router-link to="/login">Login here</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/authStore'
import { useRouter } from 'vue-router'

const name = ref('')
const email = ref('')
const password = ref('')
const successMessage = ref('')
const authStore = useAuthStore()
const router = useRouter()

const handleRegister = async () => {
  const success = await authStore.register(name.value, email.value, password.value)
  if (success) {
    successMessage.value = 'Registration successful! Redirecting to login...'
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  }
}
</script>

<style scoped>
/* Reusing styles from LoginView - In a real project we'd use common CSS classes */
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

.success-message {
  background: #e6fffa;
  color: #2c7a7b;
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
