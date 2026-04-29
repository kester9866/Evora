import api from './index.js'

// Stub: API not yet implemented on backend
// export function getLevels() {
//   return api.get('/game/levels').then(r => r.data)
// }

export function getLevels() {
  // Return static demo data
  return Promise.resolve([
    {
      level: 1,
      name: '基础榫卯',
      tenon: { x: 100, y: 250, width: 60, height: 40 },
      mortise: { x: 450, y: 250, width: 70, height: 50 },
      knowledge: '榫卯节点是中国木结构建筑的核心技术。'
    }
  ])
}
