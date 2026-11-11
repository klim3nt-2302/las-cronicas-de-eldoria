"""Genera la portada (1920x1080) y el icono (1024x1024) del juego a partir de sus propios sprites.

Uso:  python3 herramientas/gen_portada.py   (desde la carpeta Eldoria)
Salida: assets/portada/portada.png y assets/portada/icono.png
"""
import math
import os
import random
import struct
import zlib

from pixel import Canvas, hex2rgba as H

ROOT = os.path.join(os.path.dirname(__file__), '..')


def load(path):
    """Lee un PNG RGBA de 8 bits (como los que genera pixel.py)."""
    d = open(os.path.join(ROOT, path), 'rb').read()
    i, idat = 8, b''
    while i < len(d):
        n = struct.unpack('>I', d[i:i + 4])[0]
        t, c = d[i + 4:i + 8], d[i + 8:i + 8 + n]
        if t == b'IHDR':
            w, h = struct.unpack('>II', c[:8])
        elif t == b'IDAT':
            idat += c
        i += 12 + n
    raw = zlib.decompress(idat)
    cv, st = Canvas(w, h), w * 4 + 1
    for y in range(h):
        row = raw[y * st + 1:(y + 1) * st]
        for x in range(w):
            cv.px[y * w + x] = list(row[x * 4:x * 4 + 4])
    return cv
SPR = 'assets/sprites/'
OUT = os.path.join(ROOT, 'assets', 'portada')
os.makedirs(OUT, exist_ok=True)

# Fuente pixel 5x9 (2 filas superiores para tildes)
GLYPHS = {
    'A': [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    'B': ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    'C': [".####", "#....", "#....", "#....", "#....", "#....", ".####"],
    'D': ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    'E': ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    'I': ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    'L': ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    'N': ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    'O': [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    'R': ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    'S': [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    'T': ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    ' ': ["....."] * 7,
}
ACCENT = {'Ó': 'O'}


def glyph(ch):
    if ch in ACCENT:
        return ["...#.", "..#.."] + GLYPHS[ACCENT[ch]]
    return [".....", "....."] + GLYPHS[ch]


def text_mask(txt):
    rows = [''] * 9
    for ch in txt:
        g = glyph(ch)
        for i in range(9):
            rows[i] += g[i] + '.'
    return [r[:-1] for r in rows]


def draw_text(cv, txt, cx, y, px, top, bottom, outline=H('#1b1024'), shadow=H('#000000', 150)):
    """Texto centrado en cx, con relleno degradado, contorno y sombra. px = tamaño de cada pixel."""
    m = text_mask(txt)
    w = len(m[0]) * px
    x0 = int(cx - w / 2)
    on = lambda r, c: 0 <= r < 9 and 0 <= c < len(m[0]) and m[r][c] == '#'
    # sombra y contorno
    for r in range(-1, 10):
        for c in range(-1, len(m[0]) + 1):
            if on(r, c):
                continue
            if any(on(r + dr, c + dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1)):
                cv.rect(x0 + c * px, y + r * px, x0 + (c + 1) * px, y + (r + 1) * px, outline)
    for r in range(9):
        for c in range(len(m[0])):
            if on(r, c):
                cv.rect(x0 + c * px + px, y + r * px + px * 2, x0 + (c + 1) * px + px, y + (r + 1) * px + px * 2, shadow)
    for r in range(9):
        k = max(0, r - 2) / 6
        col = tuple(int(top[i] + (bottom[i] - top[i]) * k) for i in range(3)) + (255,)
        for c in range(len(m[0])):
            if on(r, c):
                cv.rect(x0 + c * px, y + r * px, x0 + (c + 1) * px, y + (r + 1) * px, col)
                if r in (2, 3) and m[r - 1][c] != '#':
                    cv.rect(x0 + c * px, y + r * px, x0 + (c + 1) * px, y + r * px + max(1, px // 3), H('#ffffff', 170))


def sprite(name, scale=1):
    img = load(SPR + name)
    return img.scaled(scale) if scale > 1 else img


def glow(cv, cx, cy, r, color, steps=6, alpha=40):
    for i in range(steps):
        cv.circle(cx, cy, r * (1 - i / steps), H(color, alpha))


# ------------------------------------------------------------------ Portada 960x540 → x2 = 1920x1080
cv = load(SPR + 'fondo_bosque_cielo.png')
cv.paste(load(SPR + 'fondo_bosque_montanas.png'), 0, 0)
cv.paste(load(SPR + 'fondo_bosque_arboles.png'), 0, 0)
# oscurecer arriba para que el título destaque
for y in range(0, 230):
    a = int(170 * (1 - y / 230) ** 1.4)
    cv.rect(0, y, 960, y + 1, (12, 8, 32, a))
suelo = load(SPR + 'suelo_bosque.png')
for x in range(0, 960, 48):
    cv.paste(suelo, x, 450)

glow(cv, 812, 330, 150, "#b06eff", 16, 13)
cv.paste(sprite('portal1.png', 2), 740, 210)
cv.paste(sprite('arbusto.png', 2), 40, 402)
cv.paste(sprite('arbusto.png', 2), 860, 402)
for x in (250, 560, 700):
    cv.paste(sprite('flor.png'), x, 432)
cv.paste(sprite('sabio1.png', 2), 130, 306)
cv.paste(sprite('goblin1.png', 2).flipped(), 610, 354)
cv.paste(sprite('murcielago1.png', 2), 560, 200)
cv.paste(sprite('murcielago2.png', 2).flipped(), 850, 150)
glow(cv, 425, 300, 90, "#ffe9a0", 16, 11)
cv.paste(sprite('lyra_saltar.png', 2), 380, 222)
cv.paste(sprite('hada1.png', 2), 280, 230)
for (x, y) in [(330, 360), (510, 300), (560, 360), (470, 200)]:
    cv.paste(sprite('gema%d.png' % random.Random(x).randint(1, 4)), x, y)
for (x, y) in [(500, 196), (300, 330), (700, 280)]:
    cv.paste(sprite('destello2.png'), x, y)

# viñeta suave en los bordes
for y in range(540):
    for x in range(0, 960, 2):
        d = math.hypot((x - 480) / 480, (y - 270) / 270)
        if d > 0.85:
            a = int(min(120, (d - 0.85) * 260))
            cv.blend(x, y, (8, 4, 20, a))
            cv.blend(x + 1, y, (8, 4, 20, a))

draw_text(cv, 'LAS CRÓNICAS', 480, 18, 7, H('#fff2a0'), H('#ff9a2a'))
draw_text(cv, 'DE ELDORIA', 480, 92, 7, H('#fff2a0'), H('#ff9a2a'))
draw_text(cv, 'EL CRISTAL DEL ALBA', 480, 168, 3, H('#e8dcff'), H('#a98aff'))
cv.scaled(2).save(os.path.join(OUT, 'portada.png'))

# ------------------------------------------------------------------ Icono 256x256 → x4 = 1024x1024
ic = Canvas(256, 256)
for y in range(256):
    for x in range(256):
        d = math.hypot(x - 128, y - 128) / 181
        c0, c1 = H('#4a2f8a'), H('#0d0a24')
        ic.set(x, y, tuple(int(c0[i] + (c1[i] - c0[i]) * d) for i in range(3)) + (255,))
r = random.Random(3)
for _ in range(40):
    ic.blend(r.randrange(256), r.randrange(256), H('#ffffff', r.choice([90, 160, 255])))
glow(ic, 128, 120, 110, "#ffe9a0", 18, 10)
ic.paste(sprite('lyra_quieto1.png', 3), 128 - 72, 26)
ic.paste(sprite('gema1.png'), 196, 52)
ic.paste(sprite('destello2.png'), 30, 60)
ic.paste(sprite('destello3.png'), 200, 170)
# marco dorado
for i, col in enumerate(['#1b1024', '#ffd84a', '#8a6a20']):
    ic.rect(i * 2, i * 2, 256 - i * 2, i * 2 + 2, H(col))
    ic.rect(i * 2, 254 - i * 2, 256 - i * 2, 256 - i * 2, H(col))
    ic.rect(i * 2, i * 2, i * 2 + 2, 256 - i * 2, H(col))
    ic.rect(254 - i * 2, i * 2, 256 - i * 2, 256 - i * 2, H(col))
ic.scaled(4).save(os.path.join(OUT, 'icono.png'))
print('assets/portada/portada.png (1920x1080) y assets/portada/icono.png (1024x1024)')
