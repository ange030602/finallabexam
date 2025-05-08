<template>
  <div class="container mt-5">
    <h2 class="mb-4">📦 Products</h2>

    <!-- Product Grid -->
    <div class="row">
      <div v-for="product in products" :key="product.id" class="col-12 col-md-6 col-lg-4 mb-4">
        <div class="card shadow-sm h-100">
          <div class="card-body d-flex flex-column">
            <img
              v-if="product.image"
              :src="product.image"
              alt="Product image"
              class="img-fluid mb-3"
              style="max-height: 200px; object-fit: contain;"
            />
            <h5 class="card-title">{{ product.name }}</h5>
            <p class="card-text">{{ product.description }}</p>
            <p><strong>Price:</strong> ${{ product.price }}</p>
            <p><strong>In stock:</strong> {{ product.stock }}</p>
            <button class="btn btn-success mt-auto" @click="addToCart(product)" :disabled="product.stock <= 0">
              Add to Cart
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 🧾 Order Summary Section -->
    <div class="alert alert-info mt-4" v-if="cartSummary.totalItems > 0">
      <h5>Order Summary</h5>
      <p><strong>Total Items:</strong> {{ cartSummary.totalItems }}</p>
      <p><strong>Total Cost:</strong> ${{ cartSummary.totalCost.toFixed(2) }}</p>
    </div>

    <router-link to="/cart" class="btn btn-primary mt-4">View Cart</router-link>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  data() {
    return {
      products: [],
      cartKey: 0, // used to force reactivity
    };
  },
  mounted() {
    this.fetchProducts();
  },
  methods: {
    async fetchProducts() {
      try {
        const res = await axios.get('/api/products/');
        this.products = res.data;
      } catch (error) {
        console.error('Failed to fetch products:', error);
      }
    },
    addToCart(product) {
      if (!localStorage.getItem('token')) {
        alert('Please log in first.');
        this.$router.push('/login');
        return;
      }

      if (product.stock <= 0) {
        alert('Sorry, this item is out of stock.');
        return;
      }

      let cart = JSON.parse(localStorage.getItem('cart') || '[]');
      const idx = cart.findIndex(item => item.product.id === product.id);

      if (idx !== -1) {
        if (cart[idx].quantity + 1 > product.stock) {
          alert('Cannot add more than available stock.');
          return;
        }
        cart[idx].quantity += 1;
      } else {
        cart.push({ product, quantity: 1 });
      }

      localStorage.setItem('cart', JSON.stringify(cart));

      const productIndex = this.products.findIndex(p => p.id === product.id);
      if (productIndex !== -1 && this.products[productIndex].stock > 0) {
        this.products[productIndex].stock -= 1;
      }

      this.cartKey++; 
      alert('Added to cart!');
    }
  },
  computed: {
    cartSummary() {
      this.cartKey; 
      const cart = JSON.parse(localStorage.getItem('cart') || '[]');
      let totalItems = 0;
      let totalCost = 0;

      for (const item of cart) {
        totalItems += item.quantity;
        totalCost += item.product.price * item.quantity;
      }

      return { totalItems, totalCost };
    }
  }
};
</script>

<style scoped>
.card-body img {
  display: block;
  margin-left: auto;
  margin-right: auto;
}

.card {
  border-radius: 1rem;
}

.card-title {
  font-weight: 600;
}

.card-text {
  font-size: 0.95rem;
}

button:disabled {
  opacity: 0.7;
}
</style>
