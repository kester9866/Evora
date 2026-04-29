<template>
  <div class="graph-page">
    <div class="graph-main">
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
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { Network } from 'vis-network'
import { DataSet } from 'vis-data'
import { getGraphData } from '../api/kg.js'

const networkRef = ref(null)
const selectedNode = ref(null)
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

onMounted(async () => {
  try {
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

    const nodes = new DataSet(nodesData)
    const edges = new DataSet(edgesData)

    network = new Network(networkRef.value, { nodes, edges }, {
      physics: { solver: 'forceAtlas2Based' },
      interaction: { hover: true }
    })

    network.on('click', (params) => {
      if (params.nodes.length > 0) {
        const nodeId = params.nodes[0]
        const node = nodesData.find(n => n.id === nodeId)
        if (node) selectedNode.value = node
      } else {
        selectedNode.value = null
      }
    })
  } catch {
    // No data available
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
}
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
  padding: 6px 12px;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 6px;
  cursor: pointer;
  font-size: 13px;
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
  border-left: 1px solid #eee;
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
</style>
