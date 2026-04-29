<template>
  <div class="admin-page">
    <div class="tabs">
      <button :class="{ active: tab === 'bridges' }" @click="tab = 'bridges'">桥梁管理</button>
      <button :class="{ active: tab === 'products' }" @click="tab = 'products'">商品管理</button>
      <button :class="{ active: tab === 'chunks' }" @click="tab = 'chunks'">知识片段</button>
    </div>

    <!-- Bridges Tab -->
    <div v-if="tab === 'bridges'">
      <div class="tab-header">
        <h2>桥梁管理</h2>
        <button class="add-btn" @click="openBridgeForm()">新增桥梁</button>
      </div>
      <table>
        <thead>
          <tr>
            <th>ID</th><th>名称</th><th>朝代</th><th>类型</th><th>省份</th><th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="b in bridges" :key="b.id">
            <td>{{ b.id }}</td>
            <td>{{ b.name_zh }}</td>
            <td>{{ b.dynasty }}</td>
            <td>{{ b.type }}</td>
            <td>{{ b.province }}</td>
            <td class="actions">
              <button @click="openBridgeForm(b)">编辑</button>
              <button class="delete" @click="deleteBridgeItem(b.id)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="pagination">
        <button :disabled="bridgePage <= 1" @click="bridgePage--">上一页</button>
        <span>第 {{ bridgePage }} 页</span>
        <button @click="bridgePage++">下一页</button>
      </div>

      <div v-if="showBridgeForm" class="modal" @click.self="showBridgeForm = false">
        <div class="modal-content form-modal">
          <h3>{{ editingBridge?.id ? '编辑桥梁' : '新增桥梁' }}</h3>
          <form @submit.prevent="saveBridge">
            <label>中文名称<input v-model="bridgeForm.name_zh" required /></label>
            <label>英文名称<input v-model="bridgeForm.name_en" /></label>
            <label>朝代<select v-model="bridgeForm.dynasty"><option v-for="d in dynastyList" :key="d" :value="d">{{ d }}</option></select></label>
            <label>类型<select v-model="bridgeForm.type"><option v-for="t in typeList" :key="t" :value="t">{{ t }}</option></select></label>
            <label>材料<input v-model="bridgeForm.material" /></label>
            <label>省份<input v-model="bridgeForm.province" /></label>
            <label>城市<input v-model="bridgeForm.city" /></label>
            <label>区/县<input v-model="bridgeForm.district" /></label>
            <label>坐标 (lat,lon)<input v-model="bridgeForm.coordinates" placeholder="30.25,120.16" /></label>
            <label>长度(m)<input v-model.number="bridgeForm.length_m" type="number" step="0.1" /></label>
            <label>宽度(m)<input v-model.number="bridgeForm.width_m" type="number" step="0.1" /></label>
            <label>跨度(m)<input v-model.number="bridgeForm.span_m" type="number" step="0.1" /></label>
            <label>建造年份<input v-model="bridgeForm.year_built" /></label>
            <label>描述<textarea v-model="bridgeForm.description" rows="3"></textarea></label>
            <label class="checkbox-label"><input type="checkbox" v-model="bridgeForm.has_model" /> 有3D模型</label>
            <label v-if="bridgeForm.has_model">模型URL<input v-model="bridgeForm.model_url" /></label>
            <label>图片URL<input v-model="bridgeForm.image_url" /></label>
            <div class="form-actions">
              <button type="submit">保存</button>
              <button type="button" class="cancel" @click="showBridgeForm = false">取消</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Products Tab -->
    <div v-if="tab === 'products'">
      <div class="tab-header">
        <h2>商品管理</h2>
        <button class="add-btn" @click="openProductForm()">新增商品</button>
      </div>
      <table>
        <thead>
          <tr><th>ID</th><th>名称</th><th>价格</th><th>操作</th></tr>
        </thead>
        <tbody>
          <tr v-for="p in products" :key="p.id">
            <td>{{ p.id }}</td>
            <td>{{ p.name_zh }}</td>
            <td>¥{{ p.price }}</td>
            <td class="actions">
              <button @click="openProductForm(p)">编辑</button>
              <button class="delete" @click="deleteProductItem(p.id)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="showProductForm" class="modal" @click.self="showProductForm = false">
        <div class="modal-content form-modal">
          <h3>{{ editingProduct?.id ? '编辑商品' : '新增商品' }}</h3>
          <form @submit.prevent="saveProduct">
            <label>名称<input v-model="productForm.name_zh" required /></label>
            <label>价格<input v-model.number="productForm.price" type="number" step="0.01" required /></label>
            <label>描述<textarea v-model="productForm.description" rows="3"></textarea></label>
            <label>图片URL<input v-model="productForm.image_url" /></label>
            <label>购买链接<input v-model="productForm.buy_link" /></label>
            <div class="form-actions">
              <button type="submit">保存</button>
              <button type="button" class="cancel" @click="showProductForm = false">取消</button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Knowledge Chunks Tab -->
    <div v-if="tab === 'chunks'">
      <div class="tab-header">
        <h2>知识片段管理</h2>
        <button class="add-btn" @click="openChunkForm()">新增片段</button>
      </div>
      <table>
        <thead>
          <tr><th>ID</th><th>桥梁</th><th>内容</th><th>操作</th></tr>
        </thead>
        <tbody>
          <tr v-for="c in chunks" :key="c.id">
            <td>{{ c.id }}</td>
            <td>{{ c.bridge_name || c.bridge_id }}</td>
            <td class="chunk-text">{{ truncate(c.text || c.content, 60) }}</td>
            <td class="actions">
              <button @click="openChunkForm(c)">编辑</button>
              <button class="delete" @click="deleteChunkItem(c.id)">删除</button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="showChunkForm" class="modal" @click.self="showChunkForm = false">
        <div class="modal-content form-modal">
          <h3>{{ editingChunk?.id ? '编辑片段' : '新增片段' }}</h3>
          <form @submit.prevent="saveChunk">
            <label>桥梁ID<input v-model.number="chunkForm.bridge_id" type="number" required /></label>
            <label>内容<textarea v-model="chunkForm.text" rows="5" required></textarea></label>
            <div class="form-actions">
              <button type="submit">保存</button>
              <button type="button" class="cancel" @click="showChunkForm = false">取消</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import {
  getBridgesAdmin, createBridge, updateBridge, deleteBridge,
  getProductsAdmin, createProduct, updateProduct, deleteProduct,
  getChunksAdmin, createChunk, updateChunk, deleteChunk
} from '../api/admin.js'

const tab = ref('bridges')

// Bridges state
const bridges = ref([])
const bridgePage = ref(1)
const showBridgeForm = ref(false)
const editingBridge = ref(null)
const bridgeForm = ref({})

// Products state
const products = ref([])
const showProductForm = ref(false)
const editingProduct = ref(null)
const productForm = ref({})

// Chunks state
const chunks = ref([])
const showChunkForm = ref(false)
const editingChunk = ref(null)
const chunkForm = ref({})

const dynastyList = ['先秦', '秦', '汉', '隋', '唐', '宋', '元', '明', '清']
const typeList = ['梁桥', '拱桥', '木桥', '索桥', '廊桥', '浮桥']

// --- Bridges ---
async function fetchBridges() {
  try {
    const data = await getBridgesAdmin(bridgePage.value, 20)
    bridges.value = data.items || []
  } catch { bridges.value = [] }
}
function openBridgeForm(bridge) {
  editingBridge.value = bridge || null
  bridgeForm.value = bridge ? { ...bridge } : {
    name_zh: '', name_en: '', dynasty: '宋', type: '拱桥', material: '', province: '', city: '', district: '',
    coordinates: '', length_m: null, width_m: null, span_m: null, year_built: '',
    description: '', has_model: false, model_url: '', image_url: ''
  }
  showBridgeForm.value = true
}
async function saveBridge() {
  try {
    if (editingBridge.value?.id) {
      await updateBridge(editingBridge.value.id, bridgeForm.value)
    } else {
      await createBridge(bridgeForm.value)
    }
    showBridgeForm.value = false
    await fetchBridges()
  } catch { /* handle error */ }
}
async function deleteBridgeItem(id) {
  if (!confirm('确认删除？')) return
  try { await deleteBridge(id); await fetchBridges() } catch {}
}

// --- Products ---
async function fetchProducts() {
  try {
    const data = await getProductsAdmin(1, 50)
    products.value = data.items || []
  } catch { products.value = [] }
}
function openProductForm(product) {
  editingProduct.value = product || null
  productForm.value = product ? { ...product } : { name_zh: '', price: 0, description: '', image_url: '', buy_link: '' }
  showProductForm.value = true
}
async function saveProduct() {
  try {
    if (editingProduct.value?.id) {
      await updateProduct(editingProduct.value.id, productForm.value)
    } else {
      await createProduct(productForm.value)
    }
    showProductForm.value = false
    await fetchProducts()
  } catch {}
}
async function deleteProductItem(id) {
  if (!confirm('确认删除？')) return
  try { await deleteProduct(id); await fetchProducts() } catch {}
}

// --- Chunks ---
async function fetchChunks() {
  try {
    const data = await getChunksAdmin(1, 50)
    chunks.value = data.items || []
  } catch { chunks.value = [] }
}
function openChunkForm(chunk) {
  editingChunk.value = chunk || null
  chunkForm.value = chunk ? { ...chunk, text: chunk.text || chunk.content } : { bridge_id: null, text: '' }
  showChunkForm.value = true
}
async function saveChunk() {
  try {
    if (editingChunk.value?.id) {
      await updateChunk(editingChunk.value.id, chunkForm.value)
    } else {
      await createChunk(chunkForm.value)
    }
    showChunkForm.value = false
    await fetchChunks()
  } catch {}
}
async function deleteChunkItem(id) {
  if (!confirm('确认删除？')) return
  try { await deleteChunk(id); await fetchChunks() } catch {}
}

function truncate(text, n) {
  if (!text) return ''
  return text.length > n ? text.slice(0, n) + '...' : text
}

onMounted(() => {
  fetchBridges()
  fetchProducts()
  fetchChunks()
})

watch(bridgePage, () => { fetchBridges() })
</script>

<style scoped>
.admin-page { font-family: "PingFang SC", "Microsoft YaHei", sans-serif; }
.tabs { display: flex; gap: 0; margin-bottom: 24px; }
.tabs button {
  padding: 10px 24px;
  border: 1px solid #ddd;
  background: #fff;
  cursor: pointer;
  font-size: 14px;
}
.tabs button.active { background: #6B4F3A; color: #fff; border-color: #9C5A2C; }
.tab-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.tab-header h2 { margin: 0; font-size: 18px; }
.add-btn {
  padding: 10px 20px;
  background: linear-gradient(135deg, #6B4F3A, #7d5e4a);
  color: #fff;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.25s ease;
  box-shadow: 0 2px 8px rgba(107,79,58,0.2);
}
.add-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(107,79,58,0.3);
}
table { width: 100%; border-collapse: collapse; background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 16px rgba(0,0,0,0.04); }
th, td { padding: 12px 16px; text-align: left; border-bottom: 1px solid #eee; font-size: 14px; }
th { background: linear-gradient(180deg, #f5f0ea, #f0ebe3); font-weight: 600; }
.actions { display: flex; gap: 8px; }
.actions button { padding: 6px 12px; background: #8A9A9A; color: #fff; border: none; border-radius: 8px; cursor: pointer; font-size: 12px; transition: all 0.2s ease; }
.actions button:hover { background: #6B4F3A; }
.actions button.delete { background: #e74c3c; }
.pagination { display: flex; align-items: center; gap: 12px; margin-top: 16px; justify-content: center; }
.pagination button { padding: 6px 14px; background: #fff; border: 1px solid #ddd; border-radius: 4px; cursor: pointer; }
.pagination button:disabled { opacity: 0.5; cursor: not-allowed; }
.chunk-text { max-width: 300px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.modal {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center;
  z-index: 200;
}
.form-modal {
  background: #fff; border-radius: 12px; padding: 24px; width: 560px; max-height: 80vh; overflow-y: auto;
}
.form-modal h3 { margin: 0 0 16px; }
.form-modal form { display: flex; flex-direction: column; gap: 10px; }
.form-modal label { font-size: 13px; color: #555; display: flex; flex-direction: column; gap: 4px; }
.form-modal input, .form-modal select, .form-modal textarea {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
}
.checkbox-label { flex-direction: row !important; align-items: center; gap: 8px; }
.form-actions { display: flex; gap: 12px; margin-top: 8px; }
.form-actions button { padding: 10px 20px; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; }
.form-actions button[type="submit"] {
  background: linear-gradient(135deg, #6B4F3A, #7d5e4a);
  color: #fff;
  border-radius: 10px;
  transition: all 0.25s ease;
}
.form-actions button[type="submit"]:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(107,79,58,0.3);
}
.form-actions button.cancel { background: #eee; color: #333; }
</style>
