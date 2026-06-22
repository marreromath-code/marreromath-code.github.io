const fs = require('fs');
let SEQ = 0;
const pad = n => String(n).padStart(4, '0');
const rnd = (lo, hi) => Math.floor(Math.random() * (hi - lo + 1)) + lo;
const pick = a => a[Math.floor(Math.random() * a.length)];
const gcd = (a, b) => b ? gcd(b, a % b) : Math.abs(a);
const frac = (a, b) => { const g = gcd(a, b) || 1; return `${a / g}/${b / g}`; };

// ---------- SVG geometry primitives ----------
const norm = (x, y) => { const m = Math.hypot(x, y) || 1; return [x / m, y / m]; };
function angleMark(cx, cy, p1, p2, text) {
  const [u1x, u1y] = norm(p1[0] - cx, p1[1] - cy);
  const [u2x, u2y] = norm(p2[0] - cx, p2[1] - cy);
  const r = 20, s = [cx + u1x * r, cy + u1y * r], e = [cx + u2x * r, cy + u2y * r];
  let d = Math.atan2(u2y, u2x) - Math.atan2(u1y, u1x);
  while (d <= -Math.PI) d += 2 * Math.PI; while (d > Math.PI) d -= 2 * Math.PI;
  const sweep = d > 0 ? 1 : 0;
  const [bx, by] = norm(u1x + u2x, u1y + u2y);
  const lx = cx + bx * (r + 16), ly = cy + by * (r + 16) + 4;
  return `<path d="M ${s[0].toFixed(1)} ${s[1].toFixed(1)} A ${r} ${r} 0 0 ${sweep} ${e[0].toFixed(1)} ${e[1].toFixed(1)}" fill="none" stroke="#1a1a2e" stroke-width="1.3"/>`
    + `<text x="${lx.toFixed(1)}" y="${ly.toFixed(1)}" text-anchor="middle">${text}</text>`;
}
function tick(p, q, dbl) {
  const [dx, dy] = norm(q[0] - p[0], q[1] - p[1]); const px = -dy, py = dx;
  const mx = (p[0] + q[0]) / 2, my = (p[1] + q[1]) / 2;
  const seg = (ox) => `<line x1="${(mx + ox * dx - 5 * px).toFixed(1)}" y1="${(my + ox * dy - 5 * py).toFixed(1)}" x2="${(mx + ox * dx + 5 * px).toFixed(1)}" y2="${(my + ox * dy + 5 * py).toFixed(1)}" stroke="#1a1a2e" stroke-width="1.5"/>`;
  return dbl ? seg(-3) + seg(3) : seg(0);
}
function frameSVG(inner, w = 300, h = 230, note = true) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" font-family="Inter,Arial,sans-serif" font-size="13" fill="#1a1a2e">`
    + `<rect width="${w}" height="${h}" fill="#ffffff"/>${inner}`
    + (note ? `<text x="${w / 2}" y="${h - 8}" text-anchor="middle" font-size="11" fill="#5a5a7a">Note: figure not drawn to scale.</text>` : '')
    + `</svg>`;
}
const line = (p, q) => `<line x1="${p[0]}" y1="${p[1]}" x2="${q[0]}" y2="${q[1]}" stroke="#1a2744" stroke-width="2"/>`;
const lbl = (p, t, dx = 0, dy = 0, anchor = 'middle') => `<text x="${p[0] + dx}" y="${p[1] + dy}" text-anchor="${anchor}">${t}</text>`;

// ---------- question helpers ----------
function mc({ dom = 'Geometry & Trig', diff, stem, figure = '', correct, distractors, explanation }) {
  const seen = new Set([correct]); const ds = [];
  for (const d of distractors) { if (!seen.has(d)) { seen.add(d); ds.push(d); } if (ds.length === 3) break; }
  let b = 1; while (ds.length < 3) { const c = correct + ' (' + b++ + ')'; if (!seen.has(c)) { seen.add(c); ds.push(c); } }
  const opts = [correct, ...ds];
  for (let i = opts.length - 1; i > 0; i--) { const j = rnd(0, i); [opts[i], opts[j]] = [opts[j], opts[i]]; }
  return { question_id: 'geo' + pad(++SEQ), section: 'math', section_name: 'Math', domain: dom, difficulty: diff, difficulty_label: ['', 'Easy', 'Medium', 'Hard'][diff], type: 'mc', passage: '', figure, stem, choices: opts, answer_index: opts.indexOf(correct), answer_text: correct, explanation, is_premium: false, active: true };
}
function grid({ dom = 'Geometry & Trig', diff, stem, figure = '', correct, explanation }) {
  return { question_id: 'geo' + pad(++SEQ), section: 'math', section_name: 'Math', domain: dom, difficulty: diff, difficulty_label: ['', 'Easy', 'Medium', 'Hard'][diff], type: 'grid', passage: '', figure, stem, choices: [], answer_index: null, answer_text: String(correct), explanation, is_premium: false, active: true };
}
const Q = []; const add = q => Q.push(q);

/* 1) Triangle angle sum (diagram) */
function angleSum(n) {
  const A = [55, 185], B = [248, 185], C = [150, 55];
  for (let i = 0; i < n; i++) {
    const a = rnd(35, 80), b = rnd(30, 80); const c = 180 - a - b; if (c < 20 || c > 120) { i--; continue; }
    const fig = frameSVG(line(A, B) + line(B, C) + line(C, A)
      + angleMark(A[0], A[1], B, C, a + '°') + angleMark(B[0], B[1], C, A, b + '°') + angleMark(C[0], C[1], A, B, 'x°')
      + lbl(A, 'P', -10, 6) + lbl(B, 'Q', 10, 6) + lbl(C, 'R', 0, -10));
    add(mc({ diff: 2, figure: fig, stem: 'In triangle PQR shown, what is the value of x?',
      correct: c + '', distractors: [(a + b) + '', (180 - a) + '', (180 - b) + ''],
      explanation: `The angles of a triangle sum to 180°, so x = 180 − ${a} − ${b} = ${c}.` }));
  }
}

/* 2) Isosceles triangle base/apex (diagram, with equal-side ticks) */
function isosceles(n) {
  const T = [150, 50], L = [60, 188], R = [240, 188];
  for (let i = 0; i < n; i++) {
    const giveApex = i % 2 === 0;
    let apex, base;
    if (giveApex) { apex = rnd(20, 100) * 1; if ((180 - apex) % 2) apex += 1; base = (180 - apex) / 2; }
    else { base = rnd(35, 75); apex = 180 - 2 * base; }
    const ticks = tick(T, L) + tick(T, R);
    const marks = giveApex
      ? angleMark(T[0], T[1], L, R, apex + '°') + angleMark(L[0], L[1], T, R, 'x°')
      : angleMark(L[0], L[1], T, R, base + '°') + angleMark(T[0], T[1], L, R, 'x°');
    const fig = frameSVG(line(T, L) + line(T, R) + line(L, R) + ticks + marks
      + lbl(T, 'A', 0, -10) + lbl(L, 'B', -10, 8) + lbl(R, 'C', 10, 8));
    add(mc({ diff: 2, figure: fig,
      stem: 'In triangle ABC, AB = AC (shown by tick marks). What is the value of x?',
      correct: (giveApex ? base : apex) + '',
      distractors: giveApex ? [(180 - apex) + '', apex + '', (90 - apex) + '', (2 * base) + '', (base + 10) + ''] : [base + '', (180 - base) + '', (90 - base) + '', (2 * base) + '', (apex - 10) + ''],
      explanation: giveApex
        ? `Since AB = AC, the base angles are equal. They sum with the ${apex}° apex to 180°, so each base angle x = (180 − ${apex})/2 = ${base}.`
        : `Since AB = AC, both base angles are ${base}°. The apex x = 180 − 2(${base}) = ${apex}.` }));
  }
}

/* 3) Exterior angle theorem (diagram, base extended) */
function exterior(n) {
  const A = [60, 175], B = [205, 175], C = [120, 60], D = [285, 175];
  for (let i = 0; i < n; i++) {
    const a = rnd(35, 70), c = rnd(35, 70); const ext = a + c;
    const fig = frameSVG(line(A, B) + line(B, D) + line(A, C) + line(C, B)
      + angleMark(A[0], A[1], B, C, a + '°') + angleMark(C[0], C[1], A, B, c + '°') + angleMark(B[0], B[1], C, D, 'x°')
      + lbl(A, 'A', -10, 6) + lbl(B, 'B', 0, 16) + lbl(C, 'C', 0, -10) + lbl(D, 'D', 10, 6));
    add(mc({ diff: 3, figure: fig,
      stem: 'In the figure, side AB is extended to D. What is the value of x, the measure of exterior angle CBD?',
      correct: ext + '', distractors: [(180 - ext) + '', a + '', c + ''],
      explanation: `An exterior angle equals the sum of the two remote interior angles: x = ${a} + ${c} = ${ext}.` }));
  }
}

/* 4) Right triangle — Pythagorean (diagram) */
const TRIP = [[3, 4, 5], [6, 8, 10], [5, 12, 13], [8, 15, 17], [9, 12, 15], [7, 24, 25], [20, 21, 29]];
function rightTri(p, lblB, lblL, lblH, theta) {
  const A = [55, 175]; const sc = 115 / Math.max(p[0], p[1]); const B = [55 + p[0] * sc, 175], C = [55, 175 - p[1] * sc];
  let s = line(A, B) + line(A, C) + line(B, C);
  s += `<path d="M ${A[0] + 11} ${A[1]} L ${A[0] + 11} ${A[1] - 11} L ${A[0]} ${A[1] - 11}" fill="none" stroke="#1a1a2e" stroke-width="1.2"/>`;
  s += lbl([(A[0] + B[0]) / 2, A[1] + 17], lblB) + lbl([A[0] - 12, (A[1] + C[1]) / 2 + 4], lblL, 0, 0, 'end') + lbl([(B[0] + C[0]) / 2 + 10, (B[1] + C[1]) / 2 - 2], lblH);
  if (theta) s += angleMark(B[0], B[1], A, C, 'θ');
  return frameSVG(s, 300, 215);
}
function pythag(n) {
  for (let i = 0; i < n; i++) {
    const [a, b, c] = pick(TRIP); const findHyp = i % 2 === 0;
    if (findHyp) add(grid({ diff: 2, figure: rightTri([a, b], String(a), String(b), '?'),
      stem: 'In the right triangle shown, what is the length of the hypotenuse?',
      correct: c, explanation: `c² = ${a}² + ${b}² = ${a * a + b * b}, so c = ${c}.` }));
    else add(grid({ diff: 2, figure: rightTri([a, b], String(a), '?', String(c)),
      stem: 'In the right triangle shown, what is the length of the unknown leg?',
      correct: b, explanation: `leg² = ${c}² − ${a}² = ${c * c - a * a}, so the leg = ${b}.` }));
  }
}

/* 5) Right triangle trig ratio (diagram, θ marked) */
function trig(n) {
  for (let i = 0; i < n; i++) {
    const [a, b, c] = pick(TRIP); const r = pick(['sin', 'cos', 'tan']); // θ at bottom-right: opp=vertical(b), adj=base(a), hyp=c
    const val = r === 'sin' ? frac(b, c) : r === 'cos' ? frac(a, c) : frac(b, a);
    add(mc({ diff: 2, figure: rightTri([a, b], String(a), String(b), String(c), true),
      stem: `In the right triangle shown, what is the value of ${r} θ?`,
      correct: val, distractors: [frac(a, c), frac(b, c), frac(b, a), frac(a, b), frac(c, b)].filter(x => x !== val),
      explanation: `${r} θ = ${r === 'sin' ? 'opposite/hypotenuse' : r === 'cos' ? 'adjacent/hypotenuse' : 'opposite/adjacent'} = ${val}.` }));
  }
}

/* 6) Circle area / circumference (diagram) */
function circle(n) {
  for (let i = 0; i < n; i++) {
    const r = rnd(2, 11); const C = [150, 110];
    const fig = frameSVG(`<circle cx="150" cy="110" r="70" fill="none" stroke="#1a2744" stroke-width="2"/>`
      + line(C, [220, 110]) + `<circle cx="150" cy="110" r="2.5" fill="#1a2744"/>` + lbl([185, 102], r + ''), 300, 215, false);
    const area = i % 2 === 0;
    add(mc({ diff: 1, figure: fig, dom: 'Geometry & Trig',
      stem: area ? 'The circle shown has the radius marked. What is its area?' : 'The circle shown has the radius marked. What is its circumference?',
      correct: area ? `${r * r}π` : `${2 * r}π`,
      distractors: area ? [`${2 * r}π`, `${r}π`, `${4 * r}π`, `${r * r + 1}π`] : [`${r * r}π`, `${r}π`, `${2 * r * r}π`, `${3 * r}π`],
      explanation: area ? `A = πr² = π(${r})² = ${r * r}π.` : `C = 2πr = 2π(${r}) = ${2 * r}π.` }));
  }
}

/* 7) 45-45-90 special triangle (diagram) */
function special45(n) {
  for (let i = 0; i < n; i++) {
    const leg = rnd(2, 12);
    add(mc({ diff: 2, figure: rightTri([leg, leg], String(leg), String(leg), '?') ,
      stem: 'The right triangle shown has two legs of equal length. What is the length of the hypotenuse?',
      correct: `${leg}√2`, distractors: [`${leg * 2}`, `${leg}√3`, `${leg * leg}`, `${3 * leg}`],
      explanation: `In a 45-45-90 triangle the hypotenuse equals a leg times √2: ${leg}√2.` }));
  }
}

/* 8) Congruent triangles — corresponding angle (text) */
function congruent(n) {
  for (let i = 0; i < n; i++) {
    const a = rnd(30, 80), b = rnd(30, 80); const c = 180 - a - b; if (c < 20) { i--; continue; }
    const askThird = i % 2 === 1;
    add(mc({ diff: 1, dom: 'Geometry & Trig',
      stem: `Triangles ABC and DEF are congruent, where A, B, and C correspond to D, E, and F, respectively. The measure of angle A is ${a}° and the measure of angle B is ${b}°. What is the measure of angle ${askThird ? 'F' : 'D'}?`,
      correct: (askThird ? c : a) + '°',
      distractors: askThird ? [a + '°', b + '°', (a + b) + '°'] : [b + '°', c + '°', (180 - a) + '°'],
      explanation: askThird ? `Angle F corresponds to angle C. Angle C = 180 − ${a} − ${b} = ${c}°.` : `Angle D corresponds to angle A, so angle D = ${a}°.` }));
  }
}

/* 9) Similar right triangles — corresponding trig ratio (text) */
function similarTrig(n) {
  for (let i = 0; i < n; i++) {
    const [a, b, c] = pick(TRIP);
    add(mc({ diff: 2, dom: 'Geometry & Trig',
      stem: `Triangle FGH is similar to triangle JKL, where angle F corresponds to angle J and angles H and L are right angles. If sin(F) = ${frac(a, c)}, what is the value of sin(J)?`,
      correct: frac(a, c), distractors: [frac(c, a), frac(b, c), frac(a, b)].filter(x => x !== frac(a, c)),
      explanation: `Similar triangles have equal corresponding angles, and equal angles have equal sine. So sin(J) = sin(F) = ${frac(a, c)}.` }));
  }
}

/* 10) Cube / box surface area (text, grid-in) */
function surface(n) {
  for (let i = 0; i < n; i++) {
    const t = i % 3;
    if (t === 0) { const s = rnd(4, 30); add(grid({ diff: 2, dom: 'Geometry & Trig', stem: `Each edge of a cube is ${s} inches. What is the total surface area, in square inches, of the cube?`, correct: 6 * s * s, explanation: `A cube has 6 square faces: 6 × ${s}² = 6 × ${s * s} = ${6 * s * s}.` })); }
    else if (t === 1) { const s = rnd(4, 30); add(grid({ diff: 2, dom: 'Geometry & Trig', stem: `Each edge of a cube is ${s} inches. Each face is a square, and the cube has no lid (top face). What is the exterior surface area, in square inches, of this cube without a lid?`, correct: 5 * s * s, explanation: `Without the lid there are 5 faces: 5 × ${s}² = 5 × ${s * s} = ${5 * s * s}.` })); }
    else { const l = rnd(3, 12), w = rnd(3, 12), h = rnd(3, 12); const sa = 2 * (l * w + l * h + w * h); add(grid({ diff: 3, dom: 'Geometry & Trig', stem: `A rectangular box has length ${l}, width ${w}, and height ${h} inches. What is its total surface area, in square inches?`, correct: sa, explanation: `SA = 2(ℓw + ℓh + wh) = 2(${l * w} + ${l * h} + ${w * h}) = ${sa}.` })); }
  }
}

angleSum(7); isosceles(8); exterior(6); pythag(8); trig(8); circle(6); special45(5); congruent(6); similarTrig(6); surface(9);
const seen = new Set();
const uniq = Q.filter(q => { const k = q.stem + q.figure; if (seen.has(k)) return false; seen.add(k); return true; });
fs.writeFileSync('base44/questions_pack9_geo.json', JSON.stringify(uniq, null, 2));
const withFig = uniq.filter(q => q.figure).length;
console.log('Generated', uniq.length, 'geometry/trig questions (pack 9) —', withFig, 'with SVG diagrams');
