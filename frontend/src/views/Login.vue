<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card shadow p-4" style="width: 100%; max-width: 400px;">
      <h3 class="text-center mb-4">Login to Your Account</h3>

      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <input v-model="username" id="username" class="form-control" placeholder="Enter your username" />
      </div>

      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input type="password" v-model="password" id="password" class="form-control" placeholder="Enter your password" />
      </div>

      <button @click="login" :disabled="loading" class="btn btn-success w-100">
        {{ loading ? 'Logging in...' : 'Login' }}
      </button>

      <div v-if="message" class="alert alert-danger mt-3 text-center">{{ message }}</div>
    </div>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      message: '',
      loading: false,
    };
  },
  methods: {
    async login() {
      this.message = '';
      this.loading = true;
      try {
        const response = await axios.post('/api/login/', {
          username: this.username,
          password: this.password,
        });

        localStorage.setItem('token', response.data.token);
        localStorage.setItem('user_id', response.data.user_id);

        const roleResp = await axios.get('/api/role/');
        this.$router.push(roleResp.data.role === 'employee' ? '/employee' : '/consumer');
      } catch (error) {
        this.message = 'Invalid credentials.';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
