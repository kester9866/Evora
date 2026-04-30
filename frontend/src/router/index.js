import { createRouter, createWebHistory } from 'vue-router'
import DefaultLayout from '../layouts/DefaultLayout.vue'
import AdminLayout from '../layouts/AdminLayout.vue'

const routes = [
  {
    path: '/',
    component: DefaultLayout,
    children: [
      { path: '', name: 'home', component: () => import('../pages/HomePage.vue'), meta: { title: '首页 — 檐下千秋 | 中国古桥数字博物馆' } },
      { path: 'map', name: 'map', component: () => import('../pages/MapPage.vue'), meta: { title: '江山桥迹 — 桥梁地图 | 檐下千秋' } },
      { path: 'model/:id', name: 'model', component: () => import('../pages/ModelPage.vue'), meta: { title: '三维观摩 — 桥梁模型 | 檐下千秋' } },
      { path: 'game', name: 'game', component: () => import('../pages/GamePage.vue'), meta: { title: '榫卯工坊 — 木构游戏 | 檐下千秋' } },
      { path: 'shop', name: 'shop', component: () => import('../pages/ShopPage.vue'), meta: { title: '桥韵雅集 — 文创商店 | 檐下千秋' } },
      { path: 'graph', name: 'graph', component: () => import('../pages/GraphPage.vue'), meta: { title: '桥脉纵横 — 知识图谱 | 檐下千秋' } },
      { path: 'knowledge', name: 'knowledge', component: () => import('../pages/KnowledgeSearch.vue'), meta: { title: '博古知桥 — 知识搜索 | 檐下千秋' } }
    ]
  },
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      { path: '', name: 'admin', component: () => import('../pages/AdminPage.vue'), meta: { requiresAuth: true, title: '营造司 — 后台管理 | 檐下千秋' } },
      { path: 'login', name: 'admin-login', component: () => import('../pages/AdminLoginPage.vue'), meta: { title: '登录 — 营造司 | 檐下千秋' } }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.afterEach((to) => {
  if (to.meta?.title) {
    document.title = to.meta.title
  }
})

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('evora_admin_token')
    if (!token) {
      next({ name: 'admin-login' })
      return
    }
  }
  next()
})

export default router
