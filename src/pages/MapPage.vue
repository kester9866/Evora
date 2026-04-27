<script setup>
import MapView from "../components/MapView.vue";
</script>

<template>
  <div class="map-page">
    <header class="nav">
      <div class="brand">Evora</div>
      <nav class="links">
        <a href="/">首页</a>
        <a href="/map.html">桥梁地图</a>
        <a href="/arch-bridge.html">结构分析</a>
      </nav>
    </header>

    <main class="content">
      <MapView />
    </main>
  </div>
</template>

<style scoped>
.map-page {
  min-height: 100vh;
  background: #f7faff;
}

.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  background: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  position: sticky;
  top: 0;
  z-index: 10;
}

.brand {
  font-size: 16px;
  font-weight: 600;
  color: #1f2d3d;
}

.links {
  display: flex;
  gap: 16px;
}

.links a {
  text-decoration: none;
  color: #4b5563;
  font-size: 14px;
}

.links a:hover {
  color: #2563eb;
}

.content {
  padding-top: 8px;
}
</style>
