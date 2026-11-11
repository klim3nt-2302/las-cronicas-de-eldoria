"""Utilidades mínimas para dibujar pixel art y guardar PNG sin dependencias externas."""
import math
import struct
import zlib


def hex2rgba(h, a=255):
    h = h.lstrip('#')
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


class Canvas:
    def __init__(self, w, h, fill=(0, 0, 0, 0)):
        self.w, self.h = w, h
        self.px = [list(fill) for _ in range(w * h)]

    def get(self, x, y):
        return self.px[y * self.w + x]

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[y * self.w + x] = list(c)

    def blend(self, x, y, c):
        """Mezcla alfa de un color sobre el píxel existente."""
        x, y = int(x), int(y)
        if not (0 <= x < self.w and 0 <= y < self.h):
            return
        dst = self.px[y * self.w + x]
        sa = c[3] / 255.0
        da = dst[3] / 255.0
        oa = sa + da * (1 - sa)
        if oa <= 0:
            self.px[y * self.w + x] = [0, 0, 0, 0]
            return
        out = [int((c[i] * sa + dst[i] * da * (1 - sa)) / oa) for i in range(3)]
        self.px[y * self.w + x] = out + [int(oa * 255)]

    def rect(self, x0, y0, x1, y1, c):
        for y in range(max(0, int(y0)), min(self.h, int(y1))):
            for x in range(max(0, int(x0)), min(self.w, int(x1))):
                self.blend(x, y, c)

    def circle(self, cx, cy, r, c):
        for y in range(int(cy - r - 1), int(cy + r + 2)):
            for x in range(int(cx - r - 1), int(cx + r + 2)):
                if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
                    self.blend(x, y, c)

    def polygon(self, pts, c):
        ys = [p[1] for p in pts]
        for y in range(max(0, int(min(ys))), min(self.h, int(max(ys)) + 1)):
            yc = y + 0.5
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= yc < y1) or (y1 <= yc < y0):
                    xs.append(x0 + (yc - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for i in range(0, len(xs) - 1, 2):
                for x in range(int(math.ceil(xs[i] - 0.5)), int(math.floor(xs[i + 1] - 0.5)) + 1):
                    self.blend(x, y, c)

    def paste(self, other, ox, oy):
        for y in range(other.h):
            for x in range(other.w):
                c = other.get(x, y)
                if c[3]:
                    self.blend(ox + x, oy + y, c)

    def scaled(self, s):
        out = Canvas(self.w * s, self.h * s)
        for y in range(self.h):
            for x in range(self.w):
                c = self.get(x, y)
                for dy in range(s):
                    row = (y * s + dy) * out.w
                    for dx in range(s):
                        out.px[row + x * s + dx] = list(c)
        return out

    def flipped(self):
        out = Canvas(self.w, self.h)
        for y in range(self.h):
            for x in range(self.w):
                out.set(self.w - 1 - x, y, self.get(x, y))
        return out

    def save(self, path):
        raw = bytearray()
        for y in range(self.h):
            raw.append(0)
            for x in range(self.w):
                raw.extend(bytes(self.px[y * self.w + x]))

        def chunk(tag, data):
            c = struct.pack('>I', len(data)) + tag + data
            return c + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)

        png = b'\x89PNG\r\n\x1a\n'
        png += chunk(b'IHDR', struct.pack('>IIBBBBB', self.w, self.h, 8, 6, 0, 0, 0))
        png += chunk(b'IDAT', zlib.compress(bytes(raw), 9))
        png += chunk(b'IEND', b'')
        with open(path, 'wb') as f:
            f.write(png)


def from_ascii(rows, palette, width=None):
    """Convierte un dibujo ASCII en Canvas. '.' es transparente."""
    w = width or max(len(r) for r in rows)
    cv = Canvas(w, len(rows))
    for y, row in enumerate(rows):
        if len(row) > w:
            raise ValueError('fila demasiado larga (%d>%d): %r' % (len(row), w, row))
        for x, ch in enumerate(row):
            if ch in ('.', ' '):
                continue
            cv.set(x, y, palette[ch])
    return cv
