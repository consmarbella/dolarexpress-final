#!/usr/bin/env python3
import os
import re
from pathlib import Path

def remove_transbank_references(file_path):
    """Remove all Transbank references from an HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Remove Transbank mentions from meta descriptions and og:description
        content = re.sub(
            r',?\s*mecanismo\s+vía\s+Transbank\s+y\s+riesgos\.',
            '',
            content,
            flags=re.IGNORECASE
        )
        content = re.sub(
            r',?\s*vía\s+Transbank\s+y\s+riesgos\.',
            '',
            content,
            flags=re.IGNORECASE
        )

        # Remove "operamos como comercio afiliado a Transbank" and similar phrases
        content = re.sub(
            r'\s*Somos un comercio afiliado a Transbank que ofrece un servicio de conversión de cupo a efectivo\.',
            ' Ofrecemos un servicio seguro de conversión de cupo de tarjetas a efectivo.',
            content,
            flags=re.IGNORECASE
        )

        content = re.sub(
            r'terminal POS certificado por Transbank',
            'plataforma de pagos certificada',
            content,
            flags=re.IGNORECASE
        )

        content = re.sub(
            r'voucher de Transbank',
            'comprobante de transacción',
            content,
            flags=re.IGNORECASE
        )

        content = re.sub(
            r'Transbank\s+y\s+genera\s+un\s+voucher\s+verificable',
            'y genera un comprobante verificable',
            content,
            flags=re.IGNORECASE
        )

        content = re.sub(
            r'transacción queda registrada en Transbank',
            'transacción queda registrada y verificable',
            content,
            flags=re.IGNORECASE
        )

        content = re.sub(
            r'comisión de Transbank',
            'comisiones de procesamiento',
            content,
            flags=re.IGNORECASE
        )

        content = re.sub(
            r'DolarExpress opera como comercio afiliado a Transbank para convertir',
            'DolarExpress te permite convertir',
            content,
            flags=re.IGNORECASE
        )

        content = re.sub(
            r'terminal POS habilitado para recibir pagos',
            'sistema seguro de procesamiento de pagos',
            content,
            flags=re.IGNORECASE
        )

        content = re.sub(
            r'Servicio de conversión de cupo de tarjetas de tienda a efectivo vía Transbank\.',
            'Servicio seguro de conversión de cupo de tarjetas a efectivo.',
            content,
            flags=re.IGNORECASE
        )

        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    public_folder = Path('/home/user/dolarexpress-final/public')
    html_files = list(public_folder.glob('*.html'))

    modified_count = 0
    total_count = len(html_files)

    print(f"Processing {total_count} HTML files...")

    for i, html_file in enumerate(html_files, 1):
        if remove_transbank_references(html_file):
            modified_count += 1
            if i % 100 == 0:
                print(f"  {i}/{total_count} processed ({modified_count} modified)")

    print(f"\n✅ Complete: {modified_count}/{total_count} files modified")

if __name__ == '__main__':
    main()
