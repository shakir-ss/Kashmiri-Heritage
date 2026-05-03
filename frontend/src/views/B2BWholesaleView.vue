<template>
  <div class="b2b-view container">
    <div class="b2b-hero">
      <h1 class="editorial">Partner with Authentic Kashmir</h1>
      <p>Premium Saffron, Walnuts, and Almonds at wholesale scale for businesses worldwide.</p>
    </div>

    <div v-if="success" class="success-screen card">
      <div class="success-icon">🤝</div>
      <h2>Inquiry Received</h2>
      <p>Our B2B team will contact you within 24 hours to discuss tier-pricing and samples.</p>
      <button @click="success = false" class="btn btn-secondary mt-2">Submit Another Request</button>
    </div>

    <div v-else class="b2b-content">
      <div class="b2b-info">
        <h3>Why Partner With Us?</h3>
        <ul>
          <li><strong>Direct from Source:</strong> We bypass middlemen to bring you authentic Pampore Saffron and Kupwara Walnuts.</li>
          <li><strong>Tiered Discounts:</strong> Up to 40% off on MOQ of 50kg+ or ₹1 Lakh+ orders.</li>
          <li><strong>Custom Packaging:</strong> White-labeling available for corporate gifting.</li>
          <li><strong>Priority Logistics:</strong> Specialized air-freight handling for delicate produce.</li>
        </ul>
      </div>

      <div class="b2b-form card">
        <h3>Submit Wholesale Inquiry</h3>
        <div class="form-group">
          <label>Company Name</label>
          <input v-model="form.company_name" placeholder="E.g., Global Traders LLC" />
        </div>
        <div class="form-group">
          <label>Contact Person</label>
          <input v-model="form.contact_name" placeholder="Your Name" />
        </div>
        <div class="form-group">
          <label>Email Address</label>
          <input v-model="form.email" type="email" placeholder="work@company.com" />
        </div>
        <div class="form-group">
          <label>Phone Number</label>
          <input v-model="form.phone" type="tel" placeholder="+91 XXXXXXXXXX" />
        </div>
        <div class="form-group">
          <label>Requirements</label>
          <textarea v-model="form.requirements" rows="4" placeholder="E.g., Need 10kg Mongra Saffron..."></textarea>
        </div>
        <button @click="submitInquiry" class="btn btn-primary btn-block mt-2" :disabled="loading">
          {{ loading ? 'Submitting...' : 'Request Quote' }}
        </button>
        <div class="error-text" v-if="error">{{ error }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const form = ref({
  company_name: '',
  contact_name: '',
  email: '',
  phone: '',
  requirements: ''
})

const loading = ref(false)
const success = ref(false)
const error = ref('')

const submitInquiry = async () => {
  error.value = ''
  if (!form.value.company_name || !form.value.contact_name || !form.value.email || !form.value.requirements) {
    error.value = 'Please fill out all required fields.'
    return
  }

  loading.value = true
  try {
    await axios.post('/api/orders/b2b/inquiry', form.value)
    success.value = true
    form.value = { company_name: '', contact_name: '', email: '', phone: '', requirements: '' }
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to submit inquiry'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.b2b-view {
  padding-top: 4rem;
  padding-bottom: 6rem;
}

.b2b-hero {
  text-align: center;
  margin-bottom: 4rem;
}

.editorial {
  font-family: 'Playfair Display', serif;
  font-size: 3rem;
  color: var(--primary);
  margin-bottom: 1rem;
}

.b2b-hero p {
  font-size: 1.2rem;
  color: #555;
  max-width: 600px;
  margin: 0 auto;
}

.b2b-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: start;
}

.b2b-info h3 {
  font-size: 1.5rem;
  color: var(--primary);
  margin-bottom: 1.5rem;
}

.b2b-info ul {
  list-style: none;
  padding: 0;
}

.b2b-info li {
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
  line-height: 1.6;
  color: #444;
  padding-left: 2rem;
  position: relative;
}

.b2b-info li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #1e7e34;
  font-weight: bold;
}

.b2b-info strong {
  color: var(--primary);
}

.b2b-form {
  padding: 2.5rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}

.b2b-form h3 {
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  color: var(--primary);
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #555;
}

.form-group input, .form-group textarea {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-family: inherit;
  font-size: 1rem;
}

.error-text {
  color: #d00;
  margin-top: 1rem;
  text-align: center;
}

.success-screen {
  text-align: center;
  padding: 5rem 2rem;
  background: white;
}

.success-icon {
  font-size: 5rem;
  margin-bottom: 1rem;
}

@media (max-width: 768px) {
  .b2b-content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
}
</style>
