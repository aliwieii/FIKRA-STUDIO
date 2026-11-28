# python3 -I sync.py voice_file meta.json timing.js [lead=0.35] [tail=1.3] [model_dir=/tmp/asr/small]
# Times every caption word to a voice recording and writes timing.js (window.TIMING) for the scene.
#  1) ASR mode (preferred): faster-whisper word timestamps, matched to the script words (fuzzy DP),
#     unmatched words interpolated between matched neighbours by letter count.
#  2) Fallback (no model): energy-based pauses + DP over each beat's letter count.
import json, subprocess, sys, os, re, difflib, numpy as np
voice, metaf, outf = sys.argv[1:4]
LEAD = float(sys.argv[4]) if len(sys.argv) > 4 else .35
TAIL = float(sys.argv[5]) if len(sys.argv) > 5 else 1.3
MODEL = sys.argv[6] if len(sys.argv) > 6 else '/tmp/asr/small'
SR = 16000
pcm = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-i', voice, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout, np.float32)
meta = json.load(open(metaf)); B = meta['beats']; NB = len(B)
def norm(w):
    w = re.sub(r'[\u064B-\u0652\u0670\u0640]', '', w); w = re.sub(r'[^\w]', '', w)
    return w.translate(str.maketrans('أإآىة', 'ااايه'))
letters = lambda w: max(1, len(norm(w)))
SW = [(k, w) for k, b in enumerate(B) for w in b['words']]                      # script words in order
times = [None] * len(SW); mode = ''
if os.path.exists(os.path.join(MODEL, 'model.bin')):
    from faster_whisper import WhisperModel
    m = WhisperModel(MODEL, device='cpu', compute_type='int8', cpu_threads=os.cpu_count() or 2)
    segs, _ = m.transcribe(pcm, language='ar', word_timestamps=True, beam_size=5, temperature=0.0, condition_on_previous_text=False)  # no initial_prompt: it makes Arabic loop
    A = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words if w.word.strip()]
    if A:
        n, q = len(SW), len(A); sim = lambda i, j: difflib.SequenceMatcher(None, norm(SW[i][1]), norm(A[j][0])).ratio()
        F = np.zeros((n + 1, q + 1)); bt = np.zeros((n + 1, q + 1), int)
        for i in range(1, n + 1):
            for j in range(1, q + 1):
                s = sim(i - 1, j - 1); best, arg = F[i - 1][j], 1
                if F[i][j - 1] > best: best, arg = F[i][j - 1], 2
                if s >= .45 and F[i - 1][j - 1] + s > best: best, arg = F[i - 1][j - 1] + s, 3
                F[i][j], bt[i][j] = best, arg
        i, j = n, q
        while i and j:
            if bt[i][j] == 3: times[i - 1] = A[j - 1][1]; i -= 1; j -= 1
            elif bt[i][j] == 1: i -= 1
            else: j -= 1
        matched = sum(t is not None for t in times)
        mode = f'asr: {matched}/{len(SW)} words matched'
        if matched < .7 * len(SW): print('LOW MATCH - what the recording says:\n' + ' '.join(w for w, _, _ in A))
        end_speech = A[-1][2]
if not any(t is not None for t in times):
    # ---- fallback: pauses by energy ----
    hop = 160; nf = len(pcm) // hop; rms = np.sqrt((pcm[:nf * hop].reshape(nf, hop) ** 2).mean(1)) + 1e-9
    db = 20 * np.log10(rms / np.percentile(rms, 99)); fl, tp = np.percentile(db, 12), np.percentile(db, 92); on = db > fl + max(7, (tp - fl) * .38)
    iv, a = [], None
    for i, v in enumerate(list(on) + [False]):
        if v and a is None: a = i
        if not v and a is not None: iv.append([a * .01, i * .01]); a = None
    merged = [iv[0]]
    for s, e in iv[1:]:
        if s - merged[-1][1] < .14: merged[-1][1] = e
        else: merged.append([s, e])
    iv = [x for x in merged if x[1] - x[0] >= .07]
    cb = np.array([sum(letters(w) for w in b['words']) or 1 for b in B], float); dur = np.array([e - s for s, e in iv]); S = np.concatenate([[0], np.cumsum(dur)]); rate = S[-1] / cb.sum()
    gl = [iv[i + 1][0] - iv[i][1] for i in range(len(iv) - 1)]
    cost = lambda k, i0, i1: (((S[i1 + 1] - S[i0]) - cb[k] * rate) / max(cb[k] * rate, .6)) ** 2
    INF = 1e18; f = np.full((NB, len(iv)), INF); bk = np.zeros((NB, len(iv)), int)
    for i1 in range(len(iv)): f[0][i1] = cost(0, 0, i1)
    for k in range(1, NB):
        for i1 in range(k, len(iv)):
            for j in range(k - 1, i1):
                c = f[k - 1][j] + cost(k, j + 1, i1) - 1.6 * min(gl[j], 1) + (.6 if gl[j] < .2 else 0)
                if c < f[k][i1]: f[k][i1], bk[k][i1] = c, j
    ends = [len(iv) - 1]
    for k in range(NB - 1, 0, -1): ends.append(bk[k][ends[-1]])
    ends = ends[::-1]; idx = 0
    for k in range(NB):
        ivs = iv[(0 if k == 0 else ends[k - 1] + 1):ends[k] + 1]; d = np.array([e - s for s, e in ivs]); c = np.concatenate([[0], np.cumsum(d)])
        L = np.array([letters(w) for w in B[k]['words']], float); st = np.concatenate([[0], np.cumsum(L)[:-1]]) / L.sum()
        for fr in st:
            qq = fr * c[-1]; ii = min(np.searchsorted(c, qq, 'right') - 1, len(ivs) - 1); times[idx] = ivs[ii][0] + qq - c[ii]; idx += 1
    end_speech = iv[-1][1]; mode = 'pauses (no ASR model) - check the sync by ear'
# ---- fill unmatched words by letters between anchors ----
cum = np.concatenate([[0], np.cumsum([letters(w) for _, w in SW])])
anc = [i for i, t in enumerate(times) if t is not None]
for i in range(len(SW)):
    if times[i] is not None: continue
    p = max([a for a in anc if a < i], default=None); nx = min([a for a in anc if a > i], default=None)
    if p is not None and nx is not None: times[i] = times[p] + (times[nx] - times[p]) * (cum[i] - cum[p]) / (cum[nx] - cum[p])
    elif p is not None: times[i] = times[p] + (cum[i] - cum[p]) / 13
    else: times[i] = max(0, times[nx] - (cum[nx] - cum[i]) / 13)
for i in range(1, len(times)): times[i] = max(times[i], times[i - 1] + .06)
# ---- beats ----
abs_w = [[] for _ in range(NB)]
for (k, _), t in zip(SW, times): abs_w[k].append(LEAD + t)
ts = [0.0]
for k in range(1, NB):
    first = abs_w[k][0] if abs_w[k] else ts[-1] + 1.5; prev_last = abs_w[k - 1][-1] if abs_w[k - 1] else ts[-1]
    ts.append(max(first - .32, prev_last + .35, ts[-1] + .6))
dur_total = round(max(LEAD + end_speech, abs_w[-1][-1] + .6 if abs_w[-1] else 0) + TAIL, 2)
beats = []
for k in range(NB):
    t = ts[k]; d = (ts[k + 1] if k + 1 < NB else dur_total) - t
    beats.append({'t': round(t, 3), 'd': round(d, 3), 'w': [round(max(.05, v - t), 3) for v in abs_w[k]]})
open(outf, 'w').write('window.TIMING = ' + json.dumps({'dur': dur_total, 'lead': LEAD, 'beats': beats}, ensure_ascii=False) + ';\n')
print(f'mode: {mode} | video {dur_total}s (voice starts at {LEAD}s)')
for k, b in enumerate(beats): print(f'{k:2d} t={b["t"]:6.2f} d={b["d"]:5.2f}  {" ".join(B[k]["words"])[:46]}')
