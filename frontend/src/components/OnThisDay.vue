<template>
  <div class="on-this-day">
    <div class="otd-inner">
      <h3>历史上的今天</h3>
      <div v-if="loading" class="otd-loading">加载中...</div>
      <div v-else-if="event" class="otd-event">
        <p class="otd-description">{{ event.description }}</p>
        <p class="otd-fact" v-if="fact">{{ fact }}</p>
      </div>
      <div v-else class="otd-empty">暂无历史记录</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getOnThisDay, getRandomFact } from '../api/home.js'

const event = ref(null)
const fact = ref('')
const loading = ref(true)

onMounted(async () => {
  const now = new Date()
  try {
    const data = await getOnThisDay(now.getMonth() + 1, now.getDate())
    event.value = data
    const factData = await getRandomFact()
    fact.value = factData.text || ''
  } catch {
    event.value = null
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.on-this-day {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 50;
}
.otd-inner {
  background: rgba(255,255,255,0.95);
  backdrop-filter: blur(12px);
  border-radius: 12px;
  padding: 16px 20px;
  box-shadow: 0 8px 32px rgba(15,23,42,0.1);
  max-width: 280px;
}
h3 {
  margin: 0 0 8px;
  font-size: 14px;
  color: #9C5A2C;
}
.otd-description {
  font-size: 13px;
  color: #333;
  margin: 0;
}
.otd-fact {
  font-size: 12px;
  color: #666;
  margin: 6px 0 0;
  font-style: italic;
}
.otd-loading, .otd-empty {
  font-size: 13px;
  color: #999;
}
</style>
