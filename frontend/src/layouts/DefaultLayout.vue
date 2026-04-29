<template>
  <div class="default-layout">
    <nav class="main-nav">
      <router-link to="/" class="brand">檐下千秋</router-link>
      <div class="nav-links">
        <router-link to="/">首页</router-link>
        <router-link to="/map">桥梁地图</router-link>
        <router-link to="/graph">知识图谱</router-link>
        <router-link to="/game">榫卯游戏</router-link>
        <router-link to="/shop">文创商店</router-link>
        <router-link to="/admin">管理</router-link>
      </div>
    </nav>
    <main class="page-content">
      <router-view />
    </main>
    <AiAssistant />
  </div>
</template>

<script setup>
import AiAssistant from '../components/AiAssistant.vue'
</script>

<style scoped>
.default-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.main-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
  height: 64px;
  background: rgba(255,255,255,0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid #e8e0d5;
  position: sticky;
  top: 0;
  z-index: 100;
}
.brand {
  font-size: 1.25rem;
  font-weight: 700;
  color: #8b4513;
  text-decoration: none;
}
.nav-links {
  display: flex;
  gap: 1.5rem;
}
.nav-links a {
  color: #5d4037;
  text-decoration: none;
  font-size: 0.95rem;
  transition: color 0.2s;
}
.nav-links a:hover,
.nav-links a.router-link-active {
  color: #8b4513;
}
.page-content {
  flex: 1;
}
</style>
