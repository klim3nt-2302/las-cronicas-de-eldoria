"""Genera todos los sprites y fondos del juego (pixel art original, PNG con transparencia).

Uso:  python3 herramientas/gen_imagenes.py   (desde la carpeta Eldoria)
"""
import math
import os
import random

from pixel import Canvas, from_ascii, hex2rgba as H

S = 3  # escala de pixel art (1 pixel lógico = 3x3 pixeles reales)
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'sprites')
os.makedirs(OUT, exist_ok=True)


def save(cv, name, scale=S):
    (cv.scaled(scale) if scale > 1 else cv).save(os.path.join(OUT, name))


# ---------------------------------------------------------------- Avatar: Lyra
PAL_LYRA = {
    'k': H('#1b1424'), 'G': H('#2e6b3a'), 'g': H('#4caf50'), 'h': H('#f0a640'),
    's': H('#f6c9a0'), 'S': H('#d9966b'), 'e': H('#1b1424'), 'c': H('#b8323e'),
    'B': H('#3d63c9'), 'b': H('#7a4a26'), 'y': H('#ffd84a'), 'P': H('#5b4636'),
    'n': H('#6d3d1f'), 'w': H('#ffffff'),
}
LYRA_TOP = [
    "................",
    "......kkkkk.....",
    ".....kGgggggk...",
    "....kGggggggk...",
    "....kGgggggggk..",
    "...kGgghhhhggk..",
    "...kGghhssssgk..",
    "...kGghssseskk..",
    "...kGgsssssSk...",
    "....kGgsssSk....",
    "....kkkGkkk.....",
    "...kcBBBBBBk....",
    "..kccBBBBBBBk...",
    "..kccBBBBBsSk...",
    "..kccbbybbbkk...",
    "..kcBBBBBBBk....",
    "...kBBBBBBBk....",
]
LYRA_LEGS = {
    'quieto': [
        "...kPPPkPPPk....",
        "....kPPkPPk.....",
        "....kPPkPPk.....",
        "....kPPkPPk.....",
        "....knnknnk.....",
        "...knnnknnnk....",
        "...kkkkkkkkk....",
    ],
    'correr1': [
        "...kPPPPPPPk....",
        "..kPPk..kPPk....",
        ".kPPk....kPPk...",
        ".kPk......kPk...",
        "knnk......knnk..",
        "knnnk.....knnnk.",
        "kkkk.......kkkk.",
    ],
    'correr2': [
        "...kPPPPPPk.....",
        "....kPPPPk......",
        "....kPPkPk......",
        "....kPkkPk......",
        "...knnkknnk.....",
        "...knnnkknnk....",
        "...kkkk.kkkk....",
    ],
    'correr3': [
        "...kPPPPPPPk....",
        "...kPPk.kPPk....",
        "..kPPk...kPPk...",
        "..kPk.....kPk...",
        ".knnk.....knnk..",
        ".knnnk....knnnk.",
        ".kkkk......kkkk.",
    ],
    'saltar': [
        "...kPPPPPPPk....",
        "...kPPkkPPPPk...",
        "..kPPk..kkPPk...",
        "..knnk....knnk..",
        "..knnnk...knnnk.",
        "..kkkk....kkkk..",
        "................",
    ],
}


def lyra(legs, blink=False):
    top = list(LYRA_TOP)
    if blink:
        top[7] = "...kGghsssSskk.."
    return from_ascii(top + LYRA_LEGS[legs], PAL_LYRA, 16)


save(lyra('quieto'), 'lyra_quieto1.png')
save(lyra('quieto', blink=True), 'lyra_quieto2.png')
save(lyra('correr1'), 'lyra_correr1.png')
save(lyra('correr2'), 'lyra_correr2.png')
save(lyra('correr3'), 'lyra_correr3.png')
save(lyra('correr2'), 'lyra_correr4.png')
save(lyra('saltar'), 'lyra_saltar.png')

# ---------------------------------------------------------------- NPC: Goblin
PAL_GOB = {'k': H('#1b1424'), 'L': H('#6dbf3a'), 'D': H('#3f7d22'), 'r': H('#ff3b3b'),
           'w': H('#ffffff'), 'b': H('#8a5a2b'), 'y': H('#c9c9c9')}
GOB_TOP = [
    "................",
    "................",
    ".....kkkkk......",
    "....kLLLLLk..k..",
    "...kDLLLLLLkkLk.",
    "...kDLLLLrLLLk..",
    "..kDDLLLLLLLk...",
    "..kDLLLLLLkwkw..",
    "...kDLLLLLLLk...",
    "....kkbbbbkk....",
    "...kbbbbbbbbk...",
    "..kLbbbybbbbLk..",
    "..kkbbbbbbbbkk..",
]
GOB_LEGS = [
    ["....kbbkkbbk....", "....kLLk.kLLk...", "...kkkk..kkkk..."],
    ["....kbbkkbbk....", "...kLLk...kLLk..", "..kkkk....kkkk.."],
]
save(from_ascii(GOB_TOP + GOB_LEGS[0], PAL_GOB, 16), 'goblin1.png')
save(from_ascii(GOB_TOP + GOB_LEGS[1], PAL_GOB, 16), 'goblin2.png')

# ---------------------------------------------------------------- NPC: Murciélago
PAL_BAT = {'k': H('#140c1c'), 'V': H('#6b3fa0'), 'r': H('#ffe14a'), 'w': H('#ffffff')}
BAT_A = [
    "k..............k",
    "kk............kk",
    "kVk..........kVk",
    "kVVk..kkkk..kVVk",
    ".kVVkkVVVVkkVVk.",
    ".kVVVVVrVrVVVVk.",
    "..kVVVVVVVVVVk..",
    "...kkVVwVwVkk...",
    ".....kVVVVk.....",
    "......kkkk......",
    "................",
    "................",
]
BAT_B = [
    "................",
    "................",
    "................",
    "......kkkk......",
    ".....kVVVVk.....",
    "...kkVrVVrVkk...",
    "..kVVVVVVVVVVk..",
    ".kVVVkVwVwkVVVk.",
    "kVVk.kVVVVk.kVVk",
    "kVk...kkkk...kVk",
    "kk............kk",
    "k..............k",
]
save(from_ascii(BAT_A, PAL_BAT, 16), 'murcielago1.png')
save(from_ascii(BAT_B, PAL_BAT, 16), 'murcielago2.png')

# ---------------------------------------------------------------- NPC: Sabio Eldric
SAGE = [
    "......k.........",
    ".....kMk........",
    ".....kMMk.......",
    "....kMMMk.......",
    "....kMyMMk..kkk.",
    "...kMMMMMMk.kOOk",
    "..kkkkkkkkkkkOOk",
    "...kWsssssk..kk.",
    "...kWsssesk...n.",
    "...kWWsssSk...n.",
    "..kWWWWWWWk...n.",
    "..kMWWWWWWMk..n.",
    ".kMMWWWWWMMsk.n.",
    ".kMMMWWWMMMssnn.",
    ".kMMMMWMMMMkk.n.",
    ".kMMyMMMMMMk..n.",
    ".kMMMMMMMMMk..n.",
    ".kMMMMMMMMMk..n.",
    ".kmMMMMMMMMk..n.",
    ".kmmMMMMMMMk..n.",
    ".kmmmMMMMMMk..n.",
    ".kmmmmMMMMMk..n.",
    "..knnkknnk....n.",
    "..kkkkkkkk....n.",
]
pal_sage = {'k': H('#1b1424'), 'M': H('#5a3fa8'), 'm': H('#3e2a78'), 'W': H('#f0f0f0'),
            's': H('#f6c9a0'), 'S': H('#d9966b'), 'e': H('#1b1424'), 'y': H('#ffd84a'),
            'O': H('#6ef0ff'), 'n': H('#7a4a26')}
save(from_ascii(SAGE, pal_sage, 16), 'sabio1.png')
pal_sage2 = dict(pal_sage, O=H('#e6ffff'))
save(from_ascii(SAGE, pal_sage2, 16), 'sabio2.png')

# ---------------------------------------------------------------- NPC: Hada Lumi
FAIRY_A = [
    "....kkkk....",
    "...khhhhk...",
    "cc.khssek.cc",
    "ccc.kssk.ccc",
    "cccckPPkcccc",
    ".ccckPPkccc.",
    "..cckPPkcc..",
    "...kPPPPk...",
    "...kPPPPk...",
    "....kssk....",
    "....k..k....",
    "............",
]
FAIRY_B = [
    "....kkkk....",
    "...khhhhk...",
    "...khssek...",
    ".cc.kssk.cc.",
    ".ccckPPkccc.",
    "..cckPPkcc..",
    "...ckPPkc...",
    "...kPPPPk...",
    "...kPPPPk...",
    "....kssk....",
    "....k..k....",
    "............",
]
pal_fairy = {'k': H('#2a1430'), 'h': H('#ff7ac8'), 's': H('#ffe0c8'), 'e': H('#2a1430'),
             'P': H('#ffb3e6'), 'c': H('#a8f0ff', 170)}
for i, rows in enumerate((FAIRY_A, FAIRY_B), 1):
    base = from_ascii(rows, pal_fairy, 12)
    glow = Canvas(16, 16)
    glow.circle(7.5, 7.5, 7.5, H('#fff6a8', 50))
    glow.circle(7.5, 7.5, 5, H('#fff6a8', 50))
    glow.paste(base, 2, 2)
    save(glow, 'hada%d.png' % i)

# ---------------------------------------------------------------- Terrenos
rnd = random.Random(7)


def ground_texture(top_colors, body, body_dark, pebble, crystal=None):
    cv = Canvas(16, 96)
    for y in range(96):
        for x in range(16):
            c = body if (x * 7 + y * 3) % 11 else body_dark
            cv.set(x, y, c)
    for _ in range(40):
        x, y = rnd.randrange(16), rnd.randrange(8, 96)
        cv.set(x, y, pebble)
        cv.set(min(15, x + 1), y, pebble)
    # borde superior
    for x in range(16):
        h = 4 + (1 if (x * 5) % 7 < 3 else 0)
        for y in range(h):
            cv.set(x, y, top_colors[0] if y < h - 2 else top_colors[1])
        cv.set(x, h, top_colors[2])
    for x in range(0, 16, 3):
        cv.set(x, 0, top_colors[3])
    if crystal:
        for x0 in (3, 11):
            cv.polygon([(x0, 5), (x0 + 1.5, 0), (x0 + 3, 5)], crystal)
    return cv


save(ground_texture([H('#5fd35a'), H('#3c9c3e'), H('#2a5a2a'), H('#9df08a')],
                    H('#7a5233'), H('#6a4529'), H('#9b7550')), 'suelo_bosque.png')
save(ground_texture([H('#8a7ad6'), H('#5c4ca8'), H('#2a1f4a'), H('#c7bbff')],
                    H('#3b3060'), H('#332854'), H('#56488a'), crystal=H('#6ef0ff')), 'suelo_cueva.png')


def plank(c1, c2, edge):
    cv = Canvas(16, 8)
    cv.rect(0, 0, 16, 8, H('#1b1424'))
    cv.rect(0, 1, 16, 7, c1)
    cv.rect(0, 1, 16, 2, edge)
    cv.rect(0, 5, 16, 7, c2)
    cv.set(7, 3, H('#1b1424'))
    cv.set(15, 2, H('#1b1424'))
    cv.set(15, 3, H('#1b1424'))
    cv.set(15, 4, H('#1b1424'))
    return cv


save(plank(H('#a0703f'), H('#7a5233'), H('#c99a60')), 'plataforma_madera.png')
save(plank(H('#5fb8e0'), H('#3b7fb0'), H('#bdf3ff')), 'plataforma_cristal.png')

pinchos = Canvas(16, 8)
for i in range(4):
    x = i * 4
    pinchos.polygon([(x, 8), (x + 2, 0), (x + 4, 8)], H('#1b1424'))
    pinchos.polygon([(x + 0.8, 8), (x + 2, 1.5), (x + 3.2, 8)], H('#c9d1dc'))
    pinchos.polygon([(x + 2, 8), (x + 2, 1.5), (x + 3.2, 8)], H('#8890a0'))
save(pinchos, 'pinchos.png')

movil = Canvas(48, 8)
movil.rect(0, 0, 48, 8, H('#1b1424'))
movil.rect(1, 1, 47, 7, H('#6f6a8a'))
movil.rect(1, 1, 47, 2, H('#a7a1c9'))
for x in range(6, 44, 9):
    movil.rect(x, 3, x + 3, 5, H('#6ef0ff'))
save(movil, 'plataforma_movil.png')

# ---------------------------------------------------------------- Objetos
PAL_GEM = {'k': H('#0d2a40'), 'c': H('#39e0ff'), 'C': H('#1a8fc9'), 'w': H('#ffffff')}
GEM = [
    "...kkkkkk...",
    "..kccccCCk..",
    ".kccccccCCk.",
    "kkkkkkkkkkkk",
    ".kcccccCCCk.",
    "..kccccCCk..",
    "...kcccCk...",
    "....kcCk....",
    ".....kk.....",
]
shine = [[(1, 4), (2, 4)], [(2, 6), (3, 5)], [(4, 7), (5, 6)], [(4, 3), (5, 3)]]
for i, pts in enumerate(shine, 1):
    cv = from_ascii(GEM, PAL_GEM, 12)
    for (y, x) in pts:
        cv.set(x, y, PAL_GEM['w'])
    save(cv, 'gema%d.png' % i)

HEART = [
    ".kk...kk.",
    "kRRk.kRRk",
    "kRwRkRRRk",
    "kRRRRRRRk",
    ".kRRRRRk.",
    "..kRRRk..",
    "...kRk...",
    "....k....",
]
heart = from_ascii(HEART, {'k': H('#2a0c14'), 'R': H('#ff3b5c'), 'w': H('#ffffff')}, 9)
heart_empty = from_ascii(HEART, {'k': H('#2a0c14'), 'R': H('#4a3346'), 'w': H('#6a5266')}, 9)
save(heart, 'corazon.png')
for n in range(4):
    cv = Canvas(31, 8)
    for i in range(3):
        cv.paste(heart if i < n else heart_empty, i * 11, 0)
    save(cv, 'hud_vidas%d.png' % n)

KEY = [
    ".kkkk.........",
    "kyyyyk........",
    "kyk.kykkkkkkk.",
    "kyk.kyyyyyyyyk",
    "kyyyykkkykykyk",
    ".kkkk...k.k.k.",
]
save(from_ascii(KEY, {'k': H('#3a2400'), 'y': H('#ffd84a')}, 14), 'llave.png')

CHEST_BODY = [
    "kbBBBBkyykBBBBbk",
    "kbBBBBkyykBBBBbk",
    "kbBBBBBkkBBBBBbk",
    "kbBBBBBBBBBBBBbk",
    "kyyyyyyyyyyyyyyk",
    "kbBBBBBBBBBBBBbk",
    "kbbbbbbbbbbbbbbk",
    "kkkkkkkkkkkkkkkk",
]
pal_chest = {'k': H('#1b1424'), 'b': H('#5c3a1e'), 'B': H('#8a5a2b'), 'y': H('#ffd84a'),
             'o': H('#fff3a0')}
save(from_ascii(["..kkkkkkkkkkkk..", ".kbbbbbbbbbbbbk.", "kbBBBBBBBBBBBBbk",
                 "kbBBBBBBBBBBBBbk", "kyyyyyykkyyyyyyk"] + CHEST_BODY, pal_chest, 16), 'cofre_cerrado.png')
save(from_ascii(["kbbbbbbbbbbbbbbk", "kbBBBBBBBBBBBBbk", "kyyyyyyyyyyyyyyk",
                 "kkkkkkkkkkkkkkkk", "kooooooooooooook"] + CHEST_BODY, pal_chest, 16), 'cofre_abierto.png')

MUSH_CAP = [
    "....kkkkkkkk....",
    "..kkRRwwRRRRkk..",
    ".kRRwwwRRRRwwRk.",
    "kRRRwwRRRRRwwRRk",
    "kRRRRRRRwwRRRRRk",
    "kRwwRRRRwwRRRRRk",
    "kkkkkkkkkkkkkkkk",
]
pal_mush = {'k': H('#1b1424'), 'R': H('#d63aa8'), 'w': H('#ffd6f5'), 's': H('#f2e6c9'),
            'e': H('#1b1424')}
stem = ["....kssssssk....", "....ksekseks....", "....kssssssk....", "....kssssssk....",
        "....kssssssk....", "...kkkkkkkkkk..."]
save(from_ascii(MUSH_CAP + stem, pal_mush, 16), 'hongo1.png')
save(from_ascii(["................"] * 3 + MUSH_CAP + stem[3:], pal_mush, 16), 'hongo2.png')


def flag(color):
    rows = [".kk.........", "kyyk........", ".kk.........", ".kpkkkkkkk..",
            ".kpFFFFFFFk.", ".kpFFFFFFFFk", ".kpFFFyFFFk.", ".kpFFFFFFFFk",
            ".kpFFFFFFFk.", ".kpkkkkkkk.."] + [".kpk........"] * 12 + ["kkkkk.......", "kpppk......."]
    return from_ascii(rows, {'k': H('#1b1424'), 'y': H('#ffd84a'), 'p': H('#b0a090'),
                             'F': color}, 12)


save(flag(H('#6b6b7a')), 'bandera_apagada.png')
save(flag(H('#3ddc84')), 'bandera_encendida.png')

for f in range(4):
    cv = Canvas(24, 40)
    for y in range(40):
        for x in range(24):
            dx, dy = (x - 11.5) / 11.5, (y - 19.5) / 19.5
            r = math.sqrt(dx * dx + dy * dy)
            if r <= 1:
                ang = math.atan2(dy, dx)
                v = math.sin(ang * 3 + r * 9 - f * math.pi / 2)
                if r > 0.86:
                    c = H('#2a1040')
                elif v > 0.4:
                    c = H('#e7a6ff')
                elif v > -0.3:
                    c = H('#a24ee0')
                else:
                    c = H('#5a1f9a')
                cv.set(x, y, c)
    save(cv, 'portal%d.png' % (f + 1))

LEVER = {
    'off': ["..kk........", ".kRRk.......", ".kRRk.......", "..kkn.......",
            "....nn......", ".....nn.....", "......nn....", "..kkkkkkkk.."],
    'on': ["........kk..", ".......kRRk.", ".......kRRk.", ".......nkk..",
           "......nn....", ".....nn.....", "....nn......", "..kkkkkkkk.."],
}
lever_base = [".kGGGGGGGGk.", ".kGgGGGGgGk.", ".kGGGGGGGGk.", ".kkkkkkkkkk."]
pal_lever = {'k': H('#1b1424'), 'R': H('#ff4a4a'), 'n': H('#9a9aa8'), 'G': H('#6f6a8a'),
             'g': H('#a7a1c9')}
save(from_ascii(LEVER['off'] + lever_base, pal_lever, 12), 'palanca_off.png')
pal_lever_on = dict(pal_lever, R=H('#3ddc84'))
save(from_ascii(LEVER['on'] + lever_base, pal_lever_on, 12), 'palanca_on.png')

gate = Canvas(16, 48)
gate.rect(0, 0, 16, 48, H('#1b1424'))
gate.rect(1, 1, 15, 47, H('#2b2440'))
for x in range(2, 15, 3):
    gate.rect(x, 1, x + 2, 47, H('#7d7a92'))
    gate.rect(x, 1, x + 1, 47, H('#b5b2c9'))
for y in (6, 24, 42):
    gate.rect(1, y, 15, y + 2, H('#5c5872'))
save(gate, 'compuerta.png')

altar = Canvas(24, 34)
altar.rect(3, 24, 21, 34, H('#1b1424'))
altar.rect(4, 25, 20, 33, H('#7d7a92'))
altar.rect(4, 25, 20, 26, H('#b5b2c9'))
altar.rect(1, 22, 23, 25, H('#1b1424'))
altar.rect(2, 23, 22, 24, H('#a7a1c9'))
for f in range(2):
    cv = Canvas(24, 34)
    glow = H('#fff2a8', 70 if f == 0 else 120)
    cv.circle(12, 11, 11, glow)
    cv.paste(altar, 0, 0)
    cv.polygon([(12, 0), (19, 9), (12, 22), (5, 9)], H('#3a2400'))
    cv.polygon([(12, 1.5), (17.5, 9), (12, 20.5), (6.5, 9)], H('#ffd84a'))
    cv.polygon([(12, 1.5), (12, 20.5), (6.5, 9)], H('#fff6c8'))
    cv.rect(11, 5, 13, 7, H('#ffffff'))
    save(cv, 'altar_cristal%d.png' % (f + 1))

for f in range(3):
    cv = Canvas(8, 20)
    cv.rect(3, 8, 5, 20, H('#5c3a1e'))
    cv.rect(2, 7, 6, 9, H('#7d7a92'))
    hgt = [6, 7, 5][f]
    cv.polygon([(1, 7), (4, 7 - hgt), (7, 7)], H('#ff8a2a'))
    cv.polygon([(2.5, 7), (4 + (f - 1) * 0.5, 7 - hgt + 2), (5.5, 7)], H('#ffe14a'))
    save(cv, 'antorcha%d.png' % (f + 1))

cristales = Canvas(16, 16)
for (x, h, c) in [(2, 9, '#6ef0ff'), (6, 14, '#b06eff'), (10, 10, '#6ef0ff'), (12, 6, '#ff7ac8')]:
    cristales.polygon([(x - 2, 16), (x, 16 - h), (x + 2, 16)], H(c))
    cristales.polygon([(x, 16), (x, 16 - h), (x + 2, 16)], H('#ffffff', 90))
save(cristales, 'cristales.png')

arbusto = Canvas(24, 12)
for (x, y, r) in [(5, 8, 4.5), (12, 6, 6), (19, 8, 4.5)]:
    arbusto.circle(x, y, r + 0.8, H('#173a20'))
for (x, y, r) in [(5, 8, 4.5), (12, 6, 6), (19, 8, 4.5)]:
    arbusto.circle(x, y, r, H('#2f7a3a'))
    arbusto.circle(x - 1, y - 1.5, r * 0.5, H('#4caf50'))
for (x, y) in [(8, 5), (15, 7), (20, 6)]:
    arbusto.set(x, y, H('#ff7ac8'))
save(arbusto, 'arbusto.png')

flor = from_ascii(["..y...", ".yry..", "..y...", "..g.g.", "..gg..", "..g..."],
                  {'y': H('#ffe14a'), 'r': H('#ff5a8a'), 'g': H('#3c9c3e')}, 6)
save(flor, 'flor.png')

CARTEL = [
    "kkkkkkkkkkkkkk",
    "kbbbbbbbbbbbbk",
    "kbBBBBBBBBBBbk",
    "kbBkkkBBkkkBbk",
    "kbBBBBBBBBBBbk",
    "kbBkkBkkkkBBbk",
    "kbbbbbbbbbbbbk",
    "kkkkkkkkkkkkkk",
    "......kbk.....",
    "......kbk.....",
    "......kbk.....",
    "......kbk.....",
    ".....kkkkk....",
]
save(from_ascii(CARTEL, {'k': H('#1b1424'), 'b': H('#7a4a26'), 'B': H('#c99a60')}, 14), 'cartel.png')

for f in range(4):
    cv = Canvas(12, 12)
    r = 1 + f * 1.4
    a = 255 - f * 55
    for i in range(4):
        ang = i * math.pi / 2 + f * 0.4
        cv.circle(5.5 + math.cos(ang) * r * 1.4, 5.5 + math.sin(ang) * r * 1.4, 1.2, H('#ffffff', a))
    cv.circle(5.5, 5.5, max(0.6, 2.5 - f * 0.7), H('#bff6ff', a))
    save(cv, 'destello%d.png' % (f + 1))

for f in range(4):
    cv = Canvas(16, 16)
    a = 230 - f * 50
    for (dx, dy) in [(-3, 1), (3, 1), (0, -2), (0, 3)]:
        cv.circle(7.5 + dx * (1 + f * 0.4), 7.5 + dy * (1 + f * 0.4), 3 - f * 0.4, H('#e8e0f0', a))
    save(cv, 'humo%d.png' % (f + 1))

ICON_E = [
    ".kkkkkkkkkk.",
    "kwwwwwwwwwwk",
    "kwwkkkkkkwwk",
    "kwwkwwwwwwwk",
    "kwwkkkkkwwwk",
    "kwwkwwwwwwwk",
    "kwwkkkkkkwwk",
    "kwwwwwwwwwwk",
    ".kkkkwkkkkk.",
    ".....kwk....",
    "......k.....",
]
save(from_ascii(ICON_E, {'k': H('#1b1424'), 'w': H('#fff6d8')}, 12), 'icono_e.png')

caja = Canvas(300, 46)
caja.rect(0, 0, 300, 46, H('#0c0a1e', 235))
caja.rect(0, 0, 300, 1, H('#ffd84a'))
caja.rect(0, 45, 300, 46, H('#ffd84a'))
caja.rect(0, 0, 1, 46, H('#ffd84a'))
caja.rect(299, 0, 300, 46, H('#ffd84a'))
caja.rect(2, 2, 298, 3, H('#8a6a20'))
caja.rect(2, 43, 298, 44, H('#8a6a20'))
for (x, y) in [(2, 2), (297, 2), (2, 43), (297, 43)]:
    caja.rect(x - 1, y - 1, x + 2, y + 2, H('#ffd84a'))
save(caja, 'caja_dialogo.png')

negro = Canvas(8, 8, (0, 0, 0, 255))
negro.save(os.path.join(OUT, 'negro.png'))
blanco = Canvas(8, 8, (255, 255, 255, 255))
blanco.save(os.path.join(OUT, 'blanco.png'))

# ---------------------------------------------------------------- Fondos (320x180 lógicos → 960x540)
BW, BH = 320, 180


def gradient(stops):
    cv = Canvas(BW, BH)
    for y in range(BH):
        t = y / (BH - 1)
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                k = (t - t0) / (t1 - t0)
                # tramado de 2 niveles para el look pixel art
                c = [int(c0[j] + (c1[j] - c0[j]) * k) for j in range(3)] + [255]
                break
        for x in range(BW):
            cv.set(x, y, c)
    return cv


def stars(cv, n, seed, ymax=120, color='#ffffff'):
    r = random.Random(seed)
    for _ in range(n):
        x, y = r.randrange(BW), r.randrange(ymax)
        cv.blend(x, y, H(color, r.choice([120, 180, 255])))


def periodic(x, terms):
    return sum(a * math.sin(2 * math.pi * (k * x / BW) + p) for (a, k, p) in terms)


# Bosque
cielo = gradient([(0, H('#2b2d6e')), (0.55, H('#c4638e')), (1, H('#ffc58a'))])
stars(cielo, 60, 1, 70)
cielo.circle(250, 40, 14, H('#fff2c8', 90))
cielo.circle(250, 40, 10, H('#fff6dc'))
save(cielo, 'fondo_bosque_cielo.png')

mont = Canvas(BW, BH)
for x in range(BW):
    top = 95 + periodic(x, [(14, 2, 0.3), (8, 5, 1.7), (3, 11, 0.5)])
    for y in range(int(top), BH):
        mont.set(x, y, H('#5b4a8a'))
    top2 = 120 + periodic(x, [(10, 3, 2.1), (5, 7, 0.2)])
    for y in range(int(top2), BH):
        mont.set(x, y, H('#43386e'))
# castillo lejano
cx = 70
mont.rect(cx, 70, cx + 26, 100, H('#3a2f60'))
for tx in (cx - 4, cx + 26):
    mont.rect(tx, 60, tx + 8, 100, H('#3a2f60'))
    mont.polygon([(tx - 1, 60), (tx + 4, 50), (tx + 9, 60)], H('#3a2f60'))
mont.rect(cx + 10, 55, cx + 16, 72, H('#3a2f60'))
mont.polygon([(cx + 9, 55), (cx + 13, 44), (cx + 17, 55)], H('#3a2f60'))
mont.rect(cx + 12, 62, cx + 14, 65, H('#ffd84a'))
save(mont, 'fondo_bosque_montanas.png')

arb = Canvas(BW, BH)
r = random.Random(3)
xs = list(range(0, BW, 22))
for i, x0 in enumerate(xs):
    x0 += r.randrange(-4, 5)
    h = r.randrange(55, 85)
    base = BH
    col = H('#1f3d3a') if i % 2 else H('#24494a')
    # pino con forma de flecha, se repite en los bordes para que el mosaico sea continuo
    for off in (-BW, 0, BW):
        X = x0 + off
        arb.rect(X - 1, base - 20, X + 2, base, H('#2a2030'))
        for lvl in range(4):
            yb = base - 14 - lvl * (h / 5)
            w = 14 - lvl * 3
            arb.polygon([(X - w, yb), (X, yb - h / 3.2), (X + w, yb)], col)
for _ in range(30):
    x, y = r.randrange(BW), r.randrange(60, 170)
    arb.blend(x, y, H('#fff6a8', 200))
save(arb, 'fondo_bosque_arboles.png')

# Cueva
cielo_c = gradient([(0, H('#0d0a1f')), (0.6, H('#22143d')), (1, H('#3a1f5a'))])
stars(cielo_c, 50, 5, 180, '#b06eff')
save(cielo_c, 'fondo_cueva_cielo.png')

roc = Canvas(BW, BH)
for x in range(BW):
    hang = 30 + periodic(x, [(10, 3, 0.4), (6, 8, 1.1), (4, 17, 2.0)])
    for y in range(0, int(hang)):
        roc.set(x, y, H('#2e2150'))
    floor = 130 + periodic(x, [(12, 2, 1.0), (5, 9, 0.3)])
    for y in range(int(floor), BH):
        roc.set(x, y, H('#2e2150'))
r = random.Random(11)
for i in range(14):
    x = r.randrange(BW)
    h = r.randrange(15, 40)
    for off in (-BW, 0, BW):
        roc.polygon([(x - 5 + off, 30), (x + off, 30 + h), (x + 5 + off, 30)], H('#2e2150'))
save(roc, 'fondo_cueva_rocas.png')

cri = Canvas(BW, BH)
r = random.Random(13)
for i in range(16):
    x = r.randrange(BW)
    base = BH - r.randrange(0, 20)
    for j in range(3):
        h = r.randrange(12, 34)
        dx = (j - 1) * 4
        c = r.choice(['#3fb6d6', '#8a4ed6', '#d64ea8'])
        for off in (-BW, 0, BW):
            X = x + dx + off
            cri.polygon([(X - 3, base), (X, base - h), (X + 3, base)], H(c, 200))
            cri.polygon([(X, base), (X, base - h), (X + 3, base)], H('#ffffff', 60))
save(cri, 'fondo_cueva_cristales.png')

# Menú (noche con castillo)
menu = gradient([(0, H('#0b0a24')), (0.7, H('#2b1f5a')), (1, H('#5a2f6e'))])
stars(menu, 140, 21, 130)
menu.circle(255, 38, 20, H('#fff2c8', 60))
menu.circle(255, 38, 15, H('#fff6dc'))
menu.circle(250, 34, 3, H('#e8dcb8'))
for x in range(BW):
    top = 140 + periodic(x, [(10, 1, 0.2), (5, 4, 1.4)])
    for y in range(int(top), BH):
        menu.set(x, y, H('#140f2e'))
cx = 40
menu.rect(cx, 92, cx + 60, 140, H('#140f2e'))
for tx in (cx - 8, cx + 24, cx + 60):
    menu.rect(tx, 74, tx + 12, 140, H('#140f2e'))
    menu.polygon([(tx - 2, 74), (tx + 6, 58), (tx + 14, 74)], H('#140f2e'))
for (wx, wy) in [(cx - 4, 84), (cx + 28, 82), (cx + 64, 86), (cx + 10, 104), (cx + 44, 104)]:
    menu.rect(wx, wy, wx + 3, wy + 5, H('#ffd84a'))
save(menu, 'fondo_menu.png')

# Cinemática (noche, sendero hacia el portal)
cine = gradient([(0, H('#0b0a24')), (0.6, H('#3a1f6e')), (1, H('#7a3f8e'))])
stars(cine, 120, 31, 110)
cine.circle(60, 36, 12, H('#fff6dc'))
for x in range(BW):
    top = 118 + periodic(x, [(8, 2, 0.6), (4, 6, 0.1)])
    for y in range(int(top), BH):
        cine.set(x, y, H('#2a2050'))
cine.rect(0, 150, BW, BH, H('#1b1530'))
cine.rect(0, 150, BW, 152, H('#3c9c3e'))
save(cine, 'fondo_cinematica.png')

# Final (amanecer)
fin = gradient([(0, H('#3a6ed6')), (0.5, H('#ffb36e')), (1, H('#fff2a8'))])
for i in range(12):
    ang = math.pi + i * math.pi / 11
    fin.polygon([(160, 120), (160 + math.cos(ang - 0.05) * 300, 120 + math.sin(ang - 0.05) * 300),
                 (160 + math.cos(ang + 0.05) * 300, 120 + math.sin(ang + 0.05) * 300)], H('#ffffff', 40))
fin.circle(160, 120, 30, H('#fff6c8'))
for x in range(BW):
    top = 125 + periodic(x, [(10, 1, 2.0), (6, 4, 0.7)])
    for y in range(int(top), BH):
        fin.set(x, y, H('#4a7a3a'))
    top2 = 150 + periodic(x, [(6, 3, 0.4)])
    for y in range(int(top2), BH):
        fin.set(x, y, H('#2f5a2a'))
save(fin, 'fondo_final.png')

go = gradient([(0, H('#000000')), (1, H('#3a0c1e'))])
stars(go, 40, 41, 180, '#ff6a6a')
save(go, 'fondo_gameover.png')

print('Imágenes generadas en', os.path.abspath(OUT))
