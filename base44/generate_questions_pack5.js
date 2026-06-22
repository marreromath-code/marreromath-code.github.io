/* Pack 5: original questions modeled on uploaded CB "Linear Functions" archetypes.
   Text-friendly skills only (rate interpretation, constant function, equation from two points).
   Graph-reading items are intentionally excluded until the app supports figures. IDs prefix 'p'. */
const fs = require('fs');
let SEQ = 0;
const pad = n => String(n).padStart(4, '0');
const rnd = (lo, hi) => Math.floor(Math.random() * (hi - lo + 1)) + lo;
const sg = n => (n < 0 ? '− ' + (-n) : '+ ' + n);
function mc({ dom, diff, stem, correct, distractors, explanation }) {
  const seen = new Set([String(correct)]); const ds = [];
  for (const d of distractors) { const k = String(d); if (!seen.has(k)) { seen.add(k); ds.push(d); } if (ds.length === 3) break; }
  let bump = 1; while (ds.length < 3) { const cand = correct + ' (' + bump + ')'; if (!seen.has(cand)) { seen.add(cand); ds.push(cand); } bump++; }
  const opts = [correct, ...ds];
  for (let i = opts.length - 1; i > 0; i--) { const j = rnd(0, i); [opts[i], opts[j]] = [opts[j], opts[i]]; }
  return { question_id: 'p' + pad(++SEQ), section: 'math', section_name: 'Math', domain: dom, difficulty: diff, difficulty_label: ['', 'Easy', 'Medium', 'Hard'][diff], type: 'mc', passage: '', stem, choices: opts, answer_index: opts.indexOf(correct), answer_text: correct, explanation, is_premium: false, active: true };
}
const Q = []; const add = q => Q.push(q);

/* Archetype 5 — interpret the rate (coefficient) in a context equation */
const RATE_CTX = [
  { v: 'w', q: 'the amount of water w, in liters', tn: 'minutes', per: 'minute', subj: 'tank', rate: 'is filling', tot: 'has held', vb: 'filling' },
  { v: 's', q: 'the total savings s, in dollars', tn: 'weeks', per: 'week', subj: 'account', rate: 'is growing', tot: 'has held', vb: 'growing' },
  { v: 'h', q: 'the height h, in centimeters', tn: 'days', per: 'day', subj: 'plant', rate: 'is growing', tot: 'has grown', vb: 'growing' },
  { v: 'p', q: 'the number of pages p', tn: 'hours', per: 'hour', subj: 'reader', rate: 'is reading', tot: 'has read', vb: 'reading' },
  { v: 'c', q: 'the number of copies c', tn: 'minutes', per: 'minute', subj: 'printer', rate: 'is printing', tot: 'has printed', vb: 'printing' },
  { v: 'e', q: 'the energy e, in kilojoules', tn: 'seconds', per: 'second', subj: 'device', rate: 'is using energy', tot: 'has used', vb: 'using energy' },
];
function arch5(n) {
  for (let i = 0; i < n; i++) {
    const ctx = RATE_CTX[i % RATE_CTX.length]; const k = rnd(3, 25);
    const correct = `The ${ctx.subj} ${ctx.rate} at a rate of ${k} ${unitOf(ctx)} per ${ctx.per}.`;
    add(mc({ dom: 'Algebra', diff: 1,
      stem: `The equation ${ctx.v} = ${k}t represents ${ctx.q}, where t is the number of ${ctx.tn}. Which of the following is the best interpretation of ${k} in this context?`,
      correct,
      distractors: [
        `The ${ctx.subj} ${ctx.tot} a total of ${k} ${unitOf(ctx)}.`,
        `The ${ctx.subj} ${ctx.tot} a total of ${k}t ${unitOf(ctx)}.`,
        `The ${ctx.subj} ${ctx.rate} at a rate of 1/${k} ${unitOf(ctx)} per ${ctx.per}.`,
      ],
      explanation: `In ${ctx.v} = ${k}t, t is multiplied by ${k}, so ${ctx.v} increases by ${k} ${unitOf(ctx)} for each ${ctx.per} — a rate of ${k} ${unitOf(ctx)} per ${ctx.per}.` }));
  }
}
function unitOf(ctx) { const m = ctx.q.match(/in (\w+)/); return m ? m[1] : (ctx.q.includes('pages') ? 'pages' : ctx.q.includes('copies') ? 'copies' : 'units'); }

/* Archetype 6 — constant function: which set of values matches f(x) = c */
function arch6(n) {
  for (let i = 0; i < n; i++) {
    const c = rnd(2, 9) * (rnd(0, 1) ? 1 : 10) + rnd(0, 9);
    const correct = `x = 0, 1, 2 give f(x) = ${c}, ${c}, ${c}`;
    add(mc({ dom: 'Algebra', diff: 1,
      stem: `The function f is defined by f(x) = ${c}. Which of the following correctly lists three values of x and their corresponding values of f(x)?`,
      correct,
      distractors: [
        `x = 0, 1, 2 give f(x) = 0, 0, 0`,
        `x = 0, 1, 2 give f(x) = 0, ${c}, ${2 * c}`,
        `x = 0, 1, 2 give f(x) = ${c}, 0, ${-c}`,
      ],
      explanation: `f(x) = ${c} is a constant function, so f(x) = ${c} for every x. Thus f(0) = f(1) = f(2) = ${c}.` }));
  }
}

/* Archetype 7 — build the equation from two points (one on the y-axis) */
function arch7(n) {
  for (let i = 0; i < n; i++) {
    const b = rnd(-5, 9), p = rnd(3, 8), m = rnd(2, 7), q = b + m * p;
    const correct = `f(x) = ${m}x ${sg(b)}`;
    add(mc({ dom: 'Algebra', diff: 2,
      stem: `In the xy-plane, the graph of the linear function f contains the points (0, ${b}) and (${p}, ${q}). Which equation defines f, where y = f(x)?`,
      correct,
      distractors: [`f(x) = ${m}x ${sg(q)}`, `f(x) = ${q}x ${sg(b)}`, `f(x) = ${p}x ${sg(b)}`],
      explanation: `The point (0, ${b}) is the y-intercept, so b = ${b}. The slope is (${q} − ${b})/(${p} − 0) = ${q - b}/${p} = ${m}. So f(x) = ${m}x ${sg(b)}.` }));
  }
}

arch5(16); arch6(13); arch7(16);
const seenStem = new Set();
const unique = Q.filter(q => { if (seenStem.has(q.stem)) return false; seenStem.add(q.stem); return true; });
fs.writeFileSync('base44/questions_pack5.json', JSON.stringify(unique, null, 2));
const by = {}; unique.forEach(q => by[q.difficulty_label] = (by[q.difficulty_label] || 0) + 1);
console.log('Generated', unique.length, 'original questions (pack 5)');
console.log('By difficulty:', by);
