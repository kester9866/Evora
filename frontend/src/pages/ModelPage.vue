<template>
  <div class="model-page">
    <button class="back-btn" @click="$router.push('/map')">← 返回地图</button>

    <div class="model-layout">
      <div class="viewer" ref="viewerRef">
        <div v-if="loading" class="spinner">加载模型中...</div>
        <div v-else-if="error" class="error-state">
          <p>{{ error }}</p>
          <button @click="$router.push('/map')">返回地图</button>
        </div>
        <div v-if="!loading && !error" class="viewer-hints">
          <span>🖱 左键拖拽旋转</span>
          <span>🔍 滚轮缩放</span>
          <span>✋ 右键拖拽平移</span>
        </div>
      </div>

      <aside class="info-sidebar" v-if="bridge">
        <h2>{{ bridge.name_zh }}</h2>
        <div class="field" v-if="bridge.name_en">{{ bridge.name_en }}</div>
        <div class="field" v-if="bridge.dynasty">{{ bridge.dynasty }}</div>
        <div class="field" v-if="bridge.type">{{ bridge.type }}</div>
        <div class="field" v-if="bridge.material">{{ bridge.material }}</div>
        <div class="field" v-if="bridge.province">{{ bridge.province }}{{ bridge.city ? ' · ' + bridge.city : '' }}</div>
        <div class="field" v-if="bridge.year_built">建造年份：{{ bridge.year_built }}</div>
        <div class="field" v-if="bridge.length_m">长度：{{ bridge.length_m }}m</div>
        <div class="field" v-if="bridge.width_m">宽度：{{ bridge.width_m }}m</div>
        <div class="field" v-if="bridge.span_m">跨度：{{ bridge.span_m }}m</div>
        <div class="field desc" v-if="bridge.description">{{ bridge.description }}</div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import { getBridge } from '../api/bridges.js'
import { resolveAssetUrl } from '../utils/asset'

const route = useRoute()
const viewerRef = ref(null)
const bridge = ref(null)
const loading = ref(true)
const error = ref('')

let renderer, scene, camera, controls, animationId

onMounted(async () => {
  try {
    bridge.value = await getBridge(route.params.id)
  } catch {
    bridge.value = null
    error.value = '无法加载桥梁数据'
    loading.value = false
    return
  }

  if (!bridge.value.model_url) {
    error.value = '该桥梁暂无3D模型'
    loading.value = false
    return
  }

  try {
    const THREE = await import('three')
    const { OrbitControls } = await import('three/examples/jsm/controls/OrbitControls.js')
    const { GLTFLoader } = await import('three/examples/jsm/loaders/GLTFLoader.js')

    const container = viewerRef.value
    if (!container) return

    scene = new THREE.Scene()
    scene.background = new THREE.Color(0xf5f0ea)

    camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.01, 10000)
    camera.position.set(5, 3, 5)

    renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setSize(container.clientWidth, container.clientHeight)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    container.appendChild(renderer.domElement)

    controls = new OrbitControls(camera, renderer.domElement)
    controls.enableDamping = true
    controls.dampingFactor = 0.1

    scene.add(new THREE.AmbientLight(0xffffff, 0.6))
    const dirLight = new THREE.DirectionalLight(0xffffff, 0.8)
    dirLight.position.set(5, 10, 5)
    scene.add(dirLight)

    const loader = new GLTFLoader()
    loader.load(
      resolveAssetUrl(bridge.value.model_url),
      (gltf) => {
        scene.add(gltf.scene)

        // Auto-fit camera to model bounding box
        const box = new THREE.Box3().setFromObject(gltf.scene)
        const center = new THREE.Vector3()
        const size = new THREE.Vector3()
        box.getCenter(center)
        box.getSize(size)

        const maxDim = Math.max(size.x, size.y, size.z)
        const dist = maxDim * 1.8

        camera.position.set(center.x + dist * 0.6, center.y + dist * 0.5, center.z + dist)
        controls.target.copy(center)
        controls.update()

        loading.value = false
      },
      undefined,
      () => {
        error.value = '模型加载失败'
        loading.value = false
      }
    )

    function animate() {
      animationId = requestAnimationFrame(animate)
      controls.update()
      renderer.render(scene, camera)
    }
    animate()

    window.addEventListener('resize', onResize)
  } catch {
    error.value = '3D引擎初始化失败'
    loading.value = false
  }
})

function onResize() {
  if (!renderer || !viewerRef.value) return
  const w = viewerRef.value.clientWidth
  const h = viewerRef.value.clientHeight
  camera.aspect = w / h
  camera.updateProjectionMatrix()
  renderer.setSize(w, h)
}

onBeforeUnmount(() => {
  if (animationId) cancelAnimationFrame(animationId)
  if (renderer) renderer.dispose()
  window.removeEventListener('resize', onResize)
})
</script>

<style scoped>
.model-page {
  min-height: calc(100vh - 64px);
  padding: 24px;
}
.back-btn {
  padding: 8px 16px;
  border: 1px solid #6B4F3A;
  background: #fff;
  color: #6B4F3A;
  border-radius: 10px;
  transition: all 0.25s ease;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  margin-bottom: 16px;
}
.model-layout {
  display: flex;
  gap: 24px;
  height: calc(100vh - 160px);
}
.viewer {
  flex: 1;
  border-radius: 12px;
  overflow: hidden;
  position: relative;
  background: #f5f0ea;
}
.spinner {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  font-size: 16px;
  color: #9C5A2C;
}
.error-state {
  position: absolute;
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}
.error-state p { margin-bottom: 12px; color: #666; }
.viewer-hints {
  position: absolute;
  bottom: 16px; left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 20px;
  background: rgba(0,0,0,0.45);
  color: #fff;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 12px;
  pointer-events: none;
  backdrop-filter: blur(4px);
  animation: hint-fade 6s ease-in-out forwards;
}
@keyframes hint-fade {
  0%, 70% { opacity: 1; }
  100% { opacity: 0.15; }
}
.info-sidebar {
  width: 300px;
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  overflow-y: auto;
  box-shadow: 0 4px 16px rgba(0,0,0,0.06);
}
.info-sidebar h2 { margin: 0 0 16px; font-size: 18px; }
.field {
  font-size: 14px;
  color: #555;
  margin-bottom: 6px;
}
.desc {
  margin-top: 12px;
  color: #333;
  line-height: 1.6;
}
</style>
