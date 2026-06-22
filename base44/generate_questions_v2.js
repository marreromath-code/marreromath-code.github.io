/* Pack 3: a larger batch of original, answer-verified SAT Math questions.
   IDs start with 'h' so they never collide with the existing g-prefixed bank.
   Every answer is computed → guaranteed correct. Covers more of the 12 official skills. */
const fs = require('fs');
let SEQ = 0;
const pad = n => String(n).padStart(4, '0');
const rnd = (lo, hi) => Math.floor(Math.random() * (hi - lo + 1)) + lo;
const pick = a => a[Math.floor(Math.random() * a.length)];
const gcd = (a, b) => b ? gcd(b, a % b) : Math.abs(a);
const frac = (a, b) => { const g = gcd(a, b) || 1; return `${a / g}/${b / g}`; };
function quad(a, b, c) { let s = (a === 1 ? '' : a) + 'x²'; if (b !== 0) s += (b < 0 ? ' − ' : ' + ') + (Math.abs(b) === 1 ? '' : Math.abs(b)) + 'x'; if (c !== 0) s += (c < 0 ? ' − ' : ' + ') + Math.abs(c); return s; }
const sg = n => (n < 0 ? '− ' + (-n) : '+ ' + n);

function mc({ dom, diff, stem, correct, distractors, explanation, fmt = (x => String(x)) }) {
  const seen = new Set([String(correct)]); const ds = [];
  for (const d of distractors) { const k = String(d); if (!seen.has(k)) { seen.add(k); ds.push(d); } if (ds.length === 3) break; }
  let bump = 1;
  while (ds.length < 3) { const cand = (typeof correct === 'number') ? correct + bump : correct + ' ' + bump; if (!seen.has(String(cand))) { seen.add(String(cand)); ds.push(cand); } bump++; }
  const opts = [correct, ...ds];
  for (let i = opts.length - 1; i > 0; i--) { const j = rnd(0, i); [opts[i], opts[j]] = [opts[j], opts[i]]; }
  return { question_id: 'h' + pad(++SEQ), section: 'math', section_name: 'Math', domain: dom, difficulty: diff, difficulty_label: ['', 'Easy', 'Medium', 'Hard'][diff], type: 'mc', passage: '', stem, choices: opts.map(fmt), answer_index: opts.findIndex(o => String(o) === String(correct)), answer_text: fmt(correct), explanation, is_premium: false, active: true };
}
function grid({ dom, diff, stem, correct, explanation }) {
  return { question_id: 'h' + pad(++SEQ), section: 'math', section_name: 'Math', domain: dom, difficulty: diff, difficulty_label: ['', 'Easy', 'Medium', 'Hard'][diff], type: 'grid', passage: '', stem, choices: [], answer_index: null, answer_text: String(correct), explanation, is_premium: false, active: true };
}
const Q = []; const add = q => Q.push(q);

/* ───── ALGEBRA ───── */
function genAlgebra(n) {
  for (let i = 0; i < n; i++) {
    const t = i % 6;
    if (t === 0) { // x-intercept of a line
      const m = pick([2, 3, -2, 4, -3]), x0 = rnd(1, 6), b = -m * x0; // y = mx + b, x-int at x0
      add(mc({ dom: 'Algebra', diff: 2, stem: `What is the x-intercept of the line y = ${m === 1 ? '' : m}x ${sg(b)}?`,
        correct: x0, distractors: [b, -x0, m], explanation: `Set y = 0: 0 = ${m}x ${sg(b)} → x = ${x0}.` }));
    } else if (t === 1) { // system, find x+y
      const x = rnd(1, 7), y = rnd(1, 7), s = x + y, d = x - y;
      add(mc({ dom: 'Algebra', diff: 3, stem: `If x + y = ${s} and x − y = ${d}, what is the value of y?`,
        correct: y, distractors: [x, s, d], explanation: `Subtract the equations: 2y = ${s - d}, so y = ${y} (and x = ${x}).` }));
    } else if (t === 2) { // proportion
      const k = rnd(2, 6), a = rnd(2, 6), b = k * a, c = rnd(2, 6), d = k * c;
      add(grid({ dom: 'Algebra', diff: 1, stem: `If ${a} is to ${b} as ${c} is to x, what is x?`,
        correct: d, explanation: `The ratio is ${a}/${b} = 1/${k}, so x = ${c} × ${k} = ${d}.` }));
    } else if (t === 3) { // linear function from rate word problem
      const start = rnd(2, 8) * 10, rate = rnd(2, 7), wk = rnd(3, 9), tot = start + rate * wk;
      add(grid({ dom: 'Algebra', diff: 2, stem: `A tank holds ${start} liters and is filled at ${rate} liters per minute. How many liters are in the tank after ${wk} minutes?`,
        correct: tot, explanation: `${start} + ${rate}(${wk}) = ${start} + ${rate * wk} = ${tot}.` }));
    } else if (t === 4) { // ax - b = cx + d
      const a = rnd(3, 7), c = rnd(1, a - 1), x = rnd(2, 8), b = rnd(1, 9), d = (a - c) * x - b;
      add(mc({ dom: 'Algebra', diff: 2, stem: `Solve for x: ${a}x − ${b} = ${c}x + ${d}.`,
        correct: x, distractors: [x + 1, -x, b + d], explanation: `${a}x − ${c}x = ${d} + ${b} → ${a - c}x = ${d + b} → x = ${x}.` }));
    } else { // evaluate linear function
      const m = rnd(2, 6), b = rnd(-5, 8), x = rnd(2, 7), v = m * x + b;
      add(grid({ dom: 'Algebra', diff: 1, stem: `If f(x) = ${m}x ${sg(b)}, what is f(${x})?`,
        correct: v, explanation: `f(${x}) = ${m}(${x}) ${sg(b)} = ${v}.` }));
    }
  }
}

/* ───── ADVANCED MATH ───── */
function genAdvanced(n) {
  for (let i = 0; i < n; i++) {
    const t = i % 6;
    if (t === 0) { // sum of roots (monic)
      let r1 = rnd(-6, 6), r2 = rnd(-6, 6); if (r1 === r2) r2++;
      const b = -(r1 + r2), c = r1 * r2, sum = r1 + r2;
      add(mc({ dom: 'Advanced Math', diff: 2, stem: `The solutions of x² ${sg(b)}x ${sg(c)} = 0 are r and s. What is r + s?`,
        correct: sum, distractors: [c, -sum, b], explanation: `For x² + bx + c, the sum of roots is −b = ${sum}. (Roots are ${r1} and ${r2}.)` }));
    } else if (t === 1) { // product of roots
      let r1 = rnd(-6, 6), r2 = rnd(-6, 6); if (r1 === 0) r1 = 2; if (r2 === r1) r2++;
      const b = -(r1 + r2), c = r1 * r2, prod = r1 * r2;
      add(mc({ dom: 'Advanced Math', diff: 2, stem: `The solutions of x² ${sg(b)}x ${sg(c)} = 0 are r and s. What is r · s?`,
        correct: prod, distractors: [-(r1 + r2), -prod, r1 + r2], explanation: `For x² + bx + c, the product of roots is c = ${prod}.` }));
    } else if (t === 2) { // composition f(g(x))
      const a = rnd(1, 4), bg = rnd(1, 6), bf = rnd(2, 5), cf = rnd(-4, 6), x = rnd(1, 4);
      const g = a * x + bg, v = bf * g + cf;
      add(grid({ dom: 'Advanced Math', diff: 3, stem: `If g(x) = ${a}x ${sg(bg)} and f(x) = ${bf}x ${sg(cf)}, what is f(g(${x}))?`,
        correct: v, explanation: `g(${x}) = ${a}(${x}) ${sg(bg)} = ${g}. Then f(${g}) = ${bf}(${g}) ${sg(cf)} = ${v}.` }));
    } else if (t === 3) { // solve x^2 = k (perfect square)
      const x = rnd(4, 12), k = x * x;
      add(mc({ dom: 'Advanced Math', diff: 1, stem: `What is the positive solution to x² = ${k}?`,
        correct: x, distractors: [k / 2, x + 1, k], explanation: `x = √${k} = ${x} (taking the positive root).` }));
    } else if (t === 4) { // difference of squares evaluate
      const a = rnd(5, 12), b = rnd(1, a - 1), v = a * a - b * b;
      add(grid({ dom: 'Advanced Math', diff: 2, stem: `What is the value of ${a}² − ${b}²?`,
        correct: v, explanation: `${a}² − ${b}² = (${a} − ${b})(${a} + ${b}) = ${a - b} × ${a + b} = ${v}.` }));
    } else { // exponential growth rate interpretation
      const a0 = rnd(2, 9) * 100, r = pick([10, 20, 25, 50]), t1 = a0 * (1 + r / 100);
      add(mc({ dom: 'Advanced Math', diff: 2, stem: `A population of ${a0} grows by ${r}% each year, modeled by P = ${a0}(1 + ${r / 100})ᵗ. What is the population after 1 year?`,
        correct: t1, distractors: [a0 + r, a0 * r / 100, a0 * 2], explanation: `After t = 1: ${a0}(1 + ${r / 100}) = ${a0}(${1 + r / 100}) = ${t1}.` }));
    }
  }
}

/* ───── PROBLEM-SOLVING & DATA ───── */
function genData(n) {
  for (let i = 0; i < n; i++) {
    const t = i % 7;
    if (t === 0) { // line of best fit prediction
      const m = rnd(2, 8), b = rnd(1, 10), x = rnd(5, 12), y = m * x + b;
      add(grid({ dom: 'Problem-Solving & Data', diff: 2, stem: `A line of best fit for a data set is y = ${m}x ${sg(b)}. Based on this model, what value of y is predicted when x = ${x}?`,
        correct: y, explanation: `y = ${m}(${x}) ${sg(b)} = ${y}.` }));
    } else if (t === 1) { // mean: find missing value
      const cnt = pick([4, 5]), mean = rnd(6, 15), total = cnt * mean;
      const vals = Array.from({ length: cnt - 1 }, () => rnd(2, 20)); const sum = vals.reduce((s, v) => s + v, 0);
      const missing = total - sum;
      if (missing >= 1 && missing <= 30) {
        add(grid({ dom: 'Problem-Solving & Data', diff: 3, stem: `The mean of ${cnt} numbers is ${mean}. ${cnt - 1} of the numbers are ${vals.join(', ')}. What is the remaining number?`,
          correct: missing, explanation: `Total must be ${cnt} × ${mean} = ${total}. The given numbers sum to ${sum}, so the last is ${total} − ${sum} = ${missing}.` }));
      } else { i--; }
    } else if (t === 2) { // two-way table probability
      const a = rnd(8, 20), b = rnd(8, 20), tot = a + b;
      add(mc({ dom: 'Problem-Solving & Data', diff: 2, stem: `A survey of ${tot} people found ${a} prefer tea and ${b} prefer coffee. If one person is chosen at random, what is the probability they prefer tea?`,
        correct: frac(a, tot), distractors: [frac(b, tot), frac(a, b), frac(a, tot - 1)].filter(d => d !== frac(a, tot)),
        explanation: `P(tea) = ${a}/${tot}${frac(a, tot) !== `${a}/${tot}` ? ' = ' + frac(a, tot) : ''}.` }));
    } else if (t === 3) { // unit conversion (rate)
      const rate = rnd(30, 70), hrs = pick([2, 3, 4, 5]), d = rate * hrs;
      add(grid({ dom: 'Problem-Solving & Data', diff: 1, stem: `A car travels at a constant ${rate} miles per hour. How far does it travel in ${hrs} hours?`,
        correct: d, explanation: `Distance = rate × time = ${rate} × ${hrs} = ${d} miles.` }));
    } else if (t === 4) { // median odd-length list
      const arr = Array.from({ length: 5 }, () => rnd(1, 30)); const sorted = [...arr].sort((a, b) => a - b); const med = sorted[2];
      add(mc({ dom: 'Problem-Solving & Data', diff: 2, stem: `What is the median of the data set ${arr.join(', ')}?`,
        correct: med, distractors: [Math.round(arr.reduce((s, v) => s + v, 0) / 5), sorted[1], sorted[3]],
        explanation: `Ordered: ${sorted.join(', ')}. The middle value is ${med}.` }));
    } else if (t === 5) { // percent more than
      const base = rnd(2, 12) * 10, p = pick([10, 20, 25, 50]), more = base * (1 + p / 100);
      add(mc({ dom: 'Problem-Solving & Data', diff: 2, stem: `What number is ${p}% more than ${base}?`,
        correct: more, distractors: [base * p / 100, base - p, base * (1 - p / 100)],
        explanation: `${p}% of ${base} = ${base * p / 100}; ${base} + ${base * p / 100} = ${more}.` }));
    } else { // ratio with total (grid)
      const a = rnd(2, 5), b = rnd(2, 5), unit = rnd(2, 7), total = (a + b) * unit, smaller = Math.min(a, b) * unit;
      add(grid({ dom: 'Problem-Solving & Data', diff: 2, stem: `Two quantities are in the ratio ${a} : ${b} and together total ${total}. What is the smaller quantity?`,
        correct: smaller, explanation: `${a + b} parts = ${total}, so 1 part = ${unit}. Smaller = ${Math.min(a, b)} × ${unit} = ${smaller}.` }));
    }
  }
}

/* ───── GEOMETRY & TRIG ───── */
function genGeometry(n) {
  const triples = [[3, 4, 5], [6, 8, 10], [5, 12, 13], [8, 15, 17], [9, 12, 15], [7, 24, 25]];
  for (let i = 0; i < n; i++) {
    const t = i % 7;
    if (t === 0) { // cylinder volume (coefficient of π)
      const r = rnd(2, 6), h = rnd(2, 8), coef = r * r * h;
      add(mc({ dom: 'Geometry & Trig', diff: 2, stem: `A cylinder has radius ${r} and height ${h}. What is its volume? (V = πr²h)`,
        correct: `${coef}π`, distractors: [`${2 * r * h}π`, `${r * h}π`, `${coef * 2}π`], explanation: `V = πr²h = π(${r})²(${h}) = ${coef}π.` }));
    } else if (t === 1) { // cone volume
      let r = rnd(2, 6), h = rnd(3, 9); while ((r * r * h) % 3 !== 0) h++; const coef = r * r * h / 3;
      add(mc({ dom: 'Geometry & Trig', diff: 2, stem: `A cone has radius ${r} and height ${h}. What is its volume? (V = ⅓πr²h)`,
        correct: `${coef}π`, distractors: [`${r * r * h}π`, `${coef * 2}π`, `${r * h}π`], explanation: `V = ⅓πr²h = ⅓π(${r})²(${h}) = ${coef}π.` }));
    } else if (t === 2) { // complementary trig identity
      const [a, b, c] = pick(triples);
      add(mc({ dom: 'Geometry & Trig', diff: 2, stem: `In a right triangle, sin(A) = ${frac(a, c)}. What is cos(90° − A)?`,
        correct: frac(a, c), distractors: [frac(b, c), frac(a, b), frac(c, a)].filter(d => d !== frac(a, c)),
        explanation: `cos(90° − A) = sin(A), so cos(90° − A) = ${frac(a, c)}.` }));
    } else if (t === 3) { // coordinate distance
      const [a, b, c] = pick(triples); const x1 = rnd(-3, 3), y1 = rnd(-3, 3), x2 = x1 + a, y2 = y1 + b;
      add(mc({ dom: 'Geometry & Trig', diff: 2, stem: `What is the distance between the points (${x1}, ${y1}) and (${x2}, ${y2})?`,
        correct: c, distractors: [a + b, c + 1, Math.round(c / 2)], explanation: `Distance = √((${a})² + (${b})²) = √${a * a + b * b} = ${c}.` }));
    } else if (t === 4) { // parallel lines / supplementary angle
      const ang = rnd(35, 140);
      add(grid({ dom: 'Geometry & Trig', diff: 1, stem: `Two angles are supplementary. One measures ${ang}°. What is the measure, in degrees, of the other?`,
        correct: 180 - ang, explanation: `Supplementary angles sum to 180°: 180 − ${ang} = ${180 - ang}°.` }));
    } else if (t === 5) { // rectangle: area or perimeter
      const l = rnd(4, 14), w = rnd(2, 10);
      if (Math.random() < 0.5) add(grid({ dom: 'Geometry & Trig', diff: 1, stem: `A rectangle has length ${l} and width ${w}. What is its area?`, correct: l * w, explanation: `Area = ℓ × w = ${l} × ${w} = ${l * w}.` }));
      else add(grid({ dom: 'Geometry & Trig', diff: 1, stem: `A rectangle has length ${l} and width ${w}. What is its perimeter?`, correct: 2 * (l + w), explanation: `Perimeter = 2(ℓ + w) = 2(${l} + ${w}) = ${2 * (l + w)}.` }));
    } else { // pythagorean find missing leg
      const [a, b, c] = pick(triples);
      add(grid({ dom: 'Geometry & Trig', diff: 2, stem: `A right triangle has a hypotenuse of ${c} and one leg of ${a}. What is the length of the other leg?`,
        correct: b, explanation: `leg² = ${c}² − ${a}² = ${c * c - a * a}, so leg = ${b}.` }));
    }
  }
}

genAlgebra(50);
genAdvanced(48);
genData(56);
genGeometry(56);

const seenStem = new Set();
const unique = Q.filter(q => { if (seenStem.has(q.stem)) return false; seenStem.add(q.stem); return true; });
fs.writeFileSync('base44/questions_pack3.json', JSON.stringify(unique, null, 2));
const by = {}; const byDiff = { 1: 0, 2: 0, 3: 0 };
unique.forEach(q => { by[q.domain] = (by[q.domain] || 0) + 1; byDiff[q.difficulty]++; });
console.log('Generated', unique.length, 'new questions (pack 3)');
console.log('By domain:', by);
console.log('By difficulty:', byDiff, '| grid-ins:', unique.filter(q => q.type === 'grid').length);
