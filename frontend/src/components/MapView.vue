<template>
  <div class="map-page">
    <div class="header">
      <h1>中国古桥结构与分布可视化</h1>
      <p>从空间分布到结构智慧的演化探索</p>
    </div>

    <div class="filters">
      <div class="filter-item">
        <span>朝代</span>
        <select v-model="selectedDynasty">
          <option value="全部">全部</option>
          <option value="隋">隋</option>
          <option value="唐">唐</option>
          <option value="宋">宋</option>
          <option value="元">元</option>
          <option value="明">明</option>
          <option value="清">清</option>
        </select>
      </div>

      <div class="filter-item">
        <span>类型</span>
        <select v-model="selectedType">
          <option value="全部">全部</option>
          <option value="梁桥">梁桥</option>
          <option value="拱桥">拱桥</option>
          <option value="木桥">木桥</option>
        </select>
      </div>
    </div>

    <div class="main">
      <div class="map-card">
        <div class="card-title">桥梁空间分布</div>
        <div ref="chartRef" class="map-container"></div>
      </div>

      <div class="list-card">
        <div class="card-title">
          {{ listTitle }}（{{ displayBridges.length }}）
        </div>

        <ul>
          <li v-for="item in displayBridges" :key="item.name">
            <div class="bridge-info">
              <span class="name">{{ item.name }}</span>
              <span class="meta">{{ item.dynasty }} · {{ item.type }}</span>
              <span class="location">{{ item.province }}-{{ item.city }}</span>
            </div>

            <button @click="goDetail(item)">结构分析</button>
          </li>
        </ul>

        <div v-if="displayBridges.length === 0" class="empty">
          暂无数据
        </div>
      </div>
    </div>

    <div v-if="showDetail" class="modal">
      <div class="modal-content">
        <h2>{{ currentBridge.name }}</h2>
        <p>{{ currentBridge.dynasty }} · {{ currentBridge.type }}</p>

        <div class="structure-box">
          <p v-if="currentBridge.type === '拱桥'">
            拱桥通过将受力从桥面传递至两侧桥墩，实现稳定结构。
          </p>

          <p v-else-if="currentBridge.type === '梁桥'">
            梁桥主要通过水平梁承受荷载，结构简单但跨度有限。
          </p>

          <p v-else>
            木桥依靠榫卯结构连接，体现传统建筑智慧。
          </p>
        </div>

        <button @click="showDetail = false">关闭</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, computed } from "vue";
import * as echarts from "echarts";
import chinaJson from "../data/china.json";
import bridgeData from "../data/bridgeData.json";

echarts.registerMap("china", chinaJson);

const chartRef = ref(null);
let chartInstance = null;

const selectedDynasty = ref("全部");
const selectedType = ref("全部");
const selectedProvince = ref("");
const showDetail = ref(false);
const currentBridge = ref(null);

const provinceNameMap = {
  北京: "北京市",
  天津: "天津市",
  上海: "上海市",
  重庆: "重庆市",
  内蒙古: "内蒙古自治区",
  广西: "广西壮族自治区",
  宁夏: "宁夏回族自治区",
  新疆: "新疆维吾尔自治区",
  西藏: "西藏自治区",
  香港: "香港特别行政区",
  澳门: "澳门特别行政区",
  台湾: "台湾省"
};

const geoToBaseMap = Object.fromEntries(
  Object.entries(provinceNameMap).map(([base, geo]) => [geo, base])
);

const toGeoName = (baseName) => {
  if (provinceNameMap[baseName]) return provinceNameMap[baseName];
  if (baseName.endsWith("省") || baseName.endsWith("市")) return baseName;
  return `${baseName}省`;
};

const toBaseName = (geoName) => {
  if (geoToBaseMap[geoName]) return geoToBaseMap[geoName];
  if (geoName.endsWith("省")) return geoName.replace(/省$/, "");
  if (geoName.endsWith("市")) return geoName.replace(/市$/, "");
  return geoName;
};

const filteredBridges = computed(() => {
  return bridgeData.filter((item) => {
    const dynastyMatch =
      selectedDynasty.value === "全部" || item.dynasty === selectedDynasty.value;
    const typeMatch =
      selectedType.value === "全部" || item.type === selectedType.value;
    return dynastyMatch && typeMatch;
  });
});

const displayBridges = computed(() => {
  if (!selectedProvince.value) return filteredBridges.value;
  return filteredBridges.value.filter(
    (item) => item.province === selectedProvince.value
  );
});

const listTitle = computed(() => {
  return selectedProvince.value
    ? `桥梁列表（${selectedProvince.value}）`
    : "桥梁列表（全部）";
});

const goDetail = (item) => {
  currentBridge.value = item;
  showDetail.value = true;
};

const getProvinceStats = (data) => {
  const provinceCount = data.reduce((acc, item) => {
    const key = item.province;
    acc[key] = (acc[key] || 0) + 1;
    return acc;
  }, {});

  const mapData = Object.entries(provinceCount).map(([name, value]) => ({
    name: toGeoName(name),
    value
  }));

  const maxValue = mapData.reduce((max, item) => Math.max(max, item.value), 0);

  return { mapData, maxValue };
};

const initChart = () => {
  if (!chartRef.value) return;
  if (!chartInstance) {
    chartInstance = echarts.init(chartRef.value);

    chartInstance.on("click", (params) => {
      if (params.componentType !== "series") return;
      const province = toBaseName(params.name);
      selectedProvince.value = province;
      const list = filteredBridges.value
        .filter((item) => item.province === province)
        .map((item) => `${item.name} ${item.dynasty} ${item.type}`);
      console.log(`[${province}]`, list);
    });
  }

  updateChart();
};

const updateChart = () => {
  if (!chartInstance) return;
  const { mapData, maxValue } = getProvinceStats(filteredBridges.value);

  const option = {
    tooltip: {
      trigger: "item",
      formatter: (params) => {
        const value = params.value ?? 0;
        return `${params.name}<br/>桥梁数量：${value}`;
      }
    },
    visualMap: {
      min: 0,
      max: maxValue || 1,
      left: "left",
      bottom: "5%",
      text: ["多", "少"],
      inRange: {
        color: ["#f5f0ea", "#d4a574", "#9C5A2C", "#4a3020"]
      },
      calculable: false
    },
    series: [
      {
        name: "桥梁数量",
        type: "map",
        map: "china",
        roam: true,
        label: {
          show: false
        },
        data: mapData
      }
    ]
  };

  chartInstance.setOption(option, true);
};

const handleResize = () => {
  if (chartInstance) chartInstance.resize();
};

watch([selectedDynasty, selectedType], () => {
  selectedProvince.value = "";
  updateChart();
});

onMounted(() => {
  initChart();
  window.addEventListener("resize", handleResize);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", handleResize);
  if (chartInstance) {
    chartInstance.dispose();
    chartInstance = null;
  }
});
</script>

<style scoped>
.map-page {
  padding: 24px;
  background: linear-gradient(135deg, #f0f4ff, #f7faff);
  min-height: 100vh;
  font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
}

.header {
  margin-bottom: 20px;
}

.header h1 {
  font-size: 26px;
  font-weight: 600;
  margin-bottom: 6px;
  color: #1f2d3d;
}

.header p {
  color: #6b7280;
  font-size: 14px;
}

.filters {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #ffffff;
  padding: 10px 14px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.filter-item span {
  font-size: 14px;
  color: #555;
}

.filter-item select {
  border: none;
  outline: none;
  font-size: 14px;
  background: transparent;
}

.main {
  display: flex;
  gap: 20px;
}

.map-card,
.list-card {
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
  padding: 16px;
}

.map-card {
  flex: 7;
}

.map-container {
  width: 100%;
  height: 580px;
}

.list-card {
  flex: 3;
  display: flex;
  flex-direction: column;
  height: 612px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
}

.list-card ul {
  padding: 0;
  margin: 0;
  list-style: none;
  overflow-y: auto;
}

.list-card li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.bridge-info {
  display: flex;
  flex-direction: column;
}

.name {
  font-weight: 500;
  color: #222;
}

.meta {
  font-size: 12px;
  color: #888;
}

.location {
  font-size: 12px;
  color: #aaa;
}

button {
  padding: 4px 10px;
  border: none;
  background: linear-gradient(135deg, #8A9A9A, #a0aaaa);
  color: white;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
}

button:hover {
  opacity: 0.85;
}

.empty {
  text-align: center;
  margin-top: 20px;
  color: #999;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  width: 500px;
  background: #fff;
  border-radius: 12px;
  padding: 20px;
}

.structure-box {
  margin: 20px 0;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
}
</style>
