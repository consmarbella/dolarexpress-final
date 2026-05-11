import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const publicDir = path.join(__dirname, 'public');
const distDir = path.join(__dirname, 'dist');

if (!fs.existsSync(distDir)) {
  fs.mkdirSync(distDir, { recursive: true });
}

function copyFilesRecursive(src, dest) {
  let copied = 0;

  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }

  const entries = fs.readdirSync(src, { withFileTypes: true });

  entries.forEach(entry => {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copied += copyFilesRecursive(srcPath, destPath);
    } else if (entry.name.endsWith('.html')) {
      const baseName = entry.name.replace('.html', '');
      const folderPath = path.join(dest, baseName);
      if (!fs.existsSync(folderPath)) {
        fs.mkdirSync(folderPath, { recursive: true });
      }
      fs.copyFileSync(srcPath, path.join(folderPath, 'index.html'));
      copied++;
    } else if (entry.name.endsWith('.xml')) {
      fs.copyFileSync(srcPath, destPath);
      copied++;
    } else if (entry.name === 'sitemap.xml') {
      fs.copyFileSync(srcPath, destPath);
      copied++;
    }
  });

  return copied;
}

const copied = copyFilesRecursive(publicDir, distDir);
console.log(`✅ Copied ${copied} HTML files to dist/`);

console.log(`✅ Build complete - HTML pages will be served as static files, bypassing SPA`);
