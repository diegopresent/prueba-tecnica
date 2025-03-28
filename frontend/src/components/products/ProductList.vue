<script setup>
import { ref, onMounted } from 'vue';
import { getProducts, deleteProduct as deleteProductApi } from '../../services/api';
import ProductForm from './ProductForm.vue';
import { Carousel, Slide, Navigation, Pagination } from 'vue3-carousel';
import 'vue3-carousel/dist/carousel.css';

const products = ref([]);
const showProductForm = ref(false);
const editingProductId = ref(null);

const fetchProducts = async () => {
    const { data } = await getProducts();
    products.value = data;
    console.log(products.value);
};

const showForm = () => {
    showProductForm.value = true;
};

const editProduct = (id) => {
    editingProductId.value = id;
};

const deleteProduct = async (id) => {
    await deleteProductApi(id);
    fetchProducts();
};

onMounted(fetchProducts);
</script>

<template>
    <div class="product-list">
        <h2>Products</h2>
        <button class="add-product-btn" @click="showForm()">Add Product</button>

        <ProductForm v-if="showProductForm" @product-created="fetchProducts" @close-form="showProductForm = false" />

        <div class="product-grid">
            <div v-for="product in products" :key="product.id" class="product-card">
                <div class="product-image-container">
                    <Carousel :items-to-show="1" :wrap-around="true" class="product-carousel">
                        <Slide v-for="image in product.images" :key="image.id">
                            <img :src="'http://127.0.0.1:8000/' + image.image_url" alt="Product"
                                class="product-image" />
                        </Slide>
                        <template #addons>
                            <Navigation />
                            <Pagination />
                        </template>
                    </Carousel>
                </div>
                <h3>name: {{ product.name }}</h3>
                <p class="product-description">Description: {{ product.description }}</p>
                <p class="product-price">Price: ${{ product.price }}</p>

                <div class="product-actions">
                    <button class="edit-btn" @click="editProduct(product.id)">Edit</button>
                    <button class="delete-btn" @click="deleteProduct(product.id)">Delete</button>
                </div>

                <ProductForm v-if="editingProductId === product.id" :productId="product.id"
                    @product-updated="fetchProducts" @close-form="editingProductId = null" />
            </div>
        </div>
    </div>
</template>

<style scoped>
.product-list {
    padding: 20px;
}

.product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}

.product-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.product-card:hover {
    transform: translateY(-8px);
}

.product-image-container {
    display: flex;
    justify-content: center;
    margin-bottom: 15px;
    width: 100%;
}

.product-carousel {
    width: 100%;
}

.product-image {
    max-width: 100%;
    max-height: 200px;
    height: auto;
    border-radius: 4px;
    object-fit: contain;
}

.product-description,
.product-price {
    margin-bottom: 10px;
}

.product-actions {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 15px;
}

.add-product-btn,
.edit-btn,
.delete-btn {
    padding: 12px 20px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    font-size: 1rem;
}

.add-product-btn {
    background-color: #4CAF50;
    color: white;
}

.edit-btn {
    background-color: #2196F3;
    color: white;
}

.delete-btn {
    background-color: #f44336;
    color: white;
}

.add-product-btn:hover,
.edit-btn:hover,
.delete-btn:hover {
    background-color: #333;
    color: white;
}
</style>