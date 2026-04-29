import api from './index.js'

export function getGraphData() {
  return api.get('/kg/graph-data').then(r => r.data)
}
