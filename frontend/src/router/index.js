import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Register from '../views/Register.vue';
import Login from '../views/Login.vue';
import ConsumerPanel from '../views/ConsumerPanel.vue';
import EmployeePanel from '../views/EmployeePanel.vue';
import Cart from '../views/Cart.vue';
import OrderSummary from '../views/OrderSummary.vue';
import Checkout from '../views/Checkout.vue'; // ✅ Import the new Checkout component

const routes = [
  { path: '/', component: Home },
  { path: '/register', component: Register },
  { path: '/login', component: Login },
  { path: '/consumer', component: ConsumerPanel },
  { path: '/employee', component: EmployeePanel },
  { path: '/cart', component: Cart },
  { path: '/orders', component: OrderSummary },
  { path: '/admin/checkout', component: Checkout } // ✅ Add the new route
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
