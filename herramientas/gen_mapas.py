"""Dibuja un mapa completo de cada nivel (a 1/4 de escala) leyendo game.json.

Uso:  python3 herramientas/gen_mapas.py   (desde la carpeta Eldoria)
"""
import json
import os
import struct
import zlib

from pixel import Canvas

ROOT = os.path.join(os.path.dirname(__file__), '..')
K = 4  # factor de reducción


def load(path):
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


def shrink(cv, w, h):
    out = Canvas(max(1, w), max(1, h))
    for y in range(out.h):
        for x in range(out.w):
            out.px[y * out.w + x] = list(cv.get(min(cv.w - 1, x * cv.w // out.w), min(cv.h - 1, y * cv.h // out.h)))
    return out


def tile(tex, w, h):
    out = Canvas(w, h)
    for y in range(h):
        for x in range(w):
            out.px[y * w + x] = list(tex.get(x % tex.w, y % tex.h))
    return out


d = json.load(open(os.path.join(ROOT, 'game.json'), encoding='utf-8'))
objs = {o['name']: o for o in d['objects']}
os.makedirs(os.path.join(ROOT, 'docs'), exist_ok=True)
for L in d['layouts']:
    if not L['name'].startswith('Nivel'):
        continue
    lo = dict(objs, **{o['name']: o for o in L['objects']})
    mapa = Canvas(4800 // K, 540 // K)
    fondo = [i for i in L['instances'] if i['layer'] == 'Fondo']
    for scr in range(5):
        for i in sorted(fondo, key=lambda i: i['zOrder']):
            o = lo[i['name']]
            img = load(o.get('texture') or o['animations'][0]['directions'][0]['sprites'][0]['image'])
            mapa.paste(shrink(img, 960 // K, 540 // K), scr * 960 // K, 0)
    for i in sorted([i for i in L['instances'] if i['layer'] == ''], key=lambda i: i['zOrder']):
        o = lo[i['name']]
        if i['x'] < 0:
            continue
        img = load(o.get('texture') or o['animations'][0]['directions'][0]['sprites'][0]['image'])
        if o['type'] == 'TiledSpriteObject::TiledSprite':
            full = tile(img, int(i['width']), int(i['height']))
        elif i['customSize']:
            full = shrink(img, int(i['width']), int(i['height']))
        else:
            full = img
        mapa.paste(shrink(full, full.w // K, full.h // K), int(i['x']) // K, int(i['y']) // K)
    for scr in range(1, 5):  # separadores de pantalla
        for y in range(0, mapa.h, 4):
            mapa.blend(scr * 960 // K, y, (255, 255, 255, 140))
    mapa.scaled(1).save(os.path.join(ROOT, 'docs', 'mapa_%s.png' % L['name'].lower()))
    print('docs/mapa_%s.png' % L['name'].lower())
