# python3 sfx.py meta.json out.wav
# Sound effects only (no music), synthesized, timed from meta.json (render.js --meta). No samples, no network.
# Auto: 'whoosh' on every wipe, 'swell' on every iris, 'soft' on fades.
# Per beat: beat.sfx = [[lt, name, gain_db], ...]  names: pop tick click chime ding thud step sparkle riser heartbeat whoosh swell soft
import json, sys, wave, numpy as np
from scipy.signal import lfilter, fftconvolve
SR = 44100
meta = json.load(open(sys.argv[1])); OUT = sys.argv[2]; rng = np.random.default_rng(1)
DUR = meta['dur'] + 0.3; N = int(SR * DUR)
def lp(x, fc): a = np.exp(-2 * np.pi * fc / SR); return lfilter([1 - a], [1, -a], x)
def hp(x, fc): return x - lp(x, fc)
def env(n, a, r): t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / max(r, 1e-4))
def sine(f, n): return np.sin(2 * np.pi * np.cumsum(np.broadcast_to(f, (n,)).astype(float)) / SR)
def noise(n): return rng.standard_normal(n)
def mtof(m): return 440 * 2 ** ((m - 69) / 12)
def put(buf, t, x, g=1.0):
    i = int(t * SR)
    if i >= len(buf) or i + len(x) <= 0: return
    j = max(0, -i); x = x[j:]; i = max(0, i); buf[i:i + len(x)] += g * x[:len(buf) - i]
def whoosh(d=.45):
    n = int(SR * d); k = np.linspace(0, 1, n); x = noise(n); y = np.zeros(n); a = np.exp(-2 * np.pi * (300 + 3500 * np.sin(np.pi * k) ** 2) / SR); acc = 0.
    for i in range(n): acc = a[i] * acc + (1 - a[i]) * x[i]; y[i] = acc
    return hp(y, 150) * np.sin(np.pi * k) ** 2 * 3.2
def swell(d=.62):
    n = int(SR * d); k = np.linspace(0, 1, n); x = lp(hp(noise(n), 800), 7000) * k ** 2.5 * .5 + .25 * sine(np.linspace(mtof(76), mtof(88), n), n) * k ** 3
    return x * np.minimum(1, (1 - k) * 12)
def soft(d=.5): n = int(SR * d); return lp(noise(n), 900) * np.sin(np.pi * np.linspace(0, 1, n)) * .6
def pop(d=.12): n = int(SR * d); return sine(np.linspace(900, 320, n), n) * env(n, .002, .03)
def tick(d=.04): n = int(SR * d); return sine(2600, n) * env(n, .0005, .005)
def click(d=.03): n = int(SR * d); return hp(noise(n), 2000) * env(n, .0005, .004) * .8
def chime(d=1.6): n = int(SR * d); return sum(sine(mtof(m), n) * g for m, g in [(84, 1), (91, .4), (96, .25)]) * env(n, .003, .45) * .45
def ding(d=1.0): n = int(SR * d); return (sine(1320, n) + .5 * sine(2640, n)) * env(n, .002, .3) * .5
def thud(d=.4): n = int(SR * d); return (sine(np.linspace(110, 40, n), n) + .3 * lp(noise(n), 300)) * env(n, .002, .1)
def step(d=.09): n = int(SR * d); return lp(noise(n), 700) * env(n, .001, .02) * 1.4
def sparkle(d=.9):
    out = np.zeros(int(SR * d)); m = int(SR * .25)
    for i in range(8): put(out, i * .07, sine(mtof(88 + 3 * (i % 4)), m) * env(m, .002, .07), .4)
    return out
def riser(d=1.2): n = int(SR * d); k = np.linspace(0, 1, n); return (sine(np.geomspace(220, 1200, n), n) * .3 + lp(noise(n), 2500) * .5) * k ** 2
def heartbeat(d=1.6):
    out = np.zeros(int(SR * d))
    for s, g in [(0, 1), (.18, .7), (.8, 1), (.98, .7)]:
        if s < d - .25: put(out, s, thud(.25), g)
    return out
SFX = dict(whoosh=whoosh, swell=swell, soft=soft, pop=pop, tick=tick, click=click, chime=chime, ding=ding, thud=thud, step=step, sparkle=sparkle, riser=riser, heartbeat=heartbeat)
fx = np.zeros(N)
for i, b in enumerate(meta['beats']):
    if i > 0:
        tr = b.get('tr', 'iris')
        if tr == 'wipe': put(fx, b['t'] - .22, whoosh(), .55)
        elif tr == 'iris': put(fx, b['t'] - .5, swell(), .5)
        elif tr == 'fade': put(fx, b['t'] - .2, soft(), .4)
    for c in b.get('sfx', []):
        g = 10 ** ((c[2] if len(c) > 2 else 0) / 20); put(fx, b['t'] + c[0], SFX[c[1]](), .5 * g)
n = int(SR * .8); ir = noise(n) * np.exp(-np.arange(n) / SR * 8); ir = lp(ir, 5000); ir /= np.abs(ir).sum() ** .5 * 6
fx = fx * .85 + fftconvolve(fx, ir)[:N] * .15                      # small room so the effects don't sound dry
fx = fx / max(1e-6, np.abs(fx).max()) * .85
st = np.stack([fx, np.roll(fx, int(SR * .008)) * .97], 1)
w = wave.open(OUT, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype('<i2').tobytes()); w.close()
print(f'{OUT}: {DUR:.1f}s, sfx only')
