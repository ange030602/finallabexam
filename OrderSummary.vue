<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="container" style="max-width: 800px;">
      <h2 class="mb-4">Your Orders</h2>

      <!-- Loading Spinner -->
      <div v-if="loading" class="d-flex justify-content-center">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="alert alert-danger text-center">
        There was an error fetching your orders. Please try again later.
      </div>

      <!-- Orders List -->
      <div v-if="!loading && !error && orders.length === 0" class="alert alert-info text-center">
        You have no orders yet.
      </div>

      <!-- Order Cards -->
      <div v-for="order in orders" :key="order.id" class="card mb-3 shadow-sm">
        <div class="card-body">
          <h5 class="card-title">Product: {{ order.product_name }}</h5>
          <p class="card-text">
            <strong>Quantity:</strong> {{ order.quantity }} <br />
            <strong>Total Price:</strong> ${{ order.total_price.toFixed(2) }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  data() {
    return {
      orders: [],
      loading: true,
      error: false,
    };
  },
  async mounted() {
    try {
      const userId = localStorage.getItem('user_id');
      const response = await axios.get(`/api/orders/?user=${userId}`);
      this.orders = response.data;
    } catch (err) {
      this.error = true;
    } finally {
      this.loading = false;
    }
  },
};
</script>

<style scoped>
.card {
  border-radius: 0.75rem;
}
.card-body {
  padding: 1.5rem;
}
</style>
