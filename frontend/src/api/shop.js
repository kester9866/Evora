import api from './index.js'

export function getProducts() {
  return api.get('/shop/products').then(r => r.data)
}
