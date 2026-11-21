# HYPERFRAMES DESIGN SYSTEM — FIKRA STUDIO V2.0

- **Canvas:** 1080×1920 (9:16 Vertical) @ 30 FPS.
- **Deterministic Seeking:** Every visual state is computed purely from `currentFrame` via `window.seekToFrame(frame)` so frame-by-frame capture or HyperFrames CLI rendering produces pixel-identical frames.
- **Typography:** Cairo / Tajawal for narrative Arabic (White `#F8FAFC`), Amiri for Quranic verses (Gold `#F59E0B`).
- **Audio & Compliance:** Zero music over Quranic segments; visual silence indicator when Quranic scene is active.
