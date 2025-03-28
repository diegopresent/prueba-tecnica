<script setup>
import { ref, onMounted } from 'vue';
import { getImages, deleteImage as deleteImageApi } from '../../services/api';
import ImageForm from './ImageForm.vue';

const images = ref([]);
const showImageForm = ref(false);

const fetchImages = async () => {
    const { data } = await getImages();
    images.value = data;
};

const showForm = () => {
    showImageForm.value = true;
};

const deleteImage = async (id) => {
    await deleteImageApi(id);
    fetchImages();
};

onMounted(fetchImages);
</script>

<template>
    <div class="image-list">
        <h2>Images</h2>
        <button class="add-image-btn" @click="showForm()">Add Image</button>
        <ImageForm v-if="showImageForm" @image-created="fetchImages" @close-form="showImageForm = false" />
        <div class="image-grid">
            <div v-for="image in images" :key="image.id" class="image-card">
                <img :src="'http://127.0.0.1:8000/' + image.image_url" alt="test" class="image-preview" />
                <div class="image-actions">
                    <button class="delete-btn" @click="deleteImage(image.id)">Delete</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.image-list {
    padding: 20px;
}

.image-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
}

.image-card {
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

.image-card:hover {
    transform: translateY(-8px);
}

.image-preview {
    max-width: 100%;
    max-height: 150px;
    object-fit: contain;
    margin-bottom: 15px;
}

.image-actions {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-top: 15px;
}

.add-image-btn,
.delete-btn {
    padding: 12px 20px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    font-size: 1rem;
}

.add-image-btn {
    background-color: #4CAF50;
    color: white;
}

.delete-btn {
    background-color: #f44336;
    color: white;
}

.add-image-btn:hover,
.delete-btn:hover {
    background-color: #333;
    color: white;
}
</style>