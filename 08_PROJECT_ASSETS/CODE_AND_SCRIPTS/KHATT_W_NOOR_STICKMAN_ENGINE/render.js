// node render.js scene.html out_dir [fps=30] [workers=2] [W] [H]   -> out_dir/00000.jpg ...
// node render.js scene.html out_dir --stills 1,4.5,9 [W] [H]        -> out_dir/s1.png ... (for checking)
// node render.js scene.html out_dir --meta [W] [H]                  -> out_dir/meta.json (beats, words, transitions)
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const a = process.argv.slice(2), [html, out] = a, stills = a[2] === '--stills' ? a[3].split(',').map(Number) : null, metaOnly = a[2] === '--meta';
  const rest = metaOnly ? a.slice(3) : a.slice(4), fps = stills ? 30 : (+a[2] || 30), workers = stills ? 1 : (+a[3] || 2);
  const Wd = +(rest[0] || 1080), Hd = +(rest[1] || 1920);
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const errs = [];
  const open = async () => {
    const p = await b.newPage({ viewport: { width: Wd, height: Hd }, deviceScaleFactor: 1 });
    p.on('pageerror', e => errs.push(String(e)));
    await p.goto('file://' + path.resolve(html) + `?w=${Wd}&h=${Hd}`);
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
    return p;
  };
  const shot = async (p, t, file, png) => { await p.evaluate(t => render(t), t); await (await p.$('#stage')).screenshot({ path: file, ...(png ? {} : { type: 'jpeg', quality: 93 }) }); };
  if (metaOnly) { const p = await open(); fs.writeFileSync(`${out}/meta.json`, JSON.stringify(await p.evaluate(() => meta()), null, 1)); await b.close(); console.log('meta ->', `${out}/meta.json`, 'errors:', errs.length ? errs.join('\n') : 'none'); return; }
  if (stills) { const p = await open(); for (const t of stills) await shot(p, t, `${out}/s${String(t).replace('.', '_')}.png`, 1); await b.close(); console.log('errors:', errs.length ? errs.join('\n') : 'none'); return; }
  const p0 = await open(); const n = Math.round(await p0.evaluate(() => window.DUR) * fps); await p0.close();
  let done = 0; const t0 = Date.now();
  await Promise.all([...Array(workers)].map(async (_, w) => {
    const p = await open();
    for (let i = w; i < n; i += workers) { await shot(p, i / fps, `${out}/${String(i).padStart(5, '0')}.jpg`); if (++done % 150 === 0) console.log(`${done}/${n} ${((Date.now() - t0) / done).toFixed(0)}ms/frame`); }
  }));
  await b.close(); console.log(`done ${n} frames in ${((Date.now() - t0) / 1000).toFixed(0)}s; errors: ${errs.length ? errs.join('\n') : 'none'}`);
})();
