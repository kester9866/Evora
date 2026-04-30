<template>
  <div class="game-page">
    <div class="game-layout">
      <div class="hints-panel">
        <h3>榫卯拼接</h3>
        <p class="hint-desc">将<span class="hl">榫头</span>（赭色方块）嵌入<span class="hl">卯口</span>（木棕框架）中</p>

        <div class="control-group">
          <h4>移动</h4>
          <div class="key-row"><kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd> <span>水平移动</span></div>
          <div class="key-row"><kbd>Q</kbd><kbd>E</kbd> <span>上下升降</span></div>
        </div>

        <div class="control-group">
          <h4>旋转</h4>
          <div class="key-row"><kbd>←</kbd><kbd>→</kbd> <span>水平旋转</span></div>
          <div class="key-row"><kbd>↑</kbd><kbd>↓</kbd> <span>前后倾斜</span></div>
        </div>

        <div class="control-group">
          <h4>视角</h4>
          <div class="key-row"><span>🖱 拖拽</span> <span>旋转视角</span></div>
          <div class="key-row"><span>🖱 滚轮</span> <span>缩放距离</span></div>
        </div>

        <div class="action-row">
          <button class="reset-btn" @click="resetTenon">↺ 复位</button>
          <button class="hint-btn" @click="showHint">💡 提示</button>
        </div>
      </div>

      <div ref="containerRef" class="viewer"></div>
    </div>

    <div v-if="showPopup" class="completion-popup" @click.self="showPopup = false">
      <div class="popup-content">
        <h3>拼合成功</h3>
        <p>{{ knowledgeText }}</p>
        <button class="close-btn" @click="showPopup = false">关闭</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js'

const containerRef = ref(null)
const showPopup = ref(false)
const knowledgeText = ref('')

let tenonMesh, mortiseGroup, scene, camera, renderer, controls
let keys = {}
let snapTarget = null
let isSnapped = false

// Mortise slot dimensions
const SLOT_W = 1.0   // inner width
const SLOT_D = 0.6   // inner depth
const SLOT_H = 0.5   // inner height
const WALL_T = 0.15  // wall thickness
const SNAP_DIST = 0.25
const SNAP_ANGLE = 25 * Math.PI / 180

// The tenon piece is slightly smaller than the slot for a snug fit
const TENON_W = SLOT_W - 0.06
const TENON_D = SLOT_D - 0.06
const TENON_H = SLOT_H

function createMortise() {
  const group = new THREE.Group()
  const matBase = new THREE.MeshStandardMaterial({ color: 0x6B4F3A, roughness: 0.6 })
  const matWall = new THREE.MeshStandardMaterial({ color: 0x5a3d28, roughness: 0.55 })

  // Base plate
  const baseW = SLOT_W + WALL_T * 2 + 0.4
  const baseD = SLOT_D + WALL_T * 2 + 0.4
  const baseH = 0.1
  const base = new THREE.Mesh(new THREE.BoxGeometry(baseW, baseH, baseD), matBase)
  base.position.y = -baseH / 2
  group.add(base)

  // Four walls forming the slot
  const walls = [
    { w: WALL_T, d: SLOT_D, x: -(SLOT_W / 2 + WALL_T / 2), z: 0 },           // left
    { w: WALL_T, d: SLOT_D, x: (SLOT_W / 2 + WALL_T / 2), z: 0 },            // right
    { w: SLOT_W + WALL_T * 2, d: WALL_T, x: 0, z: -(SLOT_D / 2 + WALL_T / 2) }, // front
    { w: SLOT_W + WALL_T * 2, d: WALL_T, x: 0, z: (SLOT_D / 2 + WALL_T / 2) },  // back
  ]
  walls.forEach(({ w, d, x, z }) => {
    const wall = new THREE.Mesh(new THREE.BoxGeometry(w, SLOT_H, d), matWall)
    wall.position.set(x, SLOT_H / 2, z)
    group.add(wall)
  })

  // Ghost guide — semi-transparent tenon at target position
  const ghostMat = new THREE.MeshStandardMaterial({ color: 0xffd700, roughness: 0.3, transparent: true, opacity: 0.25 })
  const ghostGeo = new THREE.BoxGeometry(TENON_W, TENON_H, TENON_D)
  const ghost = new THREE.Mesh(ghostGeo, ghostMat)
  ghost.position.set(0, TENON_H / 2, 0)
  ghost.name = 'ghost'
  group.add(ghost)

  // Wireframe outline for ghost
  const edges = new THREE.EdgesGeometry(ghostGeo)
  const wire = new THREE.LineSegments(edges, new THREE.LineBasicMaterial({ color: 0xffd700, transparent: true, opacity: 0.35 }))
  wire.position.copy(ghost.position)
  wire.name = 'ghostWire'
  group.add(wire)

  // Snap target: tenon center sits at y = TENON_H/2 (bottom flush with base plate top)
  snapTarget = new THREE.Vector3(0, TENON_H / 2, 0)

  return group
}

function createTenon() {
  const mat = new THREE.MeshStandardMaterial({ color: 0x9C5A2C, roughness: 0.5 })
  const mesh = new THREE.Mesh(new THREE.BoxGeometry(TENON_W, TENON_H, TENON_D), mat)
  mesh.position.set(1.5, 1.2, 0)
  mesh.rotation.set(0.3, 0.5, 0.1)
  mesh.castShadow = true
  return mesh
}

function normAngle(a) {
  let v = a % (Math.PI * 2)
  if (v > Math.PI) v -= Math.PI * 2
  if (v < -Math.PI) v += Math.PI * 2
  return v
}

function checkSnap() {
  if (isSnapped || !snapTarget) return

  const tp = tenonMesh.position
  const dist = tp.distanceTo(snapTarget)

  const rx = Math.abs(normAngle(tenonMesh.rotation.x))
  const ry = Math.abs(normAngle(tenonMesh.rotation.y))
  const rz = Math.abs(normAngle(tenonMesh.rotation.z))
  const rotOk = rx < SNAP_ANGLE && ry < SNAP_ANGLE && rz < SNAP_ANGLE

  // Update ghost opacity based on proximity
  const ghost = mortiseGroup.getObjectByName('ghost')
  const ghostWire = mortiseGroup.getObjectByName('ghostWire')
  if (ghost && ghostWire) {
    const closeness = Math.max(0, 1 - dist / 1.5)
    const angleOK = rotOk ? 1 : 0.3
    const alpha = 0.15 + closeness * 0.5 * angleOK
    ghost.material.opacity = alpha
    ghostWire.material.opacity = alpha + 0.15
  }

  if (dist < SNAP_DIST && rotOk) {
    isSnapped = true
    // Hide ghost
    if (ghost) ghost.visible = false
    if (ghostWire) ghostWire.visible = false

    const startPos = tenonMesh.position.clone()
    const startRot = tenonMesh.rotation.clone()
    const startTime = Date.now()

    function animateSnap() {
      const elapsed = Date.now() - startTime
      const t = Math.min(elapsed / 300, 1)
      const ease = 1 - Math.pow(1 - t, 3)
      tenonMesh.position.lerpVectors(startPos, snapTarget, ease)
      tenonMesh.rotation.x = startRot.x + (0 - startRot.x) * ease
      tenonMesh.rotation.y = startRot.y + (0 - startRot.y) * ease
      tenonMesh.rotation.z = startRot.z + (0 - startRot.z) * ease
      if (t < 1) {
        requestAnimationFrame(animateSnap)
      } else {
        knowledgeText.value = '榫卯节点的精准咬合，使木构件在无钉无铁的条件下实现牢固连接。榫头各面与卯口紧密贴合，竖向荷载通过榫头传递给卯口侧壁，形成稳定的摩擦自锁结构，体现了中国古代匠人的卓越技艺。'
        showPopup.value = true
      }
    }
    animateSnap()
  }
}

function resetTenon() {
  isSnapped = false
  tenonMesh.position.set(1.5, 1.2, 0)
  tenonMesh.rotation.set(0.3, 0.5, 0.1)
}

function showHint() {
  const ghost = mortiseGroup.getObjectByName('ghost')
  const ghostWire = mortiseGroup.getObjectByName('ghostWire')
  if (!ghost) return

  // Flash the ghost to full opacity briefly
  const orig = ghost.material.opacity
  const origWire = ghostWire ? ghostWire.material.opacity : 0.35
  ghost.material.opacity = 0.7
  if (ghostWire) ghostWire.material.opacity = 0.7

  // Also highlight the snap target with a pulsing ring
  const ringGeo = new THREE.TorusGeometry(0.45, 0.03, 8, 32)
  const ring = new THREE.Mesh(ringGeo, new THREE.MeshBasicMaterial({ color: 0xffd700 }))
  ring.position.copy(snapTarget)
  ring.rotation.x = -Math.PI / 2
  scene.add(ring)

  const startTime = Date.now()
  function pulseRing() {
    const elapsed = Date.now() - startTime
    if (elapsed > 1500) {
      scene.remove(ring); ringGeo.dispose(); ring.material.dispose()
      return
    }
    const s = 1 + Math.sin(elapsed * 0.01) * 0.3
    ring.scale.setScalar(s)
    ring.material.opacity = 1 - elapsed / 1500
    requestAnimationFrame(pulseRing)
  }
  pulseRing()

  setTimeout(() => {
    ghost.material.opacity = orig
    if (ghostWire) ghostWire.material.opacity = origWire
  }, 1500)
}

onMounted(() => {
  const container = containerRef.value
  const w = container.clientWidth
  const h = container.clientHeight

  // Scene
  scene = new THREE.Scene()
  scene.background = new THREE.Color(0xf5f0ea)
  scene.fog = new THREE.Fog(0xf5f0ea, 6, 20)

  // Camera
  camera = new THREE.PerspectiveCamera(50, w / h, 0.1, 50)
  camera.position.set(3.5, 3.0, 4.5)
  camera.lookAt(0, 0.6, 0)

  // Renderer
  renderer = new THREE.WebGLRenderer({ antialias: true })
  renderer.setSize(w, h)
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  renderer.shadowMap.enabled = true
  container.appendChild(renderer.domElement)

  // Lights
  scene.add(new THREE.AmbientLight(0xffffff, 0.6))
  const dirLight = new THREE.DirectionalLight(0xffffff, 0.9)
  dirLight.position.set(5, 10, 5)
  dirLight.castShadow = true
  dirLight.shadow.mapSize.set(512, 512)
  scene.add(dirLight)
  scene.add(new THREE.HemisphereLight(0xddeeff, 0x8899aa, 0.3))

  // Ground
  const groundGeo = new THREE.PlaneGeometry(8, 8)
  const groundMat = new THREE.MeshStandardMaterial({ color: 0xe8dcc8, roughness: 0.8 })
  const ground = new THREE.Mesh(groundGeo, groundMat)
  ground.rotation.x = -Math.PI / 2
  ground.position.y = -0.5
  ground.receiveShadow = true
  scene.add(ground)

  // Grid helper for spatial reference
  const grid = new THREE.GridHelper(8, 16, 0xcccccc, 0xe0d5c5)
  grid.position.y = -0.49
  scene.add(grid)

  // Mortise (fixed)
  mortiseGroup = createMortise()
  mortiseGroup.receiveShadow = true
  scene.add(mortiseGroup)

  // Tenon (movable)
  tenonMesh = createTenon()
  scene.add(tenonMesh)

  // OrbitControls
  controls = new OrbitControls(camera, renderer.domElement)
  controls.target.set(0, 0.6, 0)
  controls.enableDamping = true
  controls.dampingFactor = 0.1
  controls.minDistance = 2
  controls.maxDistance = 10
  controls.maxPolarAngle = Math.PI / 2 + 0.3
  controls.update()

  // Keyboard
  window.addEventListener('keydown', onKeyDown)
  window.addEventListener('keyup', onKeyUp)

  // Resize
  window.addEventListener('resize', onResize)

  // Animation loop
  function animate() {
    requestAnimationFrame(animate)

    if (!isSnapped) {
      handleMovement()
      checkSnap()
    }

    controls.update()
    renderer.render(scene, camera)
  }
  animate()
})

const MOVE_SPEED = 0.04
const ROT_SPEED = 0.04

function onKeyDown(e) { keys[e.key.toLowerCase()] = true }
function onKeyUp(e) { keys[e.key.toLowerCase()] = false }

function handleMovement() {
  const p = tenonMesh.position
  const r = tenonMesh.rotation

  // Translation — WASD + QE
  if (keys['w']) { p.z -= MOVE_SPEED }
  if (keys['s']) { p.z += MOVE_SPEED }
  if (keys['a']) { p.x -= MOVE_SPEED }
  if (keys['d']) { p.x += MOVE_SPEED }
  if (keys['q']) { p.y += MOVE_SPEED }
  if (keys['e']) { p.y -= MOVE_SPEED }

  // Rotation — Arrow keys
  if (keys['arrowleft'])  { r.y -= ROT_SPEED }
  if (keys['arrowright']) { r.y += ROT_SPEED }
  if (keys['arrowup'])    { r.x -= ROT_SPEED }
  if (keys['arrowdown'])  { r.x += ROT_SPEED }

  // Clamp position
  p.x = Math.max(-3, Math.min(3, p.x))
  p.y = Math.max(0.1, Math.min(4, p.y))
  p.z = Math.max(-3, Math.min(3, p.z))
}

function onResize() {
  if (!containerRef.value || !renderer) return
  const w = containerRef.value.clientWidth
  const h = containerRef.value.clientHeight
  camera.aspect = w / h
  camera.updateProjectionMatrix()
  renderer.setSize(w, h)
}

onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKeyDown)
  window.removeEventListener('keyup', onKeyUp)
  window.removeEventListener('resize', onResize)
  if (renderer) {
    renderer.dispose()
    renderer.domElement.remove()
  }
})
</script>

<style scoped>
.game-page {
  height: calc(100vh - 64px);
  display: flex;
  flex-direction: column;
  font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
  overflow: hidden;
}

.game-layout {
  flex: 1;
  display: flex;
  gap: 0;
}

/* ===== Hints panel ===== */
.hints-panel {
  width: 240px;
  padding: 24px 20px;
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(10px);
  border-right: 1px solid rgba(156,92,44,0.08);
  display: flex;
  flex-direction: column;
  gap: 18px;
  z-index: 10;
  flex-shrink: 0;
}
.hints-panel h3 {
  margin: 0;
  font-size: 18px;
  color: #3d3020;
  font-weight: 700;
}
.hint-desc {
  margin: 0;
  font-size: 13px;
  color: #5a4a3a;
  line-height: 1.7;
}
.hint-desc .hl {
  color: #9C5A2C;
  font-weight: 600;
}

.control-group h4 {
  margin: 0 0 6px;
  font-size: 11px;
  color: #A09080;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
.key-row {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 4px;
  font-size: 12px;
  color: #5a4a3a;
}
.key-row span:last-child {
  margin-left: 6px;
  color: #8A7A6A;
}
kbd {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 22px;
  height: 20px;
  padding: 0 5px;
  background: #fff;
  border: 1px solid #d5c8b5;
  border-radius: 4px;
  font-size: 10px;
  font-family: inherit;
  color: #5a4a3a;
  box-shadow: 0 1px 0 rgba(0,0,0,0.06);
}

.action-row {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.reset-btn, .hint-btn {
  padding: 8px 0;
  border: 1px solid rgba(156,92,44,0.15);
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-family: inherit;
  transition: all 0.2s ease;
}
.reset-btn {
  background: rgba(255,255,255,0.8);
  color: #6B4F3A;
}
.reset-btn:hover { background: rgba(107,79,58,0.06); border-color: #9C5A2C; }
.hint-btn {
  background: linear-gradient(135deg, rgba(156,92,44,0.08), rgba(107,79,58,0.04));
  color: #6B4F3A;
}
.hint-btn:hover { background: linear-gradient(135deg, rgba(156,92,44,0.16), rgba(107,79,58,0.08)); border-color: #9C5A2C; }

/* ===== 3D viewer ===== */
.viewer {
  flex: 1;
  min-width: 0;
  position: relative;
}

/* ===== Completion popup ===== */
.completion-popup {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex; align-items: center; justify-content: center;
  z-index: 200;
}
.popup-content {
  background: #fff;
  border-radius: 16px;
  padding: 32px;
  max-width: 420px;
  text-align: center;
}
.popup-content h3 { margin: 0 0 12px; font-size: 20px; color: #3d3020; }
.popup-content p { font-size: 14px; color: #555; line-height: 1.7; }
.close-btn {
  margin-top: 16px;
  padding: 10px 28px;
  background: #6B4F3A;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-family: inherit;
  transition: all 0.25s ease;
}
.close-btn:hover {
  background: #7d5e4a;
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .game-layout { flex-direction: column-reverse; }
  .hints-panel {
    width: 100%;
    padding: 12px 16px;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 8px;
    align-items: flex-start;
  }
  .hints-panel h3 { font-size: 15px; }
  .hints-panel h4 { margin: 0; }
  .control-group { flex: 1; min-width: 120px; }
  .key-row { font-size: 11px; }
  .action-row { flex-direction: row; margin-top: 0; width: 100%; }
  .action-row button { flex: 1; }
  .hint-desc { display: none; }
}
</style>
