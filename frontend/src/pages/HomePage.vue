<template>
  <div class="home-page">
    <!-- Background image layer — scattered, off-center, crossfading -->
    <div class="bg-layer" aria-hidden="true">
      <div
        v-for="(img, i) in bgImages"
        :key="i"
        :ref="el => setBgRef(el, i)"
        class="bg-image"
        :class="`bg-pos-${i}`"
        v-html="img.svg"
      ></div>
    </div>

    <!-- Hero -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">檐下千秋</h1>
        <p class="hero-sub">探索中国古桥的营造智慧</p>
        <div class="search-bar">
          <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>
          </svg>
          <input
            v-model="searchText"
            placeholder="搜索古桥 · 技艺 · 文化 · 朝代 ..."
            @keyup.enter="onSearch"
          />
        </div>
      </div>
      <div class="scroll-hint" aria-hidden="true">
        <span>向下探索</span>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="chevron">
          <polyline points="6 9 12 15 18 9"/>
        </svg>
      </div>
    </section>

    <!-- Chapters -->
    <div class="chapters">
      <section
        v-for="(sec, i) in sections"
        :key="i"
        class="chapter"
        :ref="el => setChapterRef(el, i)"
      >
        <div class="chapter-boundary">
          <div class="boundary-line"></div>
          <div class="boundary-tab">
            <span class="tab-num">{{ String(i + 1).padStart(2, '0') }}</span>
            <span class="tab-label">{{ sec.tab }}</span>
          </div>
          <div class="boundary-line"></div>
        </div>

        <div class="chapter-body">
          <div class="chapter-text">
            <h2>{{ sec.title }}</h2>
            <p>{{ sec.desc }}</p>
          </div>
          <div class="chapter-illustration" v-html="sec.illustration"></div>
        </div>
      </section>
    </div>

    <!-- Scroll progress -->
    <div class="scroll-progress">
      <div class="progress-bar" :style="{ width: progressPct + '%' }"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'

gsap.registerPlugin(ScrollTrigger)

const router = useRouter()
const searchText = ref('')
const progressPct = ref(0)

const triggers = []

function onSearch() {
  const q = searchText.value.trim()
  if (q) router.push(`/knowledge?q=${encodeURIComponent(q)}`)
}

// === Background images ===
// Each image is a decorative SVG positioned off-center, crossfading on scroll
const bgImages = [
  {
    // 起源 — simple beam bridge, top-right
    svg: `<svg viewBox="0 0 600 400" fill="none"><path d="M100 280 L500 280" stroke="#6B4F3A" stroke-width="6" opacity="0.7"/><rect x="140" y="280" width="18" height="60" rx="4" fill="#6B4F3A" opacity="0.7"/><rect x="460" y="280" width="18" height="60" rx="4" fill="#6B4F3A" opacity="0.7"/><path d="M180 300 Q340 260 480 300" fill="none" stroke="#6B4F3A" stroke-width="3" opacity="0.5"/><circle cx="310" cy="252" r="20" fill="#9C5A2C" opacity="0.08"/><circle cx="330" cy="242" r="12" fill="#9C5A2C" opacity="0.06"/></svg>`
  },
  {
    // 石筑 — stone masonry arches, bottom-left
    svg: `<svg viewBox="0 0 500 500" fill="none"><rect x="60" y="200" width="80" height="28" rx="4" fill="#6B4F3A" opacity="0.6"/><rect x="150" y="180" width="90" height="32" rx="4" fill="#6B4F3A" opacity="0.65"/><rect x="250" y="170" width="90" height="36" rx="4" fill="#6B4F3A" opacity="0.7"/><rect x="350" y="190" width="80" height="28" rx="4" fill="#6B4F3A" opacity="0.55"/><rect x="60" y="228" width="80" height="16" rx="3" fill="#6B4F3A" opacity="0.35"/><rect x="150" y="212" width="90" height="18" rx="3" fill="#6B4F3A" opacity="0.4"/><rect x="250" y="206" width="90" height="18" rx="3" fill="#6B4F3A" opacity="0.45"/><rect x="350" y="218" width="80" height="16" rx="3" fill="#6B4F3A" opacity="0.35"/><path d="M70 320 Q250 280 430 320" fill="none" stroke="#8A9A9A" stroke-width="2" opacity="0.3"/></svg>`
  },
  {
    // 拱跨 — grand sweeping arch, center-right
    svg: `<svg viewBox="0 0 600 500" fill="none"><path d="M40 400 Q300 60 560 400" fill="none" stroke="#6B4F3A" stroke-width="10" opacity="0.55"/><path d="M40 400 Q300 80 560 400" fill="none" stroke="#6B4F3A" stroke-width="5" opacity="0.3"/><line x1="40" y1="400" x2="560" y2="400" stroke="#6B4F3A" stroke-width="6" opacity="0.45"/><line x1="120" y1="400" x2="120" y2="460" stroke="#6B4F3A" stroke-width="6" opacity="0.5"/><line x1="480" y1="400" x2="480" y2="460" stroke="#6B4F3A" stroke-width="6" opacity="0.5"/><circle cx="180" cy="362" r="6" fill="#C53D3D" opacity="0.35"/><circle cx="420" cy="362" r="6" fill="#C53D3D" opacity="0.35"/><circle cx="300" cy="234" r="30" fill="#9C5A2C" opacity="0.04"/></svg>`
  },
  {
    // 木构 — timber woven structure, top-left
    svg: `<svg viewBox="0 0 500 500" fill="none"><rect x="160" y="100" width="40" height="28" rx="3" fill="#6B4F3A" opacity="0.55"/><rect x="205" y="130" width="56" height="28" rx="3" fill="#6B4F3A" opacity="0.6"/><rect x="130" y="130" width="32" height="12" rx="2" fill="#6B4F3A" opacity="0.4"/><rect x="264" y="130" width="32" height="12" rx="2" fill="#6B4F3A" opacity="0.4"/><circle cx="180" cy="132" r="5" fill="#C53D3D" opacity="0.25"/><circle cx="235" cy="132" r="5" fill="#C53D3D" opacity="0.25"/><path d="M100 260 L400 260" fill="none" stroke="#6B4F3A" stroke-width="6" opacity="0.45"/><line x1="100" y1="260" x2="100" y2="320" stroke="#6B4F3A" stroke-width="6" opacity="0.5"/><line x1="400" y1="260" x2="400" y2="320" stroke="#6B4F3A" stroke-width="6" opacity="0.5"/><path d="M120 300 Q250 260 380 300" fill="none" stroke="#8A9A9A" stroke-width="2" opacity="0.25"/><circle cx="250" cy="200" r="40" fill="#9C5A2C" opacity="0.04"/></svg>`
  }
]

// === Section data ===
const sections = [
  {
    tab: '起源',
    title: '最早的桥，是一根木梁',
    desc: '先民砍倒一棵树，横跨溪涧，从此脚步不再被流水阻隔。从独木桥到竹索桥，桥梁的传奇就此展开。',
    illustration: `<svg viewBox="0 0 320 200" fill="none"><rect x="30" y="100" width="260" height="12" rx="4" fill="#6B4F3A" opacity="0.12"/><rect x="40" y="112" width="240" height="5" rx="2" fill="#6B4F3A" opacity="0.08"/><rect x="50" y="112" width="14" height="40" rx="3" fill="#6B4F3A" opacity="0.18"/><rect x="256" y="112" width="14" height="40" rx="3" fill="#6B4F3A" opacity="0.18"/><path d="M80 136 Q160 118 240 136" fill="none" stroke="#9C5A2C" stroke-width="1.5" opacity="0.45"/><circle cx="75" cy="108" r="12" fill="#6B4F3A" opacity="0.06"/><circle cx="245" cy="108" r="12" fill="#6B4F3A" opacity="0.06"/></svg>`
  },
  {
    tab: '石筑',
    title: '石材拼接，桥面更稳定',
    desc: '秦汉时期，石梁桥与石墩桥出现，泉州洛阳桥以筏形基础和牡蛎固基，让桥梁屹立千年不倒。',
    illustration: `<svg viewBox="0 0 320 200" fill="none"><rect x="30" y="66" width="55" height="22" rx="3" fill="#6B4F3A" opacity="0.1"/><rect x="95" y="56" width="60" height="28" rx="3" fill="#6B4F3A" opacity="0.14"/><rect x="165" y="52" width="60" height="32" rx="3" fill="#6B4F3A" opacity="0.18"/><rect x="235" y="60" width="55" height="24" rx="3" fill="#6B4F3A" opacity="0.12"/><rect x="30" y="88" width="55" height="14" rx="3" fill="#6B4F3A" opacity="0.06"/><rect x="95" y="84" width="60" height="16" rx="3" fill="#6B4F3A" opacity="0.08"/><rect x="165" y="84" width="60" height="16" rx="3" fill="#6B4F3A" opacity="0.1"/><rect x="235" y="84" width="55" height="14" rx="3" fill="#6B4F3A" opacity="0.07"/><path d="M40 142 Q160 120 280 142" fill="none" stroke="#8A9A9A" stroke-width="1.5" opacity="0.4"/></svg>`
  },
  {
    tab: '拱跨',
    title: '拱形传力，跨越更长更稳',
    desc: '敞肩拱的出现是桥梁科技的一次飞跃。赵州桥以空腹式圆弧拱设计，领先世界千年，至今仍可通行。',
    illustration: `<svg viewBox="0 0 320 220" fill="none"><path d="M20 180 Q160 20 300 180" fill="none" stroke="#6B4F3A" stroke-width="4" opacity="0.22"/><path d="M20 180 Q160 32 300 180" fill="none" stroke="#6B4F3A" stroke-width="2" opacity="0.1"/><line x1="20" y1="180" x2="300" y2="180" stroke="#6B4F3A" stroke-width="3" opacity="0.18"/><line x1="60" y1="180" x2="60" y2="210" stroke="#6B4F3A" stroke-width="3" opacity="0.2"/><line x1="260" y1="180" x2="260" y2="210" stroke="#6B4F3A" stroke-width="3" opacity="0.2"/><circle cx="100" cy="163" r="3" fill="#C53D3D" opacity="0.45"/><circle cx="220" cy="163" r="3" fill="#C53D3D" opacity="0.45"/></svg>`
  },
  {
    tab: '木构',
    title: '榫卯木构，无需一钉一铁',
    desc: '闽浙山间的木拱桥，以编木结构穿插纵横，不用一根钉子，却能在风雨中挽住山河。',
    illustration: `<svg viewBox="0 0 320 220" fill="none"><rect x="110" y="54" width="32" height="24" rx="2" fill="#6B4F3A" opacity="0.12"/><rect x="148" y="76" width="44" height="24" rx="2" fill="#6B4F3A" opacity="0.15"/><rect x="98" y="76" width="28" height="10" rx="2" fill="#6B4F3A" opacity="0.08"/><rect x="194" y="76" width="28" height="10" rx="2" fill="#6B4F3A" opacity="0.08"/><circle cx="124" cy="78" r="3" fill="#C53D3D" opacity="0.35"/><circle cx="168" cy="78" r="3" fill="#C53D3D" opacity="0.35"/><path d="M60 130 L260 130" fill="none" stroke="#6B4F3A" stroke-width="3" opacity="0.15"/><line x1="60" y1="130" x2="60" y2="165" stroke="#6B4F3A" stroke-width="3" opacity="0.2"/><line x1="260" y1="130" x2="260" y2="165" stroke="#6B4F3A" stroke-width="3" opacity="0.2"/><path d="M70 150 Q160 130 250 150" fill="none" stroke="#8A9A9A" stroke-width="1.5" opacity="0.35"/></svg>`
  }
]

const chapterRefs = ref([])
const bgRefs = ref([])
function setChapterRef(el, i) { if (el) chapterRefs.value[i] = el }
function setBgRef(el, i) { if (el) bgRefs.value[i] = el }

onMounted(() => {
  // Progress bar
  ScrollTrigger.create({
    trigger: document.body,
    start: 'top top',
    end: 'bottom bottom',
    onUpdate: (self) => { progressPct.value = Math.round(self.progress * 100) }
  })

  // Background image crossfading — each image tied to its chapter's scroll zone
  bgRefs.value.forEach((el, i) => {
    if (!el) return
    const chapter = chapterRefs.value[i]
    gsap.set(el, { opacity: 0 })

    ScrollTrigger.create({
      trigger: chapter,
      start: 'top 90%',
      end: 'bottom 30%',
      scrub: 2,
      onUpdate: (self) => {
        // Fade in as chapter enters view, fade out as it leaves
        const t = self.progress
        // Peak opacity 0.08-0.12 at center of chapter, trails off at edges
        const curve = t < 0.25 ? t / 0.25
          : t > 0.75 ? (1 - t) / 0.25
          : 1
        el.style.opacity = (0.1 * curve).toFixed(3)
      }
    })
  })

  // Chapter body: drawer-like reveal with damping
  chapterRefs.value.forEach((el, i) => {
    if (!el) return
    const body = el.querySelector('.chapter-body')
    const boundary = el.querySelector('.chapter-boundary')

    gsap.set(body, { opacity: 0, y: 70 })

    gsap.to(body, {
      opacity: 1,
      y: 0,
      duration: 0.9,
      ease: 'power3.out',
      scrollTrigger: {
        trigger: boundary,
        start: 'top 72%',
        end: 'top 32%',
        scrub: 1.5,
        id: `chapter-${i}`
      }
    })

    triggers.push(ScrollTrigger.getById(`chapter-${i}`))
  })
})

onBeforeUnmount(() => {
  triggers.forEach(t => t?.kill())
  ScrollTrigger.getAll().forEach(t => t.kill())
})
</script>

<style scoped>
.home-page {
  font-family: "PingFang SC", "Noto Serif SC", "Source Han Serif SC", "SimSun", serif;
  color: #2c2416;
  position: relative;
  overflow-x: hidden;
  background: linear-gradient(180deg, #FDF8F0 0%, #F7EFE4 25%, #F0E7DD 50%, #EBDFD2 75%, #DDC8B0 100%);
}

/* ===== Background image layer ===== */
.bg-layer {
  position: fixed;
  inset: 0;
  z-index: 0;
  pointer-events: none;
}
.bg-image {
  position: absolute;
  opacity: 0;
  will-change: opacity;
}
.bg-image :deep(svg) {
  width: 100%;
  height: 100%;
}

/* Off-center positions — each image is placed asymmetrically */
.bg-pos-0 { /* 起源 beam — top-right */
  top: 8%;
  right: -6%;
  width: 45vw;
  max-width: 550px;
}
.bg-pos-1 { /* 石筑 masonry — bottom-left */
  bottom: 5%;
  left: -4%;
  width: 42vw;
  max-width: 500px;
}
.bg-pos-2 { /* 拱跨 arch — center-right, lower */
  top: 45%;
  right: -2%;
  width: 48vw;
  max-width: 580px;
}
.bg-pos-3 { /* 木构 timber — top-left */
  top: 12%;
  left: -5%;
  width: 40vw;
  max-width: 480px;
}

/* ===== Hero ===== */
.hero {
  height: 80vh;
  min-height: 520px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 1;
}
.hero-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 18px;
}
.hero-title {
  font-size: 52px;
  font-weight: 700;
  color: #3d3020;
  margin: 0;
  letter-spacing: 0.08em;
}
.hero-sub {
  font-size: 16px;
  color: #8A7A6A;
  margin: 0 0 14px;
  letter-spacing: 0.1em;
}

/* Search */
.search-bar {
  display: flex;
  align-items: center;
  width: 480px;
  height: 56px;
  background: rgba(255,255,255,0.7);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border: 1px solid rgba(180,160,140,0.2);
  border-radius: 28px;
  padding: 0 22px;
  box-shadow: 0 2px 20px rgba(0,0,0,0.05), 0 0 0 1px rgba(255,255,255,0.3) inset;
  transition: box-shadow 0.3s ease;
}
.search-bar:focus-within {
  box-shadow: 0 4px 28px rgba(107,79,58,0.12), 0 0 0 1px rgba(255,255,255,0.3) inset;
}
.search-icon {
  width: 20px;
  height: 20px;
  color: #A09080;
  flex-shrink: 0;
  margin-right: 12px;
}
.search-bar input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 16px;
  color: #3d3020;
  font-family: inherit;
}
.search-bar input::placeholder {
  color: #B0A090;
  font-size: 15px;
}

/* Scroll hint */
.scroll-hint {
  position: absolute;
  bottom: 24px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  color: #B0A090;
  font-size: 13px;
  animation: float 2.2s ease-in-out infinite;
}
.chevron {
  width: 20px;
  height: 20px;
}
@keyframes float {
  0%, 100% { transform: translateY(0); opacity: 0.7; }
  50% { transform: translateY(7px); opacity: 1; }
}

/* ===== Chapters ===== */
.chapters {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 32px 140px;
  position: relative;
  z-index: 1;
}

.chapter {
  min-height: 85vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* Boundary / drawer handle */
.chapter-boundary {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 56px 0 28px;
  position: sticky;
  top: 64px;
  z-index: 2;
}
.boundary-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(156,92,44,0.18), transparent);
}
.boundary-tab {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 22px;
  background: rgba(255,255,255,0.7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(156,92,44,0.12);
  border-radius: 24px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.03);
}
.tab-num {
  font-size: 13px;
  font-weight: 600;
  color: #C53D3D;
  letter-spacing: 0.12em;
}
.tab-label {
  font-size: 15px;
  color: #5a4a3a;
  font-weight: 500;
}

/* Chapter body */
.chapter-body {
  display: flex;
  gap: 64px;
  align-items: center;
}
.chapter-text {
  flex: 1.1;
  min-width: 0;
}
.chapter-text h2 {
  font-size: 30px;
  font-weight: 700;
  margin: 0 0 20px;
  color: #2c2416;
  line-height: 1.35;
}
.chapter-text p {
  font-size: 17px;
  line-height: 2;
  color: #5a4a3a;
  margin: 0;
}
.chapter-illustration {
  flex: 0.9;
  display: flex;
  justify-content: center;
  align-items: center;
}
.chapter-illustration :deep(svg) {
  width: 100%;
  height: auto;
  max-width: 320px;
}

/* ===== Scroll progress ===== */
.scroll-progress {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 3px;
  background: rgba(0,0,0,0.03);
  z-index: 60;
}
.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #C53D3D, #9C5A2C, #6B4F3A);
  transition: width 0.15s linear;
}

/* ===== Responsive ===== */
@media (max-width: 768px) {
  .hero-title { font-size: 36px; }
  .hero-sub { font-size: 14px; }
  .search-bar { width: 100%; max-width: 400px; height: 48px; }
  .chapter { min-height: 70vh; }
  .chapter-body {
    flex-direction: column;
    gap: 36px;
  }
  .chapter-text h2 { font-size: 24px; }
  .chapter-text p { font-size: 15px; }
  .chapter-illustration { max-width: 260px; }
  .chapter-boundary { top: 56px; }
  .bg-pos-0, .bg-pos-1, .bg-pos-2, .bg-pos-3 {
    width: 55vw;
    opacity: 0.04 !important;
  }
}
</style>
