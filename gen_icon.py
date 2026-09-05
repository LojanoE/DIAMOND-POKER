"""Genera los iconos de la app DIAMOND CLUB (diamante de poker con glow)."""
from PIL import Image, ImageDraw, ImageFilter

SIZE = 512
CX = SIZE // 2
CY = SIZE // 2

# Colores del tema
BG = (5, 5, 5, 255)
RED = (255, 42, 42)
ORANGE = (255, 107, 0)
GOLD = (255, 170, 0)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def make_icon():
    img = Image.new("RGBA", (SIZE, SIZE), BG)

    # ---- Brillo radial de fondo ----
    glow_bg = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(glow_bg)
    d.ellipse([CX - 200, CY - 200, CX + 200, CY + 200], fill=(255, 43, 43, 60))
    glow_bg = glow_bg.filter(ImageFilter.GaussianBlur(90))
    img = Image.alpha_composite(img, glow_bg)

    # ---- Anillo exterior (ficha de poker) ----
    ring = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(ring)
    d.ellipse([40, 40, SIZE - 40, SIZE - 40], outline=GOLD + (255,), width=10)
    # Muescas de la ficha
    import math
    for ang in range(0, 360, 45):
        rad = math.radians(ang)
        x1 = CX + int(232 * math.cos(rad)); y1 = CY + int(232 * math.sin(rad))
        x2 = CX + int(196 * math.cos(rad)); y2 = CY + int(196 * math.sin(rad))
        d.line([x1, y1, x2, y2], fill=GOLD + (255,), width=14)
    img = Image.alpha_composite(img, ring)

    # ---- Diamante con glow ----
    w, h = 110, 150
    points = [(CX, CY - h), (CX + w, CY), (CX, CY + h), (CX - w, CY)]

    glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(glow).polygon(points, fill=(255, 60, 60, 200))
    glow = glow.filter(ImageFilter.GaussianBlur(35))
    img = Image.alpha_composite(img, glow)

    # Relleno con gradiente vertical rojo -> naranja -> dorado
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).polygon(points, fill=255)
    grad = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    top, bottom = CY - h, CY + h
    for y in range(top, bottom + 1):
        t = (y - top) / (bottom - top)
        c = lerp(RED, ORANGE, t * 2) if t < 0.5 else lerp(ORANGE, GOLD, (t - 0.5) * 2)
        gd.line([(0, y), (SIZE, y)], fill=c + (255,))
    img.paste(grad, (0, 0), mask)

    # Brillo superior del diamante
    shine = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(shine).polygon(
        [(CX, CY - h + 18), (CX + w - 40, CY - 10), (CX, CY - 20)],
        fill=(255, 255, 255, 90),
    )
    shine = shine.filter(ImageFilter.GaussianBlur(6))
    shine.putalpha(Image.composite(shine.split()[3], Image.new("L", (SIZE, SIZE), 0), mask))
    img = Image.alpha_composite(img, shine)

    return img


icon = make_icon()
icon.save("icon-512.png")
icon.resize((192, 192), Image.LANCZOS).save("icon-192.png")
icon.resize((180, 180), Image.LANCZOS).save("apple-touch-icon.png")
print("Iconos generados: icon-512.png, icon-192.png, apple-touch-icon.png")
