const fs = require('fs');
// Draw a coordinate-plane line graph as inline SVG. World range -9..9.
function lineGraph({ slope, intercept }) {
  const min = -9, max = 9, unit = 18, cx = 180, cy = 180, W = 360;
  const sx = x => cx + x * unit, sy = y => cy - y * unit;
  let s = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${W}" width="${W}" height="${W}" font-family="Inter,Arial,sans-serif" font-size="11">`;
  s += `<rect width="${W}" height="${W}" fill="#ffffff"/>`;
  // grid
  for (let i = min; i <= max; i++) {
    s += `<line x1="${sx(i)}" y1="${sy(min)}" x2="${sx(i)}" y2="${sy(max)}" stroke="#e3ddcd" stroke-width="1"/>`;
    s += `<line x1="${sx(min)}" y1="${sy(i)}" x2="${sx(max)}" y2="${sy(i)}" stroke="#e3ddcd" stroke-width="1"/>`;
  }
  // axes
  s += `<line x1="${sx(min)}" y1="${cy}" x2="${sx(max)}" y2="${cy}" stroke="#1a1a2e" stroke-width="2"/>`;
  s += `<line x1="${cx}" y1="${sy(min)}" x2="${cx}" y2="${sy(max)}" stroke="#1a1a2e" stroke-width="2"/>`;
  // arrowheads
  s += `<polygon points="${sx(max)},${cy} ${sx(max) - 7},${cy - 4} ${sx(max) - 7},${cy + 4}" fill="#1a1a2e"/>`;
  s += `<polygon points="${cx},${sy(max)} ${cx - 4},${sy(max) + 7} ${cx + 4},${sy(max) + 7}" fill="#1a1a2e"/>`;
  s += `<text x="${sx(max) - 2}" y="${cy + 16}" fill="#1a1a2e">x</text>`;
  s += `<text x="${cx + 7}" y="${sy(max) + 9}" fill="#1a1a2e">y</text>`;
  // tick labels every 3
  for (let i = min; i <= max; i += 3) {
    if (i === 0) continue;
    s += `<text x="${sx(i) - 4}" y="${cy + 14}" fill="#5a5a7a">${i}</text>`;
    s += `<text x="${cx + 5}" y="${sy(i) + 4}" fill="#5a5a7a">${i}</text>`;
  }
  // the line, clamped to view
  const y1 = slope * min + intercept, y2 = slope * max + intercept;
  s += `<line x1="${sx(min)}" y1="${sy(y1)}" x2="${sx(max)}" y2="${sy(y2)}" stroke="#1a2744" stroke-width="3"/>`;
  s += `</svg>`;
  return s;
}

const svg = lineGraph({ slope: 0.5, intercept: 2 });   // y = ½x + 2 → y-int (0,2), x-int (-4,0)
fs.writeFileSync('base44/sample_graph.svg', svg);

const q = {
  question_id: 'fig0001', section: 'math', section_name: 'Math',
  domain: 'Algebra', difficulty: 2, difficulty_label: 'Medium', type: 'mc',
  figure: svg,
  passage: '',
  stem: 'The graph of the linear function f is shown, where y = f(x). What is the y-intercept of the graph of f?',
  choices: ['(0, 2)', '(2, 0)', '(−4, 0)', '(0, −4)'],
  answer_index: 0, answer_text: '(0, 2)',
  explanation: 'The y-intercept is where the line crosses the y-axis. The line crosses at y = 2, so the y-intercept is (0, 2).',
  is_premium: false, active: true
};
fs.writeFileSync('base44/sample_graph_question.json', JSON.stringify([q], null, 2));
console.log('Wrote sample_graph.svg and sample_graph_question.json');
console.log('Question:', q.stem);
console.log('Choices:', q.choices.join('  '), '| Answer:', q.answer_text);
