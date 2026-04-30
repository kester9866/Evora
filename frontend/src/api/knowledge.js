import api from './index'

export function searchKnowledge(q, k = 10) {
  return api.get('/knowledge/search', { params: { q, k } })
}
