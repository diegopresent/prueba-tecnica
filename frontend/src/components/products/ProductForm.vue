<script setup>
import { ref, onMounted } from 'vue';
import { createProduct, updateProduct, getProduct, getCategories } from '../../services/api';

const props = defineProps({
    productId: Number,
});

const emit = defineEmits(['product-created', 'product-updated', 'close-form']);

const product = ref({
    name: '',
    description: '',
    price: 0,
    category_id: 0,
    image: null,
    imageUrl: '',
});

const categories = ref([]);

const handleImageUpload = (event) => {
    product.value.image = event.target.files[0];
};

const submitForm = async () => {
    const formData = new FormData();
    formData.append('name', product.value.name);
    formData.append('description', product.value.description);
    formData.append('price', product.value.price);
    formData.append('category_id', product.value.category_id);

    if (product.value.image) {
        formData.append('image', product.value.image);
    } else if (props.productId && product.value.imageUrl) {
        // Para actualización, si no se carga una nueva imagen, usa la imageUrl existente
        formData.append('imageUrl', product.value.imageUrl);
    }

    // Verifica el FormData antes de enviar
    console.log('FormData:', formData.get('image'));

    try {
        if (props.productId) {
            await updateProduct(props.productId, formData);
            emit('product-updated');
        } else {
            await createProduct(formData);
            emit('product-created');
        }
        emit('close-form');
    } catch (error) {
        console.error('Error submitting form:', error);
        // Manejo de errores más detallado
        if (error.response) {
            console.error('Response data:', error.response.data);
            console.error('Response status:', error.response.status);
            console.error('Response headers:', error.response.headers);
        } else if (error.request) {
            console.error('Request:', error.request);
        } else {
            console.error('Error message:', error.message);
        }
    }

    if (props.productId && product.value.image) {
        const { data } = await getProduct(props.productId);
        product.value.imageUrl = data.images && data.images.length > 0 ? 'http://127.0.0.1:8000/' + data.images[0].image_url : '';
    }
};

onMounted(async () => {
    if (props.productId) {
        const { data } = await getProduct(props.productId);
        product.value = {
            ...data,
            imageUrl: data.images && data.images.length > 0 ? 'http://127.0.0.1:8000/' + data.images[0].image_url : '',
            image: null,
        };
    }
    const { data } = await getCategories();
    categories.value = data;
});
</script>

<template>
    <form @submit.prevent="submitForm" class="product-form">
        <div class="form-group">
            <label for="name">Name <span class="required">*</span></label>
            <input v-model="product.name" id="name" placeholder="Enter product name" required />
        </div>

        <div class="form-group">
            <label for="description">Description <span class="required">*</span></label>
            <textarea v-model="product.description" id="description" placeholder="Enter product description" required></textarea>
        </div>

        <div class="form-group">
            <label for="price">Price <span class="required">*</span></label>
            <input v-model="product.price" id="price" type="number" placeholder="Enter product price" required />
        </div>

        <div class="form-group">
            <label for="category_id">Category <span class="required">*</span></label>
            <select v-model="product.category_id" id="category_id" required>
                <option value="" disabled>Select a category</option>
                <option v-for="category in categories" :key="category.id" :value="category.id">
                    {{ category.name }}
                </option>
            </select>
        </div>

        <div class="form-group">
            <label for="image">Image</label>
            <img v-if="product.imageUrl" :src="product.imageUrl" alt="Product" style="max-width: 150px; margin-bottom: 10px;" />
            <input type="file" id="image" @change="handleImageUpload" />
        </div>

        <button type="submit" class="submit-btn">Submit</button>
    </form>
</template>

<style scoped>
.product-form {
    display: flex;
    flex-direction: column;
    max-width: 400px;
    margin: 20px auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
    margin-bottom: 15px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}

.form-group input,
.form-group textarea,
.form-group select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
}

.form-group textarea {
    resize: vertical;
}

.submit-btn {
    padding: 12px 20px;
    border: none;
    border-radius: 6px;
    background-color: #4CAF50;
    color: white;
    cursor: pointer;
    font-size: 1rem;
    transition: background-color 0.3s ease;
}

.submit-btn:hover {
    background-color: #45a049;
}

.required {
    color: red;
}
</style>