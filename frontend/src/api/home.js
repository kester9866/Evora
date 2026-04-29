import api from './index.js'

export function getOnThisDay(month, day) {
  return api.get('/home/on-this-day', { params: { month, day } }).then(r => r.data)
}

export function getRandomFact() {
  return api.get('/home/random-fact').then(r => r.data)
}
