<script setup>
import { ref, onMounted } from 'vue';
import { createCategory, updateCategory, getCategory } from '../../services/api';

const props = defineProps({
    categoryId: Number,
});

const emit = defineEmits(['category-created', 'category-updated', 'close-form']);

const category = ref({
    name: '',
});

const submitForm = async () => {
    try {
        const payload = JSON.stringify(category.value);

        console.log('Payload:', payload);

        if (props.categoryId) {
            await updateCategory(props.categoryId, payload);
            emit('category-updated');
        } else {
            await createCategory(payload);
            emit('category-created');
        }
        emit('close-form');
    } catch (error) {
        console.error('Error submitting form:', error);
    }
};

onMounted(async () => {
    if (props.categoryId) {
        const { data } = await getCategory(props.categoryId);
        category.value = data;
    }
});
</script>

<template>
    <form @submit.prevent="submitForm" class="product-form">
        <div class="form-group">
            <label for="name">Name <span class="required">*</span></label>
            <input v-model="category.name" id="name" placeholder="Enter category name" required />
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

.form-group input {
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