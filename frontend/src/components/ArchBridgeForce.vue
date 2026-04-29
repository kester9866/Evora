<template>
  <div class="arch-bridge">
    <h2>拱桥受力可视化</h2>
    <p class="desc">拱桥将荷载转化为沿拱圈传递的压力，并向两侧桥墩分散，从而保持稳定。</p>

    <svg class="bridge-svg" viewBox="0 0 600 320" role="img" aria-label="拱桥受力示意图">
      <defs>
        <marker
          id="arrow"
          markerWidth="8"
          markerHeight="8"
          refX="6"
          refY="3"
          orient="auto"
        >
          <path d="M0,0 L6,3 L0,6 Z" fill="#2b6cb0" />
        </marker>
      </defs>

      <path
        class="arch"
        d="M80,240 Q300,80 520,240"
        fill="none"
        stroke="#2f3b52"
        stroke-width="8"
      />

      <line
        x1="110"
        y1="180"
        x2="490"
        y2="180"
        stroke="#4a5568"
        stroke-width="6"
        stroke-linecap="round"
      />

      <line
        class="force-line load"
        x1="300"
        y1="150"
        x2="300"
        y2="220"
        marker-end="url(#arrow)"
      />

      <path
        class="force-line left"
        d="M300,220 Q210,200 140,230"
        fill="none"
        marker-end="url(#arrow)"
      />

      <path
        class="force-line right"
        d="M300,220 Q390,200 460,230"
        fill="none"
        marker-end="url(#arrow)"
      />

      <circle cx="300" cy="220" r="6" fill="#2b6cb0" />
    </svg>

    <div class="note">
      受力路径以虚线流动动画表示：先出现荷载，再向两侧传递，体现拱桥结构的稳定性。
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.arch-bridge {
  padding: 16px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.06);
}

.arch-bridge h2 {
  margin: 0 0 6px;
  font-size: 18px;
  color: #1f2d3d;
}

.desc {
  margin: 0 0 12px;
  color: #6b7280;
  font-size: 13px;
}

.bridge-svg {
  width: 100%;
  height: 260px;
  display: block;
}

.force-line {
  stroke: #2b6cb0;
  stroke-width: 3;
  stroke-dasharray: 6 6;
  animation: flow 2.6s linear infinite;
}

.force-line.load {
  animation-delay: 0s;
}

.force-line.left {
  animation-delay: 0.6s;
}

.force-line.right {
  animation-delay: 1.2s;
}

@keyframes flow {
  from {
    stroke-dashoffset: 0;
    opacity: 0.2;
  }
  30% {
    opacity: 1;
  }
  to {
    stroke-dashoffset: -24;
    opacity: 1;
  }
}

.note {
  margin-top: 10px;
  font-size: 12px;
  color: #6b7280;
}
</style>
