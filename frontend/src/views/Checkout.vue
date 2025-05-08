<template>
  <div class="container mt-5">
    <h2 class="mb-4">Consumer Checkout Details</h2>
    <table class="table table-striped" v-if="checkouts.length">
      <thead class="table-dark">
        <tr>
          <th>Order ID</th>
          <th>Consumer Name</th>
          <th>Products</th>
          <th>Total Price</th>
          <th>Status</th>
          <th>Date</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="checkout in checkouts" :key="checkout.id">
          <td>{{ checkout.id }}</td>
          <td>{{ checkout.consumer_name || 'N/A' }}</td>
          <td>
            <ul>
              <li>{{ checkout.product.name }} x{{ checkout.quantity }}</li>
            </ul>
          </td>
          <td>{{ (checkout.product.price * checkout.quantity).toFixed(2) }} ₱</td>
          <td>{{ checkout.status || 'Pending' }}</td>
          <td>{{ new Date(checkout.created_at).toLocaleString() }}</td>
        </tr>
      </tbody>
    </table>
    <div v-else>
      <p>No Checkout Data Found.</p>
    </div>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  name: 'Checkout',
  data() {
    return {
      checkouts: []
    };
  },
  mounted() {
    this.fetchCheckouts();
  },
  methods: {
    async fetchCheckouts() {
      try {
        const response = await axios.get('/api/admin/checkouts/');
        this.checkouts = response.data;
      } catch (error) {
        console.error('Failed to fetch checkouts:', error.response?.data || error);
      }
    }
  }
};
</script>
