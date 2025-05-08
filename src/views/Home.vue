<template>
  <div class="home-hero">
    <div class="welcome-card">
      <h1 class="title">Welcome to ShopSphere</h1>
      <p class="subtitle">Your one-stop shop for all your needs. Whether you're a shopper or store staff, you're in the right place.</p>
      <div class="actions">
        <router-link to="/register" class="btn register">Register</router-link>
        <router-link to="/login" class="btn login">Login</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
};
</script>

<style scoped>
.home-hero {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #4f46e5, #3b82f6);
  color: #fff;
  padding: 2rem;
}

.welcome-card {
  background-color: white;
  color: #1f2937;
  padding: 3rem 2rem;
  border-radius: 1rem;
  max-width: 500px;
  text-align: center;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
  animation: fadeIn 1s ease;
}

.title {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.subtitle {
  font-size: 1.2rem;
  margin-bottom: 2rem;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  text-decoration: none;
  font-weight: 600;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.register {
  background-color: #10b981;
  color: white;
}

.register:hover {
  background-color: #059669;
  transform: scale(1.05);
}

.login {
  background-color: #3b82f6;
  color: white;
}

.login:hover {
  background-color: #2563eb;
  transform: scale(1.05);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
