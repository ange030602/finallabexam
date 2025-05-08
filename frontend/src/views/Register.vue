<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card shadow p-4" style="width: 100%; max-width: 400px;">
      <h3 class="text-center mb-4">Create a New Account</h3>

      <!-- Username Input -->
      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <input v-model="username" id="username" class="form-control" placeholder="Enter your username" />
      </div>

      <!-- Password Input -->
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input type="password" v-model="password" id="password" class="form-control" placeholder="Enter your password" />
      </div>

      <!-- Role Selector -->
      <div class="mb-3">
        <label for="role" class="form-label">Role</label>
        <select v-model="role" id="role" class="form-control">
          <option value="employee">Employee</option>
          <option value="consumer">Consumer</option>
        </select>
      </div>

      <!-- Register Button -->
      <button @click="register" :disabled="loading" class="btn btn-primary w-100">
        {{ loading ? 'Registering...' : 'Register' }}
      </button>

      <!-- Feedback Message -->
      <div v-if="message" class="alert mt-3" :class="{'alert-success': success, 'alert-danger': !success}">
        {{ message }}
      </div>
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
      role: 'consumer',
      message: '',
      success: false,
      loading: false,
    };
  },
  methods: {
    async register() {
      this.loading = true;
      this.message = '';
      try {
        await axios.post('/api/register/', {
          username: this.username,
          password: this.password,
          role: this.role,
        });
        this.success = true;
        this.message = 'Registration successful! You can now log in.';
      } catch (error) {
        this.success = false;
        this.message = 'Registration failed. Please try again.';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
