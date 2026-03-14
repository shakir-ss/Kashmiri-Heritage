<template>
  <div class="product-card">
    <div class="product-image">
      <img :src="product.image_url || 'https://via.placeholder.com/300x200?text=Kashmiri+Product'" :alt="product.name" />
      <div v-if="product.discount_price" class="badge">Offer</div>
    </div>
    <div class="product-info">
      <p class="category-tag">{{ product.category }}</p>
      <h4>{{ product.name }}</h4>
      <div class="price-row">
        <span class="price">₹{{ product.discount_price || product.price }}</span>
        <span v-if="product.discount_price" class="old-price">₹{{ product.price }}</span>
      </div>
      <button 
        @click="$emit('add-to-cart', product)" 
        class="btn btn-secondary btn-sm"
        :disabled="product.stock <= 0"
      >
        {{ product.stock > 0 ? 'Add to Cart' : 'Out of Stock' }}
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps(['product'])
defineEmits(['add-to-cart'])
</script>

<style scoped>
.product-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: var(--shadow);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.08);
}

.product-image {
  height: 200px;
  position: relative;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: var(--secondary);
  color: white;
  padding: 0.25rem 0.6rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 700;
}

.product-info {
  padding: 1.25rem;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.category-tag {
  font-size: 0.7rem;
  text-transform: uppercase;
  color: #888;
  letter-spacing: 1px;
  margin-bottom: 0.25rem;
}

.product-info h4 {
  color: var(--primary);
  margin-bottom: 0.75rem;
  font-size: 1.1rem;
}

.price-row {
  margin-bottom: 1.25rem;
}

.price {
  font-size: 1.2rem;
  font-weight: 800;
  color: var(--accent);
}

.old-price {
  text-decoration: line-through;
  color: #999;
  font-size: 0.9rem;
  margin-left: 0.5rem;
}

.btn-sm {
  width: 100%;
  margin-top: auto;
}
</style>
