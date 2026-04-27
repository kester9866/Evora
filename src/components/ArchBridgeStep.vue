<template>
  <div class="step-bridge">
    <svg class="bridge-svg" viewBox="0 0 640 320" role="img" aria-label="拱桥受力分步示意图">
      <defs>
        <marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
          <path d="M0,0 L6,3 L0,6 Z" fill="#2563eb" />
        </marker>
      </defs>

      <path
        class="arch"
        d="M80,230 Q320,80 560,230"
        fill="none"
        stroke="#2f3b52"
        stroke-width="8"
      />

      <line
        x1="120"
        y1="170"
        x2="520"
        y2="170"
        stroke="#4a5568"
        stroke-width="6"
        stroke-linecap="round"
      />

      <rect class="pier" :class="{ active: step >= 3 }" x="70" y="230" width="40" height="60" rx="4" />
      <rect class="pier" :class="{ active: step >= 3 }" x="530" y="230" width="40" height="60" rx="4" />

      <line
        v-if="step >= 1"
        :key="`load-${step}`"
        class="force-line load"
        x1="320"
        y1="130"
        x2="320"
        y2="210"
        marker-end="url(#arrow)"
      />

      <path
        v-if="step >= 2"
        :key="`left-${step}`"
        class="force-line left"
        d="M320,210 Q220,200 140,225"
        fill="none"
        marker-end="url(#arrow)"
      />

      <path
        v-if="step >= 2"
        :key="`right-${step}`"
        class="force-line right"
        d="M320,210 Q420,200 500,225"
        fill="none"
        marker-end="url(#arrow)"
      />

      <circle cx="320" cy="210" r="6" fill="#2563eb" />
    </svg>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  step: {
    type: Number,
    default: 1
  }
});

const step = computed(() => props.step);
</script>

<style scoped>
.step-bridge {
  width: 100%;
}

.bridge-svg {
  width: 100%;
  height: 300px;
  display: block;
}

.pier {
  fill: #cbd5e1;
  transition: fill 0.3s ease;
}

.pier.active {
  fill: #2563eb;
}

.force-line {
  stroke: #2563eb;
  stroke-width: 3;
  stroke-dasharray: 6 6;
}

.force-line.load {
  animation: flow 1.4s linear;
}

.force-line.left,
.force-line.right {
  animation: flow 1.4s linear;
}

@keyframes flow {
  from {
    stroke-dashoffset: 18;
    opacity: 0.2;
  }
  to {
    stroke-dashoffset: 0;
    opacity: 1;
  }
}
</style>
