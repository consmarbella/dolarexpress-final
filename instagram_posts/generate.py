from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, json, textwrap, io

# ─── CONFIG ───
OUT = r"C:\Users\matte\dolarexpress-final\instagram_posts"
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1080
BG = (26, 26, 26)
GOLD = (200, 160, 69)
WHITE = (245, 245, 245)
GRAY = (120, 120, 120)

def make_post(elements, filename):
    """elements: list of (type, kwargs)"""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    
    # Try to load fonts, fall back to default
    try:
        font_big = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 80)
        font_title = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 55)
        font_body = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 38)
        font_small = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 30)
    except:
        font_big = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    for el in elements:
        t = el["type"]
        if t == "rect":
            draw.rectangle(el["xy"], fill=el.get("fill", GOLD), width=0)
        elif t == "text":
            draw.text(el["pos"], el["text"], fill=el.get("color", WHITE), font=el.get("font", font_body), anchor=el.get("anchor", "lt"))
        elif t == "line":
            draw.line(el["xy"], fill=GOLD, width=el.get("width", 3))
        elif t == "circle":
            draw.ellipse(el["xy"], fill=el.get("fill", GOLD))
        elif t == "rounded_rect":
            draw.rounded_rectangle(el["xy"], radius=el.get("radius", 20), fill=el.get("fill", GOLD))
    
    path = os.path.join(OUT, filename)
    img.save(path, "PNG", optimize=True)
    return path

def wrap(text, max_chars=25):
    """Simple word wrap"""
    lines = []
    for word in text.split():
        if not lines or len(lines[-1]) + len(word) + 1 > max_chars:
            lines.append(word)
        else:
            lines[-1] += " " + word
    return "\n".join(lines)

# ─── POST 1: TASA DEL DÍA ───
post1 = make_post([
    {"type": "text", "pos": (540, 120), "text": "💵 TASA DEL DÍA", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 65), "color": GOLD, "anchor": "mt"},
    {"type": "line", "xy": [(340, 190), (740, 190)], "width": 3},
    {"type": "text", "pos": (540, 270), "text": "Dólar: $894 CLP", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 50), "color": WHITE, "anchor": "mt"},
    {"type": "text", "pos": (540, 340), "text": "Recibes el 85%", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 45), "color": GOLD, "anchor": "mt"},
    {"type": "text", "pos": (540, 400), "text": "(comisión solo 15%)", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 35), "color": GRAY, "anchor": "mt"},
    {"type": "rounded_rect", "xy": [(190, 480), (890, 680)], "fill": (40, 40, 40), "radius": 25},
    {"type": "text", "pos": (540, 530), "text": "US$500  →  $379.950", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 42), "color": WHITE, "anchor": "mt"},
    {"type": "text", "pos": (540, 585), "text": "US$1.500  →  $1.139.850", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 42), "color": WHITE, "anchor": "mt"},
    {"type": "text", "pos": (540, 640), "text": "US$3.000  →  $2.279.700", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 42), "color": WHITE, "anchor": "mt"},
    {"type": "text", "pos": (540, 750), "text": "Transferencia en 15 minutos ⏱️", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 38), "color": GOLD, "anchor": "mt"},
    {"type": "text", "pos": (540, 810), "text": "100% online por WhatsApp", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 35), "color": GRAY, "anchor": "mt"},
    {"type": "text", "pos": (540, 970), "text": "@cupo_dolarcl", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 28), "color": GRAY, "anchor": "mb"},
], "post1_tasa.png")

# ─── POST 2: SIN AVANCE ───
post2 = make_post([
    {"type": "text", "pos": (540, 140), "text": "❌ ¿SIN AVANCE?", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 65), "color": GOLD, "anchor": "mt"},
    {"type": "text", "pos": (540, 220), "text": "No importa.", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 50), "color": WHITE, "anchor": "mt"},
    {"type": "text", "pos": (540, 290), "text": "Te compramos tu cupo igual", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 40), "color": WHITE, "anchor": "mt"},
    {"type": "rounded_rect", "xy": [(190, 390), (890, 490)], "fill": (40, 40, 40), "radius": 25},
    {"type": "text", "pos": (540, 440), "text": "💳 CMR / Ripley / Cencosud / Lider", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 35), "color": WHITE, "anchor": "mt"},
    {"type": "rounded_rect", "xy": [(190, 520), (890, 620)], "fill": (40, 40, 40), "radius": 25},
    {"type": "text", "pos": (540, 570), "text": "🏦 Banco Chile / Santander / BCI", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 35), "color": WHITE, "anchor": "mt"},
    {"type": "rounded_rect", "xy": [(290, 700), (790, 780)], "fill": GOLD, "radius": 30},
    {"type": "text", "pos": (540, 740), "text": "WA.ME/56967658939", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 35), "color": (26,26,26), "anchor": "mt"},
    {"type": "text", "pos": (540, 830), "text": "Cotiza hoy, recibe tu dinero en 15 min", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 30), "color": GRAY, "anchor": "mt"},
    {"type": "text", "pos": (540, 970), "text": "@cupo_dolarcl", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 28), "color": GRAY, "anchor": "mb"},
], "post2_sinavance.png")

# ─── POST 3: 3 RAZONES ───
post3 = make_post([
    {"type": "text", "pos": (540, 130), "text": "🔥 3 RAZONES", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 55), "color": GOLD, "anchor": "mt"},
    {"type": "text", "pos": (540, 195), "text": "para vender tu cupo con nosotros", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 35), "color": WHITE, "anchor": "mt"},
    {"type": "rounded_rect", "xy": [(190, 280), (890, 400)], "fill": (40, 40, 40), "radius": 25},
    {"type": "text", "pos": (220, 310), "text": "1️⃣", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 40), "color": GOLD},
    {"type": "text", "pos": (280, 315), "text": "Transferencia en 15 minutos", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 35), "color": WHITE},
    {"type": "text", "pos": (280, 355), "text": "Tu dinero en la cuenta al instante", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 28), "color": GRAY},
    {"type": "rounded_rect", "xy": [(190, 430), (890, 550)], "fill": (40, 40, 40), "radius": 25},
    {"type": "text", "pos": (220, 460), "text": "2️⃣", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 40), "color": GOLD},
    {"type": "text", "pos": (280, 465), "text": "Sin Dicom ni aval", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 35), "color": WHITE},
    {"type": "text", "pos": (280, 505), "text": "Sin revisar tu historial crediticio", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 28), "color": GRAY},
    {"type": "rounded_rect", "xy": [(190, 580), (890, 700)], "fill": (40, 40, 40), "radius": 25},
    {"type": "text", "pos": (220, 610), "text": "3️⃣", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 40), "color": GOLD},
    {"type": "text", "pos": (280, 615), "text": "Mejor tasa del mercado", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 35), "color": WHITE},
    {"type": "text", "pos": (280, 655), "text": "85% del dólar, sin comisiones ocultas", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 28), "color": GRAY},
    {"type": "text", "pos": (540, 800), "text": "👇 Cotiza por WhatsApp", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 32), "color": GOLD, "anchor": "mt"},
    {"type": "text", "pos": (540, 970), "text": "@cupo_dolarcl", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 28), "color": GRAY, "anchor": "mb"},
], "post3_razones.png")

# ─── POST 4: CÁLCULO RÁPIDO ───
post4 = make_post([
    {"type": "text", "pos": (540, 130), "text": "🧮 ¿CUÁNTO RECIBES?", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 55), "color": GOLD, "anchor": "mt"},
    {"type": "line", "xy": [(340, 190), (740, 190)], "width": 3},
    {"type": "rounded_rect", "xy": [(290, 260), (790, 340)], "fill": (40, 40, 40), "radius": 20},
    {"type": "text", "pos": (540, 300), "text": "$894  →  85%  =  $760 CLP por USD", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 30), "color": WHITE, "anchor": "mt"},
    {"type": "rounded_rect", "xy": [(190, 400), (890, 520)], "fill": (40, 40, 40), "radius": 25},
    {"type": "text", "pos": (300, 440), "text": "💵  US$ 500", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 42), "color": WHITE},
    {"type": "text", "pos": (700, 440), "text": "$ 379.950", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 42), "color": GOLD, "anchor": "mt"},
    {"type": "rounded_rect", "xy": [(190, 550), (890, 670)], "fill": (40, 40, 40), "radius": 25},
    {"type": "text", "pos": (300, 590), "text": "💵  US$ 1.500", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 42), "color": WHITE},
    {"type": "text", "pos": (720, 590), "text": "$ 1.139.850", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 42), "color": GOLD, "anchor": "mt"},
    {"type": "rounded_rect", "xy": [(190, 700), (890, 820)], "fill": (40, 40, 40), "radius": 25},
    {"type": "text", "pos": (300, 740), "text": "💵  US$ 3.000", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 42), "color": WHITE},
    {"type": "text", "pos": (720, 740), "text": "$ 2.279.700", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 42), "color": GOLD, "anchor": "mt"},
    {"type": "rounded_rect", "xy": [(290, 880), (790, 960)], "fill": GOLD, "radius": 30},
    {"type": "text", "pos": (540, 920), "text": "COTIZA AHORA", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 35), "color": (26,26,26), "anchor": "mt"},
    {"type": "text", "pos": (540, 1000), "text": "@cupo_dolarcl", "font": ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 28), "color": GRAY, "anchor": "mb"},
], "post4_calculo.png")

# ─── STORY 1: TASA (1080x1920) ───
W_STORY, H_STORY = 1080, 1920
story1 = Image.new("RGB", (W_STORY, H_STORY), BG)
draw = ImageDraw.Draw(story1)

# Flying dollar bills effect (simple circles as decoration)
for _ in range(15):
    import random
    x, y = random.randint(50, 1030), random.randint(50, 1870)
    s = random.randint(15, 40)
    draw.ellipse([(x-s, y-s), (x+s, y+s)], fill=(GOLD[0], GOLD[1]-20, GOLD[2]-20, 30))

draw.text((540, 250), "💵 TASA DEL DÍA", fill=GOLD, font=ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 60), anchor="mt")
draw.text((540, 350), "Te pagamos el 85%", fill=WHITE, font=ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 40), anchor="mt")

draw.rounded_rectangle([(140, 450), (940, 600)], radius=25, fill=(40,40,40))
draw.text((240, 500), "$", fill=GOLD, font=ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 60))
draw.text((540, 500), "894", fill=WHITE, font=ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 60), anchor="mt")
draw.text((700, 510), "CLP/USD", fill=GRAY, font=ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 30))

draw.rounded_rectangle([(140, 680), (940, 880)], radius=25, fill=(40,40,40))
draw.text((340, 710), "US$ 500  →", fill=WHITE, font=ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 40))
draw.text((700, 710), "$ 379.950", fill=GOLD, font=ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 40), anchor="mt")
draw.text((340, 775), "US$ 1.500  →", fill=WHITE, font=ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 40))
draw.text((720, 775), "$ 1.139.850", fill=GOLD, font=ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 40), anchor="mt")
draw.text((340, 840), "US$ 3.000  →", fill=WHITE, font=ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 40))
draw.text((720, 840), "$ 2.279.700", fill=GOLD, font=ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 40), anchor="mt")

draw.rounded_rectangle([(240, 980), (840, 1080)], radius=30, fill=GOLD)
draw.text((540, 1030), "WA.ME/56967658939", fill=(26,26,26), font=ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 35), anchor="mt")

draw.text((540, 1160), "Transferencia en 15 min ⏱️", fill=GRAY, font=ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 30), anchor="mt")

story1.save(os.path.join(OUT, "story_tasa.png"), "PNG", optimize=True)

# ─── STORY 2: LLAMADO RÁPIDO ───
story2 = Image.new("RGB", (W_STORY, H_STORY), BG)
draw = ImageDraw.Draw(story2)

draw.text((540, 300), "⚠️", fill=GOLD, font=ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 80), anchor="mt")
draw.text((540, 420), "¿NECESITAS PLATA", fill=WHITE, font=ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 55), anchor="mt")
draw.text((540, 490), "EN MENOS DE 15 MIN?", fill=GOLD, font=ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 50), anchor="mt")

draw.text((540, 650), "Vende tu cupo en dólares", fill=WHITE, font=ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 35), anchor="mt")
draw.text((540, 710), "y recibe la transferencia", fill=WHITE, font=ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 35), anchor="mt")
draw.text((540, 770), "al instante 📲", fill=GOLD, font=ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 35), anchor="mt")

draw.rounded_rectangle([(240, 900), (840, 1000)], radius=30, fill=GOLD)
draw.text((540, 950), "COTIZA AQUÍ", fill=(26,26,26), font=ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 35), anchor="mt")

draw.text((540, 1060), "Sin Dicom · Sin aval · 100% online", fill=GRAY, font=ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 27), anchor="mt")

story2.save(os.path.join(OUT, "story_urgente.png"), "PNG", optimize=True)

print("✅ Imágenes generadas:")
for f in os.listdir(OUT):
    size = os.path.getsize(os.path.join(OUT, f))
    print(f"  {f}: {size//1024} KB")
