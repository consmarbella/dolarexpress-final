from instagrapi import Client

cl = Client()
print("Iniciando sesion en Instagram...")
print("Si pide codigo, revisa GMAIL (xaos27@gmail.com)")
print()

try:
    cl.login("cupo_dolarcl", "Ale2401-")
    print("✅ Login exitoso!")
    
    caption = "GAN\u00c1 PLATA EXTRA \ud83d\udcb0\n\nRefer\u00ed amigos y gan\u00e1 el 2% de cada venta.\n\nUS$1.000 vendidos = $17.880 para ti\nUS$3.000 vendidos = $53.640 para ti\n10 amigos = hasta $178.800\n\nSin l\u00edmite \u00b7 Sin invertir \u00b7 Pago inmediato\n\nwa.me/56967658939\n\n#cupodolar #referidos #ganadinero #chile"
    
    media = cl.photo_upload(
        r"C:\Users\matte\dolarexpress-final\instagram_posts\post4_calculo.png",
        caption
    )
    print(f"✅ Post subido: https://instagram.com/p/{media.code}/")
    
    cl.photo_upload_to_story(r"C:\Users\matte\dolarexpress-final\instagram_posts\story_urgente.png")
    print("✅ Historia subida!")
    
    cl.dump_settings(r"C:\Users\matte\OneDrive\Escritorio\opencode\session_cupo_dolarcl.json")
    print("✅ Sesion guardada")
    
except Exception as e:
    error_msg = str(e)
    if "challenge" in error_msg.lower() or "login_required" in error_msg.lower():
        print("\n❌ Instagram pide verificacion")
        print("Revisa GMAIL (xaos27@gmail.com) o el telefono")
        print("y corre este script de nuevo con el codigo listo")
    else:
        print(f"\n❌ Error: {error_msg}")
