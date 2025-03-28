import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import ProductsView from '@/components/products/ProductsView.vue';
import CategoriesView from '@/components/categories/CategoriesView.vue';
import ImagesView from '@/components/images/ImagesView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/products', name: 'products', component: ProductsView },
    { path: '/categories', name: 'categories', component: CategoriesView },
    { path: '/images', name: 'images', component: ImagesView },
  ],
});

export default router;