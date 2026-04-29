<template>
  <div class="home-page">
    <div class="progress">
      <span v-for="i in 4" :key="i" :class="{ active: currentIndex === i - 1 }"></span>
    </div>

    <section class="story-section wood" data-index="0" :ref="el => setSectionRef(el, 0)">
      <div class="section-inner">
        <div class="text">
          <div class="eyebrow fade-in">木桥 · 原始跨越</div>
          <h1 class="fade-in">最早的桥，是一根木梁</h1>
          <p class="fade-in">以天然材料搭建简易通道，满足最基本的跨越需求，是桥梁结构演化的起点。</p>
          <div class="fact fade-in">单跨跨度约 3–5 米</div>
          <div class="question fade-in">但当河道更宽、更急时，结构还能承受吗？</div>
          <button class="cta fade-in" @click="$router.push('/map?dynasty=先秦')">探索先秦木桥</button>
        </div>
        <div class="visual">
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

    <section class="story-section stone" data-index="1" :ref="el => setSectionRef(el, 1)">
      <div class="section-inner">
        <div class="text">
          <div class="eyebrow fade-in">石桥 · 材料升级</div>
          <h1 class="fade-in">石材拼接，桥面更稳定</h1>
          <p class="fade-in">石块逐层拼接，增强承载与耐久性，桥梁从"能过"走向"更稳"。</p>
          <div class="fact fade-in">耐久寿命提升至百年级</div>
          <div class="question fade-in">但石材重量增加后，如何避免结构下挠？</div>
          <button class="cta fade-in" @click="$router.push('/map?dynasty=隋')">探索隋代石桥</button>
        </div>
        <div class="visual">
          <div class="visual-card">
            <svg viewBox="0 0 520 220" role="img" aria-label="石桥拼接结构">
              <rect class="stone-block" x="60" y="130" width="80" height="42" />
              <rect class="stone-block" x="150" y="120" width="90" height="52" />
              <rect class="stone-block" x="250" y="130" width="85" height="42" />
              <rect class="stone-block" x="340" y="115" width="95" height="57" />
              <rect class="stone-block" x="90" y="80" width="90" height="42" />
              <rect class="stone-block" x="210" y="70" width="100" height="52" />
              <rect class="stone-block" x="330" y="80" width="90" height="42" />
              <path class="river" d="M30 185 Q160 165 290 185 T500 185" />
              <ellipse class="shadow" cx="260" cy="150" rx="170" ry="12" />
            </svg>
          </div>
        </div>
      </div>
    </section>

    <section class="story-section arch" data-index="2" :ref="el => setSectionRef(el, 2)">
      <div class="section-inner">
        <div class="text">
          <div class="eyebrow fade-in">拱桥 · 结构飞跃</div>
          <h1 class="fade-in">拱形传力，跨越更长更稳</h1>
          <p class="fade-in">拱圈将荷载分散到两端，形成清晰受力路径，实现更大跨度与持久稳定。</p>
          <div class="fact fade-in">单跨可达 30–60 米</div>
          <div class="question fade-in">当工程需求不断提升，结构逻辑成为决定性力量。</div>
          <div class="summary-card fade-in">
            <div class="summary-title">结构优势总结</div>
            <ul class="summary-list">
              <li>压力传递清晰，材料利用率更高</li>
              <li>跨越能力提升，桥面更稳定</li>
              <li>耐久性强，适配复杂地形</li>
            </ul>
          </div>
          <button class="cta fade-in" @click="$router.push('/map?dynasty=宋')">探索宋代拱桥</button>
        </div>
        <div class="visual">
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

    <section class="story-section dynasty" data-index="3" :ref="el => setSectionRef(el, 3)">
      <div class="section-inner">
        <div class="text">
          <div class="eyebrow fade-in">榫卯 · 技艺巅峰</div>
          <h1 class="fade-in">榫卯木构，无需一钉一铁</h1>
          <p class="fade-in">中国古代匠人以精准的榫卯节点连接木构件，桥身可拆可换，历经千年而不坠。</p>
          <div class="fact fade-in">木拱廊桥最长达 30 米，全为榫卯结构</div>
          <div class="question fade-in">当木构件精准咬合，是否实现了结构与美学最深的结合？</div>
          <div class="summary-card fade-in">
            <div class="summary-title">中国古典桥梁成就</div>
            <ul class="summary-list">
              <li>赵州桥 · 世界最古老敞肩石拱桥</li>
              <li>清明上河图 · 汴水虹桥无柱飞渡</li>
              <li>闽浙木拱廊桥 · UNESCO 遗产</li>
            </ul>
          </div>
          <button class="cta fade-in" @click="$router.push('/game')">体验榫卯拼图</button>
        </div>
        <div class="visual">
          <div class="visual-card">
            <svg viewBox="0 0 520 240" role="img" aria-label="榫卯结构示意">
              <rect class="tenon" x="180" y="80" width="40" height="30" rx="2" />
              <rect class="mortise" x="230" y="100" width="60" height="30" rx="2" />
              <rect class="beam-h" x="160" y="105" width="30" height="10" rx="2" />
              <rect class="beam-h" x="310" y="105" width="50" height="10" rx="2" />
              <circle class="joint-dot" cx="200" cy="110" r="4" />
              <circle class="joint-dot" cx="260" cy="110" r="4" />
              <text class="label-thin" x="140" y="140">榫头</text>
              <text class="label-thin" x="310" y="140">卯口</text>
              <path class="river" d="M30 205 Q160 185 290 205 T500 205" />
            </svg>
          </div>
        </div>
      </div>
    </section>

    <OnThisDay />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import OnThisDay from '../components/OnThisDay.vue'

gsap.registerPlugin(ScrollTrigger)

const currentIndex = ref(0)
const sectionEls = ref([])

const setSectionRef = (el, index) => {
  if (el) sectionEls.value[index] = el
}

onMounted(() => {
  sectionEls.value.forEach((el, index) => {
    if (!el) return
    ScrollTrigger.create({
      trigger: el,
      start: 'top center',
      end: 'bottom center',
      onEnter: () => { currentIndex.value = index },
      onLeaveBack: () => { currentIndex.value = Math.max(0, index - 1) }
    })

    const targets = el.querySelectorAll('.fade-in')
    gsap.set(targets, { opacity: 0, y: 24 })
    gsap.to(targets, {
      opacity: 1,
      y: 0,
      duration: 0.7,
      stagger: 0.12,
      scrollTrigger: {
        trigger: el,
        start: 'top 65%',
        end: 'bottom 35%',
        toggleActions: 'play reverse play reverse'
      }
    })
  })
})
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  color: #1f2d3d;
  font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
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
  transition: background 0.3s;
}
.progress span.active {
  background: #8b4513;
  box-shadow: 0 0 0 4px rgba(139, 69, 19, 0.15);
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
}
.visual-card {
  width: 100%;
  max-width: 540px;
  padding: 18px 20px;
  border-radius: 18px;
  background: rgba(255,255,255,0.6);
  box-shadow: 0 16px 40px rgba(15,23,42,0.12);
  backdrop-filter: blur(8px);
}

.eyebrow {
  font-size: 12px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: rgba(31,41,55,0.6);
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
  color: rgba(15,23,42,0.7);
}
.summary-card {
  margin-top: 16px;
  padding: 10px 0 10px 16px;
  border-left: 2px solid rgba(139,69,19,0.35);
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
.cta {
  margin-top: 18px;
  padding: 10px 24px;
  background: #8b4513;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 15px;
  cursor: pointer;
  transition: background 0.2s;
}
.cta:hover {
  background: #a0522d;
}

.wood { background: linear-gradient(135deg, #f8e8d0, #f5caa3); }
.stone { background: linear-gradient(135deg, #f0ede6, #d8d8d8); }
.arch { background: linear-gradient(135deg, #e0f2fe, #c7d2fe); }
.dynasty { background: linear-gradient(135deg, #fdf2e9, #fadbd8); }

svg { width: 100%; max-width: 520px; }

.beam { stroke: #8b5a2b; stroke-width: 10; stroke-linecap: round; }
.support { fill: #7c4a1f; }
.river { fill: none; stroke: rgba(59,130,246,0.45); stroke-width: 6; stroke-linecap: round; }
.shadow { fill: rgba(15,23,42,0.12); }
.stone-block { fill: #8f8f8f; opacity: 0.85; }
.arch-path { fill: none; stroke: #2563eb; stroke-width: 8; stroke-linecap: round; }
.deck { stroke: #1e3a8a; stroke-width: 6; opacity: 0.6; }
.pier { stroke: #1e3a8a; stroke-width: 6; opacity: 0.6; }
.force-line { stroke: #f97316; stroke-width: 4; stroke-linecap: round; }
.force-dot { fill: #f97316; }
.force-label { fill: #f97316; font-size: 12px; }

.tenon { fill: #8b5a2b; }
.mortise { fill: #a0522d; }
.beam-h { fill: #cd853f; }
.joint-dot { fill: #ff8c00; }
.label-thin { fill: #6d4c41; font-size: 12px; }

@media (max-width: 900px) {
  .section-inner { flex-direction: column; text-align: center; }
  .visual { width: 100%; }
  .progress { right: 16px; }
}
</style>
