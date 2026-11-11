"""Sintetiza efectos de sonido, ambientes y música (estilo chiptune) en WAV 16-bit mono.

Uso:  python3 herramientas/gen_audio.py   (desde la carpeta Eldoria)
"""
import math
import os
import random
import struct
import wave

SR = 22050
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'audio')
os.makedirs(OUT, exist_ok=True)
rnd = random.Random(42)


def buf(seconds):
    return [0.0] * int(seconds * SR)


def save(samples, name, gain=0.9):
    peak = max(1e-6, max(abs(s) for s in samples))
    k = gain / peak
    with wave.open(os.path.join(OUT, name), 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b''.join(struct.pack('<h', int(max(-1, min(1, s * k)) * 32767)) for s in samples))


def osc(kind, phase, duty=0.5):
    p = phase % 1.0
    if kind == 'sq':
        return 1.0 if p < duty else -1.0
    if kind == 'tri':
        return 4 * p - 1 if p < 0.5 else 3 - 4 * p
    if kind == 'saw':
        return 2 * p - 1
    if kind == 'sin':
        return math.sin(2 * math.pi * p)
    return rnd.uniform(-1, 1)


def tone(out, start, dur, f0, f1=None, kind='sq', vol=0.3, attack=0.005, release=0.05,
         duty=0.5, vibrato=0.0):
    """Añade una nota (con barrido opcional de frecuencia f0→f1) al buffer."""
    f1 = f0 if f1 is None else f1
    n = int(dur * SR)
    i0 = int(start * SR)
    phase = 0.0
    for i in range(n):
        if i0 + i >= len(out):
            break
        t = i / SR
        k = i / max(1, n - 1)
        f = f0 * (f1 / f0) ** k if f0 > 0 and f1 > 0 else f0 + (f1 - f0) * k
        if vibrato:
            f *= 1 + vibrato * math.sin(2 * math.pi * 5.5 * t)
        phase += f / SR
        env = min(1.0, t / attack) if attack > 0 else 1.0
        rem = dur - t
        if rem < release:
            env *= max(0.0, rem / release)
        out[i0 + i] += osc(kind, phase, duty) * vol * env


def noise(out, start, dur, vol=0.3, decay=10.0, lp=0.5):
    """Ruido filtrado con caída exponencial (pasos, golpes, viento)."""
    i0 = int(start * SR)
    prev = 0.0
    for i in range(int(dur * SR)):
        if i0 + i >= len(out):
            break
        t = i / SR
        prev = prev + lp * (rnd.uniform(-1, 1) - prev)
        out[i0 + i] += prev * vol * math.exp(-decay * t)


NOTES = {'C': -9, 'C#': -8, 'D': -7, 'D#': -6, 'E': -5, 'F': -4, 'F#': -3, 'G': -2, 'G#': -1,
         'A': 0, 'A#': 1, 'B': 2}


def hz(n):
    name, octv = n[:-1], int(n[-1])
    return 440.0 * 2 ** ((NOTES[name] + (octv - 4) * 12) / 12)


# ------------------------------------------------------------------ Efectos
b = buf(0.12); noise(b, 0, 0.12, 0.8, 35, 0.25); tone(b, 0, 0.05, 90, 60, 'tri', 0.5); save(b, 'paso.wav', 0.7)
b = buf(0.25); tone(b, 0, 0.22, 300, 750, 'sq', 0.35, duty=0.25); save(b, 'salto.wav', 0.6)
b = buf(0.3); tone(b, 0, 0.08, hz('B5'), kind='sq', vol=0.3, duty=0.25); tone(b, 0.07, 0.2, hz('E6'), kind='sq', vol=0.3, duty=0.25); save(b, 'gema.wav', 0.6)
b = buf(0.35); tone(b, 0, 0.3, 420, 90, 'saw', 0.4); noise(b, 0, 0.3, 0.4, 12); save(b, 'golpe.wav', 0.8)
b = buf(0.25); tone(b, 0, 0.12, 200, 60, 'sq', 0.4); noise(b, 0, 0.2, 0.5, 18, 0.4); tone(b, 0.08, 0.15, 500, 900, 'sq', 0.2, duty=0.25); save(b, 'aplastar.wav', 0.8)
b = buf(0.9); noise(b, 0, 0.25, 0.4, 10, 0.15); tone(b, 0, 0.2, 120, 80, 'tri', 0.4)
for i, n in enumerate(['C5', 'E5', 'G5', 'C6']):
    tone(b, 0.2 + i * 0.1, 0.4, hz(n), kind='tri', vol=0.3)
save(b, 'cofre.wav', 0.8)
b = buf(0.6)
for i, n in enumerate(['G5', 'B5', 'D6', 'G6']):
    tone(b, i * 0.07, 0.3, hz(n), kind='sq', vol=0.2, duty=0.125)
save(b, 'llave.wav', 0.7)
b = buf(0.3); noise(b, 0, 0.08, 0.6, 30, 0.6); tone(b, 0.05, 0.15, 900, 500, 'sq', 0.2, duty=0.25); noise(b, 0.12, 0.1, 0.5, 40, 0.6); save(b, 'palanca.wav', 0.7)
b = buf(1.6); noise(b, 0, 1.5, 0.7, 1.6, 0.05); tone(b, 0, 1.5, 70, 45, 'saw', 0.3); save(b, 'puerta.wav', 0.8)
b = buf(1.4); tone(b, 0, 1.3, 200, 1200, 'sin', 0.4, attack=0.3, release=0.4, vibrato=0.03); noise(b, 0, 1.3, 0.3, 1.5, 0.3)
for i in range(8):
    tone(b, 0.1 + i * 0.12, 0.15, hz('C6') * (1 + i * 0.12), kind='tri', vol=0.12)
save(b, 'portal.wav', 0.8)
b = buf(0.06); tone(b, 0, 0.05, 880, kind='sq', vol=0.25, duty=0.25, release=0.02); save(b, 'dialogo.wav', 0.4)
b = buf(0.5); tone(b, 0, 0.45, 160, 640, 'tri', 0.5, vibrato=0.08); tone(b, 0, 0.45, 80, 320, 'sq', 0.15, duty=0.25); save(b, 'hongo.wav', 0.8)
b = buf(1.2)
for i, n in enumerate(['C5', 'E5', 'G5', 'C6', 'E6', 'G6', 'C7']):
    tone(b, i * 0.08, 0.5, hz(n), kind='sin', vol=0.25, release=0.3)
save(b, 'curar.wav', 0.7)
b = buf(1.0)
for i, n in enumerate(['E5', 'A5', 'C#6']):
    tone(b, i * 0.12, 0.7, hz(n), kind='tri', vol=0.3, release=0.4)
save(b, 'checkpoint.wav', 0.7)
b = buf(0.45); tone(b, 0, 0.4, 2400, 1500, 'sq', 0.2, duty=0.125, vibrato=0.06); tone(b, 0.05, 0.35, 2900, 1900, 'sq', 0.12, duty=0.125); save(b, 'murcielago.wav', 0.5)
b = buf(0.45); tone(b, 0, 0.4, 140, 95, 'saw', 0.5, vibrato=0.1); noise(b, 0, 0.35, 0.2, 6, 0.2); save(b, 'goblin.wav', 0.7)
b = buf(0.15); tone(b, 0, 0.12, 660, 990, 'sq', 0.25, duty=0.25); save(b, 'seleccionar.wav', 0.5)
b = buf(0.25); tone(b, 0, 0.1, hz('A5'), kind='tri', vol=0.3); tone(b, 0.1, 0.12, hz('E6'), kind='tri', vol=0.3); save(b, 'cartel.wav', 0.5)

# ------------------------------------------------------------------ Ambientes (bucles)
# Bosque: viento suave + pájaros
b = buf(12.0)
prev = 0.0
for i in range(len(b)):
    t = i / SR
    prev += 0.02 * (rnd.uniform(-1, 1) - prev)
    b[i] += prev * (0.6 + 0.4 * math.sin(2 * math.pi * t / 6.0)) * 1.4
r = random.Random(5)
for _ in range(14):
    st = r.uniform(0.2, 11.0)
    base = r.uniform(2200, 3400)
    for j in range(r.randint(2, 4)):
        tone(b, st + j * 0.11, 0.08, base, base * 1.35, 'sin', 0.18, attack=0.01, release=0.03)
save(b, 'ambiente_bosque.wav', 0.5)

# Cueva: zumbido grave + gotas con eco
b = buf(12.0)
for i in range(len(b)):
    t = i / SR
    b[i] += 0.12 * math.sin(2 * math.pi * 55 * t) * (0.7 + 0.3 * math.sin(2 * math.pi * t / 4))
    b[i] += 0.06 * math.sin(2 * math.pi * 82.5 * t)
r = random.Random(9)
for _ in range(10):
    st = r.uniform(0.2, 11.0)
    f = r.uniform(900, 1500)
    for echo, v in ((0, 0.35), (0.18, 0.15), (0.36, 0.06)):
        tone(b, st + echo, 0.12, f * 1.6, f, 'sin', v, attack=0.002, release=0.1)
save(b, 'ambiente_cueva.wav', 0.5)


# ------------------------------------------------------------------ Música
def render_song(bpm, bars, melody, chords, lead='sq', lead_duty=0.25, bass='tri',
                arp=True, drums=True, pad=False, lead_vol=0.22, tail=0.0):
    beat = 60.0 / bpm
    total = bars * 4 * beat
    out = buf(total + tail)
    # melodía: lista de (nota|None, duración en tiempos)
    t = 0.0
    for n, d in melody:
        if n:
            tone(out, t, d * beat * 0.95, hz(n), kind=lead, vol=lead_vol, duty=lead_duty,
                 release=min(0.12, d * beat * 0.4), vibrato=0.004)
        t += d * beat
    for bi, ch in enumerate(chords):
        t0 = bi * 4 * beat
        root = ch[0]
        # bajo
        for q in range(4):
            note = root if q % 2 == 0 else ch[2]
            tone(out, t0 + q * beat, beat * 0.9, hz(note) / 4, kind=bass, vol=0.28, release=0.05)
        if arp:
            for s in range(16):
                n = ch[s % len(ch)]
                tone(out, t0 + s * beat / 4, beat / 4 * 0.8, hz(n), kind='sq', vol=0.05, duty=0.125,
                     release=0.03)
        if pad:
            for n in ch:
                tone(out, t0, 4 * beat, hz(n) / 2, kind='saw', vol=0.035, attack=0.4, release=0.6)
        if drums:
            for q in range(4):
                if q in (0, 2):
                    tone(out, t0 + q * beat, 0.12, 150, 50, 'sin', 0.45, release=0.08)
                else:
                    noise(out, t0 + q * beat, 0.15, 0.25, 25, 0.7)
                noise(out, t0 + q * beat + beat / 2, 0.05, 0.08, 60, 0.9)
    return out


def phrase(spec):
    """'E5:1 G5:1 -:0.5' → lista de (nota, tiempos)."""
    res = []
    for tok in spec.split():
        n, d = tok.split(':')
        res.append((None if n == '-' else n, float(d)))
    return res


C, Am, F, G = ['C4', 'E4', 'G4'], ['A3', 'C4', 'E4'], ['F3', 'A3', 'C4'], ['G3', 'B3', 'D4']
bosque_mel = phrase(
    'E5:1 G5:1 A5:0.5 G5:0.5 E5:1  C5:1 E5:1 D5:0.5 C5:0.5 A4:1  F4:0.5 A4:0.5 C5:1 F5:1 E5:1  D5:1 B4:1 G4:1 D5:1 '
    'G5:1 E5:0.5 G5:0.5 C6:1 B5:1  A5:1 E5:1 C5:1 E5:1  F5:1 E5:0.5 D5:0.5 C5:1 A4:1  B4:1 D5:1 G5:2 '
    'E5:1 G5:1 A5:0.5 G5:0.5 E5:1  C5:1 E5:1 D5:0.5 C5:0.5 A4:1  F4:0.5 A4:0.5 C5:1 F5:1 A5:1  G5:1 F5:1 D5:1 B4:1')
save(render_song(120, 12, bosque_mel, [C, Am, F, G] * 3), 'musica_bosque.wav', 0.8)

Am2, F2, Dm2, E2 = ['A3', 'C4', 'E4'], ['F3', 'A3', 'C4'], ['D3', 'F3', 'A3'], ['E3', 'G#3', 'B3']
cueva_mel = phrase(
    'A4:2 C5:1 B4:1  A4:1 F4:1 E4:2  D4:1 F4:1 A4:1 D5:1  C5:1 B4:1 G#4:2 '
    'E5:2 D5:1 C5:1  C5:1 A4:1 F4:2  F4:1 A4:1 D5:1 F5:1  E5:2 B4:1 G#4:1')
save(render_song(90, 8, cueva_mel, [Am2, F2, Dm2, E2] * 2, lead='tri', lead_vol=0.3, drums=True,
                 pad=True), 'musica_cueva.wav', 0.8)

Dm, Bb, Fm, Cm = ['D4', 'F4', 'A4'], ['A#3', 'D4', 'F4'], ['F3', 'A3', 'C4'], ['C4', 'E4', 'G4']
menu_mel = phrase(
    'A4:2 D5:1 E5:1  F5:2 E5:1 D5:1  C5:2 A4:1 C5:1  E5:3 -:1 '
    'A4:2 D5:1 E5:1  F5:1 G5:1 A5:2  G5:1 F5:1 E5:1 C5:1  D5:4')
save(render_song(80, 8, menu_mel, [Dm, Bb, Fm, Cm] * 2, lead='tri', lead_vol=0.3, drums=False,
                 pad=True), 'musica_menu.wav', 0.8)

cine_mel = phrase('E5:4  F5:2 A5:2  G5:3 E5:1  A5:4')
save(render_song(70, 4, cine_mel, [Am, F, C, G], lead='saw', lead_vol=0.12, drums=False, arp=True,
                 pad=True, tail=1.5), 'musica_cinematica.wav', 0.8)

fin_mel = phrase('C5:0.5 C5:0.5 C5:0.5 C5:0.5 G5:2  E5:1 G5:1 C6:2  A5:1 F5:1 C6:1 A5:1  G5:1 E5:1 C6:2')
save(render_song(110, 4, fin_mel, [C, C, F, C], lead_vol=0.25, drums=True, tail=1.0), 'musica_final.wav', 0.8)

b = buf(3.0)
for i, n in enumerate(['E4', 'D#4', 'D4', 'C#4']):
    tone(b, i * 0.45, 0.6 if i < 3 else 1.5, hz(n), kind='tri', vol=0.35, release=0.3, vibrato=0.01)
save(b, 'musica_gameover.wav', 0.8)

print('Audio generado en', os.path.abspath(OUT))
