import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const publicDir = path.join(__dirname, 'public');
const distDir = path.join(__dirname, 'dist');

// Ensure dist exists
if (!fs.existsSync(distDir)) {
  fs.mkdirSync(distDir, { recursive: true });
}

// Copy all HTML files from public to dist
const files = fs.readdirSync(publicDir);
let copied = 0;

files.forEach(file => {
  if (file.endsWith('.html') || file.endsWith('.xml')) {
    const src = path.join(publicDir, file);
    const dest = path.join(distDir, file);
    fs.copyFileSync(src, dest);
    copied++;
  }
});

console.log(`✅ Copied ${copied} static files to dist/`);
