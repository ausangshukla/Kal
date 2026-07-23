/**
 * jor-face — Hermes Desktop plugin that forwards live gateway events to the
 * Jor face bridge (ws://127.0.0.1:8732), so the face animates in real sync
 * with what the app is actually doing (including per-token message deltas).
 *
 * Install: copy this folder to ~/.hermes/desktop-plugins/jor-face/
 * (the app hot-loads it within seconds; ⌘K → "Reload desktop plugins" to force).
 */

import { host, Tip } from '@hermes/plugin-sdk'
import { jsx } from 'react/jsx-runtime'

const ID = 'jor-face'
const BRIDGE_URL = 'ws://127.0.0.1:8732'

let ws = null
let retryTimer = null
let lastSentType = ''
let lastSentAt = 0

function closePrevious() {
  // Hot-reload safety: close any socket left by a previous plugin version.
  try { globalThis.__jorFaceWS?.close() } catch {}
  if (globalThis.__jorFaceRetry) clearTimeout(globalThis.__jorFaceRetry)
}

function connect() {
  try { ws = new WebSocket(BRIDGE_URL) } catch { scheduleRetry(); return }
  globalThis.__jorFaceWS = ws
  ws.onopen = () => host.logs?.('jor-face: bridge connected')
  ws.onclose = scheduleRetry
  ws.onerror = () => { try { ws.close() } catch {} }
}

function scheduleRetry() {
  retryTimer = setTimeout(connect, 3000)
  globalThis.__jorFaceRetry = retryTimer
}

function forward(type) {
  if (!ws || ws.readyState !== 1) return
  // Deltas arrive per-token — collapse repeats within 200 ms.
  const now = Date.now()
  if (type === lastSentType && now - lastSentAt < 200) return
  lastSentType = type
  lastSentAt = now
  try { ws.send(JSON.stringify({ hermesEvent: type })) } catch {}
}

/* ── audio tap: the mouth follows actual TTS playback, not the text stream ──
   Desktop plays voice via HTMLAudioElement (whole clips) and AudioContext
   buffer sources (live speech streaming). Patch both; report the silent→
   playing transition as audio.play and playing→silent as audio.stop. */
let audioActiveUntil = 0
let audioStopTimer = null

function markAudio(durationMs) {
  const now = Date.now()
  if (now > audioActiveUntil) forward('audio.play')
  audioActiveUntil = Math.max(audioActiveUntil, now + (durationMs || 800) + 300)
  if (audioStopTimer) clearTimeout(audioStopTimer)
  audioStopTimer = setTimeout(() => {
    if (Date.now() >= audioActiveUntil) { lastSentType = ''; forward('audio.stop') }
  }, audioActiveUntil - now + 50)
}

function audioStopped() {
  audioActiveUntil = 0
  if (audioStopTimer) clearTimeout(audioStopTimer)
  lastSentType = ''
  forward('audio.stop')
}

function installAudioTap() {
  if (globalThis.__jorFaceAudioTap) return
  globalThis.__jorFaceAudioTap = true

  const origPlay = HTMLMediaElement.prototype.play
  HTMLMediaElement.prototype.play = function (...args) {
    try {
      markAudio((this.duration && isFinite(this.duration)) ? this.duration * 1000 : 1500)
      this.addEventListener('ended', audioStopped, { once: true })
      this.addEventListener('pause', audioStopped, { once: true })
      this.addEventListener('timeupdate', () => markAudio(600))
    } catch {}
    return origPlay.apply(this, args)
  }

  const origStart = AudioBufferSourceNode.prototype.start
  AudioBufferSourceNode.prototype.start = function (...args) {
    try { markAudio(this.buffer ? this.buffer.duration * 1000 : 500) } catch {}
    return origStart.apply(this, args)
  }
}

function JorChip() {
  return jsx(Tip, {
    label: 'Jor face link — forwards agent events to the face window',
    children: jsx('button', {
      className: 'inline-flex h-full items-center px-1.5 text-[0.6875rem] text-(--ui-text-tertiary)',
      type: 'button',
      onClick: () => {
        const state = ws && ws.readyState === 1 ? 'connected' : 'disconnected'
        host.notify({ kind: 'info', message: `Jor face bridge: ${state}` })
      },
      children: '◉ jor'
    })
  })
}

export default {
  id: ID,
  name: 'Jor Face Link',
  register(ctx) {
    ctx.i18n.register({ en: { chip: 'Jor' } })
    closePrevious()
    connect()
    installAudioTap()
    host.onEvent('*', (evt) => { if (evt?.type) forward(evt.type) })
    ctx.register({
      id: 'chip',
      area: 'statusBar.right',
      order: 140,
      render: () => jsx(JorChip, {})
    })
  }
}
