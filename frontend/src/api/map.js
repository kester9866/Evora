import api from './index.js'

export function getProvinces(params) {
  return api.get('/map/provinces', { params }).then(r => r.data)
}

export function getCities(province, params) {
  return api.get(`/map/cities`, { params: { province, ...params } }).then(r => r.data)
}

export function getRegions() {
  return api.get('/map/regions').then(r => r.data)
}
