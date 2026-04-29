<template>
  <div class="game-page">
    <div ref="gameContainer" class="game-container"></div>
    <div v-if="showPopup" class="completion-popup">
      <div class="popup-content">
        <h3>🎉 拼合成功！</h3>
        <p>{{ knowledgeText }}</p>
        <button disabled class="next-btn">下一关</button>
        <button class="close-btn" @click="showPopup = false">关闭</button>
      </div>
    </div>
    <button class="hint-btn" @click="showHint" :disabled="hintActive">💡 提示</button>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

const gameContainer = ref(null)
const showPopup = ref(false)
const knowledgeText = ref('')
const hintActive = ref(false)

let game = null

const levelData = {
  tenon: { x: 100, y: 250, width: 60, height: 40 },
  mortise: { x: 450, y: 250, width: 70, height: 50 },
  snapThreshold: 30,
  knowledge: '榫卯节点的精准咬合，使木构件在无钉无铁的条件下实现牢固连接，体现了中国古代匠人的卓越技艺。'
}

onMounted(async () => {
  const Phaser = await import('phaser')

  class MortiseScene extends Phaser.Scene {
    constructor() {
      super({ key: 'MortiseScene' })
    }

    preload() {
      // Placeholder textures — rendered procedurally
    }

    create() {
      const { tenon, mortise, snapThreshold } = levelData

      // Mortise slot
      const mortiseGfx = this.add.graphics()
      mortiseGfx.fillStyle(0x6b3a2a, 1)
      mortiseGfx.fillRect(mortise.x, mortise.y, mortise.width, mortise.height)
      mortiseGfx.lineStyle(2, 0x3e1f0d)
      mortiseGfx.strokeRect(mortise.x, mortise.y, mortise.width, mortise.height)
      mortiseGfx.setData('center', { x: mortise.x + mortise.width / 2, y: mortise.y + mortise.height / 2 })

      // Tenon piece (draggable)
      const tenonGfx = this.add.graphics()
      tenonGfx.fillStyle(0xa0724a, 1)
      tenonGfx.fillRect(0, 0, tenon.width, tenon.height)
      tenonGfx.lineStyle(2, 0x7a4e30)
      tenonGfx.strokeRect(0, 0, tenon.width, tenon.height)
      tenonGfx.generateTexture('tenon', tenon.width, tenon.height)
      tenonGfx.destroy()

      const tenonSprite = this.add.image(tenon.x, tenon.y, 'tenon').setOrigin(0, 0).setInteractive({ draggable: true })

      // Label text
      this.add.text(tenon.x, tenon.y - 20, '榫头', { fontSize: 14, color: '#5d4037' })
      this.add.text(mortise.x, mortise.y - 20, '卯口', { fontSize: 14, color: '#5d4037' })

      const origin = { x: tenon.x, y: tenon.y }
      const mortiseCenter = { x: mortise.x + mortise.width / 2, y: mortise.y + mortise.height / 2 }
      const tenonCenterOffset = { x: tenon.width / 2, y: tenon.height / 2 }

      this.input.on('drag', (pointer, obj, dragX, dragY) => {
        obj.x = dragX
        obj.y = dragY
      })

      let snapped = false

      this.input.on('dragend', (pointer, obj) => {
        if (snapped) return
        const tx = obj.x + tenonCenterOffset.x
        const ty = obj.y + tenonCenterOffset.y
        const dist = Math.hypot(tx - mortiseCenter.x, ty - mortiseCenter.y)

        if (dist < snapThreshold) {
          snapped = true
          this.tweens.add({
            targets: obj,
            x: mortiseCenter.x - tenonCenterOffset.x,
            y: mortiseCenter.y - tenonCenterOffset.y,
            duration: 200,
            ease: 'Back.easeOut',
            onComplete: () => {
              knowledgeText.value = levelData.knowledge
              showPopup.value = true
            }
          })
        } else {
          this.tweens.add({
            targets: obj,
            x: origin.x,
            y: origin.y,
            duration: 300,
            ease: 'Power2'
          })
        }
      })

      // Hint glow
      this.mortiseGlow = mortiseGfx
      this.snapThreshold = snapThreshold
    }

    hintGlow() {
      const { x, y, width, height } = this.mortiseGlow.getData('center')
      const glow = this.add.graphics()
      glow.lineStyle(3, 0xffd700, 0.8)
      glow.strokeRect(
        (this.mortiseGlow.getData('center').x || 450) - 35 + 60,
        (this.mortiseGlow.getData('center').y || 250) - 25 + 40,
        (this.mortiseGlow.getData('center').x ? 70 : 70),
        (this.mortiseGlow.getData('center').y ? 50 : 50)
      )
      this.tweens.add({
        targets: glow,
        alpha: 0,
        duration: 2000,
        onComplete: () => glow.destroy()
      })
    }
  }

  game = new Phaser.Game({
    type: Phaser.AUTO,
    width: 600,
    height: 400,
    parent: gameContainer.value,
    backgroundColor: '#f5f0ea',
    scene: MortiseScene
  })
})

function showHint() {
  if (!game || hintActive.value) return
  hintActive.value = true
  const scene = game.scene.getScene('MortiseScene')
  if (scene && scene.hintGlow) {
    scene.hintGlow()
  }
  setTimeout(() => { hintActive.value = false }, 2000)
}

onBeforeUnmount(() => {
  if (game) game.destroy(true)
})
</script>

<style scoped>
.game-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
  min-height: calc(100vh - 64px);
}
.game-container {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}
.hint-btn {
  margin-top: 16px;
  padding: 10px 24px;
  border: 1px solid #ffc107;
  background: #fff8e1;
  color: #8b6914;
  border-radius: 8px;
  cursor: pointer;
  font-size: 15px;
}
.hint-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.completion-popup {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex; align-items: center; justify-content: center;
  z-index: 200;
}
.popup-content {
  background: #fff;
  border-radius: 16px;
  padding: 32px;
  max-width: 400px;
  text-align: center;
}
.popup-content h3 { margin: 0 0 12px; font-size: 20px; }
.popup-content p { font-size: 14px; color: #555; line-height: 1.6; }
.next-btn, .close-btn {
  margin: 12px 6px 0;
  padding: 8px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}
.next-btn {
  background: #eee;
  border: 1px solid #ccc;
  color: #999;
}
.close-btn {
  background: #8b4513;
  border: none;
  color: #fff;
}
</style>
