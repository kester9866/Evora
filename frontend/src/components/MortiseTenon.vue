<template>
  <div class="mt-wrap" :class="{ embedded }">
    <template v-if="showControls">
      <h2>榫卯结构拼接演示</h2>
      <p class="desc">{{ stepText }}</p>
    </template>

    <svg class="mt-svg" viewBox="0 0 900 300" role="img" aria-label="榫卯结构拼接演示">
      <defs>
        <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#000" flood-opacity="0.2" />
        </filter>
      </defs>

      <g :class="['tenon', stepClass]">
        <path d="M80 90 H340 V125 H420 V175 H340 V210 H80 Z" />
      </g>

      <g class="mortise" :class="{ highlight: normalizedStep >= 4 }">
        <path d="M520 90 H780 V210 H520 V175 H610 V125 H520 Z" />
      </g>

      <rect
        v-if="normalizedStep >= 4"
        class="join-highlight"
        x="520"
        y="125"
        width="90"
        height="60"
        rx="6"
      />
    </svg>

    <div class="controls" v-if="showControls">
      <button @click="startDemo" :disabled="playing">开始演示</button>
      <button @click="nextStep" :disabled="normalizedStep >= 4 || playing">下一步</button>
      <button class="ghost" @click="resetStep">重置</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

const props = defineProps({
  step: {
    type: Number,
    default: 0
  },
  showControls: {
    type: Boolean,
    default: true
  },
  embedded: {
    type: Boolean,
    default: false
  }
});

const localStep = ref(1);
const playing = ref(false);

const currentStep = computed(() => (props.step > 0 ? props.step : localStep.value));

const normalizedStep = computed(() => {
  const value = currentStep.value || 1;
  return Math.min(Math.max(value, 1), 4);
});

const stepText = computed(() => {
  if (normalizedStep.value === 1) return "Step1：结构分离";
  if (normalizedStep.value === 2) return "Step2：对准榫卯位置";
  if (normalizedStep.value === 3) return "Step3：榫头插入卯口";
  return "Step4：形成稳定连接，无需钉子";
});

const stepClass = computed(() => {
  if (normalizedStep.value === 1) return "s1";
  if (normalizedStep.value === 2) return "s2";
  return "s3";
});

const nextStep = () => {
  if (localStep.value < 4) localStep.value += 1;
};

const resetStep = () => {
  localStep.value = 1;
  playing.value = false;
};

const startDemo = async () => {
  if (playing.value) return;
  playing.value = true;
  localStep.value = 1;
  await new Promise((r) => setTimeout(r, 400));
  localStep.value = 2;
  await new Promise((r) => setTimeout(r, 600));
  localStep.value = 3;
  await new Promise((r) => setTimeout(r, 500));
  localStep.value = 4;
  await new Promise((r) => setTimeout(r, 300));
  playing.value = false;
};
</script>

<style scoped>
.mt-wrap {
  padding: 16px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
  width: 100%;
  max-width: 900px;
  margin: 24px auto;
}

.mt-wrap.embedded {
  padding: 0;
  background: transparent;
  box-shadow: none;
  border-radius: 0;
  margin: 0;
  max-width: none;
}

.mt-wrap h2 {
  margin: 0 0 6px;
  font-size: 18px;
  color: #1f2d3d;
}

.desc {
  margin: 0 0 12px;
  color: #6b7280;
  font-size: 13px;
}

.mt-svg {
  width: 100%;
  height: 300px;
  display: block;
  background: #f7f3ed;
  border: 1px solid #eadfce;
  border-radius: 10px;
}

.tenon path,
.mortise path {
  fill: #8b5a2b;
  filter: url(#shadow);
}

.mortise path {
  fill: #a67c52;
}

.tenon {
  transition: transform 0.6s ease;
}

.tenon.s1 {
  transform: translateX(0);
}

.tenon.s2 {
  transform: translateX(100px);
}

.tenon.s3 {
  transition: transform 0.7s ease-out;
  transform: translateX(190px);
}

.mortise.highlight path {
  stroke: rgba(255, 220, 120, 0.9);
  stroke-width: 2;
}

.join-highlight {
  fill: rgba(255, 220, 120, 0.25);
  stroke: rgba(255, 220, 120, 0.9);
  stroke-width: 2;
  filter: url(#shadow);
}

.controls {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

.controls button {
  padding: 6px 12px;
  border: none;
  background: #8b5a2b;
  color: #fff;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
}

.controls button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.controls .ghost {
  background: #e5e7eb;
  color: #374151;
}
</style>
