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
  let folders = 0;

  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }

  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      const result = copyFilesRecursive(srcPath, destPath);
      copied += result.files;
      folders += result.folders;
    } else if (entry.name === 'index.html' && src === publicDir) {
      // Never overwrite root index.html — that's the React app entry point built by Vite
      continue;
    } else if (entry.name.endsWith('.html')) {
      // 1. Copiar como carpeta/index.html (para rutas sin extensión)
      const baseName = entry.name.replace('.html', '');
      const folderPath = path.join(dest, baseName);
      if (!fs.existsSync(folderPath)) {
        fs.mkdirSync(folderPath, { recursive: true });
      }
      fs.copyFileSync(srcPath, path.join(folderPath, 'index.html'));
      folders++;

      // 2. Copiar también como archivo.html (para rutas con .html)
      fs.copyFileSync(srcPath, destPath);
      copied++;
    } else if (entry.name.endsWith('.xml')) {
      // Sitemap
      fs.copyFileSync(srcPath, destPath);
      copied++;
    } else if (entry.name === 'robots.txt') {
      fs.copyFileSync(srcPath, destPath);
      copied++;
    }
  }

  return { files: copied, folders };
}

console.log('Copiando archivos de public a dist...');
const result = copyFilesRecursive(publicDir, distDir);
console.log(`✅ Copiados ${result.files} archivos y ${result.folders} carpetas`);
console.log('✅ Las paginas HTML se serviran directamente (SPA ignorada para esas rutas)');