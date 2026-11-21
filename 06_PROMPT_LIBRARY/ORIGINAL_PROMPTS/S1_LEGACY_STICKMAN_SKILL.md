---
name: "stickman-comedy"
description: "Pitch wordless stickman comedy reel ideas, then auto-produce the chosen one as a 9:16 MP4 in the round-head stickman style (code-drawn by default, Higgsfield on request). Use for ستيك مان, اعطيني افكار."
---

# Stickman Comedy (ستيك مان كوميدي)

Short wordless comedy reels: a big-round-head stickman in a richly painted, moodily lit world, a few hard-cut shots, real sound effects, one black label pill on top, and a punchline that loops. Based on a viral reference (1760 candle-alarm vs 2026 four-phone alarm) Mahmoud analysed.

Two modes:
1. **Ideas** ("اعطيني افكار", "افكار ستيك مان", "عايز فكرة"): **ask the video length first**, then pitch 8 ideas built for that length, then stop.
2. **Production** (he picks a number, or sends his own idea, after asking the length if he hasn't given it): build the whole video automatically to a finished MP4 with no further questions.

Reply in Egyptian Arabic, short messages. He is not an experienced editor: deliver finished files, not instructions.

**Route:** draw everything in code (default, free). Use Higgsfield only when he says so ("بهيجزفيلد", "بالـ AI") - section 9.

---

## 1. Style DNA (what must survive in every video)

| Element | Rule |
|---|---|
| Character | Huge round white head with soft grey shading and a thick black outline; short stick body (head diameter ≈ torso length); thick black limbs, round white glove hands, chunky brown shoes. Simple face: dot eyes, small expressive mouth. Each character is recognised by ONE accessory (red cap, glasses+mustache+grey tufts, hijab, beard+tie...). |
| World | Simple character, detailed world. Sets drawn with dark cartoon outlines, gradient fills, a few detail strokes (planks, bricks, blanket folds), then a painterly texture and grain. |
| Light | Always a motivated light source (lamp, candle, phone, window, fridge, TV) with a darkness falloff and a coloured glow. Warm = past/cosy, cold blue = night/phone/modern, one saturated accent (red) for the eye. |
| Words | None spoken. The only text is the label pill (black rounded box, white Alexandria 800, top centre), changed at hard cuts. In-world text (posters, screens) only when it IS the joke. |
| Cutting | Hard cuts only, no transitions or zoom effects. 2-4 s per shot. Movement lives inside the shot: slow push-in, tilt/pan, small shake on impacts. Pattern per beat: wide (situation) -> detail close-up (the thing the joke hangs on) -> back wide or face close-up (reaction). |
| Sound | SFX only, no music, no voice: room tone, small foley (taps, clicks), one big sound that carries the cut (alarm, clink, thud), silence before the punch. |
| Length | The length he picks before the ideas (usually 30-60 s), 10-22 shots, 1080x1920, 30 fps. Ending loops back into the opening (same state, same sound). |

---

## 2. Ideas mode

**Step 0: ask the length.** The idea is designed around the length, so ask before writing any idea. Use AskUserQuestion with one question, «الفيديو يبقى مدته قد إيه؟», options `30 ثانية` / `45 ثانية` / `دقيقة` (he can type another number). Skip the question only when his message already names a length. His number is the target; the final video lands within ±3 s of it.

Scale the ideas to the length:

| Length | Structure | Shots |
|---|---|---|
| ~30 s | 2-3 rounds or 2 parts + punch | 10-13 |
| ~45 s | 3 rounds or 3 parts + punch | 14-17 |
| ~60 s | 4 rounds or 4 parts + punch, or a twist in the middle and another at the end | 18-22 |

Then give **8 ideas**, mixed formats, numbered. Any topic works; the format list is a menu, not a rule:

- توقع vs واقع (the plan vs what happens)
- زمان vs دلوقتي (the reference format)
- الحل البسيط vs التعقيد (one pin vs four phones)
- تصعيد (a small problem that escalates every shot)
- أنواع الناس في موقف (3 quick types, 1 shot each)
- أنا vs عقلي / جسمي
- لما يحصل X (one relatable moment, slowed down)
- قلب متوقع (twist in the last shot)

Good sources: Egyptian daily life (المواصلات، الامتحانات، الأم المصرية، العزومات، آخر الشهر، الشغل، الجيم والدايت، الواتساب والجروبات، رمضان، الفرح، الدكتور) and universal habits (sleep, phone, procrastination). No politics, no mocking religion, no real people or brand logos.

Every idea must be: wordless, readable in the first second, sized to the chosen length (enough rounds or parts to fill it without padding, never one gag stretched), a punchline in the last 3-5 s, buildable with 1-4 characters, 1-4 sets and simple props.

Shapes that fill longer runtimes without dragging:
- **Rule of three, escalating:** the same situation three times, each round bigger (3 attempts, 3 days, 3 types), then the twist.
- **Two halves + a third act:** then vs now, plan vs reality, and a final beat that flips both (the old man shows up in 2026, the plan wins after all).
- **Chain reaction:** one small action triggers a longer and longer chain until the payoff.
- **Time march:** the same spot at several timestamps (8:00, 10:00, 2:00, 6:00, 11:59) with a label pill per stamp.

Open the list with one line naming the length the ideas are built for («الأفكار دي معمولة لفيديو 45 ثانية:»).

Format (keep each idea 5 short lines):
```
1) <عنوان قصير>  ·  <الفورمات>
   اللافتة: «...» ثم «...»
   الهوك: <أول ثانية بالظبط بتبان إزاي>
   التصعيد: <الجولات أو الأجزاء اللي بتملا المدة اللي اختارها>
   الضحكة: <القفلة اللي بتلف على الأول>
```
End with one line: «اختار رقم وأنا أبدأ على طول (ولو عايزه بـ Higgsfield قول).» Then stop and wait.

If he sends his own idea instead, ask the length first (same question, unless he gave it), then go to production and shape his idea to that length.

---

## 3. Production: plan (no questions from here on)

1. Turn the idea into a **shot table**: `# | time | label | framing | action | sound`. Total = the length he chose (±3 s), shot count from the table in section 2, 2-4 s per shot, grouped into sections, each with its own label pill. Mirror structure when the idea has parallel parts (same number of shots, same order of framings per part).
   Pacing for longer runtimes:
   - 0-3 s: the hook shot, the strangest image of the video.
   - Every 8-12 s: a section turn (new label, new set or time jump, a big sound) so attention resets.
   - Each round of escalation is shorter and bigger than the one before it; cut the second half faster (2-2.5 s shots).
   - Keep one wide/establishing shot per section; reuse sets across sections (same room, different time/light) to stay buildable.
   - The last 3-5 s: the punchline, then a held reaction (~1 s) that matches the first frame for the loop.
2. Design the cast: one accessory per character, consistent colours.
3. Send the table to him in one short message (SendUserMessage), then continue immediately. Don't wait for approval.
4. Use the task list: plan, set up, scene, stills check, sound, render, final check, deliver.

---

## 4. Setup

Work in a fresh folder in the scratchpad (`job=<scratchpad>/stickman-<slug>`).

```bash
mkdir -p $job && cd $job && npm init -y >/dev/null && npm i @fontsource/alexandria >/dev/null
node -e "require('playwright')" && python3 -c "import numpy, scipy"
fc-list | grep -qi emoji && echo emoji-ok   # only use emoji marks if present
```
Write the four files below verbatim: `stick.js` (section 5), `render.js` (section 7), `sfx.py` (section 8), and a `scene.html` built from the template (section 6). Fonts and scripts load from disk, never from a CDN.

---

## 5. Engine: `stick.js` (write verbatim)

```js
// stick.js — stickman comedy engine. Every draw function is pure (time in, SVG string out).
// Shot world = 1080x1920 units. Camera zooms into it per shot.
const W = 1080, H = 1920, INK = '#151312';
const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const lerp = (a, b, k) => a + (b - a) * k;
const ease = k => (k = clamp(k), k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2);
const easeOut = k => 1 - Math.pow(1 - clamp(k), 3);
const back = k => { k = clamp(k); const c = 1.9; return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); };
const lin = k => clamp(k);
const span = (t, a, b, f = ease) => f(clamp((t - a) / (b - a)));   // 0 before a, 1 after b
const wob = (t, f = 1, a = 1, ph = 0) => Math.sin((t * f + ph) * Math.PI * 2) * a;
const rad = d => d * Math.PI / 180;
const pt = (x, y, ang, len) => [x + Math.sin(rad(ang)) * len, y + Math.cos(rad(ang)) * len]; // ang 0 = down, 90 = +x, 180 = up
const mixPose = (a, b, k) => { const o = { ...a }; for (const key in b) { const va = a[key], vb = b[key]; o[key] = Array.isArray(va) && Array.isArray(vb) && typeof va[0] === 'number' ? va.map((v, i) => lerp(v, vb[i], k)) : typeof va === 'number' && typeof vb === 'number' ? lerp(va, vb, k) : (k < .5 ? va ?? vb : vb); } return o; };

// ---------- defs: gradients + texture filters (call once per frame, seed = frame-based) ----------
function defs(seed) {
  return `<defs>
  <radialGradient id="headG" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="#ffffff"/><stop offset=".65" stop-color="#eeede9"/><stop offset="1" stop-color="#cfcdc8"/></radialGradient>
  <radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".7"/></radialGradient>
  <filter id="paint" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".012 .02" numOctaves="3" seed="7"/>
    <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.6 1.15"/></filter>
  <filter id="fiber" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9 .25" numOctaves="2" seed="3"/>
    <feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2 1.25"/></filter>
  <filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="1" seed="${seed}"/><feColorMatrix type="saturate" values="0"/></filter>
  <filter id="soft"><feGaussianBlur stdDeviation="18"/></filter>
  <filter id="blur6"><feGaussianBlur stdDeviation="6"/></filter>
  </defs>`;
}
// Painterly texture over the set (inside the camera group so it zooms with the world)
const paintTex = (x = -400, y = -400, w = W + 800, h = H + 800) =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" filter="url(#paint)" opacity=".13" style="mix-blend-mode:multiply"/>
   <rect x="${x}" y="${y}" width="${w}" height="${h}" filter="url(#fiber)" opacity=".07" style="mix-blend-mode:multiply"/>`;
// Motivated light: darkness except a pool at (lx,ly) + coloured glow. Unique id per light.
function light(lx, ly, r, color, dark = .7, glow = .5, id = 'L') {
  return `<defs><radialGradient id="${id}d" cx="${lx}" cy="${ly}" r="${r}" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset=".45" stop-color="#000" stop-opacity="${dark * .35}"/><stop offset="1" stop-color="#000" stop-opacity="${dark}"/></radialGradient>
    <radialGradient id="${id}g" cx="${lx}" cy="${ly}" r="${r * .7}" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="${color}" stop-opacity="${glow}"/><stop offset="1" stop-color="${color}" stop-opacity="0"/></radialGradient></defs>
  <rect x="-600" y="-600" width="${W + 1200}" height="${H + 1200}" fill="url(#${id}d)"/>
  <rect x="-600" y="-600" width="${W + 1200}" height="${H + 1200}" fill="url(#${id}g)" style="mix-blend-mode:screen"/>`;
}
// Screen-space finish (outside camera): vignette + moving grain
const finish = (g = .07) => `<rect width="${W}" height="${H}" fill="url(#vig)"/><rect width="${W}" height="${H}" filter="url(#grain)" opacity="${g}" style="mix-blend-mode:overlay"/>`;
// Camera: (x,y) world point at frame centre, z zoom, r roll, sx/sy screen shake
function cam(c, inner) {
  const { x = W / 2, y = H / 2, z = 1, r = 0, sx = 0, sy = 0 } = c;
  return `<g transform="translate(${W / 2 + sx} ${H / 2 + sy}) rotate(${r}) scale(${z}) translate(${-x} ${-y})">${inner}</g>`;
}
const camLerp = (a, b, k) => ({ x: lerp(a.x ?? W / 2, b.x ?? W / 2, k), y: lerp(a.y ?? H / 2, b.y ?? H / 2, k), z: lerp(a.z ?? 1, b.z ?? 1, k), r: lerp(a.r ?? 0, b.r ?? 0, k) });
const shake = (t, t0, amt = 18, dur = .35) => { const k = clamp((t - t0) / dur); if (k <= 0 || k >= 1) return { sx: 0, sy: 0 }; const d = (1 - k) * amt; return { sx: Math.sin(t * 97) * d, sy: Math.cos(t * 83) * d }; };

// ---------- the stickman ----------
// Big round head, short stick body (head diameter ≈ torso length, like the reference).
// x,y = hip (world). s = scale. dir: 1 faces right, -1 left, 0 front. rot = whole-body rotation (lying = -90/90).
// Angles in degrees, 0 = hanging down, 90 = forward (facing dir), 180 = up, negative = backward.
//   lean (+ forward), head (extra tilt, + forward/down)
//   aL / aR: [shoulder, elbow-bend]  OR  {to:[x,y]} world target  OR  {to:'face'|'chin'|'head'|'mouth'}
//   lL / lR: [hip, knee-bend]  OR  {to:[x,y]} world foot target
// face: eyes 'open'|'wide'|'closed'|'happy'|'tired'|'angry'|'side'|'dead'; mouth 'smile'|'grin'|'flat'|'frown'|'wavy'|'open'|'O'|'scream'
// acc: cap, glasses, mustache, hair, beard, tie, hijab (colour strings) | drool, sweat, tear, lids (0-1) | blush (1)
// After each call, stick.last holds world points: handL handR head headR mouth footL footR hip
function stick(o) {
  const { x = 540, y = 1300, s = 1, dir = 1, lean = 0, head = 0, aL = [12, 8], aR = [-12, -8], lL = [6, 0], lR = [-6, 0],
    face = {}, acc = {}, hidden = {}, rot = 0, dy = 0 } = o;
  const d = dir === 0 ? 1 : dir, LW = 12, T = 150, R = 96, UA = 78, LA = 74, TH = 92, SH = 88;
  const Y = y + (dy || 0);
  const cr = Math.cos(rad(rot)), sr = Math.sin(rad(rot));
  const toW = (px, py) => [x + (px * cr - py * sr) * s, Y + (px * sr + py * cr) * s];
  const toL = (wx, wy) => { const px = (wx - x) / s, py = (wy - Y) / s; return [px * cr + py * sr, -px * sr + py * cr]; };
  const [nx, ny] = pt(0, 0, 180 - lean * d, T);
  const [shx, shy] = pt(0, 0, 180 - lean * d, T - 20);
  const [hcx, hcy] = pt(nx, ny, 180 - (lean + head) * d, R - 8);
  const fx = dir === 0 ? 0 : 24 * d;
  const ex1 = hcx + fx - 31, ex2 = hcx + fx + 31, ey = hcy - 6, mx = hcx + fx * 1.1, my = hcy + 42;
  const named = { face: [hcx + fx * 1.4, hcy + 6], chin: [mx + 6 * d, my + 26], head: [hcx - 30 * d, hcy - 60], mouth: [mx, my + 6] };
  // 2-bone IK in local space; bend picks elbow/knee side
  const ik = (ox, oy, tx, ty, L1, L2, bend) => {
    let dx = tx - ox, dy2 = ty - oy, dist = Math.hypot(dx, dy2); const maxd = L1 + L2 - .5;
    if (dist > maxd) { dx *= maxd / dist; dy2 *= maxd / dist; dist = maxd; }
    const a = Math.acos(clamp((L1 * L1 + dist * dist - L2 * L2) / (2 * L1 * dist), -1, 1)), base = Math.atan2(dy2, dx), ang = base + bend * a;
    return [ox + Math.cos(ang) * L1, oy + Math.sin(ang) * L1, ox + dx, oy + dy2];
  };
  const fk = (ox, oy, a1, a2, L1, L2) => { const [ex, ey2] = pt(ox, oy, a1 * d, L1); const [hx, hy] = pt(ex, ey2, (a1 + a2) * d, L2); return [ex, ey2, hx, hy]; };
  const solve = (spec, ox, oy, L1, L2, bend) => {
    if (spec && spec.to) { const t = spec.to; const [lx, ly] = typeof t === 'string' ? named[t] : toL(t[0], t[1]); return ik(ox, oy, lx, ly, L1, L2, bend); }
    return fk(ox, oy, spec[0], spec[1], L1, L2);
  };
  const arm = a => { const [ex, ey2, hx, hy] = solve(a, shx, shy, UA, LA, d); return { p: `M${shx} ${shy} L${ex} ${ey2} L${hx} ${hy}`, hx, hy }; };
  const leg = l => { const [ex, ey2, fx2, fy] = solve(l, 0, 0, TH, SH, -d); return { p: `M0 0 L${ex} ${ey2} L${fx2} ${fy}`, fx: fx2, fy }; };
  const A1 = arm(aL), A2 = arm(aR), L1 = leg(lL), L2 = leg(lR);
  const line = p => `<path d="${p}" fill="none" stroke="${INK}" stroke-width="${LW}" stroke-linecap="round" stroke-linejoin="round"/>`;
  const shoe = f => `<ellipse cx="${f.fx + 14 * d}" cy="${f.fy + 6}" rx="32" ry="16" fill="#4a2f1d" stroke="${INK}" stroke-width="5"/><ellipse cx="${f.fx + 4 * d}" cy="${f.fy}" rx="13" ry="5" fill="#7a5236" opacity=".7"/>`;
  const hand = h => `<circle cx="${h.hx}" cy="${h.hy}" r="19" fill="#f6f5f2" stroke="${INK}" stroke-width="5"/>`;
  const eye = cx => {
    const e = face.eyes || 'open';
    if (e === 'closed') return `<path d="M${cx - 15} ${ey} Q${cx} ${ey + 13} ${cx + 15} ${ey}" fill="none" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>`;
    if (e === 'happy') return `<path d="M${cx - 15} ${ey + 6} Q${cx} ${ey - 12} ${cx + 15} ${ey + 6}" fill="none" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>`;
    if (e === 'wide') return `<circle cx="${cx}" cy="${ey}" r="19" fill="#fff" stroke="${INK}" stroke-width="4"/><circle cx="${cx + 3 * d}" cy="${ey}" r="8" fill="${INK}"/>`;
    if (e === 'dead') return `<path d="M${cx - 12} ${ey - 12} l24 24 M${cx + 12} ${ey - 12} l-24 24" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>`;
    if (e === 'side') return `<ellipse cx="${cx + 8 * d}" cy="${ey}" rx="7" ry="10" fill="${INK}"/><path d="M${cx - 16} ${ey - 16} h32" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`;
    if (e === 'tired') return `<ellipse cx="${cx}" cy="${ey + 3}" rx="8" ry="9" fill="${INK}"/><path d="M${cx - 17} ${ey - 2} L${cx + 17} ${ey - 2}" stroke="${INK}" stroke-width="5" stroke-linecap="round"/><path d="M${cx - 16} ${ey - 3} h32 v-12 h-32z" fill="url(#headG)"/>`;
    if (e === 'angry') { const inner = (cx < hcx + fx) ? 1 : -1; return `<ellipse cx="${cx}" cy="${ey + 2}" rx="8" ry="10" fill="${INK}"/><path d="M${cx - 18} ${ey - 20 - 6 * inner} L${cx + 18} ${ey - 20 + 6 * inner}" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>`; }
    return `<ellipse cx="${cx + 2 * d}" cy="${ey}" rx="8" ry="11" fill="${INK}"/><circle cx="${cx + 5 * d}" cy="${ey - 4}" r="2.6" fill="#fff"/>`;
  };
  const m = face.mouth || 'flat';
  const mouth = {
    smile: `<path d="M${mx - 20} ${my - 4} Q${mx} ${my + 14} ${mx + 20} ${my - 4}" fill="none" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>`,
    grin: `<path d="M${mx - 26} ${my - 8} Q${mx} ${my + 26} ${mx + 26} ${my - 8} Z" fill="#5a1717" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/><path d="M${mx - 22} ${my - 6} L${mx + 22} ${my - 6} L${mx + 18} ${my + 1} L${mx - 18} ${my + 1}Z" fill="#fff"/>`,
    flat: `<path d="M${mx - 14} ${my} L${mx + 14} ${my}" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>`,
    frown: `<path d="M${mx - 18} ${my + 6} Q${mx} ${my - 8} ${mx + 18} ${my + 6}" fill="none" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>`,
    wavy: `<path d="M${mx - 20} ${my} q5 -6 10 0 t10 0 t10 0 t10 0" fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`,
    open: `<ellipse cx="${mx}" cy="${my + 4}" rx="17" ry="14" fill="#5a1717" stroke="${INK}" stroke-width="5"/><ellipse cx="${mx}" cy="${my + 11}" rx="10" ry="5" fill="#d9706f"/>`,
    O: `<ellipse cx="${mx}" cy="${my + 6}" rx="13" ry="20" fill="#5a1717" stroke="${INK}" stroke-width="5"/>`,
    scream: `<path d="M${mx - 24} ${my - 6} Q${mx} ${my - 14} ${mx + 24} ${my - 6} Q${mx + 20} ${my + 44} ${mx} ${my + 46} Q${mx - 20} ${my + 44} ${mx - 24} ${my - 6}Z" fill="#5a1717" stroke="${INK}" stroke-width="5"/><ellipse cx="${mx}" cy="${my + 34}" rx="12" ry="7" fill="#d9706f"/>`,
  }[m] || '';
  let hd = `<circle cx="${hcx}" cy="${hcy}" r="${R}" fill="url(#headG)" stroke="${INK}" stroke-width="8"/>`;
  if (acc.hijab) hd = `<path d="M${hcx - R - 18} ${hcy + 40} Q${hcx - R - 26} ${hcy - R - 30} ${hcx} ${hcy - R - 22} Q${hcx + R + 26} ${hcy - R - 30} ${hcx + R + 18} ${hcy + 40} Q${hcx + R + 30} ${hcy + R + 40} ${hcx} ${hcy + R + 34} Q${hcx - R - 30} ${hcy + R + 40} ${hcx - R - 18} ${hcy + 40}Z" fill="${acc.hijab}" stroke="${INK}" stroke-width="7"/><ellipse cx="${hcx + fx * .5}" cy="${hcy + 4}" rx="${R - 18}" ry="${R - 8}" fill="url(#headG)" stroke="${INK}" stroke-width="5"/>`;
  if (acc.hair) hd += [-1, 1].map(sd => `<path d="M${hcx + sd * 64} ${hcy - 60} q${sd * 26} -6 ${sd * 30} 18 q${sd * 14} 2 ${sd * 6} 22 q${sd * -14} -4 ${sd * -22} -12z" fill="${acc.hair}" stroke="${INK}" stroke-width="4"/>`).join('');
  if (acc.beard) hd += `<path d="M${hcx - R + 14} ${hcy + 20} Q${hcx - R + 20} ${hcy + R + 26} ${hcx + fx} ${hcy + R + 22} Q${hcx + R - 20} ${hcy + R + 26} ${hcx + R - 14} ${hcy + 20} Q${hcx} ${hcy + 60} ${hcx - R + 14} ${hcy + 20}Z" fill="${acc.beard}" stroke="${INK}" stroke-width="5"/>`;
  hd += eye(ex1) + eye(ex2);
  if (acc.lids) hd += [ex1, ex2].map(cx => `<rect x="${cx - 22}" y="${ey - 24}" width="44" height="${24 * acc.lids}" fill="#e9e8e4"/><path d="M${cx - 20} ${ey - 24 + 24 * acc.lids} h40" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`).join('');
  if (acc.glasses) hd += `<g fill="none" stroke="#3a3632" stroke-width="4"><circle cx="${ex1}" cy="${ey}" r="23"/><circle cx="${ex2}" cy="${ey}" r="23"/><path d="M${ex1 + 23} ${ey} h${ex2 - ex1 - 46}"/></g>`;
  if (acc.mustache) hd += `<path d="M${mx} ${my - 14} q-14 -10 -34 0 q-6 12 -16 10 q14 14 50 -2 q36 16 50 2 q-10 2 -16 -10 q-20 -10 -34 0z" fill="${acc.mustache}" stroke="${INK}" stroke-width="4"/>`;
  hd += mouth;
  if (acc.blush) hd += `<ellipse cx="${ex1 - 6}" cy="${ey + 30}" rx="16" ry="8" fill="#f08a8a" opacity=".5"/><ellipse cx="${ex2 + 6}" cy="${ey + 30}" rx="16" ry="8" fill="#f08a8a" opacity=".5"/>`;
  if (acc.drool) hd += `<path d="M${mx + 8} ${my + 12} q4 ${30 * acc.drool} 0 ${44 * acc.drool} q-10 0 -8 -14z" fill="#9fd3f0" stroke="#4d7f9c" stroke-width="3" opacity=".9"/>`;
  if (acc.tear) hd += `<path d="M${ex1} ${ey + 14} q-8 ${40 * acc.tear} 0 ${60 * acc.tear} q8 -10 0 ${-60 * acc.tear}z" fill="#9fd3f0" stroke="#4d7f9c" stroke-width="3"/>`;
  if (acc.sweat) hd += `<path d="M${hcx - fx - 70} ${hcy - 50 + 30 * acc.sweat} q-12 20 0 26 q12 -6 0 -26z" fill="#9fd3f0" stroke="#4d7f9c" stroke-width="3"/>`;
  if (acc.cap) hd += `<path d="M${hcx - R - 4} ${hcy - 22} Q${hcx - R + 6} ${hcy - R - 32} ${hcx} ${hcy - R - 30} Q${hcx + R - 6} ${hcy - R - 32} ${hcx + R + 4} ${hcy - 22} Z" fill="${acc.cap}" stroke="${INK}" stroke-width="6"/>
    <path d="M${hcx + d * (R - 20)} ${hcy - 30} q${d * 70} -6 ${d * 96} 16 q${d * -40} 16 ${d * -110} 2z" fill="${acc.cap}" stroke="${INK}" stroke-width="6"/>
    <path d="M${hcx - R + 18} ${hcy - 60} Q${hcx} ${hcy - R - 12} ${hcx + R - 30} ${hcy - 66}" fill="none" stroke="#fff" stroke-opacity=".25" stroke-width="8" stroke-linecap="round"/>`;
  const tie = acc.tie ? `<path d="M${nx} ${ny + 6} l-12 14 l12 70 l12 -70z" fill="${acc.tie}" stroke="${INK}" stroke-width="4"/>` : '';
  const backS = d > 0 ? [A1, L1] : [A2, L2], frontS = d > 0 ? [A2, L2] : [A1, L1];
  // an arm aimed at the face/head ({to:...}) is always drawn in front of the head
  const backArmTo = (d > 0 ? aL : aR) && (d > 0 ? aL : aR).to;
  let g = '';
  if (!hidden.legs) g += line(backS[1].p) + shoe(backS[1]);
  if (!hidden.arms && !backArmTo) g += line(backS[0].p) + hand(backS[0]);
  g += line(`M0 0 L${nx} ${ny}`) + tie;
  if (!hidden.legs) g += line(frontS[1].p) + shoe(frontS[1]);
  g += hd;
  if (!hidden.arms && backArmTo) g += line(backS[0].p) + hand(backS[0]);
  if (!hidden.arms) g += line(frontS[0].p) + hand(frontS[0]);
  stick.last = { handL: toW(A1.hx, A1.hy), handR: toW(A2.hx, A2.hy), head: toW(hcx, hcy), headR: R * s, mouth: toW(mx, my), footL: toW(L1.fx, L1.fy), footR: toW(L2.fx, L2.fy), hip: [x, Y] };
  return `<g transform="translate(${x} ${Y}) rotate(${rot}) scale(${s})">${g}</g>`;
}
// Pose presets: stick({ ...P.walk(t), x, y, dir, face, acc }). Blend two with mixPose(P.stand(), P.shock(), k).
const P = {
  stand: () => ({ lean: 0, aL: [12, 8], aR: [-12, -8], lL: [6, 0], lR: [-6, 0] }),
  walk: (t, sp = 1.6) => { const k = Math.sin(t * sp * Math.PI * 2); return { lean: 4, aL: [-28 * k, 25], aR: [28 * k, 25], lL: [26 * k, -Math.max(0, -40 * k)], lR: [-26 * k, -Math.max(0, 40 * k)], dy: -Math.abs(Math.cos(t * sp * Math.PI * 2)) * 8 }; },
  run: (t, sp = 2.6) => { const k = Math.sin(t * sp * Math.PI * 2); return { lean: 16, aL: [-55 * k, 80], aR: [55 * k, 80], lL: [45 * k, -Math.max(15, -80 * k)], lR: [-45 * k, -Math.max(15, 80 * k)], dy: -Math.abs(Math.cos(t * sp * Math.PI * 2)) * 22 }; },
  sit: () => ({ lean: -4, aL: [25, 40], aR: [10, 50], lL: [90, -90], lR: [84, -86] }),
  sitFloor: () => ({ lean: 4, aL: [30, 30], aR: [20, 40], lL: [80, -10], lR: [70, -20] }),
  armsUp: (t = 0) => ({ lean: -4, aL: [120 + wob(t, 2, 8), 22], aR: [-120 - wob(t, 2, 8), -22], lL: [10, 0], lR: [-10, 0] }),
  shrug: () => ({ lean: 0, head: -6, aL: [60, 70], aR: [-60, -70], lL: [6, 0], lR: [-6, 0] }),
  point: () => ({ lean: 2, aL: [12, 8], aR: [95, 0], lL: [8, 0], lR: [-8, 0] }),
  facepalm: () => ({ lean: 8, head: 14, aL: [12, 8], aR: { to: 'face' }, lL: [6, 0], lR: [-6, 0] }),
  think: () => ({ lean: 0, head: -10, aL: { to: 'chin' }, aR: [-10, -10], lL: [6, 0], lR: [-6, 0] }),
  shock: () => ({ lean: -10, head: -6, aL: [140, -50], aR: [-140, 50], lL: [14, 0], lR: [-14, 0] }),
  headGrab: () => ({ lean: -4, head: -4, aL: { to: 'head' }, aR: [-150, -30], lL: [12, 0], lR: [-12, 0] }),
  phone: (t = 0) => ({ lean: 6, head: 18, aL: [30, 100 + wob(t, 2.2, 4)], aR: [45, 85], lL: [6, 0], lR: [-6, 0] }),
  lie: () => ({ rot: -90, lean: 0, aL: [8, 0], aR: [-8, 0], lL: [4, 0], lR: [-4, 0] }),
  slump: () => ({ lean: 30, head: 25, aL: [5, 0], aR: [-5, 0], lL: [8, 0], lR: [-8, 0] }),
};
// Effect marks (world coords)
const shakeLines = (x, y, k = 1, c = INK) => `<g stroke="${c}" stroke-width="5" stroke-linecap="round" fill="none" opacity="${k}">${[-1, 1].map(sd => `<path d="M${x + sd * 70} ${y - 30} q${sd * 14} 30 0 60"/><path d="M${x + sd * 92} ${y - 20} q${sd * 10} 20 0 40"/>`).join('')}</g>`;
const zzz = (x, y, t) => [0, 1, 2].map(i => { const k = ((t * .6 + i / 3) % 1); return `<text x="${x + k * 60 + i * 10}" y="${y - k * 120}" font-family="Alexandria" font-weight="800" font-size="${30 + i * 12}" fill="#fff" opacity="${Math.sin(k * Math.PI)}" stroke="${INK}" stroke-width="3" paint-order="stroke">z</text>`; }).join('');
const popMark = (x, y, k, txt = '!', size = 120) => `<g transform="translate(${x} ${y}) scale(${back(k)})" opacity="${clamp(k * 3)}"><text text-anchor="middle" font-family="Alexandria" font-weight="900" font-size="${size}" fill="#fff" stroke="${INK}" stroke-width="10" paint-order="stroke">${txt}</text></g>`;
const speedLines = (x, y, dir, k = 1) => `<g stroke="#fff" stroke-width="5" stroke-linecap="round" opacity="${.7 * k}">${[0, 1, 2, 3].map(i => `<path d="M${x - dir * (90 + i * 10)} ${y - 80 + i * 50} h${-dir * (80 + (i % 2) * 50)}"/>`).join('')}</g>`;
const thought = (x, y, k, inner = '') => `<g opacity="${k}" transform="translate(${x} ${y}) scale(${.6 + .4 * back(k)})"><circle cx="-80" cy="140" r="14" fill="#fff" stroke="${INK}" stroke-width="5"/><circle cx="-50" cy="100" r="22" fill="#fff" stroke="${INK}" stroke-width="5"/><ellipse cx="40" cy="0" rx="170" ry="110" fill="#fff" stroke="${INK}" stroke-width="7"/>${inner}</g>`;
```

Rig notes (tested):
- Poses: `stand walk(t) run(t) sit sitFloor armsUp(t) shrug point facepalm think shock headGrab phone(t) lie slump`. Override any field after the spread (`{...P.phone(lt), lean: -10}`); blend with `mixPose(a, b, k)` for a reaction.
- Hands reach props with `{to:[x,y]}` and reach the face with `{to:'face'|'chin'|'head'|'mouth'}`; such arms are drawn over the head automatically.
- Attach props to hands AFTER the `stick()` call using `stick.last.handL/handR` (phone, cup, pen), and aim lights at them too (`light(...stick.last.handL, ...)`).
- In bed or behind a table: `hidden:{legs:1}` and draw the blanket/table after the character.
- `armsUp` reads best side-on; front-facing (`dir:0`) the hands sit beside the head.

---

## 6. `scene.html` (one per video)

Template (keep the head, stage, label and render loop; write SETS and SHOTS for the idea):

```html
<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="node_modules/@fontsource/alexandria/800.css"><link rel="stylesheet" href="node_modules/@fontsource/alexandria/900.css">
<style>
html,body{margin:0;background:#000}
#stage{position:relative;width:1080px;height:1920px;overflow:hidden;background:#0b0d12}
#svg{position:absolute;inset:0}
#label{position:absolute;top:150px;left:50%;transform:translateX(-50%);direction:rtl;font-family:Alexandria;font-weight:800;font-size:64px;line-height:1;color:#fff;background:#0d0d0d;padding:26px 40px 30px;border-radius:26px;white-space:nowrap;box-shadow:0 6px 20px rgba(0,0,0,.35)}
#label:empty{display:none}
</style></head><body>
<div id="stage"><svg id="svg" width="1080" height="1920" viewBox="0 0 1080 1920"></svg><div id="label"></div></div>
<script src="stick.js"></script>
<script>
// ---- SETS: one function per location, world coords, returns SVG ----
function bedroom(o = {}) { return `...`; }
// ---- SHOTS: [start, end, label, (lt, t) => ({ world, light, cam })] ----
const SHOTS = [
  [0, 3.0, 'قبل النوم بـ 5 دقايق', (lt) => {
    const c = camLerp({ x: 560, y: 980, z: 1.3 }, { x: 560, y: 1000, z: 1.45 }, span(lt, 0, 3, lin)); // slow push-in
    const guy = stick({ ...P.phone(lt), x: 560, y: 1150, s: 1.15, dir: -1, lean: -14, face: { mouth: 'smile' }, acc: { cap: '#c8231f' }, hidden: { legs: 1 } });
    const prop = phone(...stick.last.handL, 15);
    return { world: bedroom() + guy + prop + blanket(1150), light: light(...stick.last.handL, 900, '#4aa3ff', .7, .5, 'p'), cam: c };
  }],
  // ...
];
const DUR = 9.0;
function render(t) {
  const sh = SHOTS.find(s => t >= s[0] && t < s[1]) || SHOTS[SHOTS.length - 1];
  const lt = t - sh[0], r = sh[3](lt, t);
  document.getElementById('svg').innerHTML = defs(Math.floor(t * 30) % 97) + cam(r.cam, r.world + paintTex() + (r.light || '')) + finish();
  document.getElementById('label').textContent = sh[2] || '';
}
window.DUR = DUR; render(0);
</script></body></html>
```

Drawing sets (this is where the "rich world" comes from):
- Build from big shapes first (wall, floor, furniture), each with a gradient or flat fill and a `#151312` outline 5-8 px. Then 3-6 detail strokes per surface: floor planks, wall bricks or plaster patches, blanket/curtain folds, wood grain, a highlight edge.
- Add one or two story props with care (the thing the joke hangs on gets the most detail: phone screens, alarm clock digits, fridge light, exam paper).
- Palette per mood: night `#262c3d` wall + navy `#26375e` fabric + warm lamp `#ffcc7a`; candle/past `#3a2a20` browns + `#ffb35c` glow; day `#e9e2d3` walls + `#f7c27a` window; office `#cfd6dd` + fluorescent `#e8f4ff`.
- Light every shot: one `light()` on the motivated source (dark .6-.8). A second light only for a second real source.
- Arabic in-world text (posters, screens) uses Alexandria 900 with `direction="rtl"`; keep it short and only when it's part of the joke. Digits come out right because the fontsource CSS loads every subset.

Framing rules (from the tests):
- Wide shots: zoom 1.3-1.6 on the set so the head is ~200-260 px on screen. Detail/face close-ups: zoom 2.4-3.5.
- Keep the action between 35% and 75% of frame height. The label owns the top 330 px, so nothing important goes behind it (pop marks included).
- Every shot moves a little: push-in 8-15% over the shot, or a slow tilt. On impacts add `shake()` to the camera. A detail shot can be a static macro of the prop.
- Time-lapse inside a shot is good comedy (candle melting, sun rising, pile growing): drive it with `span(lt, ...)`.
- Something new every ~1 s: a blink, a thumb scroll, a drip, a head turn. Idle life: `breath` via small `wob()` on `lean`/`head`, blinks by switching `eyes:'closed'` for 3 frames every ~2.5 s.
- The last shot ends in a state that matches the first (same pose or same sound), so the loop is seamless.

---

## 7. Render: `render.js` (write verbatim)

```js
// node render.js scene.html out_dir [fps=30] [workers=3]      -> out_dir/00000.jpg ...
// node render.js scene.html out_dir --stills 1,4.5,9            -> out_dir/s1.png ... (for checking)
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const [, , html, out, a3, a4] = process.argv;
  fs.mkdirSync(out, { recursive: true });
  const stills = a3 === '--stills' ? a4.split(',').map(Number) : null;
  const fps = stills ? 30 : (+a3 || 30), workers = stills ? 1 : (+a4 || 3);
  const b = await chromium.launch();
  const open = async () => {
    const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
    await p.goto('file://' + path.resolve(html));
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    return p;
  };
  const shot = async (p, t, file, png) => {
    await p.evaluate(t => render(t), t);
    await (await p.$('#stage')).screenshot({ path: file, ...(png ? {} : { type: 'jpeg', quality: 92 }) });
  };
  if (stills) { const p = await open(); for (const t of stills) await shot(p, t, `${out}/s${String(t).replace('.', '_')}.png`, 1); await b.close(); return; }
  const p0 = await open(); const n = Math.round(await p0.evaluate(() => window.DUR) * fps); await p0.close();
  let done = 0;
  await Promise.all([...Array(workers)].map(async (_, w) => {
    const p = await open();
    for (let i = w; i < n; i += workers) { await shot(p, i / fps, `${out}/${String(i).padStart(5, '0')}.jpg`); if (++done % 90 === 0) process.stdout.write(`${done}/${n} `); }
  }));
  await b.close(); console.log(`done ${n} frames`);
})();
```

Speed: about 6-7 frames/s with 4 workers, so a 30 s video renders in ~2.5 min and a 60 s video in ~4.5 min. Run the full render in the background (`run_in_background`) or with the 600 s timeout, and use 5-6 workers for 50-60 s videos.

---

## 8. Sound: `sfx.py` (write verbatim) + `cues.json`

```python
# python3 sfx.py cues.json out.wav  - synthesized SFX bed, no music
# cues.json: {"dur": 9.0, "tone": "room"|"night"|"none", "cues": [[t, "name", gain_db, {opts}], ...]}
import json, sys, numpy as np, wave
SR = 48000
rng = np.random.default_rng(1)
def env(n, a=.005, r=.1):
    t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(r, 1e-4))
def noise(d): return rng.standard_normal(int(SR * d))
def lp(x, k=.05):
    if np.ndim(k) == 0:
        from scipy.signal import lfilter
        return lfilter([k], [1, k - 1], x)
    y = np.empty_like(x); acc = 0.
    for i in range(len(x)): acc += k[i] * (x[i] - acc); y[i] = acc
    return y
def hp(x, k=.05): return x - lp(x, k)
def tone(f, d, shape='sine'):
    t = np.arange(int(SR * d)) / SR; ph = 2 * np.pi * np.cumsum(np.broadcast_to(f, t.shape) if np.ndim(f) else np.full(t.shape, f)) / SR
    return np.sin(ph) if shape == 'sine' else np.sign(np.sin(ph)) * .5 if shape == 'square' else 2 * (ph / (2 * np.pi) % 1) - 1
L = {}
def sfx(fn): L[fn.__name__] = fn; return fn
@sfx
def pop(o): d = .12; f = np.linspace(900, 300, int(SR * d)); return tone(f, d) * env(int(SR * d), .002, .03)
@sfx
def tap(o): d = .05; return hp(noise(d), .3) * env(int(SR * d), .001, .008) * .8
@sfx
def tick(o): d = .03; return tone(2500, d) * env(int(SR * d), .0005, .004)
@sfx
def whoosh(o):
    d = o.get('d', .45); n = int(SR * d); x = noise(d); t = np.linspace(0, 1, n)
    return lp(x, .02 + .25 * np.sin(np.pi * t) ** 2) * np.sin(np.pi * t) ** 2 * 3
@sfx
def thud(o): d = .35; f = np.linspace(120, 45, int(SR * d)); return (tone(f, d) + .3 * lp(noise(d), .05)) * env(int(SR * d), .002, .09)
@sfx
def clink(o):
    d = .9; n = int(SR * d); return sum(tone(f, d) * env(n, .001, r) * g for f, r, g in [(2350, .25, 1), (3720, .18, .6), (5310, .1, .4), (1180, .3, .3)]) * .5
@sfx
def ding(o): d = 1.2; n = int(SR * d); return (tone(1320, d) + .5 * tone(2640, d) + .2 * tone(3960, d)) * env(n, .002, .35) * .5
@sfx
def alarm(o):
    d = o.get('d', 3); out = np.zeros(int(SR * d)); pat = [(1568, .09), (2093, .09), (1568, .09)]; t = 0.
    while t < d - .4:
        for f, ln in pat:
            s = int(SR * t); seg = (tone(f, ln, 'square') * .6 + tone(f * 2, ln) * .2) * env(int(SR * ln), .003, .2)
            out[s:s + len(seg)] += seg[:len(out) - s]; t += ln + .03
        t += .35
    return out * .7
@sfx
def buzz(o):
    d = o.get('d', 1.5); n = int(SR * d); t = np.arange(n) / SR
    g = ((t % .6) < .4).astype(float); return tone(160, d, 'saw') * lp(g, .01) * .4
@sfx
def snore(o):
    d = o.get('d', 1.6); n = int(SR * d); t = np.linspace(0, 1, n)
    am = (1 + np.sin(2 * np.pi * 38 * t * d)) / 2; return lp(noise(d), .04) * am * np.sin(np.pi * t) ** 1.5 * 2.2
@sfx
def gasp(o):
    d = .35; n = int(SR * d); t = np.linspace(0, 1, n); return hp(lp(noise(d), .25), .02) * np.sin(np.pi * t) ** .6 * 1.4
@sfx
def boing(o):
    d = .6; n = int(SR * d); t = np.arange(n) / SR; f = 220 + 90 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 4); return tone(f, d) * env(n, .003, .25)
@sfx
def riser(o):
    d = o.get('d', 1.5); n = int(SR * d); f = np.geomspace(200, 1400, n); return tone(f, d) * np.linspace(0, 1, n) ** 2 * .35 + lp(noise(d), .1) * np.linspace(0, 1, n) ** 2 * .4
@sfx
def heartbeat(o):
    d = o.get('d', 2); out = np.zeros(int(SR * d)); t = 0.
    while t < d - .3:
        for dt in (0, .18):
            s = int(SR * (t + dt)); seg = thud({})[: int(SR * .25)] * (1 if dt == 0 else .7); out[s:s + len(seg)] += seg[:len(out) - s]
        t += .8
    return out
@sfx
def scratch(o):
    d = .45; n = int(SR * d); t = np.linspace(0, 1, n); return hp(noise(d), .2) * np.abs(np.sin(2 * np.pi * 7 * t)) * (1 - t) * 1.2
@sfx
def sting(o):
    d = 1.0; n = int(SR * d); f = np.linspace(330, 180, n); return (tone(f, d, 'saw') * .3 + tone(f / 2, d) * .4) * env(n, .01, .5)
def bed(kind, d):
    n = int(SR * d)
    if kind == 'none': return np.zeros(n)
    x = lp(noise(d), .008) * (2.5 if kind == 'room' else 3.5)
    if kind == 'night':
        t = np.arange(n) / SR; x += tone(4300, d) * (((t * 14) % 1) < .25) * ((t % 2.3) < .9) * .02
    return x * .25
def main():
    cfg = json.load(open(sys.argv[1])); d = cfg['dur']; out = bed(cfg.get('tone', 'room'), d)
    for c in cfg['cues']:
        t, name, gdb = c[0], c[1], c[2] if len(c) > 2 else 0; o = c[3] if len(c) > 3 else {}
        s = L[name](o) * 10 ** (gdb / 20); i = int(SR * t); out[i:i + len(s)] += s[:max(0, len(out) - i)]
    out = out / max(1e-6, np.abs(out).max()) * .89
    st = np.stack([out, out], 1); w = wave.open(sys.argv[2], 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((st * 32767).astype('<i2').tobytes()); w.close()
main()
```

Sounds: `pop tap tick whoosh thud clink ding alarm(d) buzz(d) snore(d) gasp boing riser(d) heartbeat(d) scratch sting`. Add a new one in the same pattern when the idea needs it (door creak, pour, keyboard).

Cue rules: room tone under everything; small foley on every visible action (each tap/drip/step); the big sound lands exactly on the cut it carries; 0.3-0.6 s of near-silence right before the punchline; the end sound continues into frame 0 of the loop.

---

## 9. Encode and check

```bash
node render.js scene.html stills --stills <middle of each shot + punch moments>
ffmpeg -y -i stills/sA.png -i stills/sB.png ... -filter_complex "...scale=360:-1...hstack" stills/row.jpg   # look at it
python3 sfx.py cues.json sfx.wav
node render.js scene.html frames 30 4
ffmpeg -v error -y -framerate 30 -i frames/%05d.jpg -i sfx.wav -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -af loudnorm=I=-14:TP=-1.5 -shortest out.mp4
ffmpeg -v error -y -i out.mp4 -vf "fps=1.5,scale=216:-1,tile=7x3" sheet.jpg        # look at it
```

Stills check (fix and re-render before the full render): character and face readable at phone size; each hand touches its prop; nothing important behind the label; no limb crossing the face by accident; light pool on the subject, not on an empty corner; the joke's key detail is legible in its close-up.

Final check: duration is within ±3 s of the length he chose, cuts land on their sounds, the label changes exactly at the cut, the loop point looks and sounds continuous, no black or blank frame.

---

## 10. Higgsfield route (only when he asks)

Same plan, same shot table, same label and sound; only the pictures change.

1. `balance`, then price one keyframe and one clip with `get_cost:true`; say the total in one line and continue.
2. Character sheet per character: `generate_image`, model `gpt_image_2_6`, quality `high`, 16:9: front, side, 3/4 views of the character. Style block for every image prompt:
   > 2D cartoon stickman comedy illustration. Perfectly round oversized white head with soft grey shading and a thick black outline, simple face (dot eyes, small expressive mouth), short thin solid-black stick body and limbs with even thick line weight, round white cartoon glove hands, chunky brown shoes. Richly detailed painterly digital background with visible texture (fabric weave, plaster, wood grain), dark cartoon outlines on objects, cinematic motivated lighting from <source>, strong vignette. Simple character, detailed world. No text, no captions, no logos, no watermark.
3. Keyframes: `generate_image_batch`, one per shot, 9:16, the sheet's job id in `medias` with role `image_references`. Look at every result; regenerate a bad one once.
4. Clips: `generate_video_batch`, model `seedance_2_5`, `mode: omni_reference`, keyframe job id as `start_image`, `aspect_ratio: 9:16`, `duration: 4`, `resolution: 720p`, `generate_audio: false`. Prompt: one action + one camera move + "keep the exact art style and character from the start image, no new characters, no text, no scene cut". Wait with `jobs_wait`.
5. Assemble: try `curl` on the result URLs locally. If the CDN is blocked, do the trimming/concat in `sandbox_exec` (ffmpeg there), render the label PNGs locally with Playwright, `media_upload` them, and curl them into the sandbox. Trim each clip to its planned length, hard-cut concat, scale to 1080x1920, overlay the label per shot, mux with `sfx.py` audio, loudnorm -14. Upload the result with `media_upload` + PUT + `media_confirm` and give him the link if the file can't come back here.

---

## 11. Deliver

Send the MP4 with the file-send tool and one line in Egyptian Arabic (what the video is, its length). Then offer, in one line, a caption + hashtags or a change. Don't recap the steps. Credit nobody else's characters; the cast is always original.