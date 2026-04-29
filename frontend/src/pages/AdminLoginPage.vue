<template>
  <div class="login-page">
    <form class="login-form" @submit.prevent="doLogin">
      <h1>管理后台登录</h1>
      <div v-if="error" class="error">{{ error }}</div>
      <input v-model="username" placeholder="用户名" autocomplete="username" />
      <input v-model="password" type="password" placeholder="密码" autocomplete="current-password" />
      <button type="submit" :disabled="loading">
        {{ loading ? '登录中...' : '登录' }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../api/admin.js'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function doLogin() {
  error.value = ''
  loading.value = true
  try {
    const data = await login(username.value, password.value)
    localStorage.setItem('evora_admin_token', data.token || data.access_token)
    router.push('/admin')
  } catch {
    error.value = '用户名或密码错误'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: #f5f0ea;
}
.login-form {
  background: #fff;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.08);
  width: 360px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
h1 { margin: 0 0 8px; font-size: 20px; text-align: center; color: #9C5A2C; }
.error { color: #e74c3c; font-size: 13px; text-align: center; }
input {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
}
input:focus { border-color: #9C5A2C; }
button {
  padding: 12px;
  background: #6B4F3A;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 15px;
}
button:disabled { background: #ccc; cursor: not-allowed; }
</style>
