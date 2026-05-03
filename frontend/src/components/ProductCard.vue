<template>
  <div class="product-card card" @click="goToDetail" :class="{ 'list-mode': listView }">
    <div class="product-image">
      <img :src="product.image_url || 'https://via.placeholder.com/300x400?text=Kashmiri+Art'" :alt="product.name" />
      <div v-if="product.discount_price" class="discount-badge">Special Offer</div>
      <button @click.stop="toggleWishlist" class="card-wishlist-btn" :class="{ active: isInWishlist }">
        {{ isInWishlist ? '❤️' : '🤍' }}
      </button>
    </div>
    <div class="product-info">
      <span class="category-tag">{{ product.category || 'Kashmiri Artisanal' }}</span>
      <h4>{{ product.name }}</h4>
      <p class="description-preview" v-if="product.description">{{ truncate(product.description, listView ? 120 : 60) }}</p>
      <div class="product-meta" v-if="listView">
        <span v-if="product.weight_grams" class="meta-chip">⚖️ {{ product.weight_grams }}g</span>
        <span v-if="product.stock > 0" class="meta-chip in-stock">✓ In Stock</span>
        <span v-else class="meta-chip out-stock">✗ Out of Stock</span>
        <span v-if="product.variants && product.variants.length" class="meta-chip">{{ product.variants.length }} variants</span>
      </div>
      <div class="price-row">
        <span class="price">₹{{ product.discount_price || product.price }}</span>
        <span v-if="product.discount_price" class="old-price">₹{{ product.price }}</span>
        <span v-if="product.discount_price" class="save-tag">
          Save {{ Math.round((1 - product.discount_price / product.price) * 100) }}%
        </span>
      </div>
      <div v-if="!listView" class="stock-status" :class="{ 'out-of-stock-text': product.stock <= 0 }">
        {{ product.stock > 0 ? 'In Stock' : 'Out of Stock' }}
      </div>
      <div class="card-actions">
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
        <button v-if="listView" @click.stop="goToDetail" class="btn btn-outline btn-sm">View Details</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useWishlistStore } from '../stores/wishlistStore'
import { useCartStore } from '../stores/cartStore'
import { computed } from 'vue'

const props = defineProps({
  product: Object,
  listView: { type: Boolean, default: false }
})
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
/* ===== GRID MODE (default) ===== */
.product-card {
  padding: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  border: 1px solid rgba(0,0,0,0.05);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  border-radius: 14px;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 16px 40px rgba(0,0,0,0.1);
}

.product-image {
  height: 220px;
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.product-card:hover .product-image img {
  transform: scale(1.08);
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
  font-size: 0.85rem;
}

.card-wishlist-btn.active { background: #fff0f0; }

.discount-badge {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  background: var(--secondary);
  color: white;
  padding: 0.3rem 0.7rem;
  border-radius: 50px;
  font-size: 0.65rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.product-info {
  padding: 1.25rem;
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
  margin-bottom: 0.4rem;
}

.product-info h4 {
  font-size: 1.05rem;
  color: var(--primary);
  margin-bottom: 0.4rem;
  line-height: 1.3;
}

.description-preview {
  font-size: 0.82rem;
  color: var(--text-muted);
  margin-bottom: 0.75rem;
  line-height: 1.5;
}

.price-row {
  margin-bottom: 0.75rem;
  margin-top: auto;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.price {
  font-weight: 800;
  font-size: 1.2rem;
  color: var(--text-dark);
}

.old-price {
  text-decoration: line-through;
  color: #bbb;
  font-size: 0.9rem;
}

.save-tag {
  background: #fef3c7;
  color: #92400e;
  padding: 0.15rem 0.5rem;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 800;
}

.stock-status {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  color: #2c7a7b;
  margin-bottom: 0.75rem;
}

.stock-status.out-of-stock-text { color: #d00; }

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-sm {
  flex: 1;
  padding: 0.65rem;
  font-size: 0.85rem;
}

/* ===== LIST MODE ===== */
.product-card.list-mode {
  flex-direction: row;
  align-items: center;
  border-radius: 12px;
}

.product-card.list-mode .product-image {
  width: 180px;
  height: 140px;
  flex-shrink: 0;
  border-radius: 0;
}

.product-card.list-mode .product-info {
  padding: 1.25rem 1.5rem;
  flex-direction: column;
  gap: 0.25rem;
}

.product-card.list-mode h4 {
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
}

.product-meta {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 0.5rem;
}

.meta-chip {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 0.2rem 0.6rem;
  border-radius: 20px;
  background: #f0ede8;
  color: var(--primary);
}

.meta-chip.in-stock { background: #e6f4ea; color: #1e7e34; }
.meta-chip.out-stock { background: #fde8e8; color: #c00; }

.product-card.list-mode .price-row { margin-top: 0; margin-bottom: 0.5rem; }

.product-card.list-mode .card-actions {
  flex-shrink: 0;
  margin-left: auto;
  flex-direction: column;
  gap: 0.4rem;
  padding-right: 1.25rem;
  min-width: 140px;
}

.product-card.list-mode .btn-sm { flex: none; width: 100%; }

@media (max-width: 640px) {
  .product-card.list-mode { flex-direction: column; }
  .product-card.list-mode .product-image { width: 100%; height: 200px; }
  .product-card.list-mode .card-actions { margin-left: 0; padding-right: 0; min-width: auto; flex-direction: row; }
}
</style>
