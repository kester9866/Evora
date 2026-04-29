const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

export function streamChat(message, history, onDelta, onDone, onError) {
  const controller = new AbortController()

  fetch(`${BASE_URL}/chat/stream`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, history }),
    signal: controller.signal
  })
    .then(async response => {
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }
      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6)
            if (data === '[DONE]') {
              onDone()
              return
            }
            try {
              const parsed = JSON.parse(data)
              if (parsed.delta) {
                onDelta(parsed.delta)
              }
            } catch {
              // skip unparseable lines
            }
          }
        }
      }
      onDone()
    })
    .catch(err => {
      if (err.name !== 'AbortError') {
        onError(err)
      }
    })

  return controller
}
