@echo off
echo.
echo === DolarExpress - Postear en Instagram ===
echo.

cd /d "C:\Users\matte\dolarexpress-final"

echo 1) Iniciando sesion en Instagram...
python -c "
from instagrapi import Client
cl = Client()
try:
    cl.login('cupo_dolarcl', 'Ale2401-')
    cl.dump_settings(r'C:\Users\matte\OneDrive\Escritorio\opencode\session_cupo_dolarcl.json')
    print('Sesion OK')
    
    caption = (
        'GANA PLATA EXTRA\n\n'
        'Referi amigos y gana el 2%% de cada venta.\n\n'
        'US$1.000 vendidos = $17.880 para ti\n'
        'US$3.000 vendidos = $53.640 para ti\n'
        '10 amigos vendiendo = hasta $178.800\n\n'
        'Sin limite - Sin invertir - Pago inmediato\n\n'
        'wa.me/56967658939\n\n'
        '#cupodolar #referidos #ganadinero #chile #cupo #efectivo'
    )
    
    media = cl.photo_upload(
        r'C:\Users\matte\dolarexpress-final\instagram_posts\post4_calculo.png',
        caption
    )
    print(f'Post subido: https://instagram.com/p/{media.code}/')
    
except Exception as e:
    print(f'Error: {e}')
    print('Si pide codigo, revisa tu celular y corre de nuevo')
"

echo.
echo 2) Subiendo historia...
python -c "
from instagrapi import Client
cl = Client()
cl.load_settings(r'C:\Users\matte\OneDrive\Escritorio\opencode\session_cupo_dolarcl.json')
try:
    cl.photo_upload_to_story(r'C:\Users\matte\dolarexpress-final\instagram_posts\story_urgente.png')
    print('Historia subida')
except:
    print('Error en historia - probablemente sesion expirada')
"

echo.
echo Listo!
pause
