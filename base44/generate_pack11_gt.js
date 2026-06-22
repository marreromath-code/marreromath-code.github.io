const fs = require('fs');
let SEQ = 0;
const pad = n => String(n).padStart(4, '0');
const rnd = (lo, hi) => Math.floor(Math.random() * (hi - lo + 1)) + lo;
const pick = a => a[Math.floor(Math.random() * a.length)];
const gcd = (a, b) => b ? gcd(b, a % b) : Math.abs(a);
const frac = (a, b) => { const g = gcd(a, b) || 1; return `${a / g}/${b / g}`; };
const N = n => (n < 0 ? '−' + (-n) : '' + n);

function mc({ dom = 'Geometry & Trig', diff, stem, figure = '', correct, distractors, explanation }) {
  const seen = new Set([correct]); const ds = [];
  for (const d of distractors) { if (!seen.has(d)) { seen.add(d); ds.push(d); } if (ds.length === 3) break; }
  const isInt = /^[−-]?\d+$/.test(correct);
  let b = 1; while (ds.length < 3) { let c; if (isInt) { const v = parseInt(correct.replace('−', '-'), 10); c = N(v + (b % 2 ? Math.ceil(b / 2) : -Math.ceil(b / 2))); } else c = correct + ' '.repeat(b); b++; if (!seen.has(c) && c !== correct) { seen.add(c); ds.push(c); } }
  const opts = [correct, ...ds];
  for (let i = opts.length - 1; i > 0; i--) { const j = rnd(0, i); [opts[i], opts[j]] = [opts[j], opts[i]]; }
  return { question_id: 'gt' + pad(++SEQ), section: 'math', section_name: 'Math', domain: dom, difficulty: diff, difficulty_label: ['', 'Easy', 'Medium', 'Hard'][diff], type: 'mc', passage: '', figure, stem, choices: opts, answer_index: opts.indexOf(correct), answer_text: correct, explanation, is_premium: false, active: true };
}
function grid({ dom = 'Geometry & Trig', diff, stem, figure = '', correct, explanation }) {
  return { question_id: 'gt' + pad(++SEQ), section: 'math', section_name: 'Math', domain: dom, difficulty: diff, difficulty_label: ['', 'Easy', 'Medium', 'Hard'][diff], type: 'grid', passage: '', figure, stem, choices: [], answer_index: null, answer_text: String(correct), explanation, is_premium: false, active: true };
}
const Q = []; const add = q => Q.push(q);

// simple cylinder figure
function cylinderSVG(rLab, hLab) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 200" width="220" height="200" font-family="Inter,Arial,sans-serif" font-size="13" fill="#1a1a2e"><rect width="220" height="200" fill="#fff"/>`
    + `<ellipse cx="110" cy="50" rx="55" ry="16" fill="none" stroke="#1a2744" stroke-width="2"/>`
    + `<line x1="55" y1="50" x2="55" y2="150" stroke="#1a2744" stroke-width="2"/><line x1="165" y1="50" x2="165" y2="150" stroke="#1a2744" stroke-width="2"/>`
    + `<path d="M55 150 A55 16 0 0 0 165 150" fill="none" stroke="#1a2744" stroke-width="2"/>`
    + `<path d="M55 150 A55 16 0 0 1 165 150" fill="none" stroke="#1a2744" stroke-width="1" stroke-dasharray="4 3"/>`
    + `<line x1="110" y1="50" x2="165" y2="50" stroke="#b8960c" stroke-width="1.5"/><text x="135" y="44" fill="#b8960c">${rLab}</text>`
    + `<line x1="185" y1="50" x2="185" y2="150" stroke="#5a5a7a" stroke-width="1"/><text x="190" y="104" fill="#5a5a7a">${hLab}</text>`
    + `</svg>`;
}
// right triangle with vertices X (angle), Y, Z (right angle); given-side label
function rtFig(givenSide) {
  const Z = [60, 170], X = [230, 170], Y = [60, 60];
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" width="300" height="200" font-family="Inter,Arial,sans-serif" font-size="13" fill="#1a1a2e"><rect width="300" height="200" fill="#fff"/>`
    + `<polygon points="${Z[0]},${Z[1]} ${X[0]},${X[1]} ${Y[0]},${Y[1]}" fill="none" stroke="#1a2744" stroke-width="2"/>`
    + `<path d="M${Z[0] + 12} ${Z[1]} L${Z[0] + 12} ${Z[1] - 12} L${Z[0]} ${Z[1] - 12}" fill="none" stroke="#1a1a2e" stroke-width="1.2"/>`
    + `<text x="${Z[0] - 12}" y="${Z[1] + 6}">Z</text><text x="${X[0] + 6}" y="${X[1] + 6}">X</text><text x="${Y[0] - 12}" y="${Y[1]}">Y</text>`
    + `<text x="${Z[0] - 16}" y="115" fill="#5a5a7a">${givenSide}</text>`
    + `<text x="${300 / 2}" y="194" text-anchor="middle" font-size="11" fill="#5a5a7a">Note: figure not drawn to scale.</text></svg>`;
}

const TRIP = [[3, 4, 5], [6, 8, 10], [5, 12, 13], [8, 15, 17], [7, 24, 25], [20, 21, 29], [9, 40, 41], [12, 35, 37]];

/* A — cylinder volume solve for radius (or height) */
function cylinder(n) {
  for (let i = 0; i < n; i++) {
    const r = rnd(2, 8), h = rnd(2, 9), coef = r * r * h; const findR = i % 2 === 0;
    if (findR) add(mc({ diff: 2, figure: cylinderSVG('r', h + ''),
      stem: `A right circular cylinder has a volume of ${coef}π and a height of ${h}. What is the radius of the cylinder?`,
      correct: N(r), distractors: [N(r * r), N(2 * r), N(coef - h)],
      explanation: `V = πr²h, so ${coef}π = πr²(${h}) → r² = ${coef}/${h} = ${r * r} → r = ${r}.` }));
    else add(mc({ diff: 2, figure: cylinderSVG(r + '', 'h'),
      stem: `A right circular cylinder has a volume of ${coef}π and a radius of ${r}. What is the height of the cylinder?`,
      correct: N(h), distractors: [N(r * r), N(2 * h), N(coef - r)],
      explanation: `V = πr²h, so ${coef}π = π(${r})²h → ${r * r}h = ${coef} → h = ${h}.` }));
  }
}

/* B — scale factor to area/volume ratio (grid-in) */
function scaleRatio(n) {
  for (let i = 0; i < n; i++) {
    const t = i % 2;
    if (t === 0) { const s = rnd(11, 200); add(grid({ diff: 2, dom: 'Geometry & Trig', stem: `Square A has side lengths that are ${s} times the side lengths of square B. The area of square A is k times the area of square B. What is the value of k?`, correct: s * s, explanation: `Area scales as the square of the side ratio: k = ${s}² = ${s * s}.` })); }
    else { const s = rnd(3, 20); add(grid({ diff: 3, dom: 'Geometry & Trig', stem: `Cube A has edge lengths that are ${s} times the edge lengths of cube B. The volume of cube A is k times the volume of cube B. What is the value of k?`, correct: s * s * s, explanation: `Volume scales as the cube of the edge ratio: k = ${s}³ = ${s * s * s}.` })); }
  }
}

/* C — cofunction identity (rational values) */
function cofunction(n) {
  for (let i = 0; i < n; i++) {
    const [a, b, c] = pick(TRIP); // sin(R) = a/c ; cos(S) = sin(R)
    add(mc({ diff: 2, dom: 'Geometry & Trig',
      stem: `In right triangle RST, the measures of angle R and angle S sum to 90°. If sin(R) = ${frac(a, c)}, what is the value of cos(S)?`,
      correct: frac(a, c), distractors: [frac(b, c), frac(c, a), frac(c, b)],
      explanation: `Angles R and S are complementary, and cos(S) = sin(90° − S) = sin(R). So cos(S) = ${frac(a, c)}.` }));
  }
}
// curated radical cofunction items (verified)
const RAD = [
  { sin: '√15/4', ds: ['1/4', '√15/15', '4√15/15'] },   // legs 1, √15, hyp 4
  { sin: '√5/3', ds: ['2/3', '√5/5', '3√5/5'] },         // legs 2, √5, hyp 3
  { sin: '√7/4', ds: ['3/4', '√7/7', '4√7/7'] },         // legs 3, √7, hyp 4
  { sin: '√21/5', ds: ['2/5', '√21/21', '5√21/21'] },    // legs 2, √21, hyp 5
];
function cofunctionRadical() {
  for (const r of RAD) add(mc({ diff: 3, dom: 'Geometry & Trig',
    stem: `In right triangle RST, the sum of the measures of angle R and angle S is 90°. The value of sin(R) is ${r.sin}. What is the value of cos(S)?`,
    correct: r.sin, distractors: r.ds,
    explanation: `Since R and S are complementary, cos(S) = sin(R) = ${r.sin}.` }));
}

/* D — side of a square equal in area to a circle of radius r */
function squareCircle(n) {
  for (let i = 0; i < n; i++) {
    const r = rnd(2, 9);
    add(mc({ diff: 2, dom: 'Geometry & Trig',
      stem: `What is the length of one side of a square that has the same area as a circle with radius ${r}?`,
      correct: `${r}√π`, distractors: [`${r}`, `${r * r}π`, `${2 * r}π`, `${r}π`],
      explanation: `Circle area = π(${r})² = ${r * r}π. A square with that area has side √(${r * r}π) = ${r}√π.` }));
  }
}

/* E — right triangle: trig ratio + a side -> perimeter */
function perimeterTrig(n) {
  for (let i = 0; i < n; i++) {
    const [a, b, c] = pick(TRIP); const g = gcd(a, b); const ta = a / g, tb = b / g; // reduced tan
    const k = rnd(2, 5); const given = a * k; // YZ (opposite to X)
    const per = (a + b + c) * k;
    add(mc({ diff: 3, dom: 'Geometry & Trig', figure: rtFig(`${given}`),
      stem: `In triangle XYZ, angle Z is a right angle and the length of side YZ is ${given} units. If tan(X) = ${frac(a, b)}, what is the perimeter, in units, of triangle XYZ?`,
      correct: N(per),
      distractors: [N(a + b + c), N((a + b) * k), N(given + b * k)],
      explanation: `tan(X) = opposite/adjacent = YZ/XZ = ${frac(a, b)}, and YZ = ${given}, so the sides are in the ratio ${a}:${b}:${c} scaled by ${k}: legs ${given} and ${b * k}, hypotenuse ${c * k}. Perimeter = ${given} + ${b * k} + ${c * k} = ${per}.` }));
  }
}

cylinder(10); scaleRatio(12); cofunction(8); cofunctionRadical(); squareCircle(8); perimeterTrig(10);
const seen = new Set();
const uniq = Q.filter(q => { const k = q.stem + q.figure; if (seen.has(k)) return false; seen.add(k); return true; });
fs.writeFileSync('base44/questions_pack11_gt.json', JSON.stringify(uniq, null, 2));
console.log('Generated', uniq.length, 'Geometry/Advanced questions (pack 11) —', uniq.filter(q => q.figure).length, 'with figures');
