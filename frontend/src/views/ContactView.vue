<template>
  <div class="contact-view container">
    <div v-if="submitted" class="success-screen card artisan-border">
      <div class="success-icon">✉️</div>
      <h2>Message Received</h2>
      <p>Thank you for reaching out to Kashmiri Heritage. Our team will review your query and get back to you shortly.</p>
      <button @click="submitted = false" class="btn btn-primary">Send Another Message</button>
    </div>

    <div v-else class="contact-grid">
      <div class="contact-info">
        <span class="category-tag">Connect with Us</span>
        <h1>We'd Love to Hear <span>From You</span></h1>
        <p>Whether you have a question about our artisanal process, need help with an order, or want to discuss a custom heritage piece, we're here to help.</p>
        
        <div class="info-items">
          <div class="info-item">
            <span class="icon">📍</span>
            <div>
              <strong>Heritage Hub</strong>
              <p>Residency Road, Srinagar, Jammu & Kashmir, 190001</p>
            </div>
          </div>
          <div class="info-item">
            <span class="icon">📞</span>
            <div>
              <strong>Call / WhatsApp</strong>
              <p>+91 9906 123 456</p>
            </div>
          </div>
          <div class="info-item">
            <span class="icon">📧</span>
            <div>
              <strong>Email Us</strong>
              <p>support@kashmiriheritage.com</p>
            </div>
          </div>
        </div>
      </div>

      <div class="contact-form-wrapper card artisan-border">
        <form @submit.prevent="handleSubmit" class="contact-form">
          <div class="form-row">
            <div class="form-group">
              <label>Full Name</label>
              <input v-model="form.name" type="text" placeholder="Your Name" required />
            </div>
            <div class="form-group">
              <label>Email Address</label>
              <input v-model="form.email" type="email" placeholder="email@example.com" required />
            </div>
          </div>
          
          <div class="form-row">
            <div class="form-group">
              <label>Phone Number (Optional)</label>
              <input v-model="form.phone" type="tel" placeholder="+91 ..." />
            </div>
            <div class="form-group">
              <label>Subject</label>
              <select v-model="form.subject">
                <option value="General Query">General Query</option>
                <option value="Order Support">Order Support</option>
                <option value="Artisan Collaboration">Artisan Collaboration</option>
                <option value="Bulk/Corporate">Bulk/Corporate Inquiries</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label>How can we help? (Optional description)</label>
            <textarea v-model="form.message" rows="5" placeholder="Share your thoughts or questions here..." required></textarea>
          </div>

          <button type="submit" class="btn btn-primary btn-block" :disabled="loading">
            {{ loading ? 'Sending Heritage Message...' : 'Send Message' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const submitted = ref(false)
const loading = ref(false)
const form = ref({
  name: '',
  email: '',
  phone: '',
  subject: 'General Query',
  message: ''
})

const handleSubmit = async () => {
  loading.ref = true
  try {
    await axios.post('/api/contact/', form.value)
    submitted.value = true
    form.value = { name: '', email: '', phone: '', subject: 'General Query', message: '' }
  } catch (error) {
    alert('Failed to send message. Please try again or contact us via WhatsApp.')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.contact-view { padding: 8rem 0; }
.contact-grid { display: grid; grid-template-columns: 1fr 1.2fr; gap: 6rem; align-items: start; }

.contact-info h1 { font-size: 3.5rem; margin: 1.5rem 0; }
.contact-info h1 span { color: var(--secondary); }
.contact-info p { color: #666; font-size: 1.1rem; margin-bottom: 3rem; }

.info-items { display: grid; gap: 2rem; }
.info-item { display: flex; gap: 1.5rem; align-items: flex-start; }
.info-item .icon { font-size: 1.5rem; background: #f9f6f2; padding: 1rem; border-radius: 12px; }
.info-item strong { display: block; color: var(--primary); margin-bottom: 0.25rem; }
.info-item p { margin: 0; font-size: 0.95rem; }

.contact-form-wrapper { padding: 3rem; background: white; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 1.5rem; }
.form-group { margin-bottom: 1.5rem; }
.form-group label { display: block; font-size: 0.85rem; font-weight: 700; margin-bottom: 0.5rem; color: var(--primary); }
.form-group input, .form-group select, .form-group textarea {
  width: 100%; padding: 0.8rem 1rem; border: 1px solid #ddd; border-radius: 8px; font-family: inherit;
}

.success-screen { text-align: center; padding: 5rem; max-width: 600px; margin: 0 auto; }
.success-icon { font-size: 4rem; margin-bottom: 2rem; }
.success-screen h2 { margin-bottom: 1rem; color: var(--primary); }
.success-screen p { margin-bottom: 3rem; color: #666; }

@media (max-width: 900px) {
  .contact-grid { grid-template-columns: 1fr; gap: 4rem; }
  .form-row { grid-template-columns: 1fr; }
}
</style>
