<script setup>
import { ref, onMounted } from 'vue';
import { getCategories, deleteCategory as deleteCategoryApi } from '../../services/api';
import CategoryForm from './CategoryForm.vue';

const categories = ref([]);
const showCategoryForm = ref(false);
const editingCategoryId = ref(null);

const fetchCategories = async () => {
    const { data } = await getCategories();
    categories.value = data;
};

const showForm = () => {
    showCategoryForm.value = true;
};

const editCategory = (id) => {
    editingCategoryId.value = id;
};

const deleteCategory = async (id) => {
    await deleteCategoryApi(id);
    fetchCategories();
};

onMounted(fetchCategories);
</script>

<template>
    <div class="category-list">
        <h2>Categories</h2>
        <button class="add-category-btn" @click="showForm()">Add Category</button>
        <CategoryForm v-if="showCategoryForm" @category-created="fetchCategories" @close-form="showCategoryForm = false" />
        <div class="category-grid">
            <div v-for="category in categories" :key="category.id" class="category-card">
                <h3>{{ category.name }}</h3>
                <div class="category-actions">
                    <button class="edit-btn" @click="editCategory(category.id)">Edit</button>
                    <button class="delete-btn" @click="deleteCategory(category.id)">Delete</button>
                </div>
                <CategoryForm v-if="editingCategoryId === category.id" :categoryId="category.id"
                    @category-updated="fetchCategories" @close-form="editingCategoryId = null" />
            </div>
        </div>
    </div>
</template>

<style scoped>
.category-list {
    padding: 20px;
}

.category-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}

.category-card {
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

.category-card:hover {
    transform: translateY(-8px);
}

.category-actions {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 15px;
}

.add-category-btn,
.edit-btn,
.delete-btn {
    padding: 12px 20px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    font-size: 1rem;
}

.add-category-btn {
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

.add-category-btn:hover,
.edit-btn:hover,
.delete-btn:hover {
    background-color: #333;
    color: white;
}
</style>