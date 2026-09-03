from instagrapi import Client
import os, sys

cl = Client()
session_path = r'C:\Users\matte\OneDrive\Escritorio\opencode\session_cupo_dolarcl.json'

if os.path.exists(session_path):
    try:
        cl.load_settings(session_path)
        cl.login('cupo_dolarcl', 'Ale2401-')
        print('Session OK, user:', cl.user_id)
        
        # Post referral image
        caption = (
            "GAN\u00c1 PLATA EXTRA \ud83d\udcb0\n\n"
            "\u00bfTienes amigos con tarjeta de cr\u00e9dito?\n"
            "Refi\u00e9relos y gana el 2% de cada venta.\n\n"
            "\ud83d\udcb5 US$1.000 vendidos = $17.880 para ti\n"
            "\ud83d\udcb5 US$3.000 vendidos = $53.640 para ti\n"
            "\ud83d\udcb5 10 amigos = hasta $178.800\n\n"
            "Sin l\u00edmite \u00b7 Sin invertir \u00b7 Pago inmediato\n\n"
            "wa.me/56967658939\n\n"
            "#cupodolar #dolar #referidos #ganadinero #chile #cupo #efectivo"
        )
        
        media = cl.photo_upload(
            r'C:\Users\matte\dolarexpress-final\instagram_posts\post3_razones.png',
            caption
        )
        print(f'Post subido: https://instagram.com/p/{media.code}/')
        
        # Save session
        cl.dump_settings(session_path)
        print('Session saved')
        
    except Exception as e:
        print(f'Error: {e}')
        # Try to delete stale session
        try:
            os.remove(session_path)
            print('Session deleted - user needs to login from their PC')
        except:
            pass
else:
    print('No session file found at', session_path)
