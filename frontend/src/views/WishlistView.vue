<template>
  <div class="wishlist-view container">
    <h2 class="section-title">My Wishlist</h2>
    
    <div v-if="wishlistStore.items.length === 0" class="empty-state card">
      <div class="empty-icon">🤍</div>
      <h3>Your wishlist is empty</h3>
      <p>Save items you love to find them easily later.</p>
      <router-link to="/products" class="btn btn-primary mt-2">Explore Products</router-link>
    </div>

    <div v-else class="wishlist-grid">
      <div v-for="item in wishlistStore.items" :key="item.id" class="wishlist-card card">
        <router-link :to="'/products/' + item.product_id" class="wishlist-image">
          <img :src="item.image_url || 'https://via.placeholder.com/300'" :alt="item.name" />
        </router-link>
        <div class="wishlist-info">
          <router-link :to="'/products/' + item.product_id" class="item-name-link">
            <h4>{{ item.name }}</h4>
          </router-link>
          <p class="price">₹{{ item.price }}</p>
          <div class="card-actions">
            <button @click="addToCart(item)" class="btn btn-secondary btn-sm">Add to Cart</button>
            <button @click="removeFromWishlist(item.product_id)" class="btn-text delete">Remove</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useWishlistStore } from '../stores/wishlistStore'
import { useCartStore } from '../stores/cartStore'

const wishlistStore = useWishlistStore()
const cartStore = useCartStore()

onMounted(() => {
  wishlistStore.fetchWishlist()
})

const addToCart = (item) => {
  cartStore.addItem({
    id: item.product_id,
    name: item.name,
    price: item.price,
    image_url: item.image_url
  })
}

const removeFromWishlist = (productId) => {
  wishlistStore.toggleWishlist({ id: productId })
}
</script>

<style scoped>
.wishlist-view {
  padding-top: 3rem;
  padding-bottom: 8rem;
}

.section-title {
  margin-bottom: 3rem;
  color: var(--primary);
}

.empty-state {
  text-align: center;
  padding: 5rem;
  max-width: 600px;
  margin: 0 auto;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  opacity: 0.2;
}

.wishlist-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2rem;
}

.wishlist-card {
  padding: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.wishlist-image {
  height: 250px;
}

.wishlist-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.wishlist-info {
  padding: 1.5rem;
}

.wishlist-info h4 {
  color: var(--primary);
  margin-bottom: 0.5rem;
}

.item-name-link {
  text-decoration: none;
}

.item-name-link:hover h4 {
  color: var(--secondary);
}

.price {
  font-weight: 700;
  margin-bottom: 1.5rem;
}

.card-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.btn-text.delete {
  color: #d00;
  font-size: 0.8rem;
}

.mt-2 { margin-top: 2rem; }
</style>
