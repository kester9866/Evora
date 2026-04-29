<template>
  <div class="home">
    <!-- 右侧进度条 -->
    <div class="dots">
      <span
        v-for="(item, index) in sections"
        :key="index"
        :class="{ active: currentIndex === index }"
      ></span>
    </div>

    <!-- 第一屏：木桥 -->
    <section class="screen wood" ref="setRef">
      <div class="content">
        <h1>桥的起点</h1>
        <p>最早的桥梁，来自最直观的跨越方式</p>

        <svg viewBox="0 0 400 200">
          <line
            x1="50"
            y1="120"
            x2="350"
            y2="120"
            class="beam"
            :class="{ active: currentIndex === 0 }"
          />
        </svg>
      </div>
    </section>

    <!-- 第二屏：石桥 -->
    <section class="screen stone" ref="setRef">
      <div class="content">
        <h1>材料的进化</h1>
        <p>从木到石，桥梁变得更加坚固</p>

        <div class="stones">
          <div
            v-for="i in 6"
            :key="i"
            class="stone-block"
            :style="{ animationDelay: i * 0.2 + 's' }"
            :class="{ active: currentIndex === 1 }"
          ></div>
        </div>
      </div>
    </section>

    <!-- 第三屏：拱桥 -->
    <section class="screen arch" ref="setRef">
      <div class="content">
        <h1>结构的突破</h1>
        <p>拱桥将压力转化为稳定，达到了工程的巅峰</p>

        <svg viewBox="0 0 400 200">
          <!-- 拱形 -->
          <path
            d="M 50 150 Q 200 50 350 150"
            class="arch-line"
            :class="{ active: currentIndex === 2 }"
          />

          <!-- 力箭头 -->
          <line
            x1="200"
            y1="110"
            x2="200"
            y2="150"
            class="force"
            :class="{ active: currentIndex === 2 }"
          />
        </svg>

        <button class="enter-btn" @click="$emit('enter')">
          进入探索 →
        </button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const sections = ref([]);
const currentIndex = ref(0);

const setRef = (el) => {
  if (el) sections.value.push(el);
};

onMounted(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const index = sections.value.indexOf(entry.target);
          currentIndex.value = index;
        }
      });
    },
    { threshold: 0.6 }
  );

  sections.value.forEach((sec) => observer.observe(sec));
});
</script>

<style scoped>
.home {
  scroll-behavior: smooth;
}

/* 每屏 */
.screen {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.content {
  text-align: center;
}

h1 {
  font-size: 36px;
  margin-bottom: 10px;
}

p {
  color: #666;
  margin-bottom: 20px;
}

/* 背景 */
.wood {
  background: #f5e6d3;
}

.stone {
  background: #f0f0f0;
}

.arch {
  background: #e6f4ff;
}

/* 木桥动画 */
.beam {
  stroke: #8b5a2b;
  stroke-width: 6;
  stroke-dasharray: 300;
  stroke-dashoffset: 300;
  transition: 1s;
}

.beam.active {
  stroke-dashoffset: 0;
}

/* 石桥 */
.stones {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.stone-block {
  width: 40px;
  height: 20px;
  background: #999;
  opacity: 0;
  transform: translateY(20px);
}

.stone-block.active {
  animation: rise 0.6s forwards;
}

@keyframes rise {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 拱桥 */
.arch-line {
  fill: none;
  stroke: #333;
  stroke-width: 4;
  stroke-dasharray: 400;
  stroke-dashoffset: 400;
  transition: 1s;
}

.arch-line.active {
  stroke-dashoffset: 0;
}

.force {
  stroke: red;
  stroke-width: 3;
  opacity: 0;
}

.force.active {
  animation: flow 1s infinite linear;
  opacity: 1;
}

@keyframes flow {
  from {
    stroke-dashoffset: 20;
  }
  to {
    stroke-dashoffset: 0;
  }
}

/* 按钮 */
.enter-btn {
  margin-top: 20px;
  padding: 10px 20px;
  border: none;
  background: #409eff;
  color: white;
  border-radius: 6px;
  cursor: pointer;
}

/* 右侧点 */
.dots {
  position: fixed;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
}

.dots span {
  display: block;
  width: 8px;
  height: 8px;
  margin: 8px 0;
  border-radius: 50%;
  background: #ccc;
}

.dots span.active {
  background: #409eff;
}
</style>