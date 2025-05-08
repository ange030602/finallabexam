// src/axios.js
import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8000',  // Change if your backend is hosted elsewhere
});

// Automatically attach token to every request
instance.interceptors.request.use(config => {
  const token = localStorage.getItem('token');  // Assuming you store it in localStorage
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export default instance;
