<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/products">Products</RouterLink>
      <RouterLink to="/categories">Categories</RouterLink>
      <RouterLink to="/images">Images</RouterLink>
    </nav>
  </header>
  <RouterView />
</template>

<style scoped>
header {
  background-color: #333;
  color: #fff;
  padding: 10px;
}

nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  justify-content: center;
}

nav a {
  color: #fff;
  text-decoration: none;
  padding: 10px;
  margin: 0 10px;
}

nav a.router-link-exact-active {
  font-weight: bold;
}
</style>