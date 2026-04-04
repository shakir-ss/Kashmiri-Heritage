<template>
  <div class="product-card card" @click="goToDetail">
    <div class="product-image">
      <img :src="product.image_url || 'https://via.placeholder.com/300x400?text=Kashmiri+Art'" :alt="product.name" />
      <div v-if="product.discount_price" class="discount-badge">Special Offer</div>
      <button @click.stop="toggleWishlist" class="card-wishlist-btn" :class="{ active: isInWishlist }">
        {{ isInWishlist ? '❤️' : '🤍' }}
      </button>
    </div>
    <div class="product-info">
      <span class="category-tag">Kashmiri Artisanal</span>
      <h4>{{ product.name }}</h4>
      <p class="description-preview" v-if="product.description">{{ truncate(product.description, 60) }}</p>
      <div class="price-row">
        <span class="price">₹{{ product.discount_price || product.price }}</span>
        <span v-if="product.discount_price" class="old-price">₹{{ product.price }}</span>
      </div>
      <div class="stock-status" :class="{ 'out-of-stock-text': product.stock <= 0 }">
        {{ product.stock > 0 ? 'In Stock' : 'Out of Stock' }}
      </div>
      <button 
        v-if="!isInCart"
        @click.stop="$emit('add-to-cart', product)" 
        class="btn btn-primary btn-sm"
        :disabled="product.stock <= 0"
      >
        {{ product.stock > 0 ? 'Add to Cart' : 'Out of Stock' }}
      </button>
      <button 
        v-else
        @click.stop="goToCart" 
        class="btn btn-secondary btn-sm"
      >
        Go to Cart →
      </button>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useWishlistStore } from '../stores/wishlistStore'
import { useCartStore } from '../stores/cartStore'
import { computed } from 'vue'

const props = defineProps(['product'])
defineEmits(['add-to-cart'])

const router = useRouter()
const wishlistStore = useWishlistStore()
const cartStore = useCartStore()

const isInWishlist = computed(() => wishlistStore.isInWishlist(props.product.id))
const isInCart = computed(() => cartStore.isInCart(props.product.id))

const goToDetail = () => {
  router.push({ name: 'product-detail', params: { id: props.product.id } })
}

const goToCart = () => {
  router.push({ name: 'cart' })
}

const toggleWishlist = () => {
  wishlistStore.toggleWishlist(props.product)
}

const truncate = (text, length) => {
  return text.length > length ? text.substring(0, length) + '...' : text
}
</script>

<style scoped>
.product-card {
  padding: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  border: 1px solid rgba(0,0,0,0.03);
  cursor: pointer;
}

.product-image {
  height: 280px;
  position: relative;
  overflow: hidden;
}

.card-wishlist-btn {
  position: absolute;
  top: 0.75rem;
  left: 0.75rem;
  background: white;
  border: none;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  cursor: pointer;
  z-index: 2;
}

.card-wishlist-btn.active { background: #fff0f0; }

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.product-card:hover .product-image img {
  transform: scale(1.1);
}

.discount-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: var(--secondary);
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: 50px;
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.product-info {
  padding: 1.5rem;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.category-tag {
  font-size: 0.65rem;
  font-weight: 800;
  text-transform: uppercase;
  color: var(--secondary);
  letter-spacing: 1.5px;
  margin-bottom: 0.5rem;
}

.product-info h4 {
  font-size: 1.2rem;
  color: var(--primary);
  margin-bottom: 0.5rem;
  line-height: 1.3;
}

.description-preview {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-bottom: 1rem;
  line-height: 1.5;
}

.price-row {
  margin-bottom: 1.5rem;
  margin-top: auto;
}

.price {
  font-weight: 800;
  font-size: 1.25rem;
  color: var(--text-dark);
}

.old-price {
  text-decoration: line-through;
  color: #bbb;
  font-size: 0.9rem;
  margin-left: 0.75rem;
}

.stock-status {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  color: #2c7a7b;
  margin-bottom: 1rem;
}

.stock-status.out-of-stock-text {
  color: #d00;
}

.btn-sm {
  width: 100%;
  padding: 0.75rem;
}
</style>
