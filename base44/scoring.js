/* ============================================================================
   SAT COMMAND CENTER — core logic for the Base44 build
   ----------------------------------------------------------------------------
   These are plain, framework-free functions. In Base44 you can paste them into
   a shared utilities file (or inline in a component / backend function) and call
   them from your React screens. They contain NO Base44-specific code, so they're
   easy to drop in and unit-test.
   ============================================================================ */

/* ---------- Constants ---------- */
export const FREE_DAILY_QUOTA = 10;      // free-plan questions per day
export const SIM_MODULE_SIZE   = 6;       // questions per simulator module (raise as your bank grows)
export const ADAPT_ROUTE_THRESHOLD = 0.6; // Module-1 accuracy needed to route to the HARDER Module 2

export const DOMAINS = {
  math: ['Algebra', 'Advanced Math', 'Problem-Solving & Data', 'Geometry & Trig'],
  rw:   ['Information & Ideas', 'Craft & Structure', 'Expression of Ideas', 'English Conventions'],
};

/* ---------- Small helpers ---------- */
export function shuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// Grid-in answers: accept numeric equivalents (e.g. "0.5" == ".5" == "1/2" if you choose to parse fractions)
export function gridMatch(given, answerText) {
  if (given == null) return false;
  const g = String(given).trim();
  const a = parseFloat(g), b = parseFloat(answerText);
  if (!isNaN(a) && !isNaN(b)) return Math.abs(a - b) < 1e-6;
  return g.replace(/\s/g, '').toLowerCase() === String(answerText).replace(/\s/g, '').toLowerCase();
}

export function isCorrect(question, response) {
  // response = { selectedIndex } for mc, or { text } for grid
  if (question.type === 'grid') return gridMatch(response.text, question.answer_text);
  return Number(response.selectedIndex) === Number(question.answer_index);
}

/* ============================================================================
   1) PRACTICE — build a question set
   questions: array of Question records (from the Question entity)
   opts: { section: 'math'|'rw'|'mix', domain: 'all'|<name>, difficulty: 'adaptive'|1|2|3, length, premium }
   ============================================================================ */
export function buildPracticeSet(questions, opts) {
  let pool = questions.filter(q => q.active !== false);
  if (opts.section !== 'mix') pool = pool.filter(q => q.section === opts.section);
  if (opts.domain && opts.domain !== 'all') pool = pool.filter(q => q.domain === opts.domain);
  if (opts.difficulty !== 'adaptive') pool = pool.filter(q => q.difficulty === Number(opts.difficulty));
  if (!opts.premium) pool = pool.filter(q => !q.is_premium);

  pool = shuffle(pool);
  if (opts.difficulty === 'adaptive') {
    // gentle easy→hard ramp with a little randomness
    pool.sort((x, y) => (x.difficulty - y.difficulty) + (Math.random() - 0.5));
  }
  let n = opts.length;
  if (!opts.premium) n = Math.min(n, Math.max(0, opts.quotaLeft ?? n));
  return pool.slice(0, n);
}

/* ============================================================================
   2) PRACTICE — running, per-question adaptive nudge (optional)
   Use when difficulty === 'adaptive' and you serve questions one at a time:
   bumps target difficulty up after 2 correct in a row, down after 2 wrong.
   ============================================================================ */
export function nextAdaptiveDifficulty(currentDiff, recentResults /* array of bools, newest last */) {
  const last2 = recentResults.slice(-2);
  if (last2.length === 2 && last2.every(r => r === true))  return Math.min(3, currentDiff + 1);
  if (last2.length === 2 && last2.every(r => r === false)) return Math.max(1, currentDiff - 1);
  return currentDiff;
}

/* ============================================================================
   3) FULL-TEST SIMULATOR — module routing + scoring
   The Digital SAT is "module-adaptive": Module 1 is mixed; if you do well,
   Module 2 is harder and your score ceiling rises.
   ============================================================================ */

// Build a module's pool. hard=false → easy/medium items; hard=true → medium/hard items.
export function buildModule(questions, section, hard) {
  let pool = questions.filter(q => q.section === section && q.active !== false);
  pool = pool.filter(q => hard ? q.difficulty >= 2 : q.difficulty <= 2);
  return shuffle(pool).slice(0, SIM_MODULE_SIZE);
}

// After Module 1, decide whether Module 2 is the harder route.
export function routeToHard(module1Correct, module1Total) {
  const acc = module1Total ? module1Correct / module1Total : 0;
  return acc >= ADAPT_ROUTE_THRESHOLD;
}

// Section scaled score (200–800). Routing to the harder module raises the ceiling.
export function sectionScore(correct, total, routedHard) {
  const acc = total ? correct / total : 0;
  const ceil = routedHard ? 800 : 650;
  const floor = 200;
  return Math.round((floor + acc * (ceil - floor)) / 10) * 10;
}

// Combine both sections into the 400–1600 report.
export function buildScoreReport(rw, math) {
  // rw / math = { correct, total, hard }
  const rwScore = sectionScore(rw.correct, rw.total, rw.hard);
  const mathScore = sectionScore(math.correct, math.total, math.hard);
  return {
    rw_score: rwScore,
    math_score: mathScore,
    total_score: rwScore + mathScore,
    rw_hard: rw.hard,
    math_hard: math.hard,
  };
}

/* Simulator state machine (4 stages). Drive it from your Simulator screen:
   stage 0: R&W Module 1   (mixed)            -> routeToHard -> stage 1
   stage 1: R&W Module 2   (standard|higher)  -> stage 2
   stage 2: Math Module 1  (mixed)            -> routeToHard -> stage 3
   stage 3: Math Module 2  (standard|higher)  -> finish -> buildScoreReport
   Suggested timers (condensed): R&W modules 10 min, Math modules ~11–12 min.
*/

/* ============================================================================
   4) STATS / DASHBOARD — derive from Attempt records
   ============================================================================ */
export function overallStats(attempts) {
  const answered = attempts.length;
  const correct = attempts.filter(a => a.is_correct).length;
  return { answered, correct, accuracy: answered ? correct / answered : 0 };
}

export function masteryByDomain(attempts) {
  const map = {};
  for (const a of attempts) {
    const d = (map[a.domain] = map[a.domain] || { total: 0, correct: 0 });
    d.total++; if (a.is_correct) d.correct++;
  }
  for (const k in map) map[k].pct = map[k].total ? Math.round(100 * map[k].correct / map[k].total) : 0;
  return map; // { 'Algebra': {total, correct, pct}, ... }
}

// Rough 400–1600 estimate from cumulative practice accuracy (needs >= 4 attempts).
export function estimatedScore(attempts) {
  if (attempts.length < 4) return null;
  const { accuracy } = overallStats(attempts);
  return Math.round((400 + accuracy * 1200) / 10) * 10;
}

/* ---------- Streak (call once per day when the user answers something) ---------- */
export function updateStreak(user /* {streak_days, last_active_date} */, todayISO) {
  if (user.last_active_date === todayISO) return user.streak_days;
  const yest = new Date(Date.parse(todayISO) - 86400000).toISOString().slice(0, 10);
  return (user.last_active_date === yest) ? (user.streak_days + 1) : 1;
}

/* ============================================================================
   5) FREE-PLAN QUOTA
   ============================================================================ */
export function quotaLeft(user, todayISO) {
  if (user.plan === 'premium') return Infinity;
  const used = (user.daily_quota_date === todayISO) ? (user.daily_quota_used || 0) : 0;
  return Math.max(0, FREE_DAILY_QUOTA - used);
}
