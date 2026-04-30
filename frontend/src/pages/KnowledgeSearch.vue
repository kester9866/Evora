<template>
  <div class="knowledge-page">
    <div class="page-header">
      <button class="back-btn" @click="$router.back()">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
        返回
      </button>
    </div>

    <div class="search-section">
      <div class="search-bar">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>
        </svg>
        <input
          ref="searchInput"
          v-model="query"
          placeholder="搜索古桥知识、建造技术、历史文化..."
          @keyup.enter="doSearch"
        />
      </div>
    </div>

    <div v-if="loading" class="loading">搜索中...</div>

    <div v-else-if="error" class="error-msg">{{ error }}</div>

    <div v-else-if="results.length === 0 && searched" class="empty">
      <h2>未找到相关内容</h2>
      <p>试试其他关键词，如"拱桥"、"榫卯"、"赵州桥"、"宋代"</p>
    </div>

    <div v-else-if="results.length > 0" class="results">
      <div class="results-meta">找到 {{ results.length }} 条相关内容</div>

      <div v-for="(chunk, i) in results" :key="i" class="result-card">
        <div class="card-header">
          <span class="card-number">{{ i + 1 }}</span>
          <span class="card-score">相关度 {{ (chunk.score * 100).toFixed(0) }}%</span>
        </div>
        <div class="card-body" v-html="renderMd(chunk.text)"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { searchKnowledge } from '../api/knowledge'

const route = useRoute()
const router = useRouter()

const query = ref('')
const results = ref([])
const loading = ref(false)
const error = ref('')
const searched = ref(false)
const searchInput = ref(null)

function renderMd(text) {
  if (!text) return ''
  let html = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')

  // highlight 【...】 tags
  html = html.replace(/【([^】]+)】/g, '<strong class="hl-tag">$1</strong>')
  // bold
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
  // headings
  html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>')
  html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>')
  html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>')
  // numbered lists
  html = html.replace(/^(\d+)[\.\)]\s+(.+)$/gm, '<li>$2</li>')
  // dash lists
  html = html.replace(/^[-*]\s+(.+)$/gm, '<li>$1</li>')
  html = html.replace(/((?:<li>.*<\/li>\n?)+)/g, '<ul>$1</ul>')
  // blockquote
  html = html.replace(/^&gt;\s?(.+)$/gm, '<blockquote>$1</blockquote>')
  // paragraphs — double newline
  html = html.replace(/\n\n+/g, '</p><p>')
  html = html.replace(/\n/g, '<br>')
  html = '<p>' + html + '</p>'
  // clean up
  html = html.replace(/<p><\/p>/g, '')
  html = html.replace(/<p>(<[huo])/g, '$1')
  html = html.replace(/(<\/[huo][^>]*>)<\/p>/g, '$1')
  return html
}

async function doSearch() {
  const q = query.value.trim()
  if (!q) return

  router.replace({ query: { q } })
  loading.value = true
  error.value = ''
  results.value = []

  try {
    const res = await searchKnowledge(q, 10)
    results.value = res.data.chunks || []
    searched.value = true
  } catch (e) {
    error.value = '搜索失败：' + (e?.response?.data?.detail || e?.message || '网络错误')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  const q = route.query.q
  if (q) {
    query.value = q
    doSearch()
  } else {
    searchInput.value?.focus()
  }
})
</script>

<style scoped>
.knowledge-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px 32px 80px;
  font-family: "PingFang SC", "Noto Serif SC", "Source Han Serif SC", "SimSun", serif;
  color: #2c2416;
  min-height: 100vh;
  background: linear-gradient(180deg, #FDF8F0 0%, #F7EFE4 100%);
}

.page-header {
  margin-bottom: 20px;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255,255,255,0.6);
  border: 1px solid rgba(156,92,44,0.12);
  border-radius: 20px;
  padding: 8px 18px;
  font-size: 14px;
  color: #6B4F3A;
  cursor: pointer;
  font-family: inherit;
  transition: background 0.2s;
}
.back-btn:hover { background: rgba(255,255,255,0.9); }
.back-btn svg { width: 16px; height: 16px; }

.search-section {
  margin-bottom: 32px;
}

.search-bar {
  display: flex;
  align-items: center;
  width: 100%;
  height: 56px;
  background: rgba(255,255,255,0.7);
  backdrop-filter: blur(14px);
  border: 1px solid rgba(180,160,140,0.2);
  border-radius: 28px;
  padding: 0 22px;
  box-shadow: 0 2px 20px rgba(0,0,0,0.05), 0 0 0 1px rgba(255,255,255,0.3) inset;
  transition: box-shadow 0.3s ease;
}
.search-bar:focus-within {
  box-shadow: 0 4px 28px rgba(107,79,58,0.12), 0 0 0 1px rgba(255,255,255,0.3) inset;
}
.search-icon {
  width: 20px; height: 20px;
  color: #A09080;
  flex-shrink: 0;
  margin-right: 12px;
}
.search-bar input {
  flex: 1;
  border: none; outline: none;
  background: transparent;
  font-size: 16px;
  color: #3d3020;
  font-family: inherit;
}
.search-bar input::placeholder {
  color: #B0A090;
  font-size: 15px;
}

.loading, .error-msg, .empty {
  text-align: center;
  padding: 60px 20px;
}
.loading { color: #8A7A6A; font-size: 16px; }
.error-msg { color: #C53D3D; font-size: 15px; }

.empty h2 {
  font-size: 22px;
  color: #5a4a3a;
  margin: 0 0 12px;
}
.empty p {
  color: #8A7A6A;
  font-size: 15px;
  margin: 0;
}

.results-meta {
  font-size: 14px;
  color: #8A7A6A;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(156,92,44,0.08);
}

.result-card {
  background: rgba(255,255,255,0.55);
  border: 1px solid rgba(180,160,140,0.15);
  border-radius: 16px;
  padding: 24px 28px;
  margin-bottom: 16px;
  transition: box-shadow 0.2s;
}
.result-card:hover {
  box-shadow: 0 4px 24px rgba(107,79,58,0.06);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}
.card-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px; height: 28px;
  border-radius: 8px;
  background: #6B4F3A;
  color: #fff;
  font-size: 13px;
  font-weight: 600;
}
.card-score {
  font-size: 12px;
  color: #A09080;
  background: rgba(107,79,58,0.06);
  padding: 4px 10px;
  border-radius: 12px;
}

.card-body {
  font-size: 15px;
  line-height: 1.9;
  color: #3d3020;
}

/* Markdown rendered content */
.card-body :deep(h1),
.card-body :deep(h2),
.card-body :deep(h3) {
  color: #6B4F3A;
  margin: 16px 0 8px;
  font-size: 17px;
  font-weight: 600;
}
.card-body :deep(p) { margin: 8px 0; }
.card-body :deep(strong) { color: #9C5A2C; }
.card-body :deep(ul), .card-body :deep(ol) { padding-left: 20px; margin: 8px 0; }
.card-body :deep(li) { margin: 4px 0; }
.card-body :deep(blockquote) {
  border-left: 3px solid #6B4F3A;
  padding-left: 14px;
  margin: 12px 0;
  color: #5a4a3a;
  background: rgba(107,79,58,0.03);
  padding: 8px 14px;
  border-radius: 0 8px 8px 0;
}
.card-body :deep(code) {
  background: rgba(107,79,58,0.06);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 14px;
}
.card-body :deep(.hl-tag) {
  color: #9C5A2C;
  font-weight: 600;
}

@media (max-width: 768px) {
  .knowledge-page { padding: 16px 16px 60px; }
  .result-card { padding: 18px 20px; }
  .search-bar { height: 48px; }
}
</style>
