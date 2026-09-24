# /archive — scripts y backups obsoletos (2026-09-24)

Contenido movido desde la raíz del repo durante la limpieza SEO. **Nada de esto participa en el build actual** (`npm run build` = `node generate-sitemap.js && node copy-html-files.js`).

- `fix-*`, `gen-*`, `generate-*` (salvo `generate-sitemap.js`), `add-*`, `check-*`, `*-sitemap*`, `run_seo_overhaul.py`, `audit_seo_completo.py`, `write-vercel.ps1`: parches de sesiones anteriores que editaban copias o archivos que nunca llegan a `dist/`. Reemplazados por edición directa + este changelog.
- `backup_20260504_*`: snapshots de mayo, sin referencia en el build.
- `sacar-*.html`, `ripley-plata-al-tiro.html`, `venta-usd.html`, `guard5.html`: HTML sueltos en raíz, fuera de `public/` → nunca se despliegan.
- `dolarexpress-seo-completo.zip`, `urls_generated.txt`, `seo_audit_*.csv`: artefactos de análisis.
- `_redirects`, `_config.yml`: configs de Netlify/Jekyll, ignorados por Vercel.

Conservados en raíz: `generate-sitemap.js`, `copy-html-files.js`, `vercel.json`, `package.json`, `public/`, `scripts/` (auditoría GSC en uso).
No tocar sin revisar `CHANGELOG_SEO.md`.
