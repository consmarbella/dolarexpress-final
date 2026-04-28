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

// Recursively copy all HTML and XML files from public to dist
function copyFilesRecursive(src, dest) {
  let copied = 0;

  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }

  const files = fs.readdirSync(src);

  files.forEach(file => {
    const srcPath = path.join(src, file);
    const destPath = path.join(dest, file);
    const stat = fs.statSync(srcPath);

    if (stat.isDirectory()) {
      copied += copyFilesRecursive(srcPath, destPath);
    } else if (file.endsWith('.html') || file.endsWith('.xml')) {
      fs.copyFileSync(srcPath, destPath);
      copied++;
    }
  });

  return copied;
}

const copied = copyFilesRecursive(publicDir, distDir);
console.log(`✅ Copied ${copied} static files to dist/`);
