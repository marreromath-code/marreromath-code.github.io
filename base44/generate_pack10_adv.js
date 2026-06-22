const fs = require('fs');
let SEQ = 0;
const pad = n => String(n).padStart(4, '0');
const rnd = (lo, hi) => Math.floor(Math.random() * (hi - lo + 1)) + lo;
const pick = a => a[Math.floor(Math.random() * a.length)];
const sg = n => (n < 0 ? '− ' + (-n) : '+ ' + n);
const N = n => (n < 0 ? '−' + (-n) : '' + n);
function quad(a, b, c) { let s = (a === 1 ? '' : a === -1 ? '−' : a) + 'x²'; if (b !== 0) s += (b < 0 ? ' − ' : ' + ') + (Math.abs(b) === 1 ? '' : Math.abs(b)) + 'x'; if (c !== 0) s += (c < 0 ? ' − ' : ' + ') + Math.abs(c); return s; }

// ---- parabola on a grid (SVG) ----
function parabola(f, dots = []) {
  const min = -6, max = 6, unit = 22, cx = 150, cy = 150, W = 300;
  const sx = x => cx + x * unit, sy = y => cy - y * unit;
  let s = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${W}" width="${W}" height="${W}" font-family="Inter,Arial,sans-serif" font-size="11" fill="#1a1a2e">`;
  s += `<rect width="${W}" height="${W}" fill="#ffffff"/>`;
  for (let i = min; i <= max; i++) { s += `<line x1="${sx(i)}" y1="${sy(min)}" x2="${sx(i)}" y2="${sy(max)}" stroke="#e3ddcd"/><line x1="${sx(min)}" y1="${sy(i)}" x2="${sx(max)}" y2="${sy(i)}" stroke="#e3ddcd"/>`; }
  s += `<line x1="${sx(min)}" y1="${cy}" x2="${sx(max)}" y2="${cy}" stroke="#1a1a2e" stroke-width="1.6"/><line x1="${cx}" y1="${sy(min)}" x2="${cx}" y2="${sy(max)}" stroke="#1a1a2e" stroke-width="1.6"/>`;
  for (let i = min; i <= max; i += 2) { if (!i) continue; s += `<text x="${sx(i) - 3}" y="${cy + 12}" fill="#5a5a7a">${i}</text><text x="${cx + 4}" y="${sy(i) + 3}" fill="#5a5a7a">${i}</text>`; }
  // plot runs of in-range points
  let run = [];
  const flush = () => { if (run.length > 1) s += `<polyline points="${run.join(' ')}" fill="none" stroke="#1a2744" stroke-width="2.5"/>`; run = []; };
  for (let x = min; x <= max + 0.01; x += 0.1) { const y = f(x); if (y >= min - 0.3 && y <= max + 0.3) run.push(`${sx(x).toFixed(1)},${sy(y).toFixed(1)}`); else flush(); }
  flush();
  for (const [dx, dy] of dots) s += `<circle cx="${sx(dx)}" cy="${sy(dy)}" r="3.6" fill="#b8960c"/>`;
  s += `</svg>`;
  return s;
}
function mc({ dom = 'Advanced Math', diff, stem, figure = '', correct, distractors, explanation }) {
  const seen = new Set([correct]); const ds = [];
  for (const d of distractors) { if (!seen.has(d)) { seen.add(d); ds.push(d); } if (ds.length === 3) break; }
  const isInt = /^[−-]?\\d+$/.test(correct);
  let b = 1; while (ds.length < 3) { let c; if (isInt) { const v = parseInt(correct.replace('−','-'),10); const off = (b%2? Math.ceil(b/2) : -Math.ceil(b/2)); c = N(v + off); } else { c = correct + ' '.repeat(b); } b++; if (!seen.has(c) && c!==correct) { seen.add(c); ds.push(c); } }
  const opts = [correct, ...ds];
  for (let i = opts.length - 1; i > 0; i--) { const j = rnd(0, i); [opts[i], opts[j]] = [opts[j], opts[i]]; }
  return { question_id: 'adv' + pad(++SEQ), section: 'math', section_name: 'Math', domain: dom, difficulty: diff, difficulty_label: ['', 'Easy', 'Medium', 'Hard'][diff], type: 'mc', passage: '', figure, stem, choices: opts, answer_index: opts.indexOf(correct), answer_text: correct, explanation, is_premium: false, active: true };
}
function grid({ dom = 'Advanced Math', diff, stem, figure = '', correct, explanation }) {
  return { question_id: 'adv' + pad(++SEQ), section: 'math', section_name: 'Math', domain: dom, difficulty: diff, difficulty_label: ['', 'Easy', 'Medium', 'Hard'][diff], type: 'grid', passage: '', figure, stem, choices: [], answer_index: null, answer_text: String(correct), explanation, is_premium: false, active: true };
}
const Q = []; const add = q => Q.push(q);
const rootsPick = () => { let r1 = rnd(-6, 6), r2 = rnd(-6, 6); if (r1 === r2) r2 += (r2 < 6 ? 1 : -1); return [r1, r2]; };

/* TEXT: solve factorable quadratic — larger root */
function solveQ(n) { for (let i = 0; i < n; i++) { const [r1, r2] = rootsPick(); const b = -(r1 + r2), c = r1 * r2, big = Math.max(r1, r2), small = Math.min(r1, r2); add(mc({ diff: 2, stem: `What is the larger solution to ${quad(1, b, c)} = 0?`, correct: N(big), distractors: [N(small), N(-big), N(r1 + r2)], explanation: `Factor: (x ${sg(-r1)})(x ${sg(-r2)}) = 0, so x = ${N(r1)} or ${N(r2)}. The larger is ${N(big)}.` })); } }
/* TEXT: vertex x-coordinate */
function vertexX(n) { for (let i = 0; i < n; i++) { let h = rnd(-4, 4); if (h === 0) h = 2; const b = -2 * h, c = rnd(-5, 5); add(mc({ diff: 2, stem: `The graph of y = ${quad(1, b, c)} is a parabola. What is the x-coordinate of its vertex?`, correct: N(h), distractors: [N(-h), N(b), N(h + 1)], explanation: `Vertex x = −b/(2a) = −(${b})/2 = ${N(h)}.` })); } }
/* TEXT: min/max value */
function minmax(n) { for (let i = 0; i < n; i++) { const a = pick([1, -1]); let h = rnd(-3, 3); if (h === 0) h = 1; let k = rnd(-5, 5); if (k === 0) k = 2; const isMin = a > 0; add(mc({ diff: 2, stem: `The function f is defined by f(x) = ${a === 1 ? '' : '−'}(x ${sg(-h)})² ${sg(k)}. What is the ${isMin ? 'minimum' : 'maximum'} value of f?`, correct: N(k), distractors: [N(h), N(-k), N(k + a)], explanation: `In vertex form the ${isMin ? 'minimum' : 'maximum'} value is k = ${N(k)}, reached at x = ${N(h)}.` })); } }
/* TEXT: sum & product of roots */
function sumprod(n) { for (let i = 0; i < n; i++) { const [r1, r2] = rootsPick(); const b = -(r1 + r2), c = r1 * r2; const askSum = i % 2 === 0; add(mc({ diff: 2, stem: `The solutions to ${quad(1, b, c)} = 0 are r and s. What is ${askSum ? 'r + s' : 'r · s'}?`, correct: N(askSum ? r1 + r2 : r1 * r2), distractors: [N(askSum ? r1 * r2 : r1 + r2), N(askSum ? -(r1 + r2) : -r1 * r2), N(b)], explanation: askSum ? `Sum of roots = −b = ${N(r1 + r2)}.` : `Product of roots = c = ${N(r1 * r2)}.` })); } }
/* TEXT: factor */
function factor(n) { for (let i = 0; i < n; i++) { let p = rnd(-6, 6) || 2, q = rnd(-6, 6) || 3; if (p + q === 0) q += 1; const b = p + q, c = p * q; add(mc({ diff: 2, stem: `Which expression is equivalent to ${quad(1, b, c)}?`, correct: `(x ${sg(p)})(x ${sg(q)})`, distractors: [`(x ${sg(-p)})(x ${sg(-q)})`, `(x ${sg(b)})(x ${sg(c)})`, `(x ${sg(p)})(x ${sg(-q)})`], explanation: `Find two numbers with sum ${N(b)} and product ${N(c)}: ${N(p)} and ${N(q)}. So it factors as (x ${sg(p)})(x ${sg(q)}).` })); } }
/* TEXT: discriminant — number of real solutions */
function discrim(n) { for (let i = 0; i < n; i++) { const sign = i % 3; let b, c; if (sign === 0) { const [r1, r2] = rootsPick(); b = -(r1 + r2); c = r1 * r2; } else if (sign === 1) { const r = rnd(-4, 4); b = -2 * r; c = r * r; } else { b = rnd(-4, 4); c = rnd(3, 9); if (b * b - 4 * c >= 0) c = b * b + rnd(1, 5); } const D = b * b - 4 * c; const cnt = D > 0 ? '2' : D === 0 ? '1' : '0'; add(mc({ diff: 3, stem: `How many distinct real solutions does the equation ${quad(1, b, c)} = 0 have?`, correct: cnt, distractors: ['0', '1', '2', 'Infinitely many'].filter(x => x !== cnt), explanation: `The discriminant is b² − 4ac = (${b})² − 4(${c}) = ${D}. ${D > 0 ? 'Positive → 2 real solutions.' : D === 0 ? 'Zero → 1 real solution.' : 'Negative → 0 real solutions.'}` })); } }

/* GRAPH: read the vertex */
function gVertex(n) { for (let i = 0; i < n; i++) { const a = pick([1, -1]); let h = rnd(-3, 3) || 1, k = rnd(-4, 4) || 2; if (h === k) k += 1; const f = x => a * (x - h) * (x - h) + k; add(mc({ diff: 2, figure: parabola(f, [[h, k]]), stem: 'The graph of a quadratic function is shown. What are the coordinates of its vertex (marked)?', correct: `(${N(h)}, ${N(k)})`, distractors: [`(${N(k)}, ${N(h)})`, `(${N(-h)}, ${N(k)})`, `(${N(h)}, ${N(-k)})`, `(${N(-h)}, ${N(-k)})`, `(${N(h + 1)}, ${N(k)})`], explanation: `The vertex is the turning point of the parabola, located at (${N(h)}, ${N(k)}).` })); } }
/* GRAPH: read x-intercepts */
function gXint(n) { for (let i = 0; i < n; i++) { const a = pick([1, -1]); let r1 = rnd(-4, 4) || 1, r2 = rnd(-4, 4) || -2; if (Math.abs(r1 - r2) < 1 || Math.abs(r1 - r2) > 4 || r1 === 0 || r2 === 0) { i--; continue; } const lo = Math.min(r1, r2), hi = Math.max(r1, r2); const f = x => a * (x - r1) * (x - r2); add(mc({ diff: 2, figure: parabola(f, [[r1, 0], [r2, 0]]), stem: 'The graph of a quadratic function is shown. What are the x-intercepts (marked)?', correct: `x = ${N(lo)} and x = ${N(hi)}`, distractors: [`x = ${N(-lo)} and x = ${N(-hi)}`, `x = ${N(lo)} and x = ${N(-hi)}`, `x = ${N(lo + hi)}`, `x = ${N(lo)} and x = ${N(hi + 1)}`, `x = ${N(lo - 1)} and x = ${N(hi)}`], explanation: `The x-intercepts are where the parabola crosses the x-axis: x = ${N(lo)} and x = ${N(hi)}.` })); } }
/* GRAPH: read y-intercept */
function gYint(n) { for (let i = 0; i < n; i++) { const a = pick([1, -1]); const h = pick([-2, -1, 1, 2]), k = rnd(-3, 3); const yint = a * h * h + k; if (Math.abs(yint) > 5 || yint === 0) { i--; continue; } const f = x => a * (x - h) * (x - h) + k; add(mc({ diff: 2, figure: parabola(f, [[0, yint]]), stem: 'The graph of a quadratic function is shown. What is its y-intercept (marked)?', correct: `(0, ${N(yint)})`, distractors: [`(${N(yint)}, 0)`, `(0, ${N(-yint)})`, `(${N(h)}, ${N(k)})`, `(0, ${N(yint + 1)})`], explanation: `The y-intercept is where the graph crosses the y-axis (x = 0): (0, ${N(yint)}).` })); } }

solveQ(8); vertexX(7); minmax(7); sumprod(8); factor(7); discrim(8); gVertex(8); gXint(8); gYint(7);
const seen = new Set();
const uniq = Q.filter(q => { const k = q.stem + q.figure; if (seen.has(k)) return false; seen.add(k); return true; });
fs.writeFileSync('base44/questions_pack10_adv.json', JSON.stringify(uniq, null, 2));
console.log('Generated', uniq.length, 'Advanced Math questions (pack 10) —', uniq.filter(q => q.figure).length, 'with parabola graphs');
