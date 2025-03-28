<script setup>
import { ref, onMounted } from 'vue';
import { createImage, getProducts } from '../../services/api';

const emit = defineEmits(['image-created', 'close-form']);

const image = ref({
    file: null,
    product_id: 0,
});

const products = ref([]);

const handleImageUpload = (event) => {
    image.value.file = event.target.files[0];
};

const submitForm = async () => {
    const formData = new FormData();
    formData.append('image', image.value.file);
    formData.append('product_id', image.value.product_id);

    console.log('FormData:', formData); // Depurar FormData

    try {
        await createImage(formData);
        emit('image-created');
        emit('close-form');
    } catch (error) {
        console.error('Error creating image:', error); // Manejar errores
    }
};

onMounted(async () => {
    const { data } = await getProducts();
    products.value = data;
});
</script>

<template>
    <form @submit.prevent="submitForm" class="product-form">
        <div class="form-group">
            <label for="image">Image File <span class="required">*</span></label>
            <input type="file" id="image" @change="handleImageUpload" required />
        </div>
        <div class="form-group">
            <label for="product_id">Product <span class="required">*</span></label>
            <select v-model="image.product_id" id="product_id" required>
                <option value="0" disabled>Select a product</option>
                <option v-for="product in products" :key="product.id" :value="product.id">
                    {{ product.name }}
                </option>
            </select>
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
.form-group select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
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