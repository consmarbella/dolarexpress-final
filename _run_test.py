import os
os.environ['DEEPSEEK_API_KEY'] = 'sk-416550d0410a4fdd87e3aa1bf89c3a5a'

import sys
sys.path.insert(0, r'c:\Users\matte\OneDrive\Escritorio\scraper')

from graph import run_pseo_pipeline

try:
    state = run_pseo_pipeline('https://dolarexpress.cl', 'legalhelp.cl', 'deuda TAG prescripcion Chile')
    print('SUCCESS:', state.get('publish_success'))
    print('Pages:', state.get('pages_generated'))
    print('Errors:', state.get('errors'))
except Exception as e:
    print(f'CRITICAL ERROR: {e}')
    import traceback
    traceback.print_exc()
