/**
 * Generate PNG icon files from SVG for the FOG Golf app.
 * Uses a simple approach: writes SVG files and an HTML generator page.
 * For actual PNG generation, we'll use the canvas approach at runtime,
 * but for the icon files we need static PNGs.
 *
 * This script creates SVG icon files that can be used directly,
 * and also creates a simple HTML page to generate PNGs from canvas.
 */
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');

// The SVG icon design (matches manifest.json)
const svgIcon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect width="512" height="512" rx="96" fill="#0f0a10"/>
  <text x="256" y="280" font-family="Arial Black,sans-serif" font-weight="900" font-size="180" fill="#ff3da7" text-anchor="middle">FOG</text>
  <text x="256" y="380" font-family="Arial,sans-serif" font-weight="700" font-size="72" fill="#ff77c4" text-anchor="middle">GOLF</text>
</svg>`;

// Save as SVG files for reference
fs.writeFileSync(path.join(root, 'resources', 'icon.svg'), svgIcon);
console.log('Created resources/icon.svg');

// Create a 1024x1024 version for App Store
const svg1024 = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024">
  <rect width="1024" height="1024" rx="192" fill="#0f0a10"/>
  <text x="512" y="560" font-family="Arial Black,sans-serif" font-weight="900" font-size="360" fill="#ff3da7" text-anchor="middle">FOG</text>
  <text x="512" y="760" font-family="Arial,sans-serif" font-weight="700" font-size="144" fill="#ff77c4" text-anchor="middle">GOLF</text>
</svg>`;

fs.writeFileSync(path.join(root, 'resources', 'icon-1024.svg'), svg1024);
console.log('Created resources/icon-1024.svg');

// Create the HTML-based PNG generator tool
const generatorHtml = `<!DOCTYPE html>
<html>
<head><title>FOG Icon Generator</title></head>
<body style="background:#333;color:#fff;font-family:sans-serif;padding:20px">
<h1>FOG Golf Icon Generator</h1>
<p>Click each button to generate and download the PNG icon at that size.</p>
<div id="buttons"></div>
<canvas id="canvas" style="border:1px solid #555;margin:20px 0"></canvas>
<script>
const sizes = [1024, 512, 192, 180, 167, 152, 120];
const container = document.getElementById('buttons');
sizes.forEach(size => {
  const btn = document.createElement('button');
  btn.textContent = 'Generate ' + size + 'x' + size;
  btn.style.cssText = 'margin:5px;padding:10px 20px;font-size:16px;cursor:pointer';
  btn.onclick = () => generateIcon(size);
  container.appendChild(btn);
});

function generateIcon(size) {
  const canvas = document.getElementById('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');

  // Background
  ctx.fillStyle = '#0f0a10';
  ctx.beginPath();
  const r = size * 0.1875; // rounded corners
  ctx.roundRect(0, 0, size, size, r);
  ctx.fill();

  // FOG text
  ctx.fillStyle = '#ff3da7';
  ctx.font = 'bold ' + (size * 0.35) + 'px "Arial Black", sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('FOG', size/2, size * 0.48);

  // GOLF text
  ctx.fillStyle = '#ff77c4';
  ctx.font = 'bold ' + (size * 0.14) + 'px Arial, sans-serif';
  ctx.fillText('GOLF', size/2, size * 0.72);

  // Download
  const link = document.createElement('a');
  link.download = 'icon-' + size + '.png';
  link.href = canvas.toDataURL('image/png');
  link.click();
}
</script>
</body>
</html>`;

fs.writeFileSync(path.join(root, 'scripts', 'icon-generator.html'), generatorHtml);
console.log('Created scripts/icon-generator.html');
console.log('');
console.log('Next steps:');
console.log('1. Open scripts/icon-generator.html in a browser');
console.log('2. Click "Generate 1024x1024" and save to resources/icon.png');
console.log('3. Click "Generate 192x192" and save as icon-192.png in the project root');
console.log('4. The 1024x1024 icon is needed for the App Store');
console.log('');
console.log('Alternatively, use any design tool to create a 1024x1024 PNG with:');
console.log('  - Dark background (#0f0a10)');
console.log('  - "FOG" in pink (#ff3da7)');
console.log('  - "GOLF" in light pink (#ff77c4)');
