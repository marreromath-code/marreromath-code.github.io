const fs = require('fs');
let SEQ = 0;
const pad = n => String(n).padStart(4, '0');
const rnd = (lo, hi) => Math.floor(Math.random() * (hi - lo + 1)) + lo;
const pick = a => a[Math.floor(Math.random() * a.length)];
const N = n => (n < 0 ? '−' + (-n) : '' + n);            // number with minus glyph
const pt = (x, y) => `(${N(x)}, ${N(y)})`;
const sg = n => (n < 0 ? '− ' + (-n) : '+ ' + n);

// ---- SVG coordinate-plane line graph (world -9..9), with marker dots ----
function lineGraph(slopeVal, intercept, dots = []) {
  const min = -9, max = 9, unit = 18, cx = 180, cy = 180, W = 360;
  const sx = x => cx + x * unit, sy = y => cy - y * unit;
  let s = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${W}" width="${W}" height="${W}" font-family="Inter,Arial,sans-serif" font-size="11">`;
  s += `<rect width="${W}" height="${W}" fill="#ffffff"/>`;
  for (let i = min; i <= max; i++) {
    s += `<line x1="${sx(i)}" y1="${sy(min)}" x2="${sx(i)}" y2="${sy(max)}" stroke="#e3ddcd"/>`;
    s += `<line x1="${sx(min)}" y1="${sy(i)}" x2="${sx(max)}" y2="${sy(i)}" stroke="#e3ddcd"/>`;
  }
  s += `<line x1="${sx(min)}" y1="${cy}" x2="${sx(max)}" y2="${cy}" stroke="#1a1a2e" stroke-width="2"/>`;
  s += `<line x1="${cx}" y1="${sy(min)}" x2="${cx}" y2="${sy(max)}" stroke="#1a1a2e" stroke-width="2"/>`;
  s += `<polygon points="${sx(max)},${cy} ${sx(max) - 7},${cy - 4} ${sx(max) - 7},${cy + 4}" fill="#1a1a2e"/>`;
  s += `<polygon points="${cx},${sy(max)} ${cx - 4},${sy(max) + 7} ${cx + 4},${sy(max) + 7}" fill="#1a1a2e"/>`;
  s += `<text x="${sx(max) - 2}" y="${cy + 16}">x</text><text x="${cx + 7}" y="${sy(max) + 9}">y</text>`;
  for (let i = min; i <= max; i += 3) { if (i === 0) continue; s += `<text x="${sx(i) - 4}" y="${cy + 14}" fill="#5a5a7a">${i}</text><text x="${cx + 5}" y="${sy(i) + 4}" fill="#5a5a7a">${i}</text>`; }
  const y1 = slopeVal * min + intercept, y2 = slopeVal * max + intercept;
  s += `<line x1="${sx(min)}" y1="${sy(y1)}" x2="${sx(max)}" y2="${sy(y2)}" stroke="#1a2744" stroke-width="3"/>`;
  for (const [dx, dy] of dots) s += `<circle cx="${sx(dx)}" cy="${sy(dy)}" r="3.6" fill="#b8960c"/>`;
  s += `</svg>`;
  return s;
}
function mc({ stem, figure, correct, distractors, explanation, diff = 2, dom = 'Algebra' }) {
  const seen = new Set([correct]); const ds = [];
  for (const d of distractors) { if (!seen.has(d)) { seen.add(d); ds.push(d); } if (ds.length === 3) break; }
  let b = 1; while (ds.length < 3) { const c = correct + ' (' + b++ + ')'; if (!seen.has(c)) { seen.add(c); ds.push(c); } }
  const opts = [correct, ...ds];
  for (let i = opts.length - 1; i > 0; i--) { const j = rnd(0, i); [opts[i], opts[j]] = [opts[j], opts[i]]; }
  return { question_id: 'fig' + pad(++SEQ), section: 'math', section_name: 'Math', domain: dom, difficulty: diff, difficulty_label: ['', 'Easy', 'Medium', 'Hard'][diff], type: 'mc', passage: '', figure, stem, choices: opts, answer_index: opts.indexOf(correct), answer_text: correct, explanation, is_premium: false, active: true };
}
const Q = []; const add = q => Q.push(q);
const fmtSlope = (p, q) => q === 1 ? N(p) : `${N(p)}/${q}`;
const eqStr = (p, q, b) => { let c = q === 1 ? (p === 1 ? '' : p === -1 ? '−' : N(p)) : `(${N(p)}/${q})`; return `y = ${c}x ${sg(b)}`; };
const gcd = (a, b) => b ? gcd(b, a % b) : Math.abs(a);
const fmtFrac = (nn, dd) => { if (dd < 0) { nn = -nn; dd = -dd; } const g = gcd(nn, dd) || 1; nn /= g; dd /= g; return dd === 1 ? N(nn) : `${N(nn)}/${dd}`; };

/* 1) y-intercept from graph */
function yints(n) {
  for (let i = 0; i < n; i++) {
    const m = pick([1, 2, -1, -2, 1]), b = rnd(-6, 6) || 3;
    const correctY = pt(0, b);
    const candY = [pt(b, 0), pt(0, -b), pt(-b, 0), pt(b, b)].filter(c => c !== correctY);
    add(mc({ figure: lineGraph(m, b, [[0, b]]), diff: 2,
      stem: 'The graph of the linear function f is shown, where y = f(x). What is the y-intercept of the graph of f?',
      correct: correctY, distractors: candY,
      explanation: `The y-intercept is where the line crosses the y-axis. Here the line crosses at y = ${N(b)}, so the y-intercept is ${pt(0, b)}.` }));
  }
}
/* 2) x-intercept from graph */
function xints(n) {
  for (let i = 0; i < n; i++) {
    const m = pick([1, 2, -1, -2]); let xi = rnd(-6, 6) || 4; const b = -m * xi;
    if (Math.abs(b) > 8) { i--; continue; }
    const correctX = pt(xi, 0);
    const candX = [pt(0, xi), pt(0, b), pt(-xi, 0), pt(b, 0), pt(xi, b)].filter(c => c !== correctX);
    add(mc({ figure: lineGraph(m, b, [[xi, 0]]), diff: 2,
      stem: 'The graph of the linear function f is shown, where y = f(x). What is the x-intercept of the graph of f?',
      correct: correctX, distractors: candX,
      explanation: `The x-intercept is where the line crosses the x-axis. Here the line crosses at x = ${N(xi)}, so the x-intercept is ${pt(xi, 0)}.` }));
  }
}
/* 3) slope from graph */
function slopes(n) {
  const SL = [[1, 1], [2, 1], [1, 2], [1, 3], [3, 1], [-1, 1], [-2, 1], [-1, 2], [3, 2], [2, 3]];
  for (let i = 0; i < n; i++) {
    const [p, q] = SL[i % SL.length]; const b = rnd(-3, 3); const val = p / q;
    let d = q; if (Math.abs(b + val * d) > 9) d = -q;
    const correctS = fmtFrac(p, q);
    const cand = [fmtFrac(-p, q), fmtFrac(q, p), fmtFrac(p + 1, q), fmtFrac(p - 1, q), fmtFrac(2 * p, q)].filter(c => c !== correctS);
    add(mc({ figure: lineGraph(val, b, [[0, b], [d, b + val * d]]), diff: 2,
      stem: 'The graph of the linear function f is shown. What is the slope of the graph of f?',
      correct: correctS, distractors: cand,
      explanation: `Slope = rise/run. From the two marked lattice points the line rises ${N(p)} for every ${q} unit(s) of run, so the slope is ${fmtSlope(p, q)}.` }));
  }
}
/* 4) match graph to equation */
function eqs(n) {
  for (let i = 0; i < n; i++) {
    const m = pick([1, 2, -1, -2, 3]); let b = rnd(-5, 5) || 2; if (b === m || b === -m) b = m + 4;
    add(mc({ figure: lineGraph(m, b, [[0, b]]), diff: 3,
      stem: 'Which equation best represents the line shown in the xy-plane?',
      correct: eqStr(m, 1, b), distractors: [eqStr(-m, 1, b), eqStr(m, 1, -b), eqStr(b, 1, m)],
      explanation: `The line crosses the y-axis at ${N(b)} (so the constant is ${N(b)}) and has slope ${N(m)}. Thus ${eqStr(m, 1, b)}.` }));
  }
}
yints(8); xints(8); slopes(7); eqs(7);
const seen = new Set();
const uniq = Q.filter(q => { if (seen.has(q.stem + q.figure)) return false; seen.add(q.stem + q.figure); return true; });
fs.writeFileSync('base44/questions_pack7_graphs.json', JSON.stringify(uniq, null, 2));
console.log('Generated', uniq.length, 'graph questions (pack 7)');
