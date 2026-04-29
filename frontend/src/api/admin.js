import api from './index.js'

export function login(username, password) {
  return api.post('/admin/login', { username, password }).then(r => r.data)
}

// Bridges admin CRUD
export function getBridgesAdmin(page = 1, limit = 20) {
  return api.get('/admin/bridges', { params: { page, limit } }).then(r => r.data)
}
export function createBridge(data) {
  return api.post('/admin/bridges', data).then(r => r.data)
}
export function updateBridge(id, data) {
  return api.put(`/admin/bridges/${id}`, data).then(r => r.data)
}
export function deleteBridge(id) {
  return api.delete(`/admin/bridges/${id}`).then(r => r.data)
}

// Products admin CRUD
export function getProductsAdmin(page = 1, limit = 20) {
  return api.get('/admin/products', { params: { page, limit } }).then(r => r.data)
}
export function createProduct(data) {
  return api.post('/admin/products', data).then(r => r.data)
}
export function updateProduct(id, data) {
  return api.put(`/admin/products/${id}`, data).then(r => r.data)
}
export function deleteProduct(id) {
  return api.delete(`/admin/products/${id}`).then(r => r.data)
}

// Knowledge chunks admin CRUD
export function getChunksAdmin(page = 1, limit = 20) {
  return api.get('/admin/knowledge-chunks', { params: { page, limit } }).then(r => r.data)
}
export function createChunk(data) {
  return api.post('/admin/knowledge-chunks', data).then(r => r.data)
}
export function updateChunk(id, data) {
  return api.put(`/admin/knowledge-chunks/${id}`, data).then(r => r.data)
}
export function deleteChunk(id) {
  return api.delete(`/admin/knowledge-chunks/${id}`).then(r => r.data)
}
