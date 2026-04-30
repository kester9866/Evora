<template>
  <div class="graph-page">
    <!-- Loading overlay -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-card">
        <h2>知识图谱</h2>
        <p>正在构建桥梁知识网络...</p>
        <div class="progress-track">
          <div class="progress-fill" :style="{ width: progress + '%' }"></div>
        </div>
        <span class="progress-text">{{ progress }}%</span>
      </div>
    </div>

    <div v-show="!loading" class="graph-main">
      <div class="toolbar">
        <button @click="zoomIn">🔍+</button>
        <button @click="zoomOut">🔍−</button>
        <button @click="resetView">重置视图</button>
      </div>
      <div ref="networkRef" class="network-container"></div>
      <div class="legend">
        <div v-for="d in dynasties" :key="d.name" class="legend-item">
          <span class="legend-dot" :style="{ background: d.color }"></span>
          {{ d.name }}
        </div>
      </div>
    </div>

    <div v-if="selectedNode" class="side-panel">
      <h3>{{ selectedNode.label }}</h3>
      <p v-if="selectedNode.summary">{{ selectedNode.summary }}</p>
      <div class="panel-actions">
        <button v-if="selectedNode.has_model" @click="$router.push(`/model/${selectedNode.id}`)">查看3D详情</button>
        <button v-else @click="$router.push('/map')">查看地图</button>
        <button class="close-panel" @click="selectedNode = null">关闭</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { Network } from 'vis-network'
import { DataSet } from 'vis-data'
import { getGraphData } from '../api/kg.js'

const networkRef = ref(null)
const selectedNode = ref(null)
const loading = ref(true)
const progress = ref(0)
let network = null

const dynasties = [
  { name: '先秦', color: '#e74c3c' },
  { name: '秦汉', color: '#e67e22' },
  { name: '隋唐', color: '#f1c40f' },
  { name: '宋', color: '#2ecc71' },
  { name: '元', color: '#3498db' },
  { name: '明', color: '#9b59b6' },
  { name: '清', color: '#1abc9c' }
]

const dynastyColors = {
  '先秦': '#e74c3c', '秦': '#e74c3c', '汉': '#e74c3c',
  '隋': '#f1c40f', '唐': '#f1c40f',
  '宋': '#2ecc71',
  '元': '#3498db',
  '明': '#9b59b6',
  '清': '#1abc9c'
}

function getDynastyColor(d) {
  return dynastyColors[d] || '#95a5a6'
}

function advanceProgress(target, delay = 300) {
  return new Promise(resolve => {
    const start = progress.value
    const startTime = Date.now()
    function tick() {
      const elapsed = Date.now() - startTime
      const t = Math.min(elapsed / delay, 1)
      const eased = t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2
      progress.value = Math.round(start + (target - start) * eased)
      if (t < 1) {
        requestAnimationFrame(tick)
      } else {
        resolve()
      }
    }
    requestAnimationFrame(tick)
  })
}

onMounted(async () => {
  try {
    advanceProgress(15, 200)

    const data = await getGraphData()
    const nodesData = (data.nodes || []).map(n => ({
      id: n.id,
      label: n.label,
      color: { background: getDynastyColor(n.dynasty), border: '#fff' },
      shape: 'box',
      summary: n.summary,
      has_model: n.has_model,
      dynasty: n.dynasty
    }))
    const edgesData = (data.edges || []).map(e => ({
      from: e.source,
      to: e.target,
      label: e.relation,
      arrows: 'to',
      color: { color: '#bdc3c7' }
    }))

    await advanceProgress(45, 250)

    const nodes = new DataSet(nodesData)
    const edges = new DataSet(edgesData)

    await nextTick()
    await advanceProgress(60, 200)

    network = new Network(networkRef.value, { nodes, edges }, {
      physics: { solver: 'forceAtlas2Based' },
      interaction: { hover: true }
    })

    await advanceProgress(80, 250)

    network.on('click', (params) => {
      if (params.nodes.length > 0) {
        const nodeId = params.nodes[0]
        const node = nodesData.find(n => n.id === nodeId)
        if (node) selectedNode.value = node
      } else {
        selectedNode.value = null
      }
    })

    // Wait for physics stabilization then finish
    await new Promise(resolve => {
      network.once('stabilizationIterationsDone', resolve)
      setTimeout(resolve, 1500)
    })

    await advanceProgress(100, 200)

    loading.value = false
  } catch {
    loading.value = false
  }
})

function zoomIn() { network?.moveTo({ scale: (network.getScale() || 1) * 1.3 }) }
function zoomOut() { network?.moveTo({ scale: (network.getScale() || 1) * 0.7 }) }
function resetView() { network?.fit({ animation: true }) }

onBeforeUnmount(() => { network?.destroy() })
</script>

<style scoped>
.graph-page {
  display: flex;
  height: calc(100vh - 64px);
  font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
  position: relative;
}

/* ===== Loading overlay ===== */
.loading-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(160deg, #f5f0ea 0%, #f0ebe3 30%, #f7f3ed 60%, #faf7f2 100%);
  z-index: 20;
}
.loading-card {
  text-align: center;
  padding: 48px 56px;
  background: rgba(255,255,255,0.8);
  backdrop-filter: blur(12px);
  border-radius: 20px;
  border: 1px solid rgba(156,92,44,0.08);
  box-shadow: 0 8px 40px rgba(107,79,58,0.06);
  min-width: 360px;
}
.loading-card h2 {
  margin: 0 0 8px;
  font-size: 24px;
  color: #3d3020;
  font-weight: 700;
  letter-spacing: 0.06em;
}
.loading-card p {
  margin: 0 0 28px;
  font-size: 14px;
  color: #8A7A6A;
}
.progress-track {
  width: 100%;
  height: 6px;
  background: rgba(107,79,58,0.08);
  border-radius: 3px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #6B4F3A, #9C5A2C);
  border-radius: 3px;
  transition: width 0.15s linear;
}
.progress-text {
  display: block;
  margin-top: 10px;
  font-size: 13px;
  color: #A09080;
}

/* ===== Graph main ===== */
.graph-main {
  flex: 1;
  position: relative;
}
.network-container {
  width: 100%;
  height: 100%;
}
.toolbar {
  position: absolute;
  top: 16px;
  left: 16px;
  z-index: 10;
  display: flex;
  gap: 8px;
}
.toolbar button {
  padding: 8px 14px;
  background: #fff;
  border: 1px solid #e8e0d5;
  border-radius: 10px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s ease;
}
.toolbar button:hover {
  border-color: #9C5A2C;
  color: #9C5A2C;
}
.legend {
  position: absolute;
  bottom: 16px;
  left: 16px;
  z-index: 10;
  background: rgba(255,255,255,0.9);
  padding: 10px 14px;
  border-radius: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.legend-item { display: flex; align-items: center; gap: 4px; font-size: 12px; }
.legend-dot { width: 10px; height: 10px; border-radius: 2px; }
.side-panel {
  width: 300px;
  background: #fff;
  border-left: 1px solid #f0ebe3;
  border-radius: 12px 0 0 12px;
  padding: 24px;
  overflow-y: auto;
}
.side-panel h3 { margin: 0 0 12px; font-size: 18px; }
.side-panel p { font-size: 14px; color: #555; line-height: 1.6; }
.panel-actions { display: flex; flex-direction: column; gap: 8px; margin-top: 16px; }
.panel-actions button {
  padding: 8px 16px;
  background: #6B4F3A;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}
.close-panel { background: #eee !important; color: #333 !important; }

@media (max-width: 768px) {
  .loading-card {
    min-width: auto;
    margin: 0 24px;
    padding: 32px 36px;
  }
}
</style>
