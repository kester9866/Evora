import api from './index.js'

export function getBridges(params) {
  return api.get('/bridges', { params }).then(r => r.data)
}

export function getBridge(id) {
  return api.get(`/bridges/${id}`).then(r => r.data)
}
