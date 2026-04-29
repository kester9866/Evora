<template>
  <div class="map-page">
    <div class="filters">
      <div class="filter-item">
        <span>朝代</span>
        <select v-model="selectedDynasty" @change="onFilterChange">
          <option value="">全部</option>
          <option v-for="d in dynasties" :key="d" :value="d">{{ d }}</option>
        </select>
      </div>
      <div class="filter-item">
        <span>类型</span>
        <select v-model="selectedType" @change="onFilterChange">
          <option value="">全部</option>
          <option v-for="t in types" :key="t" :value="t">{{ t }}</option>
        </select>
      </div>
      <div class="filter-item level-selector">
        <button :class="{ active: mapLevel === 'province' }" @click="switchLevel('province')">省级</button>
        <button :class="{ active: mapLevel === 'city' }" @click="switchLevel('city')">市级</button>
      </div>
      <button v-if="showResetBtn" class="reset-view-btn" @click="resetView">🏠 恢复默认视角</button>
    </div>

    <div class="main">
      <div class="map-card">
        <div class="card-title">桥梁空间分布</div>
        <div ref="chartRef" class="map-container"></div>
      </div>

      <div class="list-card">
        <div class="card-title">桥梁列表（{{ bridges.length }}）</div>
        <ul>
          <li
            v-for="item in bridges"
            :key="item.id || item.name_zh"
            :class="{ highlighted: highlightedBridge?.id === item.id }"
          >
            <div class="bridge-info">
              <div class="name-row">
                <span class="name">{{ item.name_zh }}</span>
                <span v-if="item.model_url" class="badge-3d" @click.stop="$router.push(`/model/${item.id}`)">3D模型</span>
              </div>
              <span class="meta">{{ item.dynasty }} · {{ item.type }}</span>
              <span class="location">{{ item.province }}-{{ item.city }}</span>
            </div>
            <button @click="highlightCity(item)">定位</button>
          </li>
        </ul>
        <div v-if="bridges.length === 0" class="empty">暂无数据</div>
      </div>
    </div>

    <div v-if="showDetail && detailBridge" class="modal" @click.self="showDetail = false">
      <div class="modal-content">
        <h2>{{ detailBridge.name_zh }}</h2>
        <p>{{ detailBridge.dynasty }} · {{ detailBridge.type }} · {{ detailBridge.material }}</p>
        <div class="fields">
          <div v-if="detailBridge.description" class="field">{{ detailBridge.description }}</div>
          <div v-if="detailBridge.length_m" class="field">长度：{{ detailBridge.length_m }}m</div>
          <div v-if="detailBridge.width_m" class="field">宽度：{{ detailBridge.width_m }}m</div>
        </div>
        <div class="modal-actions">
          <button v-if="detailBridge.model_url" @click="$router.push(`/model/${detailBridge.id}`)">查看3D模型</button>
          <button @click="showDetail = false">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import chinaJson from '../data/china.json'
import { getBridges } from '../api/bridges.js'
import { getProvinces } from '../api/map.js'

echarts.registerMap('china', chinaJson)

const mapReady = ref(false)

async function loadFullMap() {
  try {
    const resp = await fetch('/data/china-full.json')
    const geo = await resp.json()
    echarts.registerMap('china-full', geo)
    const provinceFeatures = { ...geo, features: geo.features.filter(f => f.properties.level === 'province') }
    echarts.registerMap('china-provinces', provinceFeatures)
    mapReady.value = true
  } catch {
    // fallback: use province-only map already registered
    mapReady.value = true
  }
}

const chartRef = ref(null)
let chartInstance = null

const selectedDynasty = ref('')
const selectedType = ref('')
const selectedProvince = ref('')
const bridges = ref([])
const provinceData = ref([])
const showDetail = ref(false)
const detailBridge = ref(null)
const highlightedBridge = ref(null)
const hasUserZoomed = ref(false)
let isProgrammaticUpdate = false

const showResetBtn = computed(() => {
  return hasUserZoomed.value || !!selectedProvince.value || !!highlightedBridge.value
})

const mapLevel = ref('province')

function switchLevel(level) {
  if (mapLevel.value === level) return
  mapLevel.value = level
  if (chartInstance) {
    isProgrammaticUpdate = true
    chartInstance.setOption(buildChartOption(selectedProvince.value), false)
    setTimeout(() => { isProgrammaticUpdate = false }, 300)
  }
}

const dynasties = ['先秦', '秦', '汉', '隋', '唐', '宋', '元', '明', '清']
const types = ['梁桥', '拱桥', '木桥', '索桥', '廊桥']

const provinceNameMap = {
  北京: '北京市', 天津: '天津市', 上海: '上海市', 重庆: '重庆市',
  内蒙古: '内蒙古自治区', 广西: '广西壮族自治区', 宁夏: '宁夏回族自治区',
  新疆: '新疆维吾尔自治区', 西藏: '西藏自治区',
  香港: '香港特别行政区', 澳门: '澳门特别行政区', 台湾: '台湾省'
}

const cityCoords = {
  '赵县': [114.77, 37.75], '泉州': [118.67, 24.94], '北京': [116.41, 39.90],
  '潮州': [116.65, 23.67], '西安': [109.05, 34.25], '泸定': [102.23, 29.91],
  '开封': [114.35, 34.79], '苏州': [120.62, 31.25], '绍兴': [120.58, 30.00],
  '泰顺': [119.72, 27.56], '保山': [98.87, 25.11], '丰台': [116.29, 39.86],
  '南京': [118.79, 32.06], '杭州': [120.15, 30.28], '武汉': [114.30, 30.60],
  '成都': [104.07, 30.57], '广州': [113.26, 23.13], '昆明': [102.71, 25.04]
}

const provinceCenters = {
  河北: [114.5, 38.0], 山西: [112.5, 37.5], 辽宁: [122.5, 41.5],
  吉林: [126.0, 43.5], 黑龙江: [127.0, 47.5], 江苏: [119.5, 33.0],
  浙江: [120.0, 29.5], 安徽: [117.0, 31.5], 福建: [118.0, 26.0],
  江西: [116.0, 27.5], 山东: [117.5, 36.0], 河南: [113.5, 33.5],
  湖北: [112.5, 30.5], 湖南: [111.5, 27.5], 广东: [113.5, 23.0],
  广西: [108.0, 23.0], 海南: [110.0, 19.0], 四川: [103.0, 30.5],
  贵州: [106.5, 26.5], 云南: [101.5, 25.0], 陕西: [109.0, 35.5],
  甘肃: [104.0, 37.0], 青海: [96.0, 35.5], 台湾: [121.0, 23.5],
  内蒙古: [112.0, 42.0], 西藏: [88.0, 31.5], 宁夏: [106.0, 37.0],
  新疆: [85.0, 41.5], 北京: [116.4, 39.9], 天津: [117.2, 39.1],
  上海: [121.5, 31.2], 重庆: [106.5, 29.5], 香港: [114.1, 22.3],
  澳门: [113.5, 22.2]
}

const toGeoName = (baseName) => {
  if (provinceNameMap[baseName]) return provinceNameMap[baseName]
  if (baseName.endsWith('省') || baseName.endsWith('市')) return baseName
  return `${baseName}省`
}

const toBaseName = (geoName) => {
  for (const [base, geo] of Object.entries(provinceNameMap)) {
    if (geo === geoName) return base
  }
  if (geoName.endsWith('省')) return geoName.replace(/省$/, '')
  if (geoName.endsWith('市')) return geoName.replace(/市$/, '')
  return geoName
}

function parseCoords(bridge) {
  if (bridge.coordinates) {
    const parts = bridge.coordinates.split(',').map(Number)
    if (parts.length === 2 && !isNaN(parts[0]) && !isNaN(parts[1])) {
      return [parts[1], parts[0]]
    }
  }
  if (bridge.city && cityCoords[bridge.city]) {
    return cityCoords[bridge.city]
  }
  return null
}

async function fetchBridges() {
  try {
    const params = {}
    if (selectedDynasty.value) params.dynasty = selectedDynasty.value
    if (selectedType.value) params.type = selectedType.value
    if (selectedProvince.value) params.province = selectedProvince.value
    const data = await getBridges(params)
    bridges.value = Array.isArray(data) ? data : (data.items || [])
  } catch {
    bridges.value = []
  }
}

async function fetchProvinceData() {
  try {
    const params = {}
    if (selectedDynasty.value) params.dynasty = selectedDynasty.value
    if (selectedType.value) params.type = selectedType.value
    const data = await getProvinces(params)
    provinceData.value = Array.isArray(data) ? data : []
  } catch {
    provinceData.value = []
  }
}

function formatCount(count) {
  const n = Number(count)
  if (isNaN(n) || n == null || n < 0) return '暂未收录'
  return `${n} 座桥梁`
}

function normalizeCityName(name) {
  if (!name) return ''
  return name.replace(/(市|区|县|州|自治县|自治州|地区|盟)$/, '')
}

function buildChartOption(selectedProvince) {
  const mapData = provinceData.value.map(item => ({
    name: toGeoName(item.province),
    value: Number(item.count) || 0
  }))
  const maxValue = mapData.reduce((max, d) => Math.max(max, d.value || 0), 0)

  // City and district-level bridge counts for tooltip display
  const cityCountMap = {}
  const districtCountMap = {}
  bridges.value.forEach(b => {
    if (b.city) {
      const ckey = normalizeCityName(b.city)
      cityCountMap[ckey] = (cityCountMap[ckey] || 0) + 1
    }
    if (b.district) {
      const dkey = normalizeCityName(b.district)
      districtCountMap[dkey] = (districtCountMap[dkey] || 0) + 1
    }
  })

  const scatterData = []
  bridges.value.forEach(b => {
    const coords = parseCoords(b)
    if (coords) {
      scatterData.push({
        name: b.name_zh,
        value: [...coords, b.id],
        bridgeId: b.id,
        dynasty: b.dynasty,
        type: b.type,
        city: b.city
      })
    }
  })

  const mapName = mapReady.value ? (mapLevel.value === 'province' ? 'china-provinces' : 'china-full') : 'china'

  return {
    animationDurationUpdate: 1200,
    animationEasingUpdate: 'cubicInOut',
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        if (params.componentSubType === 'effectScatter' || params.componentSubType === 'scatter') {
          const d = params.data
          return `${params.name}<br/>${d.dynasty || ''} · ${d.type || ''}<br/>📍 ${d.city || ''}`
        }
        // Check province data first, then city counts
        const pv = params.value
        if (pv != null && !isNaN(pv)) {
          return `${params.name}<br/>${formatCount(pv)}`
        }
        const normalized = normalizeCityName(params.name)
        const cityCount = cityCountMap[params.name] || cityCountMap[normalized] || districtCountMap[params.name] || districtCountMap[normalized]
        if (cityCount != null) {
          return `${params.name}<br/>${formatCount(cityCount)}`
        }
        return `${params.name}<br/>暂未收录`
      }
    },
    visualMap: {
      min: 0,
      max: maxValue || 1,
      seriesIndex: 0,
      left: 'left',
      bottom: '5%',
      text: ['多', '少'],
      inRange: { color: ['#f5f0ea', '#d4a574', '#9C5A2C', '#6B4F3A', '#4a3020'] },
      calculable: false
    },
    geo: {
      map: mapName,
      roam: true,
      center: selectedProvince ? provinceCenters[selectedProvince] : undefined,
      zoom: selectedProvince ? 4 : 1,
      label: { show: false },
      itemStyle: {
        areaColor: '#f5f0ea',
        borderColor: '#d5c8b5',
        borderWidth: 1
      }
    },
    series: [
      {
        id: 'province-map',
        name: '桥梁数量',
        type: 'map',
        map: mapName,
        geoIndex: 0,
        data: mapData,
        itemStyle: {
          areaColor: 'transparent',
          borderColor: '#8A9A9A',
          borderWidth: 1
        },
        emphasis: {
          itemStyle: {
            areaColor: '#d4a574',
            borderWidth: 1.5
          }
        }
      },
      {
        id: 'bridge-markers',
        name: '桥梁位置',
        type: 'scatter',
        coordinateSystem: 'geo',
        geoIndex: 0,
        data: scatterData,
        symbolSize: 10,
        itemStyle: {
          color: '#9C5A2C',
          borderColor: '#fff',
          borderWidth: 2
        },
        emphasis: {
          scale: 2,
          itemStyle: { color: '#e74c3c' }
        }
      },
      {
        id: 'highlight-marker',
        name: '高亮桥梁',
        type: 'effectScatter',
        coordinateSystem: 'geo',
        geoIndex: 0,
        data: [],
        symbolSize: 16,
        rippleEffect: {
          brushType: 'stroke',
          scale: 4,
          period: 3
        },
        itemStyle: {
          color: '#e74c3c',
          borderColor: '#fff',
          borderWidth: 3
        },
        label: {
          show: false,
          position: 'right',
          fontSize: 14,
          fontWeight: 'bold',
          color: '#6B4F3A'
        }
      }
    ]
  }
}

function buildHighlightOption(targetBridge) {
  const mapData = provinceData.value.map(item => ({
    name: toGeoName(item.province),
    value: Number(item.count) || 0
  }))
  const maxValue = mapData.reduce((max, d) => Math.max(max, d.value || 0), 0)

  const coords = parseCoords(targetBridge)

  // City and district-level bridge counts for tooltip display
  const cityCountMap = {}
  const districtCountMap = {}
  bridges.value.forEach(b => {
    if (b.city) {
      const ckey = normalizeCityName(b.city)
      cityCountMap[ckey] = (cityCountMap[ckey] || 0) + 1
    }
    if (b.district) {
      const dkey = normalizeCityName(b.district)
      districtCountMap[dkey] = (districtCountMap[dkey] || 0) + 1
    }
  })

  const scatterData = bridges.value.map(b => {
    const c = parseCoords(b)
    return c ? {
      name: b.name_zh,
      value: [...c, b.id],
      bridgeId: b.id,
      dynasty: b.dynasty,
      type: b.type,
      city: b.city
    } : null
  }).filter(Boolean)

  const normalMarkers = scatterData.filter(d => d.bridgeId !== targetBridge.id)
  const highlightMarker = scatterData.filter(d => d.bridgeId === targetBridge.id)

  const mapName = mapReady.value ? (mapLevel.value === 'province' ? 'china-provinces' : 'china-full') : 'china'

  return {
    animationDurationUpdate: 1200,
    animationEasingUpdate: 'cubicInOut',
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        if (params.componentSubType === 'effectScatter') {
          const d = params.data || targetBridge
          return `<b>${d.name || targetBridge.name_zh}</b><br/>${d.dynasty || targetBridge.dynasty} · ${d.type || targetBridge.type}<br/>📍 ${d.city || targetBridge.city}`
        }
        if (params.componentSubType === 'scatter') {
          const d = params.data
          return `${params.name}<br/>${d.dynasty || ''} · ${d.type || ''}<br/>📍 ${d.city || ''}`
        }
        const pv = params.value
        if (pv != null && !isNaN(pv)) {
          return `${params.name}<br/>${formatCount(pv)}`
        }
        const normalized = normalizeCityName(params.name)
        const cityCount = cityCountMap[params.name] || cityCountMap[normalized] || districtCountMap[params.name] || districtCountMap[normalized]
        if (cityCount != null) {
          return `${params.name}<br/>${formatCount(cityCount)}`
        }
        return `${params.name}<br/>暂未收录`
      }
    },
    visualMap: {
      min: 0,
      max: maxValue || 1,
      seriesIndex: 0,
      left: 'left',
      bottom: '5%',
      text: ['多', '少'],
      inRange: { color: ['#f5f0ea', '#d4a574', '#9C5A2C', '#6B4F3A', '#4a3020'] },
      calculable: false
    },
    geo: {
      map: mapName,
      roam: true,
      center: coords || undefined,
      zoom: coords ? 6 : 1,
      label: { show: false },
      itemStyle: {
        areaColor: '#f5f0ea',
        borderColor: '#d5c8b5',
        borderWidth: 1
      }
    },
    series: [
      {
        id: 'province-map',
        name: '桥梁数量',
        type: 'map',
        map: mapName,
        geoIndex: 0,
        data: mapData,
        itemStyle: {
          areaColor: 'transparent',
          borderColor: '#8A9A9A',
          borderWidth: 1
        },
        emphasis: {
          itemStyle: {
            areaColor: '#d4a574',
            borderWidth: 1.5
          }
        }
      },
      {
        id: 'bridge-markers',
        name: '其他桥梁',
        type: 'scatter',
        coordinateSystem: 'geo',
        geoIndex: 0,
        data: normalMarkers,
        symbolSize: 8,
        itemStyle: {
          color: '#bbb',
          borderColor: '#fff',
          borderWidth: 1
        }
      },
      {
        id: 'highlight-marker',
        name: targetBridge.name_zh,
        type: 'effectScatter',
        coordinateSystem: 'geo',
        geoIndex: 0,
        data: highlightMarker,
        symbolSize: 16,
        rippleEffect: {
          brushType: 'stroke',
          scale: 4,
          period: 3
        },
        itemStyle: {
          color: '#e74c3c',
          borderColor: '#fff',
          borderWidth: 3
        },
        label: {
          show: true,
          formatter: targetBridge.name_zh,
          position: 'right',
          fontSize: 14,
          fontWeight: 'bold',
          color: '#6B4F3A'
        }
      }
    ]
  }
}

async function highlightCity(bridge) {
  highlightedBridge.value = bridge
  if (!chartInstance) return
  isProgrammaticUpdate = true
  chartInstance.setOption(buildHighlightOption(bridge), false)
  setTimeout(() => { isProgrammaticUpdate = false }, 300)
}

function clearHighlight() {
  highlightedBridge.value = null
  if (chartInstance) {
    chartInstance.setOption(buildChartOption(selectedProvince.value), false)
  }
}

async function resetView() {
  selectedProvince.value = ''
  highlightedBridge.value = null
  await Promise.all([fetchBridges(), fetchProvinceData()])
  renderChart()
}

async function onProvinceClick(params) {
  if (params.componentType !== 'series') return
  if (highlightedBridge.value) return

  const province = toBaseName(params.name)
  const pd = provinceData.value.find(p => p.province === province)
  if (!pd || Number(pd.count) <= 0) return
  if (selectedProvince.value === province) {
    selectedProvince.value = ''
  } else {
    selectedProvince.value = province
  }
  await fetchBridges()
  renderChart()
}

function renderChart() {
  if (!chartRef.value) return
  if (!chartInstance) {
    chartInstance = echarts.init(chartRef.value)
    chartInstance.on('click', onProvinceClick)
    chartInstance.on('georoam', () => {
      if (!isProgrammaticUpdate) hasUserZoomed.value = true
    })
  }
  highlightedBridge.value = null
  hasUserZoomed.value = false
  isProgrammaticUpdate = true
  chartInstance.setOption(buildChartOption(selectedProvince.value), true)
  setTimeout(() => { isProgrammaticUpdate = false }, 300)
}

async function onFilterChange() {
  selectedProvince.value = ''
  highlightedBridge.value = null
  await Promise.all([fetchBridges(), fetchProvinceData()])
  renderChart()
}

function goBack() {
  selectedProvince.value = ''
  highlightedBridge.value = null
  onFilterChange()
}

function goDetail(item) {
  detailBridge.value = item
  showDetail.value = true
}

const handleResize = () => { chartInstance?.resize() }

onMounted(async () => {
  await Promise.all([fetchBridges(), fetchProvinceData(), loadFullMap()])
  renderChart()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  chartInstance?.dispose()
  chartInstance = null
})
</script>

<style scoped>
.map-page {
  padding: 24px;
  background: linear-gradient(160deg, #f5f0ea 0%, #f0ebe3 30%, #f7f3ed 60%, #faf7f2 100%);
  min-height: calc(100vh - 64px);
  font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
}
.filters {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
  align-items: center;
}
.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255,255,255,0.9);
  backdrop-filter: blur(6px);
  padding: 8px 16px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.04);
  border: 1px solid rgba(0,0,0,0.05);
  transition: box-shadow 0.25s ease;
}
.filter-item:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}
.filter-item span { font-size: 14px; color: #555; }
.filter-item select { border: none; outline: none; font-size: 14px; background: transparent; }
.level-selector {
  padding: 4px;
  gap: 0;
}
.level-selector button {
  padding: 7px 14px;
  border: 1px solid #e8e0d5;
  background: #fff;
  color: #666;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.3s ease;
}
.level-selector button:hover:not(.active) {
  color: #9C5A2C;
  background: rgba(156,92,44,0.04);
}
.level-selector button:first-child {
  border-radius: 6px 0 0 6px;
}
.level-selector button:last-child {
  border-radius: 0 6px 6px 0;
}
.level-selector button.active {
  background: #6B4F3A;
  color: #fff;
  border-color: #9C5A2C;
}
.back-btn {
  padding: 8px 16px;
  border: 1px solid #6B4F3A;
  background: #fff;
  color: #6B4F3A;
  border-radius: 10px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.25s ease;
}
.back-btn:hover {
  background: #6B4F3A;
  color: #fff;
}
.reset-view-btn {
  padding: 8px 16px;
  border: 1px solid #8A9A9A;
  background: #fff;
  color: #8A9A9A;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}
.reset-view-btn:hover {
  background: #8A9A9A;
  color: #fff;
}
.main { display: flex; gap: 20px; }
.map-card, .list-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.05);
  padding: 20px;
  transition: box-shadow 0.3s ease;
}
.map-card:hover, .list-card:hover {
  box-shadow: 0 8px 32px rgba(0,0,0,0.08);
}
.map-card { flex: 7; }
.map-container { width: 100%; height: 580px; }
.list-card { flex: 3; max-height: 612px; display: flex; flex-direction: column; }
.card-title { font-size: 16px; font-weight: 600; margin-bottom: 12px; }
.list-card ul { padding: 0; margin: 0; list-style: none; overflow-y: auto; }
.list-card li {
  display: flex; justify-content: space-between; align-items: center;
  padding: 12px 10px; border-bottom: 1px solid #f0ebe3;
  border-radius: 8px;
  transition: all 0.25s ease;
}
.list-card li:hover {
  background: rgba(107,79,58,0.03);
}
.list-card li.highlighted {
  background: linear-gradient(135deg, rgba(156,92,44,0.08), rgba(107,79,58,0.06));
  margin: 0 -6px;
  padding-left: 10px;
  padding-right: 10px;
  border-radius: 10px;
  border-left: 3px solid #9C5A2C;
}
.bridge-info { display: flex; flex-direction: column; }
.name-row { display: flex; align-items: center; gap: 8px; }
.name { font-weight: 500; color: #222; }
.badge-3d {
  font-size: 10px;
  background: linear-gradient(135deg, #9C5A2C, #6B4F3A);
  color: #fff;
  padding: 3px 8px;
  border-radius: 8px;
  cursor: pointer;
}
.meta { font-size: 12px; color: #888; }
.location { font-size: 12px; color: #aaa; }
button {
  padding: 6px 12px; border: none;
  background: linear-gradient(135deg, #8A9A9A, #a0aaaa);
  color: #fff; border-radius: 8px; cursor: pointer; font-size: 12px;
  transition: all 0.2s ease;
}
button:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.12);
}
.empty { text-align: center; margin-top: 20px; color: #999; }
.modal {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center;
  z-index: 200;
}
.modal-content {
  width: 500px; background: #fff; border-radius: 18px; padding: 28px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}
.modal-content h2 { margin: 0 0 8px; }
.fields { margin: 16px 0; }
.field { font-size: 14px; color: #555; margin-bottom: 4px; }
.modal-actions { display: flex; gap: 12px; margin-top: 16px; }
.modal-actions button { padding: 8px 20px; border-radius: 10px; transition: all 0.2s ease; }
.modal-actions button:hover { transform: translateY(-1px); }
</style>
