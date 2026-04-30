/**
 * Resolve an asset URL — supports relative `./` paths pointing to backend static files,
 * and absolute `http(s)://` URLs that pass through unchanged.
 *
 *   ./images/bridge.png  →  {apiBase}/static/images/bridge.png
 *   https://cdn.example.com/img.jpg  →  https://cdn.example.com/img.jpg
 */
export function resolveAssetUrl(path: string | null | undefined): string {
  if (!path) return ''

  const trimmed = path.trim()
  if (!trimmed) return ''

  // Absolute URL — return as-is
  if (/^https?:\/\//i.test(trimmed)) {
    return trimmed
  }

  // Relative path with ./ prefix — resolve against API base + /static/
  if (/^\.\//.test(trimmed)) {
    const base = import.meta.env.VITE_API_BASE_URL || '/api'
    const relative = trimmed.replace(/^\.\//, '')
    return `${base}/static/${relative}`
  }

  // Unknown format — return as-is (graceful fallback)
  return trimmed
}
