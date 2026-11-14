// Run from any directory: node scripts/check_visual_contrast.cjs
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const css = fs.readFileSync(path.join(root, 'frontend/src/design-system/tokens.css'), 'utf8');
const colors = Object.fromEntries([...css.matchAll(/--([\w-]+):\s*(#[\da-f]{6});/gi)].map(m => [m[1], m[2]]));
function luminance(hex) {
  const c = hex.slice(1).match(/../g).map(x => parseInt(x, 16) / 255)
    .map(x => x <= .04045 ? x / 12.92 : ((x + .055) / 1.055) ** 2.4);
  return c[0] * .2126 + c[1] * .7152 + c[2] * .0722;
}
const checks = [];
for (const bg of ['bg', 'surface', 'surface-raised']) {
  for (const fg of ['text', 'muted', 'accent', 'accent-blue', 'accent-lunar', 'accent-mint', 'warning', 'error']) {
    checks.push({foreground: fg, background: bg, minimum: 4.5});
  }
  for (const fg of ['focus', 'border-control']) checks.push({foreground: fg, background: bg, minimum: 3});
}
checks.push({foreground: 'on-accent', background: 'accent', minimum: 4.5});
for (const c of checks) {
  const a = luminance(colors[c.foreground]), b = luminance(colors[c.background]);
  const ratio = (Math.max(a, b) + .05) / (Math.min(a, b) + .05);
  c.ratio = Number(ratio.toFixed(2));
  c.pass = ratio >= c.minimum;
}
fs.writeFileSync(path.join(root, 'docs/visual/contrastes.json'), JSON.stringify({method: 'WCAG relative luminance; opaque sRGB colors only', checks}, null, 2) + '\n');
console.log(`${checks.filter(c => c.pass).length}/${checks.length} color pairs pass`);
if (checks.some(c => !c.pass)) { console.log(checks.filter(c => !c.pass)); process.exitCode = 1; }
