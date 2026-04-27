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

    <main class="container">
      <section class="hero card">
        <div class="hero-left">
          <h1>拱桥结构原理展示</h1>
          <div class="meta">隋 · 拱桥 · 石</div>
          <p class="tagline">以拱圈传力为核心的稳定结构，体现古代结构智慧。</p>
        </div>
        <div class="hero-right">
          <div class="hero-badge">结构分析</div>
          <div class="hero-note">教学式可视化</div>
        </div>
      </section>

      <section class="core card">
        <div class="card-title">结构动画演示</div>
        <div class="canvas">
          <ArchBridgeStep :step="step" />
        </div>
      </section>

      <section class="steps card">
        <div class="card-title">步骤控制</div>
        <div class="step-track">
          <div
            v-for="item in stepItems"
            :key="item.id"
            class="step-pill"
            :class="{ active: step === item.id }"
            @click="setStep(item.id)"
          >
            {{ item.label }}
          </div>
          <div class="step-line">
            <div class="step-line-active" :style="{ width: progressWidth }"></div>
          </div>
        </div>
      </section>

      <section class="desc card">
        <div class="card-title">原理说明</div>
        <div class="desc-text">{{ stepDesc }}</div>
      </section>

      <section class="summary">
        <div class="summary-card" v-for="item in summary" :key="item.title">
          <div class="icon"></div>
          <div class="summary-content">
            <div class="summary-title">{{ item.title }}</div>
            <div class="summary-text">{{ item.text }}</div>
          </div>
        </div>
      </section>

      <div class="section-divider"></div>

      <section class="hero card">
        <div class="hero-left">
          <h1>榫卯结构原理展示</h1>
          <div class="meta">明 · 榫卯 · 木</div>
          <p class="tagline">榫头与卯口精准嵌合，实现稳固连接与可拆装性。</p>
        </div>
        <div class="hero-right">
          <div class="hero-badge">结构分析</div>
          <div class="hero-note">工艺式可视化</div>
        </div>
      </section>

      <section class="core card">
        <div class="card-title">结构动画演示</div>
        <div class="canvas">
          <MortiseTenon :step="mortiseStep" :show-controls="false" embedded />
        </div>
      </section>

      <section class="steps card">
        <div class="card-title">步骤控制</div>
        <div class="step-track">
          <div
            v-for="item in mortiseStepItems"
            :key="item.id"
            class="step-pill"
            :class="{ active: mortiseStep === item.id }"
            @click="setMortiseStep(item.id)"
          >
            {{ item.label }}
          </div>
          <div class="step-line">
            <div class="step-line-active" :style="{ width: mortiseProgressWidth }"></div>
          </div>
        </div>
      </section>

      <section class="desc card">
        <div class="card-title">原理说明</div>
        <div class="desc-text">{{ mortiseDesc }}</div>
      </section>

      <section class="summary">
        <div class="summary-card" v-for="item in mortiseSummary" :key="item.title">
          <div class="icon"></div>
          <div class="summary-content">
            <div class="summary-title">{{ item.title }}</div>
            <div class="summary-text">{{ item.text }}</div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import ArchBridgeStep from "../components/ArchBridgeStep.vue";
import MortiseTenon from "../components/MortiseTenon.vue";

const step = ref(1);
const mortiseStep = ref(1);

const stepItems = [
  { id: 1, label: "Step 1" },
  { id: 2, label: "Step 2" },
  { id: 3, label: "Step 3" }
];

const mortiseStepItems = [
  { id: 1, label: "Step 1" },
  { id: 2, label: "Step 2" },
  { id: 3, label: "Step 3" },
  { id: 4, label: "Step 4" }
];

const stepDesc = computed(() => {
  if (step.value === 1) return "桥面承受竖向荷载，力集中于拱顶核心区域。";
  if (step.value === 2) return "荷载沿拱圈向两侧传递，形成稳定的压力通道。";
  return "力最终传递到桥墩与地基，形成整体稳定结构。";
});

const mortiseDesc = computed(() => {
  if (mortiseStep.value === 1) return "榫头与卯口分离，展示原始结构形态。";
  if (mortiseStep.value === 2) return "榫头平移对位，准备精准嵌合。";
  if (mortiseStep.value === 3) return "榫头插入卯口，形成摩擦与咬合。";
  return "完成锁定后结构稳固，兼具抗拉与抗剪能力。";
});

const progressWidth = computed(() => `${(step.value - 1) * 50}%`);
const mortiseProgressWidth = computed(() => `${((mortiseStep.value - 1) / 3) * 100}%`);

const summary = [
  { title: "稳定性强", text: "受力路径清晰，压力沿拱圈传导。" },
  { title: "材料高效", text: "以压代拉，充分利用石材抗压特性。" },
  { title: "跨越能力", text: "结构自稳，适合较大跨度桥面。" }
];

const mortiseSummary = [
  { title: "精准嵌合", text: "榫卯结合紧密，节点处不依赖金属连接。" },
  { title: "可拆装性", text: "结构可重复拆卸与维护，便于修复与传承。" },
  { title: "抗震性能", text: "节点允许微位移，提升木构抗震韧性。" }
];

const setStep = (value) => {
  step.value = value;
};

const setMortiseStep = (value) => {
  mortiseStep.value = value;
};
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f4ff, #f7faff);
  color: #1f2d3d;
}

.nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 24px;
  background: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  position: sticky;
  top: 0;
  z-index: 10;
}

.brand {
  font-weight: 600;
  font-size: 16px;
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

.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.card {
  background: #ffffff;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
}

.hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.hero-left h1 {
  margin: 0 0 8px;
  font-size: 26px;
}

.meta {
  color: #6b7280;
  font-size: 14px;
  margin-bottom: 8px;
}

.tagline {
  margin: 0;
  color: #4b5563;
  font-size: 14px;
}

.hero-right {
  text-align: right;
}

.hero-badge {
  font-size: 12px;
  color: #2563eb;
  background: rgba(37, 99, 235, 0.12);
  display: inline-block;
  padding: 6px 10px;
  border-radius: 999px;
  margin-bottom: 6px;
}

.hero-note {
  font-size: 12px;
  color: #6b7280;
}

.core .canvas {
  margin-top: 10px;
  padding: 16px;
  border-radius: 12px;
  background: #f8fafc;
}

.steps .step-track {
  position: relative;
  padding: 8px 0 16px;
}

.step-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 90px;
  height: 34px;
  margin-right: 12px;
  border-radius: 999px;
  border: 1px solid #e5e7eb;
  font-size: 12px;
  color: #6b7280;
  cursor: pointer;
  background: #ffffff;
}

.step-pill.active {
  border-color: #2563eb;
  color: #2563eb;
  background: rgba(37, 99, 235, 0.08);
}

.step-line {
  position: absolute;
  left: 0;
  bottom: 6px;
  width: 100%;
  height: 4px;
  background: #e5e7eb;
  border-radius: 999px;
}

.step-line-active {
  height: 100%;
  background: linear-gradient(90deg, #2563eb, #60a5fa);
  border-radius: 999px;
  transition: width 0.3s ease;
}

.desc-text {
  font-size: 14px;
  color: #4b5563;
}

.summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

.summary-card {
  background: #ffffff;
  border-radius: 14px;
  padding: 16px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
  display: flex;
  gap: 12px;
  align-items: center;
}

.icon {
  width: 36px;
  height: 36px;
  border-radius: 12px;
  background: linear-gradient(135deg, #2563eb, #60a5fa);
  opacity: 0.9;
}

.summary-title {
  font-weight: 600;
  font-size: 14px;
  margin-bottom: 4px;
}

.summary-text {
  font-size: 12px;
  color: #6b7280;
}

.section-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(148, 163, 184, 0.5), transparent);
  margin: 6px 0 2px;
}
</style>
