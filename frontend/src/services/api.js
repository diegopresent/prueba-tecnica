import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

const api = axios.create({
    baseURL: API_URL,
});

export const getProducts = () => 
    api.get('/products/');
export const getProduct = (id) => 
    api.get(`/products/${id}`);
export const createProduct = (productData) => 
    api.post('/products/', productData, { headers: { 'Content-Type': 'multipart/form-data' } });
export const updateProduct = (id, productData) => 
    api.patch(`/products/${id}`, productData, { headers: { 'Content-Type': 'multipart/form-data' } });
export const deleteProduct = (id) => api.delete(`/products/${id}`);

export const getCategories = () => api.get('/categories/');
export const getCategory = (id) => api.get(`/categories/${id}`);
export const createCategory = (categoryData) => api.post('/categories/', categoryData, { headers: { 'Content-Type': 'application/json' } });
export const updateCategory = (id, categoryData) => api.patch(`/categories/${id}`, categoryData, { headers: { 'Content-Type': 'application/json' } });
export const deleteCategory = (id) => api.delete(`/categories/${id}`);

export const getImages = () => api.get('/images/');
export const getImage = (id) => api.get(`/images/${id}`);
export const createImage = (imageData) => api.post('/images/', imageData, { headers: { 'Content-Type': 'multipart/form-data' } });
export const deleteImage = (id) => api.delete(`/images/${id}`);