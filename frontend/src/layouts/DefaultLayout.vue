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
        >
          <span class="nav-icon" v-html="icons[item.icon]"></span>
          <span>{{ item.label }}</span>
        </router-link>
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
  { to: '/', label: '首页', icon: 'home' },
  { to: '/map', label: '江山桥迹', icon: 'map' },
  { to: '/graph', label: '桥脉纵横', icon: 'graph' },
  { to: '/game', label: '榫卯工坊', icon: 'game' },
  { to: '/shop', label: '桥韵雅集', icon: 'shop' },
  { to: '/admin', label: '营造司', icon: 'admin' },
]

// Inline SVG icons — ancient bridge theme
const icons = {
  home: `<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 14 Q8 4 14 14"/><path d="M2 14 L16 14"/><line x1="3" y1="14" x2="3" y2="17"/><line x1="15" y1="14" x2="15" y2="17"/><circle cx="9" cy="8" r="1.2" fill="currentColor" stroke="none"/></svg>`,
  map: `<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 5 Q10 2 17 5"/><path d="M5 5 L5 16"/><path d="M15 5 L15 16"/><path d="M3 10 Q10 7 17 10"/><path d="M3 15 Q10 12 17 15"/><circle cx="10" cy="7" r="1.5" fill="currentColor" stroke="none"/></svg>`,
  graph: `<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="6" cy="5" r="2"/><circle cx="14" cy="5" r="2"/><circle cx="6" cy="15" r="2"/><circle cx="14" cy="15" r="2"/><circle cx="10" cy="10" r="2"/><line x1="8" y1="6" x2="12" y2="6"/><line x1="7" y1="7" x2="5" y2="13"/><line x1="13" y1="7" x2="15" y2="13"/><line x1="8" y1="14" x2="12" y2="14"/><line x1="8" y1="9" x2="5" y2="7"/><line x1="12" y1="9" x2="15" y2="7"/></svg>`,
  game: `<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="7" width="8" height="5" rx="1"/><rect x="7" y="5" width="8" height="5" rx="1"/><path d="M11 7 L11 12"/><path d="M7 10 L15 10"/></svg>`,
  shop: `<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M5 8 Q10 3 15 8"/><path d="M5 8 L5 17"/><path d="M15 8 L15 17"/><path d="M5 13 Q10 10 15 13"/><path d="M5 17 Q10 14 15 17"/></svg>`,
  admin: `<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="4" y="3" width="12" height="14" rx="2"/><circle cx="10" cy="9" r="2.5"/><path d="M7 14 Q10 11 13 14"/></svg>`
}

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
  display: flex;
  align-items: center;
  gap: 6px;
}
.nav-icon {
  width: 18px;
  height: 18px;
  display: inline-flex;
  align-items: center;
  opacity: 0.65;
  transition: opacity 0.3s ease;
}
.nav-links a:hover .nav-icon,
.nav-links a.router-link-active .nav-icon {
  opacity: 1;
}
.nav-icon :deep(svg) {
  width: 100%;
  height: 100%;
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
