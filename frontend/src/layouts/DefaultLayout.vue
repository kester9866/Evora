<template>
  <div class="default-layout">
    <nav class="main-nav">
      <router-link to="/" class="brand">檐下千秋</router-link>
      <div class="nav-links" ref="navContainer">
        <div
          class="nav-indicator"
          :style="indicatorStyle"
          :class="{ 'no-transition': lockIndicator }"
        ></div>
        <router-link
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          :ref="el => setLinkRef(el, item.to)"
        >{{ item.label }}</router-link>
      </div>
    </nav>
    <main class="page-content">
      <router-view />
    </main>
    <AiAssistant />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onBeforeUnmount, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'
import AiAssistant from '../components/AiAssistant.vue'

const route = useRoute()

const navItems = [
  { to: '/', label: '首页' },
  { to: '/map', label: '桥梁地图' },
  { to: '/graph', label: '知识图谱' },
  { to: '/game', label: '榫卯游戏' },
  { to: '/shop', label: '文创商店' },
  { to: '/admin', label: '管理' },
]

const navContainer = ref(null)
const linkRefs = reactive({})
const indicatorStyle = reactive({ left: '0px', width: '0px' })
const lockIndicator = ref(true)
let initialPositioned = false

function setLinkRef(el, to) {
  if (el) linkRefs[to] = el.$el || el
}

function getIndicatorRect(to) {
  const container = navContainer.value
  const link = linkRefs[to]
  if (!container || !link) return null
  const containerRect = container.getBoundingClientRect()
  const linkRect = link.getBoundingClientRect()
  return {
    left: linkRect.left - containerRect.left,
    width: linkRect.width,
  }
}

function moveIndicator(to, animate = true) {
  const rect = getIndicatorRect(to)
  if (!rect) return
  if (!animate) {
    lockIndicator.value = true
  }
  indicatorStyle.left = `${rect.left}px`
  indicatorStyle.width = `${rect.width}px`
  if (!animate) {
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        lockIndicator.value = false
      })
    })
  }
}

// Animate indicator on route change
watch(() => route.path, (path) => {
  nextTick(() => {
    moveIndicator(path, initialPositioned)
    initialPositioned = true
  })
})

let resizeListener = null

onMounted(() => {
  nextTick(() => {
    moveIndicator(route.path, false)
    initialPositioned = true
  })
  let resizeTicking = false
  resizeListener = () => {
    if (!resizeTicking) {
      resizeTicking = true
      requestAnimationFrame(() => {
        moveIndicator(route.path, false)
        resizeTicking = false
      })
    }
  }
  window.addEventListener('resize', resizeListener)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeListener)
})
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
  padding: 0 2.5rem;
  height: 64px;
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(16px) saturate(120%);
  border-bottom: 1px solid rgba(107,79,58,0.08);
  box-shadow: 0 1px 8px rgba(0,0,0,0.03);
  position: sticky;
  top: 0;
  z-index: 100;
}
.brand {
  font-size: 1.25rem;
  font-weight: 700;
  color: #9C5A2C;
  text-decoration: none;
}
.nav-links {
  display: flex;
  gap: 4px;
  position: relative;
}
.nav-links a {
  color: #5d4037;
  text-decoration: none;
  font-size: 0.95rem;
  padding: 8px 14px;
  border-radius: 10px;
  position: relative;
  z-index: 1;
  transition: color 0.3s ease;
}
.nav-links a:hover {
  color: #9C5A2C;
}
.nav-links a.router-link-active {
  color: #9C5A2C;
  font-weight: 500;
}

/* Animated indicator pill */
.nav-indicator {
  position: absolute;
  top: 2px;
  height: calc(100% - 4px);
  background: rgba(156,92,44,0.1);
  border-radius: 10px;
  z-index: 0;
  transition: left 0.42s cubic-bezier(0.25, 0.1, 0.25, 1),
              width 0.42s cubic-bezier(0.25, 0.1, 0.25, 1);
}
.nav-indicator.no-transition {
  transition: none;
}
.page-content {
  flex: 1;
}
</style>
