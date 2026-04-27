<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";

const activeSections = ref([false, false, false]);
const sectionEls = ref([]);
const currentIndex = ref(0);
const repeatable = true;
const parallaxOffsets = ref([0, 0, 0]);

let observer;
let rafId;

const setSectionRef = (el, index) => {
  if (el) sectionEls.value[index] = el;
};

const setActive = (index, value) => {
  const next = [...activeSections.value];
  next[index] = value;
  activeSections.value = next;
};

const updateParallax = () => {
  rafId = null;
  const next = [...parallaxOffsets.value];
  sectionEls.value.forEach((el, index) => {
    if (!el) return;
    const rect = el.getBoundingClientRect();
    const center = rect.top + rect.height / 2;
    const delta = center - window.innerHeight / 2;
    const offset = Math.max(Math.min(-delta / 18, 22), -22);
    next[index] = offset;
  });
  parallaxOffsets.value = next;
};

const onScroll = () => {
  if (rafId) return;
  rafId = requestAnimationFrame(updateParallax);
};

onMounted(() => {
  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const index = Number(entry.target.dataset.index || 0);
        if (entry.isIntersecting) {
          currentIndex.value = index;
          if (!activeSections.value[index]) setActive(index, true);
          if (!repeatable) observer.unobserve(entry.target);
        } else if (repeatable) {
          setActive(index, false);
        }
      });
    },
    { threshold: 0.5 }
  );

  sectionEls.value.forEach((el) => {
    if (el) observer.observe(el);
  });

  updateParallax();
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
});

onBeforeUnmount(() => {
  if (observer) observer.disconnect();
  window.removeEventListener("scroll", onScroll);
  window.removeEventListener("resize", onScroll);
  if (rafId) cancelAnimationFrame(rafId);
});
</script>

<template>
  <div class="page">
    <header class="nav">
      <div class="brand">Evora</div>
      <nav class="links">
        <a href="/">首页</a>
        <a href="/map.html">桥梁地图</a>
        <a href="/arch-bridge.html">结构分析</a>
      </nav>
    </header>

    <div class="progress">
      <span v-for="i in 3" :key="i" :class="{ active: currentIndex === i - 1 }"></span>
    </div>

    <section
      class="story-section wood"
      data-index="0"
      :class="{ active: activeSections[0] }"
      :ref="(el) => setSectionRef(el, 0)"
    >
      <div class="section-inner">
        <div class="text">
          <div class="eyebrow fade">木桥 · 原始跨越</div>
          <h1 class="fade delay-1">最早的桥，是一根木梁</h1>
          <p class="fade delay-2">
            以天然材料搭建简易通道，满足最基本的跨越需求，是桥梁结构演化的起点。
          </p>
          <div class="fact fade delay-2">关键事实 · 单跨跨度约 3–5 米</div>
          <div class="question fade delay-3">但当河道更宽、更急时，结构还能承受吗？</div>
        </div>
        <div class="visual" :style="{ transform: `translateY(${parallaxOffsets[0]}px)` }">
          <div class="visual-card">
            <svg viewBox="0 0 520 180" role="img" aria-label="木桥横梁结构">
              <line class="beam" x1="40" y1="90" x2="480" y2="90" />
              <circle class="support" cx="40" cy="102" r="10" />
              <circle class="support" cx="480" cy="102" r="10" />
              <path class="river" d="M20 140 Q140 120 260 140 T500 140" />
              <ellipse class="shadow" cx="260" cy="105" rx="150" ry="10" />
            </svg>
          </div>
        </div>
      </div>
    </section>

    <section
      class="story-section stone"
      data-index="1"
      :class="{ active: activeSections[1] }"
      :ref="(el) => setSectionRef(el, 1)"
    >
      <div class="section-inner">
        <div class="text">
          <div class="eyebrow fade">石桥 · 材料升级</div>
          <h1 class="fade delay-1">石材拼接，桥面更稳定</h1>
          <p class="fade delay-2">
            石块逐层拼接，增强承载与耐久性，桥梁从“能过”走向“更稳”。
          </p>
          <div class="fact fade delay-2">关键事实 · 耐久寿命提升至百年级</div>
          <div class="question fade delay-3">但石材重量增加后，如何避免结构下挠？</div>
        </div>
        <div class="visual" :style="{ transform: `translateY(${parallaxOffsets[1]}px)` }">
          <div class="visual-card">
            <svg viewBox="0 0 520 220" role="img" aria-label="石桥拼接结构">
              <rect class="stone-block" x="60" y="130" width="80" height="42" :style="{ '--delay': '0.1s' }" />
              <rect class="stone-block" x="150" y="120" width="90" height="52" :style="{ '--delay': '0.25s' }" />
              <rect class="stone-block" x="250" y="130" width="85" height="42" :style="{ '--delay': '0.4s' }" />
              <rect class="stone-block" x="340" y="115" width="95" height="57" :style="{ '--delay': '0.55s' }" />
              <rect class="stone-block" x="90" y="80" width="90" height="42" :style="{ '--delay': '0.7s' }" />
              <rect class="stone-block" x="210" y="70" width="100" height="52" :style="{ '--delay': '0.85s' }" />
              <rect class="stone-block" x="330" y="80" width="90" height="42" :style="{ '--delay': '1s' }" />
              <path class="river" d="M30 185 Q160 165 290 185 T500 185" />
              <ellipse class="shadow" cx="260" cy="150" rx="170" ry="12" />
            </svg>
          </div>
        </div>
      </div>
    </section>

    <section
      class="story-section arch"
      data-index="2"
      :class="{ active: activeSections[2] }"
      :ref="(el) => setSectionRef(el, 2)"
    >
      <div class="section-inner">
        <div class="text">
          <div class="eyebrow fade">拱桥 · 结构飞跃</div>
          <h1 class="fade delay-1">拱形传力，跨越更长更稳</h1>
          <p class="fade delay-2">
            拱圈将荷载分散到两端，形成清晰受力路径，实现更大跨度与持久稳定。
          </p>
          <div class="fact fade delay-2">关键事实 · 单跨可达 30–60 米</div>
          <div class="question fade delay-3">当工程需求不断提升，结构逻辑成为决定性力量。</div>
          <div class="summary-card fade delay-3">
            <div class="summary-title">结构优势总结</div>
            <ul class="summary-list">
              <li>压力传递清晰，材料利用率更高</li>
              <li>跨越能力提升，桥面更稳定</li>
              <li>耐久性强，适配复杂地形</li>
            </ul>
          </div>
          <div class="conclusion fade delay-3">核心结论：拱桥是结构逻辑成熟的里程碑。</div>
        </div>
        <div class="visual" :style="{ transform: `translateY(${parallaxOffsets[2]}px)` }">
          <div class="visual-card">
            <svg viewBox="0 0 520 240" role="img" aria-label="拱桥结构示意">
              <path class="arch-path" d="M60 170 Q260 40 460 170" />
              <line class="deck" x1="60" y1="170" x2="460" y2="170" />
              <line class="pier" x1="90" y1="170" x2="90" y2="215" />
              <line class="pier" x1="430" y1="170" x2="430" y2="215" />
              <line class="force-line f1" x1="180" y1="145" x2="140" y2="205" />
              <line class="force-line f2" x1="340" y1="145" x2="380" y2="205" />
              <circle class="force-dot" cx="180" cy="145" r="6" />
              <circle class="force-dot" cx="340" cy="145" r="6" />
              <text class="force-label" x="110" y="210">力向桥台传递</text>
              <text class="force-label" x="310" y="210">力向桥台传递</text>
              <path class="river" d="M30 215 Q160 195 290 215 T500 215" />
              <ellipse class="shadow" cx="260" cy="180" rx="180" ry="12" />
            </svg>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  color: #1f2d3d;
  font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
}

.nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 28px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(148, 163, 184, 0.2);
}

.brand {
  font-weight: 600;
  font-size: 16px;
}

.links {
  display: flex;
  gap: 18px;
}

.links a {
  text-decoration: none;
  color: #4b5563;
  font-size: 14px;
}

.links a:hover {
  color: #2563eb;
}

.progress {
  position: fixed;
  right: 28px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 8;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.progress span {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(148, 163, 184, 0.5);
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.6);
}

.progress span.active {
  background: #2563eb;
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.15);
}

.story-section {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 90px 40px 40px;
}

.section-inner {
  max-width: 1120px;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 36px;
}

.text {
  flex: 1;
  min-width: 280px;
}

.visual {
  flex: 1.1;
  display: flex;
  justify-content: center;
  transition: transform 0.6s ease;
}

.visual-card {
  width: 100%;
  max-width: 540px;
  padding: 18px 20px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.6);
  box-shadow: 0 16px 40px rgba(15, 23, 42, 0.12);
  backdrop-filter: blur(8px);
}

.eyebrow {
  font-size: 12px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: rgba(31, 41, 55, 0.6);
  margin-bottom: 12px;
}

h1 {
  margin: 0 0 12px;
  font-size: 36px;
  line-height: 1.2;
}

p {
  margin: 0;
  font-size: 16px;
  color: #475569;
}

.fact {
  margin-top: 16px;
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.question {
  margin-top: 10px;
  font-size: 14px;
  color: rgba(15, 23, 42, 0.7);
}

.conclusion {
  margin-top: 14px;
  font-size: 14px;
  font-weight: 600;
  color: #1e3a8a;
}

.summary-card {
  margin-top: 16px;
  padding: 10px 0 10px 16px;
  border-radius: 0;
  background: transparent;
  box-shadow: none;
  border-left: 2px solid rgba(37, 99, 235, 0.35);
}

.summary-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
}

.summary-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 6px;
  color: #475569;
  font-size: 13px;
}

.fade {
  opacity: 0;
  transform: translateY(14px);
  transition: opacity 0.8s ease, transform 0.8s ease;
}

.story-section.active .fade {
  opacity: 1;
  transform: translateY(0);
}

.delay-1 {
  transition-delay: 0.1s;
}

.delay-2 {
  transition-delay: 0.2s;
}

.delay-3 {
  transition-delay: 0.35s;
}

.wood {
  background: linear-gradient(135deg, #f8e8d0, #f5caa3);
}

.stone {
  background: linear-gradient(135deg, #f0ede6, #d8d8d8);
}

.arch {
  background: linear-gradient(135deg, #e0f2fe, #c7d2fe);
}

svg {
  width: 100%;
  max-width: 520px;
}

.beam {
  stroke: #8b5a2b;
  stroke-width: 10;
  stroke-linecap: round;
  stroke-dasharray: 460;
  stroke-dashoffset: 460;
}

.support {
  fill: #7c4a1f;
  opacity: 0;
  transform: translateY(6px);
}

.river {
  fill: none;
  stroke: rgba(59, 130, 246, 0.45);
  stroke-width: 6;
  stroke-linecap: round;
}

.shadow {
  fill: rgba(15, 23, 42, 0.12);
}

.wood.active .beam {
  animation: draw-line 1.4s ease forwards;
}

.wood.active .support {
  opacity: 1;
  transform: translateY(0);
  transition: 0.6s ease 0.9s;
}

.stone-block {
  fill: #8f8f8f;
  opacity: 0;
  transform: translateY(16px);
  transition: opacity 0.6s ease, transform 0.6s ease;
  transition-delay: var(--delay);
}

.stone.active .stone-block {
  opacity: 1;
  transform: translateY(0);
}

.arch-path {
  fill: none;
  stroke: #2563eb;
  stroke-width: 8;
  stroke-linecap: round;
  stroke-dasharray: 520;
  stroke-dashoffset: 520;
}

.deck {
  stroke: #1e3a8a;
  stroke-width: 6;
  opacity: 0.6;
}

.pier {
  stroke: #1e3a8a;
  stroke-width: 6;
  opacity: 0.6;
}

.force-line {
  stroke: #f97316;
  stroke-width: 4;
  stroke-linecap: round;
  opacity: 0;
  transform: translateY(-6px);
  transition: 0.6s ease;
}

.force-dot {
  fill: #f97316;
  opacity: 0;
  transform: scale(0.6);
  transform-origin: center;
  transition: 0.6s ease;
}

.force-label {
  fill: #f97316;
  font-size: 12px;
  opacity: 0;
  transition: 0.6s ease 0.6s;
}

.arch.active .arch-path {
  animation: draw-line 1.6s ease forwards;
}

.arch.active .force-line {
  opacity: 1;
  transform: translateY(0);
}

.arch.active .force-dot,
.arch.active .force-label {
  opacity: 1;
  transform: scale(1);
}

.arch.active .f1 {
  transition-delay: 0.6s;
}

.arch.active .f2 {
  transition-delay: 0.8s;
}

@keyframes draw-line {
  to {
    stroke-dashoffset: 0;
  }
}

@media (max-width: 900px) {
  .section-inner {
    flex-direction: column;
    text-align: center;
  }

  .visual {
    width: 100%;
  }

  .progress {
    right: 16px;
  }
}
</style>
