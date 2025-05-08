<template>
  <div class="container mt-5">
    <h2>📦 Manage Products</h2>

    <div class="d-flex gap-2 mb-3">
      <button @click="openModal()" class="btn btn-primary">
        <i class="bi bi-plus-circle"></i> Add Product
      </button>
      <button @click="$router.push('/admin/checkout')" class="btn btn-info">
        <i class="bi bi-list-check"></i> Checkout List
      </button>
    </div>

    <!-- Product Cards -->
    <div v-for="product in products" :key="product.id" class="col-12 col-md-6 col-lg-4 mb-4">
      <div class="card shadow-sm h-100">
        <div class="card-body">
          <img v-if="product.image" :src="product.image" class="img-fluid mb-2" style="max-height: 150px; object-fit: cover;" />
          <h5 class="card-title">{{ product.name }} - ${{ product.price }}</h5>
          <p class="card-text">{{ product.description }}</p>

          <div class="d-flex justify-content-between align-items-center">
            <span class="badge bg-success">In Stock: {{ product.stock }}</span>
            <div>
              <button @click="openModal(product)" class="btn btn-warning btn-sm me-2" data-bs-toggle="tooltip" data-bs-placement="top" title="Edit Product">
                <i class="bi bi-pencil"></i> Edit
              </button>
              <button @click="deleteProduct(product.id)" class="btn btn-danger btn-sm" data-bs-toggle="tooltip" data-bs-placement="top" title="Delete Product">
                <i class="bi bi-trash"></i> Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal for Adding/Editing Product -->
    <div class="modal fade" id="productModal" tabindex="-1" aria-labelledby="productModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="productModalLabel">{{ editMode ? 'Edit' : 'Add' }} Product</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveProduct">
              <div class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input v-model="productForm.name" type="text" id="name" class="form-control" placeholder="Enter product name" required />
              </div>

              <div class="mb-3">
                <label for="description" class="form-label">Description</label>
                <input v-model="productForm.description" type="text" id="description" class="form-control" placeholder="Enter product description" required />
              </div>

              <div class="mb-3">
                <label for="price" class="form-label">Price ($)</label>
                <input v-model="productForm.price" type="number" id="price" class="form-control" placeholder="Enter price (e.g., 19.99)" min="0" required />
              </div>

              <div class="mb-3">
                <label for="stock" class="form-label">Stock Quantity</label>
                <input v-model="productForm.stock" type="number" id="stock" class="form-control" placeholder="Enter stock quantity" min="0" required />
              </div>

              <div class="mb-3">
                <label for="image" class="form-label">Product Image</label>
                <input type="file" id="image" class="form-control" @change="handleImageUpload" :disabled="editMode" />
                <div v-if="productForm.image" class="mt-2">
                  <small>Current image: {{ productForm.image.name }}</small>
                </div>
              </div>

              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                <button type="submit" class="btn btn-success">
                  <i v-if="editMode" class="bi bi-pencil"></i>
                  <i v-else class="bi bi-plus-circle"></i> {{ editMode ? 'Update' : 'Add' }} Product
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../axios';
import * as bootstrap from 'bootstrap';

export default {
  data() {
    return {
      products: [],
      productForm: {
        name: '',
        description: '',
        price: '',
        stock: '',
        image: null
      },
      editMode: false,
      selectedId: null
    };
  },
  mounted() {
    this.fetchProducts();
    this.initializeTooltips();
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
    initializeTooltips() {
      const tooltipTriggerList = Array.from(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
      tooltipTriggerList.forEach(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    },
    openModal(product = null) {
      this.editMode = !!product;
      this.productForm = product
        ? { ...product, image: null }  // Prevent overwriting image
        : { name: '', description: '', price: 0, stock: 0, image: null };
      this.selectedId = product?.id || null;
      const modalEl = document.getElementById('productModal');
      const modal = new bootstrap.Modal(modalEl);
      modal.show();
    },
    handleImageUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.productForm.image = file;
      }
    },
    async saveProduct() {
      const form = new FormData();
      form.append('name', this.productForm.name);
      form.append('description', this.productForm.description);
      form.append('price', this.productForm.price);
      form.append('stock', this.productForm.stock);
      if (this.productForm.image) {
        form.append('image', this.productForm.image);
      }

      try {
        if (this.editMode) {
          await axios.put(`/api/products/${this.selectedId}/`, form, {
            headers: { 'Content-Type': 'multipart/form-data' }
          });
        } else {
          await axios.post('/api/products/', form, {
            headers: { 'Content-Type': 'multipart/form-data' }
          });
        }
        this.fetchProducts();
        const modalEl = document.getElementById('productModal');
        const modal = bootstrap.Modal.getInstance(modalEl);
        modal.hide();
      } catch (error) {
        console.error('API error:', error.response?.data || error.message);
        alert(
          'Failed to save product:\n' +
          JSON.stringify(error.response?.data, null, 2)
        );
      }
    },
    async deleteProduct(id) {
      if (confirm('Are you sure you want to delete this product?')) {
        try {
          await axios.delete(`/api/products/${id}/`);
          this.fetchProducts();
        } catch (error) {
          console.error('Failed to delete product:', error);
        }
      }
    }
  }
};
</script>

<style scoped>
.card {
  transition: transform 0.3s ease;
}

.card:hover {
  transform: scale(1.05);
}

.img-fluid {
  max-width: 100%;
  height: auto;
  object-fit: cover;
}

.modal-content {
  border-radius: 1rem;
}

.btn-close {
  background: transparent;
  border: none;
}
</style>
