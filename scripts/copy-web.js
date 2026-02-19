const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const www = path.join(root, 'www');

// Ensure www directory exists
if (!fs.existsSync(www)) {
  fs.mkdirSync(www, { recursive: true });
}

// Files to copy from project root to www/
const files = [
  'index.html',
  'manifest.json',
  'service-worker.js',
  'icon-192.png'
];

for (const file of files) {
  const src = path.join(root, file);
  const dest = path.join(www, file);
  if (fs.existsSync(src)) {
    fs.copyFileSync(src, dest);
    console.log(`Copied ${file} -> www/${file}`);
  } else {
    console.warn(`Skipped ${file} (not found)`);
  }
}

console.log('Web assets copied to www/');
