// engine.js — Khatt-w-Noor (خط ونور) engine. Pure: render(t) draws frame t. Any W x H.
const CFG = window.CFG || { W: 1080, H: 1920 };
const W = CFG.W, H = CFG.H, PORT = H > W;
const u = Math.min(W / 720, H / 900);                 // 1 unit = 1px of the 720x1280 reference
const GY = H * (PORT ? 0.745 : 0.84);                  // ground line
const CX = W / 2;
const MID = GY - 150 * u;                              // default centre of the action area
const SAFE = H * (PORT ? .37 : .36);                   // captions live above this line: keep every symbol below it
const OR = '#EE7B30', OR2 = '#F6A35F';
const PAL = {
  cream: { bg: '#EFE6DA', ink: '#1B1511', dark: 0 },
  peach: { bg: '#F6DEC6', ink: '#1B1511', dark: 0 },
  sand:  { bg: '#E9DFD0', ink: '#1B1511', dark: 0 },
  navy:  { bg: '#1D2131', ink: '#F1E6D8', dark: 1 },
  night: { bg: '#111915', ink: '#F1E6D8', dark: 1, stars: 1 },
};
let INK = '#1B1511', BG = PAL.cream;                   // set per beat while drawing
const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const lerp = (a, b, k) => a + (b - a) * k;
const ease = k => (k = clamp(k), k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2);
const easeOut = k => 1 - Math.pow(1 - clamp(k), 3);
const easeIn = k => Math.pow(clamp(k), 2.2);
const back = k => { k = clamp(k); const c = 1.7; return 1 + (c + 1) * Math.pow(k - 1, 3) + c * Math.pow(k - 1, 2); };
const lin = k => clamp(k);
const span = (t, a, b, f = ease) => f(clamp((t - a) / (b - a)));
const wob = (t, f = 1, a = 1, ph = 0) => Math.sin((t * f + ph) * Math.PI * 2) * a;
const rad = d => d * Math.PI / 180;
const pt = (x, y, ang, len) => [x + Math.sin(rad(ang)) * len, y + Math.cos(rad(ang)) * len]; // 0 down, 90 forward, 180 up
const rnd = s => { s = Math.sin(s * 127.1 + 311.7) * 43758.5453; return s - Math.floor(s); };
let GID = 0; const gid = () => 'k' + (GID++);
const f1 = n => Math.round(n * 10) / 10;

// ---------------- background + ground ----------------
function backdrop(p, lt = 0, scroll = 0) {
  let s = `<rect x="-10" y="-10" width="${W + 20}" height="${H + 20}" fill="${p.bg}"/>`;
  if (p.stars) for (let i = 0; i < 46; i++) {
    const x = rnd(i) * W, y = rnd(i + 99) * GY * .95, tw = .25 + .5 * (.5 + .5 * Math.sin(lt * 2 + i));
    s += `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1((1 + rnd(i + 7) * 1.4) * u)}" fill="#F1E6D8" opacity="${f1(tw * 10) / 10}"/>`;
  }
  return s;
}
function ground(p, lt = 0, scroll = 0) {
  const o = -(lt * scroll * u) % (40 * u);
  return `<line x1="-50" y1="${GY}" x2="${W + 50}" y2="${GY}" stroke="${p.ink}" stroke-opacity=".55" stroke-width="${2 * u}"/>
  <line x1="-50" y1="${GY + 20 * u}" x2="${W + 50}" y2="${GY + 20 * u}" stroke="${p.ink}" stroke-opacity=".22" stroke-width="${1.6 * u}" stroke-dasharray="${18 * u} ${22 * u}" stroke-dashoffset="${o}"/>
  <line x1="-50" y1="${GY + 42 * u}" x2="${W + 50}" y2="${GY + 42 * u}" stroke="${p.ink}" stroke-opacity=".12" stroke-width="${1.4 * u}" stroke-dasharray="${10 * u} ${30 * u}" stroke-dashoffset="${o * 1.6}"/>`;
}

// ---------------- the stickman ----------------
// Pose fields (degrees; 0 = hanging down, 90 = forward, 180 = up, negative = backward):
//   lean, head (+ = nod down / - = look up), aF/aB [shoulder, elbowBend] (front/back arm),
//   lF/lB [hip, kneeBend] (front/back leg; knee bends are negative), rot (whole body, 90 = lying, head forward)
const SK = { r: 28, torso: 118, ua: 58, la: 56, th: 84, sh: 82, lw: 10.5 };
const P = {
  stand: () => ({ lean: 0, head: 0, aF: [8, 6], aB: [-8, -4], lF: [4, 0], lB: [-4, 0] }),
  walk: (t, sp = 1.25) => { const k = Math.sin(t * sp * Math.PI * 2); return { lean: 3, head: 2, aF: [-24 * k, 16], aB: [24 * k, 16], lF: [26 * k, -Math.max(0, -38 * k) - 4], lB: [-26 * k, -Math.max(0, 38 * k) - 4], bob: Math.abs(Math.cos(t * sp * Math.PI * 2)) * 5 }; },
  run: (t, sp = 2.2) => { const k = Math.sin(t * sp * Math.PI * 2); return { lean: 14, head: 0, aF: [-50 * k, 85], aB: [50 * k, 85], lF: [44 * k, -Math.max(18, -80 * k)], lB: [-44 * k, -Math.max(18, 80 * k)], bob: Math.abs(Math.cos(t * sp * Math.PI * 2)) * 14 }; },
  lie: () => ({ rot: 90, lean: 0, head: -6, aF: [10, 0], aB: [4, 0], lF: [2, 0], lB: [-2, 0] }),
  kneel: () => ({ lean: 6, head: 6, aF: [20, 10], aB: [10, 10], lF: [4, -92], lB: [-2, -88] }),
  sad: () => ({ lean: 24, head: 22, aF: [6, 0], aB: [-2, 0], lF: [4, 0], lB: [-4, 0] }),
  raise: (t = 0) => ({ lean: -3, head: -10, aF: [168 + wob(t, .7, 4), 4], aB: [154 + wob(t, .7, 4, .3), 8], lF: [5, 0], lB: [-5, 0] }),
  dua: () => ({ lean: 2, head: -8, aF: [40, 112], aB: [30, 118], lF: [4, 0], lB: [-4, 0] }),
  kneelDua: () => ({ lean: 8, head: -6, aF: [40, 112], aB: [30, 118], lF: [4, -92], lB: [-2, -88] }),
  ask: (t = 0) => ({ lean: 0, head: -6, aF: [150 + wob(t, 1.2, 6), 22], aB: [-6, -4], lF: [5, 0], lB: [-5, 0] }),
  point: () => ({ lean: 2, head: 0, aF: [92, 0], aB: [-8, -4], lF: [6, 0], lB: [-6, 0] }),
  think: () => ({ lean: 0, head: 10, aF: [24, 148], aB: [30, 70], lF: [4, 0], lB: [-4, 0] }),
  shrug: () => ({ lean: 0, head: -4, aF: [48, 96], aB: [38, 96], lF: [6, 0], lB: [-6, 0] }),
  cheer: (t = 0) => ({ lean: -4, head: -12, aF: [150, 40 + wob(t, 2, 15)], aB: [140, 40 - wob(t, 2, 15)], lF: [10, -6], lB: [-10, -6], bob: Math.abs(wob(t, 2, 14)) }),
  sit: () => ({ lean: -6, head: 2, aF: [40, 40], aB: [-30, 10], lF: [92, -4], lB: [86, -2] }),
  bow: () => ({ lean: 62, head: 12, aF: [62, 8], aB: [56, 8], lF: [4, 0], lB: [-4, 0] }),
  lookUp: () => ({ lean: -4, head: -26, aF: [6, 4], aB: [-8, -4], lF: [4, 0], lB: [-4, 0] }),
  shock: () => ({ lean: -12, head: -8, aF: [120, 40], aB: [110, 40], lF: [10, 0], lB: [-12, 0] }),
};
const mixPose = (a, b, k) => { const o = {}; for (const key of new Set([...Object.keys(a), ...Object.keys(b)])) { const va = a[key] ?? (Array.isArray(b[key]) ? [0, 0] : 0), vb = b[key] ?? (Array.isArray(a[key]) ? [0, 0] : 0); o[key] = Array.isArray(va) ? va.map((v, i) => lerp(v, vb[i], k)) : lerp(va, vb, k); } return o; };

// fig({x, g=GY, s=1, dir=1|-1, pose, col, alpha, hl, air}) -> svg. Feet (or lowest point) land on g automatically.
// fig.last = {head:[x,y], hr, handF, handB, top:[x,y], foot:[x,y]} in world coords.
function fig(o) {
  const { x = CX, g = GY, s = 1, dir = 1, pose = P.stand(), col = INK, alpha = 1, hl = 0, air = 0 } = o;
  const p = pose, k = s * u, lean = p.lean || 0;
  const neck = pt(0, 0, 180 - lean, SK.torso), sh = pt(0, 0, 180 - lean, SK.torso - 10);
  const hc = pt(...neck, 180 - lean - (p.head || 0), SK.r + 4);
  const limb = (o2, a, L1, L2) => { const e = pt(...o2, a[0], L1); return [o2, e, pt(...e, a[0] + a[1], L2)]; };
  const AF = limb(sh, p.aF || [8, 6], SK.ua, SK.la), AB = limb(sh, p.aB || [-8, -4], SK.ua, SK.la);
  const LF = limb([0, 0], p.lF || [4, 0], SK.th, SK.sh), LB = limb([0, 0], p.lB || [-4, 0], SK.th, SK.sh);
  const rot = rad(p.rot || 0), cr = Math.cos(rot), sr = Math.sin(rot);
  const R = ([a, b]) => [a * cr - b * sr, a * sr + b * cr];
  const all = [...AF, ...AB, ...LF, ...LB, neck].map(R); const H0 = R(hc);
  let maxY = Math.max(...all.map(q => q[1]), H0[1] + SK.r);
  const oy = g - (maxY + SK.lw / 2) * k - air * u - (p.bob || 0) * k;
  const W2 = q => [x + q[0] * k * dir, oy + q[1] * k];
  const path = pts => 'M' + pts.map(q => W2(R(q)).map(f1).join(' ')).join(' L');
  const c = hl ? OR : col, lw = SK.lw * k;
  const st = (d, op = 1) => `<path d="${d}" fill="none" stroke="${c}" stroke-width="${f1(lw)}" stroke-linecap="round" stroke-linejoin="round" stroke-opacity="${op}"/>`;
  const hw = W2(H0);
  let svg = st(path(LB), .5) + st(path(AB), .5) + st(path([[0, 0], neck])) + st(path(LF)) + st(path(AF));
  svg += `<circle cx="${f1(hw[0])}" cy="${f1(hw[1])}" r="${f1(SK.r * k)}" fill="${c}"/>`;
  fig.last = { head: hw, hr: SK.r * k, handF: W2(R(AF[2])), handB: W2(R(AB[2])), top: [hw[0], hw[1] - SK.r * k], foot: W2(R(LF[2])), hip: W2([0, 0]) };
  return `<g opacity="${f1(alpha * 100) / 100}">${svg}</g>`;
}
// A row of n figures centred on cx (gap in units). fn(i) may return per-figure overrides.
function crowd(n, o = {}, fn = () => ({})) {
  const gap = (o.gap || 120) * u * (o.s || .6), x0 = (o.cx ?? CX) - gap * (n - 1) / 2; let s = ''; const heads = [];
  for (let i = 0; i < n; i++) { s += fig({ ...o, x: x0 + gap * i, ...fn(i) }); heads.push(fig.last); }
  crowd.last = heads; return s;
}

// ---------------- symbols (k = 0..1 reveal, t = local time) ----------------
function glow(x, y, r, a = .55, c = OR) { const id = gid(); return `<defs><radialGradient id="${id}"><stop offset="0" stop-color="${c}" stop-opacity="${a}"/><stop offset=".45" stop-color="${c}" stop-opacity="${a * .35}"/><stop offset="1" stop-color="${c}" stop-opacity="0"/></radialGradient></defs><circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(r)}" fill="url(#${id})"/>`; }
function rays(x, y, r1, r2, n, k = 1, t = 0, c = OR, w = 2.4) { let s = ''; for (let i = 0; i < n; i++) { const a = i / n * 360 + t * 8, L = lerp(r1, r2, .6 + .4 * Math.sin(t * 3 + i)); const [a1, b1] = pt(x, y, a, r1), [a2, b2] = pt(x, y, a, lerp(r1, L, k)); s += `<line x1="${f1(a1)}" y1="${f1(b1)}" x2="${f1(a2)}" y2="${f1(b2)}" stroke="${c}" stroke-width="${w * u}" stroke-linecap="round" opacity="${k}"/>`; } return s; }
// clip anything to above the ground line
function above(inner) { const id = gid(); return `<defs><clipPath id="${id}"><rect x="-10" y="-10" width="${W + 20}" height="${GY + 10}"/></clipPath></defs><g clip-path="url(#${id})">${inner}</g>`; }
// rising sun: k 0 = below the ground, 1 = fully up
function sun(x, k, t = 0, r = 62) { const R = r * u, y = GY + R * 1.2 - k * (R * 2.6 + 30 * u), id = gid();
  return glow(x, y, R * 3.2, .5) + `<defs><clipPath id="${id}"><rect x="-10" y="-10" width="${W + 20}" height="${GY + 10}"/></clipPath></defs><g clip-path="url(#${id})">${rays(x, y, R * 1.25, R * 1.6, 16, 1, t)}<circle cx="${f1(x)}" cy="${f1(y)}" r="${R}" fill="${OR}"/></g>`; }
// arched door standing on the ground; fill 0..1 = how lit it is
function door(x, fill = 0, t = 0, w = 110, h = 230) { const ww = w * u, hh = h * u, x0 = x - ww / 2, y0 = GY - hh;
  const d = `M${x0} ${GY} L${x0} ${y0 + ww / 2} A${ww / 2} ${ww / 2} 0 0 1 ${x0 + ww} ${y0 + ww / 2} L${x0 + ww} ${GY} Z`;
  return (fill > 0 ? glow(x, y0 + hh * .45, hh * 1.1, .45 * fill) + above(rays(x, y0 + hh * .45, hh * .62, hh * .78, 18, fill, t)) : '') +
    `<path d="${d}" fill="${OR}" fill-opacity="${.25 + .6 * fill}" stroke="${INK}" stroke-width="${2.6 * u}"/>`; }
// expanding rings (repentance / acceptance / signal)
function rings(x, y, r0, t, n = 3, c = OR) { let s = ''; for (let i = 0; i < n; i++) { const ph = ((t * .55 + i / n) % 1), r = r0 * (.55 + ph * 1.1); s += `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(r)}" fill="none" stroke="${c}" stroke-width="${2.4 * u}" opacity="${f1((1 - ph) * .9 * 100) / 100}"/>`; } return s; }
// dashed halo circle around a point
function halo(x, y, r, k = 1, t = 0, c = OR) { const L = 2 * Math.PI * r; return `<circle cx="${f1(x)}" cy="${f1(y)}" r="${f1(r)}" fill="none" stroke="${c}" stroke-width="${2.4 * u}" stroke-dasharray="${f1(9 * u)} ${f1(7 * u)}" stroke-dashoffset="${f1(-t * 20 * u)}" opacity="${k}" transform="rotate(${f1(t * 20)} ${f1(x)} ${f1(y)})"/>`; }
// scribble spiral = sin / problem / confusion
function scribble(x, y, r, k = 1, t = 0, c = INK) { let d = ''; const N = 46; for (let i = 0; i <= N * k; i++) { const a = i * .55 + t * 2, rr = r * (.15 + .85 * i / N) * (1 + .12 * Math.sin(i * 1.7)); d += (i ? 'L' : 'M') + f1(x + Math.cos(a) * rr) + ' ' + f1(y + Math.sin(a) * rr * .8); } return `<path d="${d}" fill="none" stroke="${c}" stroke-opacity=".75" stroke-width="${2.6 * u}" stroke-linecap="round" stroke-linejoin="round"/>`; }
// big X drawn stroke by stroke
function cross(x, y, sz, k = 1, c = INK) { const a = span(k, 0, .5, lin), b = span(k, .5, 1, lin), S = sz * u;
  return `<line x1="${f1(x - S)}" y1="${f1(y - S)}" x2="${f1(x - S + 2 * S * a)}" y2="${f1(y - S + 2 * S * a)}" stroke="${c}" stroke-width="${5 * u}" stroke-linecap="round" opacity="${a > 0 ? 1 : 0}"/><line x1="${f1(x + S)}" y1="${f1(y - S)}" x2="${f1(x + S - 2 * S * b)}" y2="${f1(y - S + 2 * S * b)}" stroke="${c}" stroke-width="${5 * u}" stroke-linecap="round" opacity="${b > 0 ? 1 : 0}"/>`; }
function check(x, y, sz, k = 1, c = OR) { const S = sz * u, d = `M${x - S} ${y} L${x - S * .3} ${y + S * .7} L${x + S} ${y - S * .8}`, L = S * 3.2; return `<path d="${d}" fill="none" stroke="${c}" stroke-width="${7 * u}" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="${L}" stroke-dashoffset="${L * (1 - k)}"/>`; }
// pedestal block on the ground; returns its top y in block.top
function block(x, w = 100, h = 40) { block.top = GY - h * u; return `<rect x="${f1(x - w * u / 2)}" y="${f1(GY - h * u)}" width="${f1(w * u)}" height="${f1(h * u)}" rx="${3 * u}" fill="${BG.dark ? '#3a3e52' : '#D8CCBD'}" stroke="${INK}" stroke-opacity=".6" stroke-width="${2 * u}"/>`; }
// open book with light
function book(x, y, k = 1, t = 0, s = 1) { const S = s * u, w = 44 * S, h = 56 * S; let lines = ''; for (let i = 0; i < 4; i++) for (const sd of [-1, 1]) { const yy = y - h * .3 + i * h * .2; lines += `<line x1="${f1(x + sd * w * .22)}" y1="${f1(yy)}" x2="${f1(x + sd * w * .82)}" y2="${f1(yy)}" stroke="${OR}" stroke-width="${3 * S}" stroke-linecap="round"/>`; }
  return glow(x, y, 150 * S, .5 * k) + rays(x, y, 70 * S, 92 * S, 18, k, t) + `<g opacity="${k}"><rect x="${f1(x - w - 2 * S)}" y="${f1(y - h / 2)}" width="${f1(w)}" height="${f1(h)}" rx="${3 * S}" fill="#F7D3B0"/><rect x="${f1(x + 2 * S)}" y="${f1(y - h / 2)}" width="${f1(w)}" height="${f1(h)}" rx="${3 * S}" fill="#F7D3B0"/>${lines}</g>`; }
// spotlight cone from the top onto x
function cone(x, k = 1, w = 180, c = OR) { const id = gid(), top = GY - 420 * u, ww = w * u;
  return `<defs><linearGradient id="${id}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${c}" stop-opacity="${.05 * k}"/><stop offset="1" stop-color="${c}" stop-opacity="${.38 * k}"/></linearGradient></defs><path d="M${x - 6 * u} ${top} L${x + 6 * u} ${top} L${x + ww} ${GY} L${x - ww} ${GY} Z" fill="url(#${id})"/>`; }
function bulb(x, y, k = 1, t = 0, s = 1) { const S = s * u * back(k);
  return glow(x, y, 120 * S, .5 * k) + rays(x, y, 52 * S, 70 * S, 10, k, t) + `<g opacity="${clamp(k * 3)}"><circle cx="${x}" cy="${y}" r="${30 * S}" fill="${OR}"/><rect x="${x - 13 * S}" y="${y + 26 * S}" width="${26 * S}" height="${16 * S}" rx="${3 * S}" fill="${INK}" opacity=".8"/></g>`; }
function clock(x, y, r, t, sp = 1, k = 1) { const R = r * u, [mx, my] = pt(x, y, 180 + t * 360 * sp, R * .75), [hx, hy] = pt(x, y, 180 + t * 30 * sp, R * .5);
  return `<g opacity="${k}"><circle cx="${x}" cy="${y}" r="${R}" fill="${BG.dark ? '#2a2f44' : '#FBF4EA'}" stroke="${INK}" stroke-width="${4 * u}"/><line x1="${x}" y1="${y}" x2="${f1(mx)}" y2="${f1(my)}" stroke="${OR}" stroke-width="${4 * u}" stroke-linecap="round"/><line x1="${x}" y1="${y}" x2="${f1(hx)}" y2="${f1(hy)}" stroke="${INK}" stroke-width="${5 * u}" stroke-linecap="round"/><circle cx="${x}" cy="${y}" r="${4 * u}" fill="${INK}"/></g>`; }
function heart(x, y, sz, k = 1, t = 0, c = OR) { const S = sz * u * back(k) * (1 + .06 * Math.max(0, Math.sin(t * 7)));
  return `<path d="M${x} ${y + S * .9} C${x - S * 1.6} ${y - S * .1} ${x - S * .8} ${y - S * 1.3} ${x} ${y - S * .45} C${x + S * .8} ${y - S * 1.3} ${x + S * 1.6} ${y - S * .1} ${x} ${y + S * .9}Z" fill="${c}" opacity="${clamp(k * 3)}"/>`; }
function word(x, y, str, size = 60, k = 1, c = OR, w = 700) { return `<text x="${f1(x)}" y="${f1(y)}" text-anchor="middle" direction="rtl" font-family="IBM Plex Sans Arabic" font-weight="${w}" font-size="${size * u}" fill="${c}" opacity="${clamp(k * 2)}" transform="translate(0 ${f1((1 - easeOut(k)) * 14 * u)})">${str}</text>`; }
function arrow(x1, y1, x2, y2, k = 1, c = OR) { const ex = lerp(x1, x2, k), ey = lerp(y1, y2, k), a = Math.atan2(ey - y1, ex - x1), L = 16 * u;
  return k <= 0 ? '' : `<path d="M${x1} ${y1} L${f1(ex)} ${f1(ey)} M${f1(ex - L * Math.cos(a - .5))} ${f1(ey - L * Math.sin(a - .5))} L${f1(ex)} ${f1(ey)} L${f1(ex - L * Math.cos(a + .5))} ${f1(ey - L * Math.sin(a + .5))}" fill="none" stroke="${c}" stroke-width="${4 * u}" stroke-linecap="round" stroke-linejoin="round"/>`; }
function coin(x, y, r, k = 1, t = 0) { const R = r * u * back(k), sx = Math.abs(Math.cos(t * 3)) * .7 + .3; return `<g transform="translate(${f1(x)} ${f1(y)}) scale(${f1(sx * 100) / 100} 1)" opacity="${clamp(k * 3)}"><circle r="${f1(R)}" fill="${OR}"/><circle r="${f1(R * .68)}" fill="none" stroke="#FBE3C8" stroke-width="${3 * u}"/></g>`; }
// bar chart standing on the ground; vals 0..1
function bars(x, vals, k = 1, w = 46, hmax = 260) { let s = ''; const gap = 22 * u, ww = w * u, x0 = x - (vals.length * (ww + gap) - gap) / 2;
  vals.forEach((v, i) => { const hh = hmax * u * v * span(k, i * .15, i * .15 + .5, easeOut); s += `<rect x="${f1(x0 + i * (ww + gap))}" y="${f1(GY - hh)}" width="${f1(ww)}" height="${f1(hh)}" rx="${4 * u}" fill="${i === vals.length - 1 ? OR : INK}" opacity="${i === vals.length - 1 ? 1 : .55}"/>`; }); return s; }
function phone(x, y, k = 1, s = 1) { const S = s * u; return glow(x, y, 90 * S, .35 * k) + `<g opacity="${k}"><rect x="${x - 22 * S}" y="${y - 38 * S}" width="${44 * S}" height="${76 * S}" rx="${8 * S}" fill="${INK}"/><rect x="${x - 17 * S}" y="${y - 31 * S}" width="${34 * S}" height="${58 * S}" rx="${4 * S}" fill="${OR2}"/></g>`; }
function qmark(x, y, sz = 60, k = 1, c = OR) { return word(x, y, '؟', sz, k, c, 700); }
// small head marker (target ring) above someone
function mark(x, y, k = 1, c = OR) { return `<g opacity="${k}"><circle cx="${f1(x)}" cy="${f1(y)}" r="${7 * u}" fill="none" stroke="${c}" stroke-width="${2 * u}"/><circle cx="${f1(x)}" cy="${f1(y)}" r="${2.4 * u}" fill="${c}"/></g>`; }
// particles drifting up out of a box (dissolve / vanish); k 0..1
function dust(x, y, w, h, k, seed = 1, n = 26) { let s = ''; if (k <= 0 || k >= 1) return s; for (let i = 0; i < n; i++) { const r1 = rnd(seed * 31 + i), r2 = rnd(seed * 17 + i * 3), px = x - w / 2 + r1 * w + (r2 - .5) * 60 * u * k, py = y - h / 2 + r2 * h - k * (60 + r1 * 120) * u;
  s += `<circle cx="${f1(px)}" cy="${f1(py)}" r="${f1((2 + r2 * 3) * u)}" fill="${i % 3 ? OR : INK}" opacity="${f1((1 - k) * 90) / 100}"/>`; } return s; }
// arcs radiating up from a point (mercy / blessing / broadcast)
function arcs(x, y, r0, t, n = 4, c = OR) { let s = ''; for (let i = 0; i < n; i++) { const ph = (t * .35 + i / n) % 1, r = r0 * (.4 + ph); s += `<path d="M${f1(x - r)} ${f1(y)} A${f1(r)} ${f1(r)} 0 0 1 ${f1(x + r)} ${f1(y)}" fill="none" stroke="${c}" stroke-width="${2.6 * u}" opacity="${f1((1 - ph) * 80) / 100}"/>`; } return s; }

// ---------------- captions (HTML overlay) ----------------
// Markup: *word* = orange keyword (may span words), {text} = small inline phrase (one token), / = line break.
function parseCap(src) { const toks = []; let hl = false, i = 0;
  while (i < src.length) { const c = src[i];
    if (c === ' ') { i++; continue; } if (c === '/') { toks.push({ br: 1 }); i++; continue; }
    if (c === '{') { const j = src.indexOf('}', i); toks.push({ w: src.slice(i + 1, j), sm: 1, hl }); i = j + 1; continue; }
    let w = ''; while (i < src.length && !' /{'.includes(src[i])) { if (src[i] === '*') { if (w) { toks.push({ w, hl }); w = ''; } hl = !hl; i++; continue; } w += src[i++]; }
    if (w) toks.push({ w, hl }); }
  return toks; }
function buildCaps() { const root = document.getElementById('caps'); root.innerHTML = '';
  BEATS.forEach((b, bi) => { const d = document.createElement('div'); d.className = 'cap'; b._toks = parseCap(b.text || ''); b._spans = [];
    b._toks.forEach(tk => { if (tk.br) { d.appendChild(document.createElement('br')); return; } const s = document.createElement('span'); s.textContent = tk.w; s.className = (tk.hl ? 'hl ' : '') + (tk.sm ? 'sm' : ''); d.appendChild(s); d.appendChild(document.createTextNode(' ')); b._spans.push(s); });
    root.appendChild(d); b._el = d; }); }
// word start times (relative to beat start). Uses b.w if given, else paces by word length.
function wordTimes(b) { if (b._wt) return b._wt; const n = b._spans.length; if (b.w && b.w.length === n) return (b._wt = b.w);
  const lens = b._spans.map(s => Math.max(2, s.textContent.length)), tot = lens.reduce((a, c) => a + c, 0), span0 = Math.min(b.d * .72, n * .42 + .1);
  let acc = 0; return (b._wt = lens.map(l => { const v = .12 + span0 * acc / tot; acc += l; return v; })); }
function drawCaps(t) { BEATS.forEach((b, i) => { const lt = t - b.t, on = lt > -0.01 && lt < b.d + .05; b._el.style.display = on ? 'block' : 'none'; if (!on) return;
  const out = b.hold ? 1 : 1 - span(lt, b.d - .3, b.d - .08, lin), wt = wordTimes(b);
  b._spans.forEach((s, j) => { const k = span(lt, wt[j], wt[j] + .2, easeOut); s.style.opacity = (k * out).toFixed(3); s.style.transform = `translateY(${((1 - k) * 14 * u).toFixed(1)}px)`; }); }); }

// ---------------- frame ----------------
const TD = { iris: .42, wipe: .24, fade: .35, cut: 0, none: 0 };
function scene(b, t) { const lt = t - b.t, p = PAL[b.bg] || PAL.cream; BG = p; INK = p.ink;
  const z = 1 + (b.push ?? .03) * span(lt, 0, b.d, lin), cx = b.focus ? b.focus[0] : CX, cy = b.focus ? b.focus[1] : MID;
  const inner = ground(p, lt, b.scroll || 0) + (b.draw ? b.draw(lt, t, b) : '');
  return backdrop(p, lt) + `<g transform="translate(${f1(cx)} ${f1(cy)}) scale(${z.toFixed(4)}) translate(${f1(-cx)} ${f1(-cy)})">${inner}</g>`; }
function render(t) { GID = 0;
  let i = 0; for (let j = 0; j < BEATS.length; j++) if (t >= BEATS[j].t - .06) i = j;
  const cur = BEATS[i], tr = i > 0 ? (cur.tr || 'iris') : 'cut', td = TD[tr] || 0;
  let svg = '';
  if (i > 0 && td > 0 && t < cur.t + td) {
    const p = clamp((t - (cur.t - .06)) / (td + .06)), prev = BEATS[i - 1];
    svg += scene(prev, t); const id = gid();
    if (tr === 'iris') { const [ax, ay] = cur.at || [CX, MID], R = Math.hypot(Math.max(ax, W - ax), Math.max(ay, H - ay)) * easeIn(p) + 3 * u;
      svg += `<defs><clipPath id="${id}"><circle cx="${f1(ax)}" cy="${f1(ay)}" r="${f1(R)}"/></clipPath></defs><g clip-path="url(#${id})">${scene(cur, t)}</g><circle cx="${f1(ax)}" cy="${f1(ay)}" r="${f1(R)}" fill="none" stroke="${OR}" stroke-width="${3 * u}" opacity="${f1((1 - p) * 100) / 100}"/>`; }
    else if (tr === 'wipe') { const X = W * (1 - ease(p));
      svg += `<defs><clipPath id="${id}"><rect x="${f1(X)}" y="-10" width="${W + 10}" height="${H + 20}"/></clipPath></defs><g clip-path="url(#${id})">${scene(cur, t)}</g><rect x="${f1(X - 3 * u)}" y="-10" width="${5 * u}" height="${H + 20}" fill="${OR}"/>`; }
    else svg += `<g opacity="${p.toFixed(3)}">${scene(cur, t)}</g>`;
  } else svg += scene(cur, t);
  document.getElementById('svg').innerHTML = svg; drawCaps(t); }
function meta() { return { dur: window.DUR, W, H, beats: BEATS.map(b => ({ t: b.t, d: b.d, tr: b.tr || 'iris', bg: b.bg, words: b._spans.map(s => s.textContent), sfx: b.sfx || [] })) }; }
function init() { if (window.TIMING) { if (TIMING.beats.length !== BEATS.length) throw new Error(`timing.js has ${TIMING.beats.length} beats, scene has ${BEATS.length}`); TIMING.beats.forEach((x, i) => Object.assign(BEATS[i], x)); window.DUR = TIMING.dur; }
  let t = 0; BEATS.forEach(b => { if (b.t == null) b.t = t; t = b.t + b.d; }); window.DUR = window.DUR || t;
  const st = document.getElementById('stage'); st.style.width = W + 'px'; st.style.height = H + 'px';
  const sv = document.getElementById('svg'); sv.setAttribute('width', W); sv.setAttribute('height', H); sv.setAttribute('viewBox', `0 0 ${W} ${H}`);
  buildCaps();
  BEATS.forEach(b => { const c = b._el; c.style.top = H * (PORT ? .235 : .2) + 'px'; c.style.transform = 'translateY(-50%)'; c.style.fontSize = (b.size || 1) * (PORT ? 64 : 54) * u + 'px'; c.style.lineHeight = '1.45'; c.style.setProperty('--ink', (PAL[b.bg] || PAL.cream).ink); });
  render(0); }
