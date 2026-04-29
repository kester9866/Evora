<template>
  <div class="shop-page">
    <h1>文创商店</h1>

    <div v-if="loading" class="skeleton-grid">
      <div v-for="i in 6" :key="i" class="skeleton-card">
        <div class="skeleton-img"></div>
        <div class="skeleton-line"></div>
        <div class="skeleton-line short"></div>
      </div>
    </div>

    <div v-else-if="products.length === 0" class="empty-state">暂无商品</div>

    <div v-else class="product-grid">
      <div v-for="product in products" :key="product.id" class="product-card" @click="selected = product">
        <img :src="product.image_url" :alt="product.name_zh" class="product-img" />
        <div class="product-info">
          <h3>{{ product.name_zh }}</h3>
          <p class="price">¥{{ product.price }}</p>
        </div>
      </div>
    </div>

    <div v-if="selected" class="modal" @click.self="selected = null">
      <div class="modal-content">
        <img :src="selected.image_url" :alt="selected.name_zh" class="modal-img" />
        <h2>{{ selected.name_zh }}</h2>
        <p class="modal-price">¥{{ selected.price }}</p>
        <p class="modal-desc" v-if="selected.description">{{ selected.description }}</p>
        <div class="modal-actions">
          <button class="buy-btn" @click="window.open(selected.buy_link, '_blank')">立即购买</button>
          <button class="close-btn" @click="selected = null">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getProducts } from '../api/shop.js'

const products = ref([])
const loading = ref(true)
const selected = ref(null)

onMounted(async () => {
  try {
    const data = await getProducts()
    products.value = Array.isArray(data) ? data : (data.items || [])
  } catch {
    products.value = []
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.shop-page {
  padding: 32px 48px;
  min-height: calc(100vh - 64px);
  font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
}
h1 { margin: 0 0 24px; font-size: 24px; color: #333; }
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 24px;
}
.product-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0,0,0,0.06);
  cursor: pointer;
  transition: transform 0.2s;
}
.product-card {
  transition: all 0.3s ease;
  border: 1px solid rgba(0,0,0,0.04);
}
.product-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 40px rgba(0,0,0,0.1);
}
.product-img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  background: #f0ebe3;
}
.product-info { padding: 16px; }
.product-info h3 { margin: 0 0 4px; font-size: 16px; }
.price { color: #9C5A2C; font-weight: 600; font-size: 18px; margin: 0; }
.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 24px;
}
.skeleton-card {
  background: #fff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0,0,0,0.06);
}
.skeleton-img { height: 200px; background: #eee; animation: shimmer 1.5s infinite; }
.skeleton-line { height: 16px; background: #eee; margin: 12px 16px 8px; border-radius: 4px; animation: shimmer 1.5s infinite; }
.skeleton-line.short { width: 60%; }
@keyframes shimmer {
  0% { opacity: 0.6; } 50% { opacity: 1; } 100% { opacity: 0.6; }
}
.empty-state {
  text-align: center;
  padding: 80px;
  color: #999;
  font-size: 18px;
}
.modal {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center;
  z-index: 200;
}
.modal-content {
  background: #fff; border-radius: 16px; padding: 32px; max-width: 480px; width: 90%;
}
.modal-img { width: 100%; max-height: 300px; object-fit: cover; border-radius: 8px; margin-bottom: 16px; }
.modal-content h2 { margin: 0 0 8px; font-size: 20px; }
.modal-price { font-size: 22px; color: #9C5A2C; font-weight: 700; margin: 0 0 12px; }
.modal-desc { font-size: 14px; color: #555; line-height: 1.6; }
.modal-actions { display: flex; gap: 12px; margin-top: 20px; }
.buy-btn {
  padding: 10px 28px; background: #6B4F3A; color: #fff; border: none;
  border-radius: 8px; cursor: pointer; font-size: 15px;
}
.close-btn {
  padding: 10px 24px; background: #eee; color: #333; border: none;
  border-radius: 8px; cursor: pointer; font-size: 15px;
}
</style>
