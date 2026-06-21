/* Generates original, answer-verified SAT Math questions in the Base44 Question schema.
   Every answer is computed (not hand-typed), so correctness is guaranteed. */
const fs = require('fs');

let SEQ = 0;
const pad = n => String(n).padStart(4, '0');
const rnd = (lo, hi) => Math.floor(Math.random() * (hi - lo + 1)) + lo;
const pick = a => a[Math.floor(Math.random() * a.length)];
const gcd = (a, b) => b ? gcd(b, a % b) : Math.abs(a);
const frac = (a, b) => { const g = gcd(a, b) || 1; return `${a / g}/${b / g}`; };
// Format a quadratic ax² + bx + c cleanly (omit zero terms, hide coefficient 1).
function quad(a, b, c) {
  let s = (a === 1 ? '' : a) + 'x²';
  if (b !== 0) s += (b < 0 ? ' − ' : ' + ') + (Math.abs(b) === 1 ? '' : Math.abs(b)) + 'x';
  if (c !== 0) s += (c < 0 ? ' − ' : ' + ') + Math.abs(c);
  return s;
}

// Build an MC question: pass correct value + array of distractor values (all numbers or strings).
function mc({ dom, diff, stem, correct, distractors, explanation, fmt = (x => String(x)) }) {
  // ensure unique, distinct distractors
  const seen = new Set([String(correct)]);
  const ds = [];
  for (const d of distractors) {
    const k = String(d);
    if (!seen.has(k)) { seen.add(k); ds.push(d); }
    if (ds.length === 3) break;
  }
  let bump = 1;
  while (ds.length < 3) { // backfill if collisions
    const cand = (typeof correct === 'number') ? correct + bump : correct + ' ' + bump;
    if (!seen.has(String(cand))) { seen.add(String(cand)); ds.push(cand); }
    bump++;
  }
  const opts = [correct, ...ds];
  // shuffle, track correct index
  for (let i = opts.length - 1; i > 0; i--) { const j = rnd(0, i); [opts[i], opts[j]] = [opts[j], opts[i]]; }
  const answer_index = opts.findIndex(o => String(o) === String(correct));
  return {
    question_id: 'g' + pad(++SEQ),
    section: 'math', section_name: 'Math',
    domain: dom, difficulty: diff, difficulty_label: ['', 'Easy', 'Medium', 'Hard'][diff],
    type: 'mc', passage: '', stem,
    choices: opts.map(fmt),
    answer_index, answer_text: fmt(correct),
    explanation, is_premium: false, active: true,
  };
}

function grid({ dom, diff, stem, correct, explanation }) {
  return {
    question_id: 'g' + pad(++SEQ),
    section: 'math', section_name: 'Math',
    domain: dom, difficulty: diff, difficulty_label: ['', 'Easy', 'Medium', 'Hard'][diff],
    type: 'grid', passage: '', stem, choices: [],
    answer_index: null, answer_text: String(correct),
    explanation, is_premium: false, active: true,
  };
}

const Q = [];
const add = q => Q.push(q);

/* ───────────────── ALGEBRA ───────────────── */
function genAlgebra(n) {
  for (let i = 0; i < n; i++) {
    const t = i % 6;
    if (t === 0) { // ax + b = c
      const a = rnd(2, 9), x = rnd(2, 12), b = rnd(1, 20), c = a * x + b;
      add(mc({ dom: 'Algebra', diff: 1, stem: `If ${a}x + ${b} = ${c}, what is the value of x?`,
        correct: x, distractors: [c - b, x + 1, Math.round(c / a)],
        explanation: `Subtract ${b}: ${a}x = ${c - b}. Divide by ${a}: x = ${x}.` }));
    } else if (t === 1) { // a(x+b)=c
      const a = rnd(2, 6), x = rnd(2, 9), b = rnd(1, 8), c = a * (x + b);
      add(mc({ dom: 'Algebra', diff: 2, stem: `Solve for x: ${a}(x + ${b}) = ${c}.`,
        correct: x, distractors: [x + b, c - b, x + 1],
        explanation: `Divide both sides by ${a}: x + ${b} = ${c / a}. Subtract ${b}: x = ${x}.` }));
    } else if (t === 2) { // slope from two points
      const x1 = rnd(-4, 2), y1 = rnd(-4, 4), m = pick([2, 3, -2, 4, -3]), dx = rnd(2, 5);
      const x2 = x1 + dx, y2 = y1 + m * dx;
      add(mc({ dom: 'Algebra', diff: 2, stem: `A line passes through (${x1}, ${y1}) and (${x2}, ${y2}). What is its slope?`,
        correct: m, distractors: [-m, m + 1, dx], explanation: `Slope = (${y2} − ${y1})/(${x2} − ${x1}) = ${y2 - y1}/${dx} = ${m}.` }));
    } else if (t === 3) { // flat fee + rate word problem (grid)
      const fee = rnd(2, 6) * 5, rate = rnd(2, 6) * 5, months = rnd(3, 10), total = fee + rate * months;
      add(grid({ dom: 'Algebra', diff: 2, stem: `A service charges a $${fee} setup fee plus $${rate} per month. After how many months is the total cost $${total}?`,
        correct: months, explanation: `${fee} + ${rate}m = ${total} → ${rate}m = ${total - fee} → m = ${months}.` }));
    } else if (t === 4) { // system, solve for x
      const x = rnd(1, 6), y = rnd(1, 6);
      const s = x + y, d = x - y; // x+y=s, x-y=d
      add(mc({ dom: 'Algebra', diff: 3, stem: `If x + y = ${s} and x − y = ${d}, what is the value of x?`,
        correct: x, distractors: [y, s, d], explanation: `Add the equations: 2x = ${s + d}, so x = ${x} (and y = ${y}).` }));
    } else { // inequality
      const a = rnd(2, 5), b = rnd(1, 10), c = rnd(1, 6);
      // ax + b > c  -> x > (c-b)/a ; choose numbers so boundary is integer
      const bound = rnd(-3, 4), cc = a * bound + b; // ax + b > cc -> x > bound
      const correct = bound + 1;
      add(mc({ dom: 'Algebra', diff: 2, stem: `Which value of x satisfies ${a}x + ${b} > ${cc}?`,
        correct, distractors: [bound, bound - 1, bound - 2],
        explanation: `${a}x + ${b} > ${cc} → ${a}x > ${cc - b} → x > ${bound}. The smallest listed value greater than ${bound} is ${correct}.` }));
    }
  }
}

/* ───────────────── ADVANCED MATH ───────────────── */
function genAdvanced(n) {
  for (let i = 0; i < n; i++) {
    const t = i % 6;
    if (t === 0) { // evaluate quadratic
      const a = rnd(1, 3), b = rnd(-4, 4), c = rnd(-5, 5), x = rnd(1, 4);
      const v = a * x * x + b * x + c;
      add(grid({ dom: 'Advanced Math', diff: 1, stem: `If f(x) = ${quad(a, b, c)}, what is f(${x})?`,
        correct: v, explanation: `Substitute x = ${x}: ${a}(${x})² ${b < 0 ? '− ' + (-b) : '+ ' + b}(${x}) ${c < 0 ? '− ' + (-c) : '+ ' + c} = ${v}.` }));
    } else if (t === 1) { // solve quadratic with integer roots
      let r1 = rnd(-6, 6), r2 = rnd(-6, 6); if (r1 === r2) r2 += 1;
      const b = -(r1 + r2), c = r1 * r2; const big = Math.max(r1, r2);
      const bs = b === 0 ? '' : (b < 0 ? ' − ' + (-b) + 'x' : ' + ' + b + 'x');
      const cs = c < 0 ? ' − ' + (-c) : ' + ' + c;
      add(mc({ dom: 'Advanced Math', diff: 2, stem: `What is the larger solution of x²${bs}${cs} = 0?`,
        correct: big, distractors: [Math.min(r1, r2), -big, big + 1],
        explanation: `Factor: (x − ${r1})(x − ${r2}) = 0 (written with signs), so x = ${r1} or ${r2}. The larger is ${big}.` }));
    } else if (t === 2) { // vertex x = -b/2a, integer
      const a = 1, h = rnd(-4, 5), b = -2 * a * h, k = rnd(-6, 6);
      const bs = b < 0 ? ' − ' + (-b) + 'x' : ' + ' + b + 'x';
      const ks = k < 0 ? ' − ' + (-k) : ' + ' + k;
      add(mc({ dom: 'Advanced Math', diff: 2, stem: `The graph of y = x²${bs}${ks} is a parabola. What is the x-coordinate of its vertex?`,
        correct: h, distractors: [-h, h + 1, b], explanation: `Vertex x = −b/(2a) = −(${b})/(2·1) = ${h}.` }));
    } else if (t === 3) { // exponential evaluate
      const a0 = rnd(2, 6) * 50, base = pick([2, 3]), per = pick([2, 3]), steps = rnd(1, 3);
      const tval = per * steps, result = a0 * Math.pow(base, steps);
      add(mc({ dom: 'Advanced Math', diff: 3, stem: `A quantity of ${a0} is multiplied by ${base} every ${per} hours, modeled by P = ${a0}·${base}^(t/${per}). What is P after ${tval} hours?`,
        correct: result, distractors: [a0 * base, a0 * Math.pow(base, steps + 1), a0 + base * steps],
        explanation: `t = ${tval} → ${base}^(${tval}/${per}) = ${base}^${steps} = ${Math.pow(base, steps)}. P = ${a0}·${Math.pow(base, steps)} = ${result}.` }));
    } else if (t === 4) { // expand (x+p)(x+q) constant term
      const p = rnd(-6, 6), q = rnd(-6, 6), constant = p * q;
      add(mc({ dom: 'Advanced Math', diff: 1, stem: `What is the constant term when (x ${p < 0 ? '− ' + (-p) : '+ ' + p})(x ${q < 0 ? '− ' + (-q) : '+ ' + q}) is expanded?`,
        correct: constant, distractors: [p + q, -constant, p * q + 1],
        explanation: `The constant term is the product of the constants: (${p})(${q}) = ${constant}.` }));
    } else { // 2^x = value
      const x = rnd(3, 7), v = Math.pow(2, x);
      add(grid({ dom: 'Advanced Math', diff: 2, stem: `If 2^x = ${v}, what is the value of x?`,
        correct: x, explanation: `${v} = 2^${x}, so x = ${x}.` }));
    }
  }
}

/* ───────────────── PROBLEM-SOLVING & DATA ───────────────── */
function genData(n) {
  for (let i = 0; i < n; i++) {
    const t = i % 7;
    if (t === 0) { // percent of number
      const p = pick([10, 20, 25, 40, 50, 75]), base = rnd(2, 20) * 10, v = p / 100 * base;
      add(grid({ dom: 'Problem-Solving & Data', diff: 1, stem: `What is ${p}% of ${base}?`,
        correct: v, explanation: `${p / 100} × ${base} = ${v}.` }));
    } else if (t === 1) { // discount price
      const price = rnd(2, 12) * 10, p = pick([10, 20, 25, 50]), sale = price * (1 - p / 100);
      add(mc({ dom: 'Problem-Solving & Data', diff: 2, stem: `A $${price} item is marked down ${p}%. What is the sale price?`,
        correct: sale, distractors: [price * p / 100, price - p, price * (1 + p / 100)], fmt: x => '$' + x,
        explanation: `${p}% of ${price} = ${price * p / 100} off, so ${price} − ${price * p / 100} = $${sale}.` }));
    } else if (t === 2) { // percent change
      const oldv = rnd(2, 10) * 10, p = pick([10, 20, 25, 50]), newv = oldv * (1 + p / 100);
      add(mc({ dom: 'Problem-Solving & Data', diff: 3, stem: `A value increases from ${oldv} to ${newv}. What is the percent increase?`,
        correct: p, distractors: [p + 5, Math.round((newv - oldv)), p - 5], fmt: x => x + '%',
        explanation: `Change = ${newv - oldv}; ${newv - oldv}/${oldv} = ${(newv - oldv) / oldv} = ${p}%.` }));
    } else if (t === 3) { // ratio split
      const a = rnd(2, 5), b = rnd(2, 6), unit = rnd(2, 6), total = (a + b) * unit, larger = Math.max(a, b) * unit;
      add(mc({ dom: 'Problem-Solving & Data', diff: 2, stem: `Two quantities are in the ratio ${a} : ${b} and sum to ${total}. What is the larger quantity?`,
        correct: larger, distractors: [Math.min(a, b) * unit, total / 2, larger + unit],
        explanation: `${a + b} parts = ${total}, so 1 part = ${unit}. The larger is ${Math.max(a, b)} × ${unit} = ${larger}.` }));
    } else if (t === 4) { // mean
      const vals = Array.from({ length: 4 }, () => rnd(2, 20)); const mean = vals.reduce((s, v) => s + v, 0) / 4;
      if (Number.isInteger(mean)) {
        add(grid({ dom: 'Problem-Solving & Data', diff: 1, stem: `What is the mean (average) of ${vals.join(', ')}?`,
          correct: mean, explanation: `Sum = ${vals.reduce((s, v) => s + v, 0)}; ÷ 4 = ${mean}.` }));
      } else { i--; } // retry for integer mean
    } else if (t === 5) { // probability
      const r = rnd(2, 6), b = rnd(2, 6), tot = r + b;
      add(mc({ dom: 'Problem-Solving & Data', diff: 2, stem: `A bag has ${r} red and ${b} blue marbles. What is the probability of drawing a red marble?`,
        correct: frac(r, tot), distractors: [frac(b, tot), frac(r, b), frac(b, r), frac(r + 1, tot)].filter(d => d !== frac(r, tot)),
        explanation: `${tot} marbles total; P(red) = ${r}/${tot}${frac(r, tot) !== `${r}/${tot}` ? ' = ' + frac(r, tot) : ''}.` }));
    } else { // unit rate scaling
      const rate = rnd(2, 9), units = rnd(2, 6), dist = rate * units, hrs = rnd(2, 8), out = rate * hrs;
      add(grid({ dom: 'Problem-Solving & Data', diff: 2, stem: `A machine produces ${dist} items in ${units} hours at a constant rate. How many items does it produce in ${hrs} hours?`,
        correct: out, explanation: `Rate = ${dist}/${units} = ${rate}/hour. ${rate} × ${hrs} = ${out}.` }));
    }
  }
}

/* ───────────────── GEOMETRY & TRIG ───────────────── */
function genGeometry(n) {
  const triples = [[3, 4, 5], [6, 8, 10], [5, 12, 13], [8, 15, 17], [9, 12, 15], [7, 24, 25]];
  for (let i = 0; i < n; i++) {
    const t = i % 7;
    if (t === 0) { // circle area
      const r = rnd(2, 10);
      add(mc({ dom: 'Geometry & Trig', diff: 1, stem: `A circle has radius ${r}. What is its area?`,
        correct: `${r * r}π`, distractors: [`${2 * r}π`, `${r}π`, `${r * r * 2}π`],
        explanation: `A = πr² = π(${r})² = ${r * r}π.` }));
    } else if (t === 1) { // pythagorean hyp (grid)
      const [a, b, c] = pick(triples);
      add(grid({ dom: 'Geometry & Trig', diff: 1, stem: `A right triangle has legs of length ${a} and ${b}. What is the length of the hypotenuse?`,
        correct: c, explanation: `c² = ${a}² + ${b}² = ${a * a + b * b}, so c = ${c}.` }));
    } else if (t === 2) { // angle sum
      const x = rnd(30, 80), y = rnd(20, 80 - 0), third = 180 - x - y;
      if (third > 10 && third < 130) {
        add(grid({ dom: 'Geometry & Trig', diff: 1, stem: `Two angles of a triangle measure ${x}° and ${y}°. What is the measure, in degrees, of the third angle?`,
          correct: third, explanation: `Angles sum to 180°: 180 − ${x} − ${y} = ${third}°.` }));
      } else { i--; }
    } else if (t === 3) { // box / cube volume
      const useCube = Math.random() < 0.5;
      if (useCube) { const s = rnd(2, 8); add(grid({ dom: 'Geometry & Trig', diff: 2, stem: `A cube has edge length ${s}. What is its volume?`, correct: s ** 3, explanation: `V = s³ = ${s}³ = ${s ** 3}.` })); }
      else { const l = rnd(2, 8), w = rnd(2, 6), h = rnd(2, 6); add(grid({ dom: 'Geometry & Trig', diff: 2, stem: `A rectangular box measures ${l} × ${w} × ${h}. What is its volume?`, correct: l * w * h, explanation: `V = ℓwh = ${l}·${w}·${h} = ${l * w * h}.` })); }
    } else if (t === 4) { // sin/cos/tan
      const [a, b, c] = pick(triples); const ratio = pick(['sin', 'cos', 'tan']);
      const val = ratio === 'sin' ? frac(a, c) : ratio === 'cos' ? frac(b, c) : frac(a, b);
      add(mc({ dom: 'Geometry & Trig', diff: 2, stem: `In a right triangle, the side opposite angle θ is ${a}, the side adjacent is ${b}, and the hypotenuse is ${c}. What is ${ratio} θ?`,
        correct: val, distractors: [frac(b, c), frac(a, b), frac(a, c), frac(c, a), frac(b, a)].filter(d => d !== val),
        explanation: `${ratio} θ = ${ratio === 'sin' ? 'opposite/hypotenuse' : ratio === 'cos' ? 'adjacent/hypotenuse' : 'opposite/adjacent'} = ${val}.` }));
    } else if (t === 5) { // similar triangles
      const a = rnd(2, 6), k = rnd(2, 4), b = rnd(3, 7), A = a * k, B = b * k;
      add(mc({ dom: 'Geometry & Trig', diff: 3, stem: `Triangle 1 has sides ${a} and ${b}. A similar triangle 2 has the side corresponding to ${a} equal to ${A}. What is the side of triangle 2 corresponding to ${b}?`,
        correct: B, distractors: [b + (A - a), B + k, b * (k + 1)],
        explanation: `Scale factor = ${A}/${a} = ${k}. Corresponding side = ${b} × ${k} = ${B}.` }));
    } else { // circumference
      const r = rnd(2, 12);
      add(mc({ dom: 'Geometry & Trig', diff: 1, stem: `A circle has radius ${r}. What is its circumference?`,
        correct: `${2 * r}π`, distractors: [`${r * r}π`, `${r}π`, `${4 * r}π`],
        explanation: `C = 2πr = 2π(${r}) = ${2 * r}π.` }));
    }
  }
}

genAlgebra(30);
genAdvanced(30);
genData(32);
genGeometry(34);

// de-dupe by (stem) to avoid identical random collisions
const seenStem = new Set();
const unique = Q.filter(q => { if (seenStem.has(q.stem)) return false; seenStem.add(q.stem); return true; });

fs.writeFileSync('base44/questions_pack2.json', JSON.stringify(unique, null, 2));
const by = {}; const byDiff = { 1: 0, 2: 0, 3: 0 };
unique.forEach(q => { by[q.domain] = (by[q.domain] || 0) + 1; byDiff[q.difficulty]++; });
console.log('Generated', unique.length, 'new questions');
console.log('By domain:', by);
console.log('By difficulty (easy/med/hard):', byDiff);
console.log('Grid-ins:', unique.filter(q => q.type === 'grid').length, '| MC:', unique.filter(q => q.type === 'mc').length);
