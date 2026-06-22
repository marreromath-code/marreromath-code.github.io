const fs = require('fs');
let SEQ = 0;
const pad = n => String(n).padStart(4, '0');
const rnd = (lo, hi) => Math.floor(Math.random() * (hi - lo + 1)) + lo;
const pick = a => a[Math.floor(Math.random() * a.length)];
const gcd = (a, b) => b ? gcd(b, a % b) : Math.abs(a);
const frac = (a, b) => { const g = gcd(a, b) || 1; return `${a / g}/${b / g}`; };
const num = x => String(Math.round(x * 1000) / 1000);
function mc({ dom = 'Problem-Solving & Data', diff, stem, figure = '', correct, distractors, explanation }) {
  const seen = new Set([correct]); const ds = [];
  for (const d of distractors) { if (!seen.has(d)) { seen.add(d); ds.push(d); } if (ds.length === 3) break; }
  let b = 1; while (ds.length < 3) { const c = correct + ' (' + b++ + ')'; if (!seen.has(c)) { seen.add(c); ds.push(c); } }
  const opts = [correct, ...ds];
  for (let i = opts.length - 1; i > 0; i--) { const j = rnd(0, i); [opts[i], opts[j]] = [opts[j], opts[i]]; }
  return { question_id: 'd' + pad(++SEQ), section: 'math', section_name: 'Math', domain: dom, difficulty: diff, difficulty_label: ['', 'Easy', 'Medium', 'Hard'][diff], type: 'mc', passage: '', figure, stem, choices: opts, answer_index: opts.indexOf(correct), answer_text: correct, explanation, is_premium: false, active: true };
}
const Q = []; const add = q => Q.push(q);

/* A — percent relationship from context: each unit = R% of allowance; x units -> p% */
const A_CTX = [
  { food: 'a fortified cereal', nutrient: 'potassium' }, { food: 'an energy bar', nutrient: 'iron' },
  { food: 'a smoothie', nutrient: 'vitamin C' }, { food: 'a protein shake', nutrient: 'calcium' },
];
function genA(n) {
  for (let i = 0; i < n; i++) {
    const c = A_CTX[i % A_CTX.length], R = pick([2, 4, 5, 8, 10]);
    add(mc({ diff: 2,
      stem: `Each serving of ${c.food} provides ${R}% of an adult's daily allowance of ${c.nutrient}. If p percent of an adult's daily allowance of ${c.nutrient} is provided by x servings per day, which equation expresses p in terms of x?`,
      correct: `p = ${R}x`,
      distractors: [`p = ${num(R / 10)}x`, `p = (${num(R / 100)})^x`, `p = (${num(1 + R / 100)})^x`],
      explanation: `Each serving gives ${R}%, so x servings give x times ${R}%. The relationship is linear: p = ${R}x.` }));
  }
}

/* B — interpret a multiplier as a percent change */
function genB(n) {
  for (let i = 0; i < n; i++) {
    const dec = rnd(0, 1); // 0 = decrease, 1 = increase
    let factor, pct, dir, correct;
    if (dec === 0) { const keep = pick([0.2, 0.35, 0.4, 0.65, 0.8, 0.9, 0.25, 0.75]); factor = keep; pct = Math.round((1 - keep) * 100); dir = 'decreasing'; }
    else { const g = pick([1.1, 1.2, 1.25, 1.4, 1.5, 1.05, 1.75]); factor = g; pct = Math.round((g - 1) * 100); dir = 'increasing'; }
    correct = pct + '%';
    add(mc({ diff: 2,
      stem: `The expression ${num(factor)}x represents the result of ${dir} a positive quantity x by what percent?`,
      correct,
      distractors: [Math.round(factor * 100) + '%', num(factor * 10) + '%', num(factor) + '%'],
      explanation: dir === 'decreasing'
        ? `Keeping ${num(factor)} of x means removing ${num(1 - factor)} of it, i.e. a decrease of ${pct}%.`
        : `Multiplying by ${num(factor)} adds ${num(factor - 1)} of x, i.e. an increase of ${pct}%.` }));
  }
}

/* C — median of a data set (shown in the stem) */
function genC(n) {
  for (let i = 0; i < n; i++) {
    const len = pick([7, 8, 9]); const arr = Array.from({ length: len }, () => rnd(1, 20));
    const s = [...arr].sort((a, b) => a - b);
    let med; if (len % 2) med = s[(len - 1) / 2]; else med = (s[len / 2 - 1] + s[len / 2]) / 2;
    if (!Number.isInteger(med)) { i--; continue; } // keep clean integer medians
    const mean = Math.round(arr.reduce((p, v) => p + v, 0) / len);
    add(mc({ diff: 2,
      stem: `What is the median of the data set shown?  ${arr.join(', ')}`,
      correct: String(med),
      distractors: [String(mean), String(s[0]), String(s[len - 1]), String(med + 1), String(med - 1), String(s[1]), String(s[len - 2])],
      explanation: `Ordered: ${s.join(', ')}. ${len % 2 ? `The middle value is ${med}.` : `The two middle values are ${s[len / 2 - 1]} and ${s[len / 2]}; their average is ${med}.`}` }));
  }
}

/* D — two-way table probability (HTML table in figure) */
function tableHTML(title, rowHead, rLabels, cLabels, m) {
  const rt = m.map(r => r[0] + r[1]); const ct = [m[0][0] + m[1][0], m[0][1] + m[1][1]]; const g = rt[0] + rt[1];
  const th = 'style="border:1px solid #1a2744;padding:6px 12px;background:#f3eee2;font-weight:600;"';
  const td = 'style="border:1px solid #1a2744;padding:6px 12px;text-align:center;"';
  let h = `<div style="text-align:center;font-family:Inter,Arial,sans-serif;font-size:13px;">`;
  h += `<div style="font-weight:600;margin-bottom:6px;">${title}</div>`;
  h += `<table style="border-collapse:collapse;margin:0 auto;"><tr><th ${th}>${rowHead}</th><th ${th}>${cLabels[0]}</th><th ${th}>${cLabels[1]}</th><th ${th}>Total</th></tr>`;
  for (let i = 0; i < 2; i++) h += `<tr><th ${th}>${rLabels[i]}</th><td ${td}>${m[i][0]}</td><td ${td}>${m[i][1]}</td><td ${td}>${rt[i]}</td></tr>`;
  h += `<tr><th ${th}>Total</th><td ${td}>${ct[0]}</td><td ${td}>${ct[1]}</td><td ${td}>${g}</td></tr></table></div>`;
  return { html: h, rt, ct, g };
}
const D_CTX = [
  { title: 'Cars Listed for Sale', rowHead: 'Type', rL: ['Nonhybrid', 'Hybrid'], cL: ['$25,000 or less', 'More than $25,000'] },
  { title: 'Students Surveyed', rowHead: 'Grade', rL: ['Junior', 'Senior'], cL: ['Plays a sport', 'Does not'] },
  { title: 'Seedlings After 4 Weeks', rowHead: 'Group', rL: ['Treated', 'Untreated'], cL: ['Survived', 'Did not survive'] },
];
function genD(n) {
  for (let i = 0; i < n; i++) {
    const c = D_CTX[i % D_CTX.length];
    const m = [[rnd(2, 9), rnd(2, 9)], [rnd(2, 9), rnd(2, 9)]];
    const { html, rt, ct, g } = tableHTML(c.title, c.rowHead, c.rL, c.cL, m);
    const ri = rnd(0, 1), ci = rnd(0, 1); const cell = m[ri][ci];
    const variant = i % 2; // 0: joint prob, 1: conditional
    let stem, correct, distractors, exp;
    if (variant === 0) {
      stem = `${c.title}: if one is selected at random, what is the probability that it is ${c.rL[ri].toLowerCase()} and "${c.cL[ci]}"?`;
      correct = frac(cell, g);
      distractors = [frac(rt[ri], g), frac(ct[ci], g), frac(cell, rt[ri]), frac(cell, ct[ci]), frac(m[1 - ri][ci], g), frac(rt[1 - ri], g)];
      exp = `There are ${cell} that are ${c.rL[ri].toLowerCase()} and "${c.cL[ci]}", out of ${g} total: ${cell}/${g} = ${frac(cell, g)}.`;
    } else {
      stem = `${c.title}: given that a randomly selected one is ${c.rL[ri].toLowerCase()}, what is the probability that it is "${c.cL[ci]}"?`;
      correct = frac(cell, rt[ri]);
      distractors = [frac(cell, g), frac(rt[ri], g), frac(ct[ci], g), frac(cell, ct[ci]), frac(m[ri][1 - ci], rt[ri])];
      exp = `Restrict to the ${rt[ri]} ${c.rL[ri].toLowerCase()} items; ${cell} of them are "${c.cL[ci]}": ${cell}/${rt[ri]} = ${frac(cell, rt[ri])}.`;
    }
    add(mc({ diff: 2, figure: html, stem, correct, distractors, explanation: exp }));
  }
}

genA(10); genB(10); genC(12); genD(12);
const seen = new Set();
const uniq = Q.filter(q => { const key = q.stem + q.figure; if (seen.has(key)) return false; seen.add(key); return true; });
fs.writeFileSync('base44/questions_pack8_data.json', JSON.stringify(uniq, null, 2));
const tbl = uniq.filter(q => q.figure).length;
console.log('Generated', uniq.length, 'data questions (pack 8) —', tbl, 'with tables');
