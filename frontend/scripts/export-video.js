// Aggregates the latest Playwright video into a single downloadable file
// Usage: npm run test:ui && npm run video:export

const fs = require('fs');
const path = require('path');

function findLatestVideoDir(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => ({ name: d.name, time: fs.statSync(path.join(dir, d.name)).mtime.getTime() }))
    .sort((a, b) => b.time - a.time);
  return entries[0]?.name ? path.join(dir, entries[0].name) : null;
}

function main() {
  const base = path.join(process.cwd(), 'test-results');
  if (!fs.existsSync(base)) {
    console.error('No test-results directory found. Run: npm run test:ui');
    process.exit(1);
  }

  const latest = findLatestVideoDir(base);
  if (!latest) {
    console.error('No Playwright result directory found.');
    process.exit(1);
  }

  // Recursively find .webm/.mp4 videos
  let videos = [];
  (function walk(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) walk(full);
      else if (/\.(webm|mp4)$/i.test(entry.name)) videos.push(full);
    }
  })(latest);

  if (videos.length === 0) {
    console.error('No videos found under:', latest);
    process.exit(1);
  }

  const outDir = path.join(process.cwd(), 'artifacts');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir);

  // Copy the largest (most complete) video as the demo
  videos.sort((a, b) => fs.statSync(b).size - fs.statSync(a).size);
  const source = videos[0];
  const target = path.join(outDir, 'AIDA-UI-Demo.webm');
  fs.copyFileSync(source, target);
  console.log('Saved:', target);
}

main();


