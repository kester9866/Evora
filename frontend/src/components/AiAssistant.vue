<template>
  <div class="ai-assistant" :style="{ left: posX + 'px', top: posY + 'px' }">
    <button
      class="toggle-btn"
      @mousedown.prevent="startDrag"
      @touchstart.prevent="startDrag"
      @click="onToggleClick"
    >
      💬 古桥问答
    </button>

    <div v-if="open" class="chat-panel">
      <div class="chat-header">
        <span>檐下千秋 · AI助手</span>
        <button class="close-btn" @click="open = false">✕</button>
      </div>

      <div class="messages" ref="messagesRef">
        <div v-for="(msg, i) in messages" :key="i" :class="['message', msg.role]">
          <div class="bubble" v-html="renderMd(msg.content)"></div>
        </div>
        <div v-if="streaming" class="message assistant">
          <div class="bubble typing" v-html="renderMd(streamContent)"></div><span class="cursor">|</span>
        </div>
      </div>

      <form class="input-area" @submit.prevent="send">
        <input
          v-model="input"
          placeholder="输入关于古桥的问题..."
          :disabled="streaming"
          autocomplete="off"
        />
        <button type="submit" :disabled="streaming || !input.trim()">发送</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onBeforeUnmount } from 'vue'
import { streamChat } from '../api/chat.js'

const open = ref(false)
const input = ref('')
const messages = ref([])
const streamContent = ref('')
const streaming = ref(false)
const messagesRef = ref(null)
let abortController = null

// Drag state
const posX = ref(24)
const posY = ref(0)
let dragging = false
let dragStartX = 0
let dragStartY = 0
let dragOrigX = 0
let dragOrigY = 0
let hasDragged = false

function startDrag(e) {
  dragging = true
  hasDragged = false
  const clientX = e.touches ? e.touches[0].clientX : e.clientX
  const clientY = e.touches ? e.touches[0].clientY : e.clientY
  dragStartX = clientX
  dragStartY = clientY
  dragOrigX = posX.value
  dragOrigY = posY.value
}

function onMove(e) {
  if (!dragging) return
  const clientX = e.touches ? e.touches[0].clientX : e.clientX
  const clientY = e.touches ? e.touches[0].clientY : e.clientY
  const dx = clientX - dragStartX
  const dy = clientY - dragStartY
  if (Math.abs(dx) > 3 || Math.abs(dy) > 3) hasDragged = true
  posX.value = Math.max(8, Math.min(window.innerWidth - 120, dragOrigX + dx))
  posY.value = Math.max(8, Math.min(window.innerHeight - 60, dragOrigY + dy))
}

function stopDrag() {
  dragging = false
}

function onToggleClick() {
  if (hasDragged) return
  open.value = !open.value
}

onMounted(() => {
  posY.value = window.innerHeight - 80
  window.addEventListener('mousemove', onMove)
  window.addEventListener('mouseup', stopDrag)
  window.addEventListener('touchmove', onMove, { passive: false })
  window.addEventListener('touchend', stopDrag)
})

onBeforeUnmount(() => {
  window.removeEventListener('mousemove', onMove)
  window.removeEventListener('mouseup', stopDrag)
  window.removeEventListener('touchmove', onMove)
  window.removeEventListener('touchend', stopDrag)
})

function renderMd(text) {
  if (!text) return ''
  let html = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')

  // code blocks (``` ... ```)
  html = html.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
  // inline code
  html = html.replace(/`([^`]+)`/g, '<code>$1</code>')
  // bold
  html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
  // italic
  html = html.replace(/\*(.+?)\*/g, '<em>$1</em>')
  // headings
  html = html.replace(/^### (.+)$/gm, '<h4>$1</h4>')
  html = html.replace(/^## (.+)$/gm, '<h3>$1</h3>')
  html = html.replace(/^# (.+)$/gm, '<h2>$1</h2>')
  // unordered lists
  html = html.replace(/^- (.+)$/gm, '<li>$1</li>')
  html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
  // ordered lists
  html = html.replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
  // links
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>')
  // line breaks
  html = html.replace(/\n\n/g, '</p><p>')
  html = html.replace(/\n/g, '<br>')
  html = '<p>' + html + '</p>'
  // clean empty paragraphs
  html = html.replace(/<p><\/p>/g, '')
  return html
}

function scrollBottom() {
  nextTick(() => {
    const el = messagesRef.value
    if (el) el.scrollTop = el.scrollHeight
  })
}

async function send() {
  const text = input.value.trim()
  if (!text || streaming.value) return

  messages.value.push({ role: 'user', content: text })
  input.value = ''
  streamContent.value = ''
  streaming.value = true
  scrollBottom()

  const history = messages.value.slice(0, -1).map(m => ({
    role: m.role === 'user' ? 'user' : 'assistant',
    content: m.content
  }))

  abortController = streamChat(
    text,
    history,
    (delta) => {
      streamContent.value += delta
      scrollBottom()
    },
    () => {
      if (streamContent.value) {
        messages.value.push({ role: 'assistant', content: streamContent.value })
      }
      streamContent.value = ''
      streaming.value = false
      abortController = null
      scrollBottom()
    },
    (err) => {
      messages.value.push({ role: 'assistant', content: '抱歉，连接出错了。请稍后再试。' })
      streamContent.value = ''
      streaming.value = false
      abortController = null
      console.error('AI chat error:', err)
    }
  )
}
</script>

<style scoped>
.ai-assistant {
  position: fixed;
  left: 24px;
  bottom: auto;
  z-index: 100;
}
.toggle-btn {
  padding: 10px 20px;
  background: #6B4F3A;
  color: #fff;
  border: none;
  border-radius: 24px;
  cursor: grab;
  font-size: 14px;
  box-shadow: 0 4px 16px rgba(107,79,58,0.3);
  transition: transform 0.2s, box-shadow 0.2s;
  user-select: none;
  -webkit-user-select: none;
}
.toggle-btn:active { cursor: grabbing; }
.toggle-btn:hover { transform: scale(1.05); box-shadow: 0 6px 20px rgba(107,79,58,0.4); }
.chat-panel {
  position: absolute;
  bottom: 60px;
  left: 0;
  width: 360px;
  height: 480px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 40px rgba(0,0,0,0.12);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 18px;
  background: #6B4F3A;
  color: #fff;
  font-size: 15px;
  font-weight: 500;
}
.close-btn {
  background: transparent;
  border: none;
  color: #fff;
  cursor: pointer;
  font-size: 18px;
}
.messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.message { display: flex; }
.message.user { justify-content: flex-end; }
.message.assistant { justify-content: flex-start; }
.bubble {
  max-width: 80%;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.5;
}
.message.user .bubble {
  background: #6B4F3A;
  color: #fff;
  border-bottom-right-radius: 4px;
}
.message.assistant .bubble {
  background: #f5f0ea;
  color: #333;
  border-bottom-left-radius: 4px;
}
.typing .cursor {
  animation: blink 0.8s infinite;
}
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
.bubble :deep(p) { margin: 0 0 6px; }
.bubble :deep(p:last-child) { margin-bottom: 0; }
.bubble :deep(strong) { color: #9C5A2C; }
.bubble :deep(h2), .bubble :deep(h3), .bubble :deep(h4) { margin: 8px 0 4px; color: #5a2d0c; }
.bubble :deep(ul), .bubble :deep(ol) { margin: 4px 0; padding-left: 20px; }
.bubble :deep(li) { margin-bottom: 2px; }
.bubble :deep(code) {
  background: #ede4d8;
  padding: 1px 6px;
  border-radius: 4px;
  font-size: 13px;
  font-family: 'SF Mono', 'Menlo', monospace;
}
.bubble :deep(pre) {
  background: #2d2420;
  color: #f0d9b5;
  padding: 12px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 8px 0;
  font-size: 13px;
}
.bubble :deep(pre code) {
  background: transparent;
  padding: 0;
  color: inherit;
}
.bubble :deep(a) {
  color: #9C5A2C;
  text-decoration: underline;
}
.bubble :deep(blockquote) {
  border-left: 3px solid #6B4F3A;
  padding-left: 12px;
  margin: 8px 0;
  color: #666;
}
.input-area {
  display: flex;
  padding: 12px;
  border-top: 1px solid #eee;
  gap: 8px;
}
.input-area input {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 20px;
  outline: none;
  font-size: 14px;
}
.input-area input:disabled { background: #f5f5f5; }
.input-area button {
  padding: 10px 18px;
  background: #6B4F3A;
  color: #fff;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
}
.input-area button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
