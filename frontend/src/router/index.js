import { createRouter, createWebHistory } from 'vue-router'
import DefaultLayout from '../layouts/DefaultLayout.vue'
import AdminLayout from '../layouts/AdminLayout.vue'

const routes = [
  {
    path: '/',
    component: DefaultLayout,
    children: [
      { path: '', name: 'home', component: () => import('../pages/HomePage.vue') },
      { path: 'map', name: 'map', component: () => import('../pages/MapPage.vue') },
      { path: 'model/:id', name: 'model', component: () => import('../pages/ModelPage.vue') },
      { path: 'game', name: 'game', component: () => import('../pages/GamePage.vue') },
      { path: 'shop', name: 'shop', component: () => import('../pages/ShopPage.vue') },
      { path: 'graph', name: 'graph', component: () => import('../pages/GraphPage.vue') }
    ]
  },
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      { path: '', name: 'admin', component: () => import('../pages/AdminPage.vue'), meta: { requiresAuth: true } },
      { path: 'login', name: 'admin-login', component: () => import('../pages/AdminLoginPage.vue') }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
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
