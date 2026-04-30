<template>
  <div class="admin-layout">
    <nav class="admin-nav">
      <router-link to="/admin" class="admin-brand">营造司</router-link>
      <div class="admin-nav-links">
        <router-link to="/admin">桥梁管理</router-link>
        <router-link to="/">返回主页</router-link>
      </div>
      <button v-if="isLoggedIn" class="logout-btn" @click="logout">退出登录</button>
    </nav>
    <main class="admin-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isLoggedIn = computed(() => !!localStorage.getItem('evora_admin_token'))

function logout() {
  localStorage.removeItem('evora_admin_token')
  router.push('/admin/login')
}
</script>

<style scoped>
.admin-layout {
  min-height: 100vh;
  background: #f5f0ea;
}
.admin-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  height: 56px;
  background: #3e2723;
  color: #fff;
}
.admin-brand {
  color: #ffd54f;
  font-weight: 700;
  text-decoration: none;
}
.admin-nav-links {
  display: flex;
  gap: 1.5rem;
}
.admin-nav-links a {
  color: #fff;
  text-decoration: none;
  font-size: 0.9rem;
}
.admin-nav-links a.router-link-active {
  color: #ffd54f;
}
.logout-btn {
  background: transparent;
  border: 1px solid #ffd54f;
  color: #ffd54f;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  cursor: pointer;
}
.admin-content {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}
</style>
