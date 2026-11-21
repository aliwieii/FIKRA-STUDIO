#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, '..');
const wordsPath = path.join(root, 'src/data/words.json');
const videoPath = path.join(root, 'src/Video.tsx');
const captionPath = path.join(root, 'src/components/ArabicCaptionOverlay.tsx');

const errors = [];
const data = JSON.parse(fs.readFileSync(wordsPath, 'utf-8'));

if (typeof data.duration !== 'number' || data.duration <= 0) {
  errors.push('words.json duration must be > 0');
}
if (!Array.isArray(data.lines) || data.lines.length === 0) {
  errors.push('words.json must contain at least one timed line');
} else {
  let prevLineEnd = 0;
  for (const [li, line] of data.lines.entries()) {
    if (!Array.isArray(line.words) || line.words.length === 0) {
      errors.push(`line[${li}] has no words`);
      continue;
    }
    if (line.start < prevLineEnd - 0.001) {
      errors.push(`line[${li}] overlaps previous line`);
    }
    prevLineEnd = line.end;
    let prevWEnd = 0;
    for (const [wi, w] of line.words.entries()) {
      if (!w.w || typeof w.start !== 'number' || typeof w.end !== 'number' || w.end <= w.start) {
        errors.push(`line[${li}].words[${wi}] invalid timing`);
      }
      if (w.start < prevWEnd - 0.001) {
        errors.push(`line[${li}].words[${wi}] overlaps previous word`);
      }
      prevWEnd = w.end;
    }
    // Verify zero-drop pagination invariant for maxWordsPerLine=6
    const pages = [];
    for (let i = 0; i < line.words.length; i += 6) pages.push(line.words.slice(i, i + 6));
    const flattened = pages.flat().length;
    if (flattened !== line.words.length) {
      errors.push(`Pagination dropped words: ${flattened} != ${line.words.length}`);
    }
  }
}

const videoSrc = fs.readFileSync(videoPath, 'utf-8');
if (videoSrc.includes('const SCENES: Scene[] = [];')) {
  errors.push('Video.tsx SCENES registry is empty');
}

const capSrc = fs.readFileSync(captionPath, 'utf-8');
if (capSrc.includes('.slice(0, maxWordsPerLine)')) {
  errors.push('ArabicCaptionOverlay.tsx still contains truncating .slice(0, maxWordsPerLine)');
}

if (errors.length > 0) {
  console.error(JSON.stringify({ pass: false, errors }, null, 2));
  process.exit(1);
}
console.log(JSON.stringify({
  pass: true,
  lines: data.lines.length,
  total_words: data.lines.reduce((acc, l) => acc + l.words.length, 0),
  duration_sec: data.duration,
}, null, 2));
