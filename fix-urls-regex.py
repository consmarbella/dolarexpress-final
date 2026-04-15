#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO URL Fixer - Corrección de Canonicals, OG:URLs y enlaces internos
Compatible con Python 3.6+
Usa SOLO expresiones regulares puras - sin BeautifulSoup ni parsers HTML
"""

import os
import re
from pathlib import Path
from collections import defaultdict


class URLFixer:
    """Fixer para URLs de SEO usando solo expresiones regulares puras"""
    
    def __init__(self, public_dir="public"):
        self.public_dir = Path(public_dir)
        self.stats = defaultdict(int)
        self.changes = defaultdict(list)
    
    def fix_canonical(self, content):
        """Corrige canonical URLs sin .html
        Regex: (<link\s+rel="canonical"\s+href=")([^\"]+?)("")
        """
        pattern = r'(<link\s+rel="canonical\s+href=")([^\"]+?)("")'
        
        def replacer(match):
            prefix = match.group(1)
            url = match.group(2)
            suffix = match.group(3)
            
            # Si no termina en .html y no es raíz, agregar
            if not url.endswith('.html') and not url.endswith('/'):  
                new_url = url + '.html'
                self.stats['canonical_fixed'] += 1
                self.changes['canonical'].append((url, new_url))
                return f'{prefix}{new_url}{suffix}'
            
            return match.group(0)
        
        return re.sub(pattern, replacer, content)
    
    def fix_og_url(self, content):
        """Corrige og:url metadata sin .html
        Regex: (<meta\s+property="og:url"\s+content=")([^\"]+?)("")
        """
        pattern = r'(<meta\s+property="og:url"\s+content=")([^\"]+?)("")'
        
        def replacer(match):
            prefix = match.group(1)
            url = match.group(2)
            suffix = match.group(3)
            
            # Si no termina en .html y no es raíz, agregar
            if not url.endswith('.html') and not url.endswith('/'):  
                new_url = url + '.html'
                self.stats['og_url_fixed'] += 1
                self.changes['og_url'].append((url, new_url))
                return f'{prefix}{new_url}{suffix}'
            
            return match.group(0)
        
        return re.sub(pattern, replacer, content)
    
    def fix_related_links(self, content):
        """Corrige links dentro de div.related-links
        Regex: <div\s+class="related-links">(.*?)</div>
        """
        pattern = r'<div\s+class="related-links">(.*?)</div>'
        
        def fix_links_in_div(match):
            div_content = match.group(1)
            
            # Patrón para encontrar href dentro del div
            href_pattern = r'<a\s+href="([^"]+?)"'
            
            def link_replacer(link_match):
                href = link_match.group(1)
                
                # Si no termina en .html, no es raíz, y no es URL externa, agregar
                if not href.endswith('.html') and not href.endswith('/') and not href.startswith('http'):
                    new_href = href + '.html'
                    self.stats['related_links_fixed'] += 1
                    self.changes['related_links'].append((href, new_href))
                    return f'<a href="{new_href}"'
                
                return link_match.group(0)
            
            fixed_div = re.sub(href_pattern, link_replacer, div_content)
            return f'<div class="related-links">{fixed_div}</div>'
        
        return re.sub(pattern, fix_links_in_div, content, flags=re.DOTALL)
    
    def fix_footer_links(self, content):
        """Corrige links en el footer (privacidad, terminos, contacto)
        Regex: (<a\s+href=")(/privacidad|terminos|contacto)("")
        """
        patterns = [
            (r'(<a\s+href=")(/privacidad)("")', r'\1\2.html\3'),
            (r'(<a\s+href=")(/terminos)("")', r'\1\2.html\3'),
            (r'(<a\s+href=")(/contacto)("")', r'\1\2.html\3'),
        ]
        
        for pattern, replacement in patterns:
            matches = list(re.finditer(pattern, content))
            for match in matches:
                old_url = match.group(2)
                new_url = old_url + '.html'
                self.stats['footer_links_fixed'] += 1
                self.changes['footer_links'].append((old_url, new_url))
            
            content = re.sub(pattern, replacement, content)
        
        return content
    
    def process_file(self, filepath):
        """Procesa un archivo HTML individual"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            content = original_content
            
            # Aplicar todas las correcciones en orden (IMPORTANTE: el orden es determinista)
            content = self.fix_canonical(content)
            content = self.fix_og_url(content)
            content = self.fix_related_links(content)
            content = self.fix_footer_links(content)
            
            # Escribir archivo si hay cambios
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.stats['files_modified'] += 1
                return True
            
            return False
        
        except Exception as e:
            print(f"❌ Error procesando {filepath}: {e}")
            self.stats['errors'] += 1
            return False
    
    def process_directory(self):
        """Procesa todos los archivos .html en el directorio public"""
        if not self.public_dir.exists():
            print(f"❌ Directorio no encontrado: {self.public_dir}")
            return
        
        html_files = sorted(self.public_dir.glob('*.html'))
        
        if not html_files:
            print(f"⚠️  No se encontraron archivos .html en {self.public_dir}")
            return
        
        print(f"📁 Procesando {len(html_files)} archivos HTML...\n")
        
        for i, filepath in enumerate(html_files, 1):
            if self.process_file(filepath):
                print(f"✅ [{i:3d}/{len(html_files)}] {filepath.name}")
            else:
                print(f"⏭️  [{i:3d}/{len(html_files)}] {filepath.name} (sin cambios)")
        
        self.print_report()
    
    def print_report(self):
        """Imprime un reporte detallado de los cambios"""
        print("\n" + "="*80)
        print("📊 REPORTE DE CORRECCIONES SEO - REGEX PURAS")
        print("="*80)
        
        total_changes = (
            self.stats['canonical_fixed'] +
            self.stats['og_url_fixed'] +
            self.stats['related_links_fixed'] +
            self.stats['footer_links_fixed']
        )
        
        print(f"\n📈 ESTADÍSTICAS:")
        print(f"   ✨ Archivos modificados: {self.stats['files_modified']}")
        print(f"   🔗 Canonicals corregidos: {self.stats['canonical_fixed']}")
        print(f"   📱 OG:URLs corregidas: {self.stats['og_url_fixed']}")
        print(f"   📄 Related links corregidos: {self.stats['related_links_fixed']}")
        print(f"   🦶 Footer links corregidos: {self.stats['footer_links_fixed']}")
        print(f"   ═══════════════════════════════════")
        print(f"   📊 TOTAL de URLs corregidas: {total_changes}")
        
        if self.stats['errors'] > 0:
            print(f"\n   ❌ Errores encontrados: {self.stats['errors']}")
        
        # Mostrar ejemplos de cambios
        if self.changes and any(self.changes.values()):
            print(f"\n📝 EJEMPLOS DE CAMBIOS REALIZADOS:\n")
            
            for category, items in self.changes.items():
                if items:
                    category_name = category.upper().replace('_', ' ')
                    print(f"   {category_name}:")
                    for old, new in items[:5]:
                        print(f"      ❌ {old}")
                        print(f"      ✅ {new}")
                    
                    if len(items) > 5:
                        print(f"      ... y {len(items) - 5} más")
                    print() 
        
        print("="*80)
        print("✨ ¡Corrección completada exitosamente!")
        print("="*80 + "\n")


def main():
    """Función principal"""
    import sys
    
    # Usar directorio especificado o 'public' por defecto
    public_dir = sys.argv[1] if len(sys.argv) > 1 else "public"
    
    fixer = URLFixer(public_dir)
    fixer.process_directory()


if __name__ == "__main__":
    main()