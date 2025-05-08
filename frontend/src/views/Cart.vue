<template>
  <div class="container mt-5">
    <h2 class="mb-4">🛒 Your Cart</h2>

    <!-- Back to Consumer Panel Button -->
    <div class="mb-3">
      <button class="btn btn-outline-primary" @click="goBackToConsumer">
        ← Back to Consumer Panel
      </button>
    </div>

    <!-- Empty Cart Message -->
    <div v-if="cart.length === 0" class="alert alert-info text-center">
      Your cart is empty. Go add some items!
    </div>

    <!-- Cart Items -->
    <div v-else>
      <div class="row">
        <div v-for="item in cart" :key="item.product.id" class="col-12 col-md-6 col-lg-4 mb-3">
          <div class="card shadow-sm h-100">
            <div class="card-body d-flex flex-column justify-content-between">
              <div>
                <h5 class="card-title mb-1">{{ item.product.name }}</h5>
                <p class="card-text mb-0">Price: ${{ item.product.price }}</p>
                <p class="mb-0">Qty: {{ item.quantity }}</p>
              </div>
              <button class="btn btn-outline-danger btn-sm mt-3" @click="removeItem(item.product.id)">
                Remove
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Checkout Button -->
      <div class="d-flex justify-content-end mt-4">
        <button class="btn btn-success px-4" :disabled="loading" @click="checkout">
          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
          Checkout
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  data() {
    return {
      cart: [],
      loading: false
    };
  },
  mounted() {
    this.cart = JSON.parse(localStorage.getItem('cart') || '[]');
  },
  methods: {
    goBackToConsumer() {
      this.$router.push('/consumer');
    },
    removeItem(productId) {
      this.cart = this.cart.filter(i => i.product.id !== productId);
      localStorage.setItem('cart', JSON.stringify(this.cart));
    },
    async checkout() {
      const userId = parseInt(localStorage.getItem('user_id'));
      const token = localStorage.getItem('token');

      if (!userId || !token) {
        alert('You must be logged in to checkout.');
        this.$router.push('/login');
        return;
      }

      if (this.cart.length === 0) {
        alert('Your cart is empty.');
        return;
      }

      this.loading = true;

      try {
        for (const item of this.cart) {
          const res = await axios.post('/api/checkout/', {
            user: userId,
            product: item.product.id,
            quantity: item.quantity
          }, {
            headers: {
              Authorization: `Token ${token}`
            }
          });

          console.log(`✔️ Checked out ${item.quantity} x ${item.product.name}`, res.data);
        }

        alert('✅ All items checked out successfully!');
        localStorage.removeItem('cart');
        this.cart = [];
        this.$router.push('/consumer');

      } catch (error) {
        console.error('❌ Checkout failed:', error.response?.data || error);
        alert(error.response?.data?.error || 'Checkout failed.');
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.card-title {
  font-weight: 600;
}

.card-body {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.card-body p {
  font-size: 0.95rem;
}

.card {
  border-radius: 1rem;
}

button:disabled {
  opacity: 0.7;
}
</style>
