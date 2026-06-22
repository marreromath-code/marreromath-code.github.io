/* Pack 4: original questions modeled on the 4 uploaded CB "Linear Functions" archetypes.
   Blueprint = skill + format + difficulty only. New contexts/numbers/structure. IDs prefix 'k'. */
const fs = require('fs');
let SEQ = 0;
const pad = n => String(n).padStart(4, '0');
const rnd = (lo, hi) => Math.floor(Math.random() * (hi - lo + 1)) + lo;
const pick = a => a[Math.floor(Math.random() * a.length)];
const sg = n => (n < 0 ? '− ' + (-n) : '+ ' + n);

function mc({ dom, diff, stem, correct, distractors, explanation, fmt = (x => String(x)) }) {
  const seen = new Set([String(correct)]); const ds = [];
  for (const d of distractors) { const k = String(d); if (!seen.has(k)) { seen.add(k); ds.push(d); } if (ds.length === 3) break; }
  let bump = 1;
  while (ds.length < 3) { const cand = (typeof correct === 'number') ? correct + bump : correct + ' ' + bump; if (!seen.has(String(cand))) { seen.add(String(cand)); ds.push(cand); } bump++; }
  const opts = [correct, ...ds];
  for (let i = opts.length - 1; i > 0; i--) { const j = rnd(0, i); [opts[i], opts[j]] = [opts[j], opts[i]]; }
  return { question_id: 'k' + pad(++SEQ), section: 'math', section_name: 'Math', domain: dom, difficulty: diff, difficulty_label: ['', 'Easy', 'Medium', 'Hard'][diff], type: 'mc', passage: '', stem, choices: opts.map(fmt), answer_index: opts.findIndex(o => String(o) === String(correct)), answer_text: fmt(correct), explanation, is_premium: false, active: true };
}
function grid({ dom, diff, stem, correct, explanation }) {
  return { question_id: 'k' + pad(++SEQ), section: 'math', section_name: 'Math', domain: dom, difficulty: diff, difficulty_label: ['', 'Easy', 'Medium', 'Hard'][diff], type: 'grid', passage: '', stem, choices: [], answer_index: null, answer_text: String(correct), explanation, is_premium: false, active: true };
}
const Q = []; const add = q => Q.push(q);

/* Archetype 1 — evaluate a linear function f(c) */
function arch1(n) {
  for (let i = 0; i < n; i++) {
    const a = rnd(3, 30), b = rnd(4, 50), c = rnd(2, 9), v = a * c + b;
    add(mc({ dom: 'Algebra', diff: 1, stem: `The function f is defined by f(x) = ${a}x ${sg(b)}. What is the value of f(${c})?`,
      correct: v, distractors: [a * c, a + c + b, (a + b) * c],
      explanation: `Substitute ${c} for x: f(${c}) = ${a}(${c}) ${sg(b)} = ${a * c} ${sg(b)} = ${v}.` }));
  }
}

/* Archetype 2 — solve a linear function for its input */
function arch2(n) {
  for (let i = 0; i < n; i++) {
    const a = rnd(3, 12), x = rnd(3, 12), v = a * x;
    add(mc({ dom: 'Algebra', diff: 1, stem: `The function f is defined by f(x) = ${a}x. For what value of x does f(x) = ${v}?`,
      correct: x, distractors: [v, v - a, a + x],
      explanation: `Set ${a}x = ${v}. Divide both sides by ${a}: x = ${x}.` }));
  }
}

/* Archetype 3 — build a linear model: fixed first unit + rate per additional unit */
const CONTEXTS = [
  { who: 'A plumber', first: 'the first hour', add: 'each additional hour', unit: 'hours', noun: 'a job lasting' },
  { who: 'A piano teacher', first: 'the first lesson', add: 'each additional lesson', unit: 'lessons', noun: 'a package of' },
  { who: 'A kayak outfitter', first: 'the first day', add: 'each additional day', unit: 'days', noun: 'a rental of' },
  { who: 'A moving company', first: 'the first hour', add: 'each additional hour', unit: 'hours', noun: 'a move lasting' },
  { who: 'A landscaping service', first: 'the first visit', add: 'each additional visit', unit: 'visits', noun: 'a plan of' },
  { who: 'A photo booth rental', first: 'the first hour', add: 'each additional hour', unit: 'hours', noun: 'an event lasting' },
  { who: 'A tutoring center', first: 'the first session', add: 'each additional session', unit: 'sessions', noun: 'a plan of' },
  { who: 'A bike-share service', first: 'the first day', add: 'each additional day', unit: 'days', noun: 'a rental of' },
];
function arch3(n) {
  for (let i = 0; i < n; i++) {
    const ctx = CONTEXTS[i % CONTEXTS.length];
    const rate = rnd(2, 9) * 5, first = rate + rnd(2, 8) * 5, cap = rnd(8, 14), intercept = first - rate; // first > rate
    const correct = `y = ${rate}x ${sg(intercept)}`;
    add(mc({ dom: 'Algebra', diff: 2,
      stem: `${ctx.who} charges $${first} for ${ctx.first} and $${rate} for ${ctx.add}. Which equation gives the total cost y, in dollars, for ${ctx.noun} x ${ctx.unit}, where x is a positive integer and x ≤ ${cap}?`,
      correct, distractors: [`y = ${first}x + ${rate}`, `y = ${rate}x + ${first}`, `y = ${first}x ${sg(intercept)}`], fmt: x => x,
      explanation: `The cost is $${first} for the first ${ctx.unit.slice(0, -1)} plus $${rate} for the other (x − 1) ${ctx.unit}: y = ${first} + ${rate}(x − 1) = ${rate}x + (${first} − ${rate}) = ${rate}x ${sg(intercept)}.` }));
  }
}

/* Archetype 4 — use a condition to solve for a constant, then evaluate (grid-in) */
function arch4(n) {
  for (let i = 0; i < n; i++) {
    const a = rnd(2, 6), c = rnd(1, 3), k = rnd(2, 6), p = rnd(c + 3, c + 6), r = rnd(p + 2, p + 6);
    const q = a * p + k * (p - c);          // f(p)
    const result = a * r + k * (r - c);     // f(r)
    add(grid({ dom: 'Advanced Math', diff: 3,
      stem: `The function f is defined by f(x) = ${a}x + k(x − ${c}), where k is a constant, and f(${p}) = ${q}. What is the value of f(${r})?`,
      correct: result,
      explanation: `Use f(${p}) = ${q}: ${q} = ${a}(${p}) + k(${p} − ${c}) = ${a * p} + ${p - c}k, so ${p - c}k = ${q - a * p} and k = ${k}. Then f(${r}) = ${a}(${r}) + ${k}(${r} − ${c}) = ${a * r} + ${k * (r - c)} = ${result}.` }));
  }
}

arch1(15); arch2(13); arch3(14); arch4(12);

const seenStem = new Set();
const unique = Q.filter(q => { if (seenStem.has(q.stem)) return false; seenStem.add(q.stem); return true; });
fs.writeFileSync('base44/questions_pack4.json', JSON.stringify(unique, null, 2));
const by = {}; unique.forEach(q => by[q.difficulty_label] = (by[q.difficulty_label] || 0) + 1);
console.log('Generated', unique.length, 'original linear-functions questions (pack 4)');
console.log('By difficulty:', by, '| grid-ins:', unique.filter(q => q.type === 'grid').length);
