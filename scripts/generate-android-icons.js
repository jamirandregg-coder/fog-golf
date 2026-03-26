/**
 * Generates Android launcher icons from the source icon.
 * Run: node scripts/generate-android-icons.js
 * Requires: sharp (already a devDependency)
 */
const sharp = require('sharp');
const path = require('path');
const fs = require('fs');

const SOURCE_ICON = path.resolve(__dirname, '..', 'icon-512.png');
const SOURCE_MASKABLE = path.resolve(__dirname, '..', 'icon-maskable-512.png');
const ANDROID_RES = path.resolve(__dirname, '..', 'android', 'app', 'src', 'main', 'res');

const DENSITIES = [
  { name: 'mipmap-mdpi',    size: 48 },
  { name: 'mipmap-hdpi',    size: 72 },
  { name: 'mipmap-xhdpi',   size: 96 },
  { name: 'mipmap-xxhdpi',  size: 144 },
  { name: 'mipmap-xxxhdpi', size: 192 },
];

async function generateIcons() {
  for (const { name, size } of DENSITIES) {
    const dir = path.join(ANDROID_RES, name);
    fs.mkdirSync(dir, { recursive: true });

    // Standard icon
    await sharp(SOURCE_ICON)
      .resize(size, size)
      .png()
      .toFile(path.join(dir, 'ic_launcher.png'));

    // Round icon (same as standard for TWA)
    await sharp(SOURCE_ICON)
      .resize(size, size)
      .png()
      .toFile(path.join(dir, 'ic_launcher_round.png'));

    console.log(`  ${name}: ${size}x${size}px`);
  }

  console.log('Android icons generated successfully!');
}

generateIcons().catch(err => {
  console.error('Error generating icons:', err);
  process.exit(1);
});
