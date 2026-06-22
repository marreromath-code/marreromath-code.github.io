/* Pack 6: original questions modeled on uploaded CB linear-model archetypes (blueprint only).
   Skills: identify a/b in f(x)=a+bx, interpret x-intercept in context, x-intercept from slope+yint,
   rate-of-change applied to a delta, evaluate initial+rate*amount. IDs prefix 'q'. */
const fs = require('fs');
let SEQ = 0;
const pad = n => String(n).padStart(4, '0');
const rnd = (lo, hi) => Math.floor(Math.random() * (hi - lo + 1)) + lo;
const pick = a => a[Math.floor(Math.random() * a.length)];
const sg = n => (n < 0 ? '− ' + (-n) : '+ ' + n);
const num = x => String(Math.round(x * 100) / 100);   // trim to 2 dp, no trailing zeros
function mc({ dom, diff, stem, correct, distractors, explanation }) {
  const seen = new Set([correct]); const ds = [];
  for (const d of distractors) { if (!seen.has(d)) { seen.add(d); ds.push(d); } if (ds.length === 3) break; }
  let bump = 1; while (ds.length < 3) { const c = correct + ' (' + bump++ + ')'; if (!seen.has(c)) { seen.add(c); ds.push(c); } }
  const opts = [correct, ...ds];
  for (let i = opts.length - 1; i > 0; i--) { const j = rnd(0, i); [opts[i], opts[j]] = [opts[j], opts[i]]; }
  return { question_id: 'q' + pad(++SEQ), section: 'math', section_name: 'Math', domain: dom, difficulty: diff, difficulty_label: ['', 'Easy', 'Medium', 'Hard'][diff], type: 'mc', passage: '', stem, choices: opts, answer_index: opts.indexOf(correct), answer_text: correct, explanation, is_premium: false, active: true };
}
function grid({ dom, diff, stem, correct, explanation }) {
  return { question_id: 'q' + pad(++SEQ), section: 'math', section_name: 'Math', domain: dom, difficulty: diff, difficulty_label: ['', 'Easy', 'Medium', 'Hard'][diff], type: 'grid', passage: '', stem, choices: [], answer_index: null, answer_text: String(correct), explanation, is_premium: false, active: true };
}
const Q = []; const add = q => Q.push(q);

/* A — identify a (initial) or b (rate) in f(x) = a + bx */
const A_CTX = [
  { thing: 'newly planted tree', init: rnd(12, 30), iu: 'inches', sp: 'tall when it was planted', cv: 'grew', ru: 'inches', per: 'week', out: 'the height, in inches, of the tree', pw: 'weeks', start: 'it was planted' },
  { thing: 'used car', init: rnd(20, 80) * 1000, iu: 'miles', sp: 'on its odometer when purchased', cv: 'was driven', ru: 'miles', per: 'day', out: 'the odometer reading, in miles', pw: 'days', start: 'it was purchased' },
  { thing: 'savings account', init: rnd(50, 400), iu: 'dollars', sp: 'when it was opened', cv: 'grew by', ru: 'dollars', per: 'month', out: 'the balance, in dollars', pw: 'months', start: 'it was opened' },
];
function genA(n) {
  for (let i = 0; i < n; i++) {
    const c = A_CTX[i % A_CTX.length]; const init = c.init === undefined ? 0 : c.init; const rate = rnd(2, 9);
    const askA = i % 2 === 0;
    add(grid({ dom: 'Algebra', diff: 2,
      stem: `A model predicts that a ${c.thing} ${c.iu === 'dollars' ? 'held ' + init + ' ' + c.iu : 'was ' + init + ' ' + c.iu} ${c.sp} and ${c.cv} ${rate} ${c.ru} per ${c.per}. The model is defined by f(x) = a + bx, where f(x) is ${c.out} x ${c.pw} after ${c.start}, and a and b are constants. What is the value of ${askA ? 'a' : 'b'}?`,
      correct: askA ? init : rate,
      explanation: askA ? `a is the value when x = 0 — the ${c.iu === 'dollars' ? 'starting balance' : 'initial amount'}, which is ${init}.` : `b is the rate of change per ${c.per}, which is ${rate}.` }));
  }
}

/* B — interpret the x-intercept of a decreasing model y = init - rate*x */
const B_CTX = [
  { subj: 'team', res: 'cargo', done: 'moved all the cargo', unit: 'tons', per: 'hour', slope: 'moving', tunit: 'hours' },
  { subj: 'pump', res: 'water', done: 'be completely drained', unit: 'liters', per: 'minute', slope: 'draining', tunit: 'minutes' },
  { subj: 'generator', res: 'fuel', done: 'run out of fuel', unit: 'gallons', per: 'hour', slope: 'using fuel', tunit: 'hours' },
];
function genB(n) {
  const pairs = [[120, 25], [90, 15], [150, 20], [300, 40], [200, 16], [96, 15], [84, 16], [105, 14]];
  for (let i = 0; i < n; i++) {
    const c = B_CTX[i % B_CTX.length]; const [init, rate] = pairs[i % pairs.length]; const T = num(init / rate);
    const correct = `The ${c.subj} will have ${c.done} in about ${T} ${c.tunit}.`;
    add(mc({ dom: 'Algebra', diff: 2,
      stem: `A ${c.subj} is ${c.slope}. The number of ${c.unit} of ${c.res} remaining, y, after x ${c.tunit} is modeled by y = ${init} − ${rate}x. The graph of this equation is a line. What is the best interpretation of the x-intercept in this context?`,
      correct,
      distractors: [
        `The ${c.subj} has been ${c.slope} about ${T} ${c.unit} per ${c.per}.`,
        `The ${c.subj} has been ${c.slope} about ${rate} ${c.unit} per ${c.per}.`,
        `The ${c.subj} started with ${init} ${c.unit} of ${c.res}.`,
      ],
      explanation: `The x-intercept is where y = 0: 0 = ${init} − ${rate}x → x = ${init}/${rate} = ${T}. So after about ${T} ${c.tunit}, no ${c.res} remains.` }));
  }
}

/* C — x-coordinate of the x-intercept from slope + y-intercept */
function genC(n) {
  for (let i = 0; i < n; i++) {
    const m = rnd(2, 7); let x = rnd(-8, 8); if (x === 0) x = 3; const b = -m * x;
    add(grid({ dom: 'Algebra', diff: 2,
      stem: `In the xy-plane, line k has a slope of ${m} and a y-intercept of (0, ${b}). What is the x-coordinate of the x-intercept of line k?`,
      correct: x,
      explanation: `The line is y = ${m}x ${sg(b)}. At the x-intercept y = 0: 0 = ${m}x ${sg(b)} → ${m}x = ${-b} → x = ${x}.` }));
  }
}

/* D — rate of change applied to a delta increase */
const D_CTX = [
  { name: 'R', out: 'the revenue, in dollars', inn: 'units sold' },
  { name: 'C', out: 'the cost, in dollars', inn: 'items produced' },
  { name: 'H', out: 'the amount of heat, in joules', inn: 'seconds' },
];
function genD(n) {
  for (let i = 0; i < n; i++) {
    const c = D_CTX[i % D_CTX.length]; const s = pick([1.5, 1.8, 2.5, 0.6, 1.2, 2.4, 3.5]); const k = rnd(10, 200); const d = pick([4, 6, 8, 9, 12, 9.1, 4.5, 6.2]);
    const inc = num(s * d);
    add(mc({ dom: 'Algebra', diff: 3,
      stem: `The function ${c.name} gives ${c.out} for an input of x ${c.inn}, where ${c.name}(x) = ${s}x + ${k}. If x increases by ${d} ${c.inn}, by how much does ${c.name}(x) increase?`,
      correct: inc,
      distractors: [num(s * d + k), num(d), num(s + d)],
      explanation: `A change in x of ${d} changes ${c.name}(x) by the slope times the change: ${s} × ${d} = ${inc}. (The constant ${k} does not affect the change.)` }));
  }
}

/* E — evaluate a real-world linear model: initial + rate * amount */
const E_CTX = [
  { q: 'the total cost, in dollars,', base: 19.5, bu: 'dollars', rate: 0.75, ru: 'dollars', step: 'class attended', amt: 'classes', who: 'A gym membership' },
  { q: 'the total pressure, in psi,', base: 14.2, bu: 'psi', rate: 0.43, ru: 'psi', step: 'foot descended', amt: 'feet', who: 'The pressure at the surface' },
  { q: 'the total fare, in dollars,', base: 3.5, bu: 'dollars', rate: 0.4, ru: 'dollars', step: 'mile traveled', amt: 'miles', who: 'A taxi ride' },
];
function genE(n) {
  for (let i = 0; i < n; i++) {
    const c = E_CTX[i % E_CTX.length]; const amt = rnd(8, 40); const total = num(c.base + c.rate * amt);
    add(mc({ dom: 'Algebra', diff: 2,
      stem: `${c.who} starts at ${c.base} ${c.bu}, and increases by ${c.rate} ${c.ru} for each ${c.step}. What is ${c.q} for ${amt} ${c.amt}?`,
      correct: total,
      distractors: [num(c.rate * amt), num(c.base), num(c.base + c.rate)],
      explanation: `Total = base + rate × amount = ${c.base} + ${c.rate} × ${amt} = ${c.base} + ${num(c.rate * amt)} = ${total}.` }));
  }
}

genA(12); genB(12); genC(14); genD(12); genE(12);
const seenStem = new Set();
const unique = Q.filter(q => { if (seenStem.has(q.stem)) return false; seenStem.add(q.stem); return true; });
fs.writeFileSync('base44/questions_pack6.json', JSON.stringify(unique, null, 2));
const by = {}; unique.forEach(q => by[q.difficulty_label] = (by[q.difficulty_label] || 0) + 1);
console.log('Generated', unique.length, 'original questions (pack 6)');
console.log('By difficulty:', by, '| grid-ins:', unique.filter(q => q.type === 'grid').length);
