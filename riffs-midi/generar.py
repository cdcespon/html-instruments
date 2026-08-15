#!/usr/bin/env python3
"""
Generador de patrones de teclado en MIDI para practicar.

No son riffs de temas: son las celdas idiomáticas de cada género, que es lo que
sirve para practicar. Un montuno real varía compás a compás; acá está la celda
básica repetida, que es por donde se empieza.

Uso:
    python3 generar.py                         # genera los seis en Do, tempo por defecto
    python3 generar.py --estilo montuno --tono F --tempo 150
    python3 generar.py --listar

Pista 1 = mano izquierda, pista 2 = mano derecha, en canales separados para que
puedas silenciar una y tocar la otra.
"""
import struct, argparse, os

PPQ = 480                      # pulsos por negra
CH_IZQ, CH_DER = 0, 1

NOTAS = {"C":0,"C#":1,"Db":1,"D":2,"D#":3,"Eb":3,"E":4,"F":5,"F#":6,"Gb":6,
         "G":7,"G#":8,"Ab":8,"A":9,"A#":10,"Bb":10,"B":11}

# ── Escritura de MIDI estándar (SMF formato 1) ──────────────────────

def vlq(n):
    """Cantidad de longitud variable, como la define el formato MIDI."""
    out = bytearray([n & 0x7F])
    n >>= 7
    while n:
        out.insert(0, (n & 0x7F) | 0x80)
        n >>= 7
    return bytes(out)

def meta(tipo, datos):
    return b"\xFF" + bytes([tipo]) + vlq(len(datos)) + datos

def pista(eventos, nombre):
    """eventos: lista de (tick_absoluto, orden, bytes). Devuelve un chunk MTrk."""
    cuerpo = bytearray(vlq(0) + meta(0x03, nombre.encode("utf-8")))
    prev = 0
    for tick, _, datos in sorted(eventos, key=lambda e: (e[0], e[1])):
        cuerpo += vlq(tick - prev) + datos
        prev = tick
    cuerpo += vlq(0) + meta(0x2F, b"")
    return b"MTrk" + struct.pack(">I", len(cuerpo)) + bytes(cuerpo)

def escribir(ruta, tempo, compas, pistas):
    cab = b"MThd" + struct.pack(">IHHH", 6, 1, len(pistas) + 1, PPQ)
    num, den = compas
    dd = {1:0, 2:1, 4:2, 8:3, 16:4}[den]
    upq = int(60_000_000 / tempo)
    conductor = [
        (0, 0, meta(0x58, bytes([num, dd, 24, 8]))),
        (0, 1, meta(0x51, struct.pack(">I", upq)[1:])),
    ]
    datos = cab + pista(conductor, "tempo")
    for evs, nombre in pistas:
        datos += pista(evs, nombre)
    with open(ruta, "wb") as f:
        f.write(datos)
    return len(datos)

def notas_a_eventos(notas, canal):
    """notas: (inicio_en_negras, duracion_en_negras, altura, velocity)."""
    evs = []
    for ini, dur, alt, vel in notas:
        t0 = int(round(ini * PPQ))
        t1 = int(round((ini + dur) * PPQ))
        if t1 <= t0:
            t1 = t0 + 1
        evs.append((t0, 1, bytes([0x90 | canal, alt, vel])))
        evs.append((t1, 0, bytes([0x80 | canal, alt, 0])))
    return evs

def swing(pos, factor):
    """Corre las corcheas débiles. factor 0.5 = recto, 0.66 ≈ tresillo."""
    if factor == 0.5:
        return pos
    entero = int(pos)
    resto = pos - entero
    if abs(resto - 0.5) < 1e-9:
        return entero + factor
    return pos

# ── Acordes ─────────────────────────────────────────────────────────

TIPOS = {"maj":[0,4,7], "min":[0,3,7], "7":[0,4,7,10],
         "maj7":[0,4,7,11], "min7":[0,3,7,10]}

def tonos(raiz, tipo):
    return [raiz + i for i in TIPOS[tipo]]

# ── Patrones ────────────────────────────────────────────────────────
# Cada patrón devuelve (notas_izq, notas_der, compases, compas, swing, notas_al_pie)
# Los grados están en semitonos sobre la tónica elegida.

def blues_shuffle(ton):
    """12 compases. Izquierda: boogie 1-5-6-♭7. Derecha: shell en 2 y 4."""
    prog = [0,0,0,0, 5,5,0,0, 7,5,0,7]           # I I I I IV IV I I V IV I V
    izq, der = [], []
    boogie = [0,7,9,10,12,10,9,7]                 # las ocho corcheas del compás
    for c, g in enumerate(prog):
        base = ton + 36 + g
        for i, iv in enumerate(boogie):
            p = swing(c*4 + i*0.5, 0.66)
            izq.append((p, 0.45, base + iv, 84 if i % 2 == 0 else 68))
        # shell voicing: 3ª y ♭7, los dos grados que definen el dominante
        for beat in (1, 3):
            p = swing(c*4 + beat, 0.66)
            for iv in (4, 10):
                der.append((p, 0.7, ton + 60 + g + iv, 78))
    return izq, der, 12, (4,4), 0.66, \
        "Shuffle. La izquierda es el boogie clásico 1-5-6-♭7; la derecha marca sólo 3ª y ♭7."

def blues_lento(ton):
    """12 compases en tresillos. Derecha: acorde en cada tresillo del pulso."""
    prog = [0,0,0,0, 5,5,0,0, 7,5,0,7]
    izq, der = [], []
    for c, g in enumerate(prog):
        base = ton + 36 + g
        for beat in range(4):
            izq.append((c*4 + beat, 0.9, base, 80))
            izq.append((c*4 + beat + 0.66, 0.3, base + 7, 62))
            for k, iv in enumerate(tonos(ton + 60 + g, "7")[1:]):
                der.append((c*4 + beat + k*0.333, 0.3, iv, 74 - k*6))
    return izq, der, 12, (4,4), 0.5, \
        "Blues lento en tresillos. Tocalo primero a 50 y subí de a diez."

def rock_octavas(ton):
    """8 compases. Izquierda en octavas, derecha con quintas: I-♭VII-IV-I."""
    prog = [0,10,5,0, 0,10,5,0]
    izq, der = [], []
    for c, g in enumerate(prog):
        base = ton + 36 + g
        for i in range(8):
            p = c*4 + i*0.5
            vel = 92 if i % 2 == 0 else 74
            izq.append((p, 0.42, base, vel))
            izq.append((p, 0.42, base + 12, vel - 8))
        for beat in (0, 1.5, 2.5):
            for iv in (0, 7, 12):
                der.append((c*4 + beat, 0.8, ton + 60 + g + iv, 88))
    return izq, der, 8, (4,4), 0.5, \
        "Mixolidio: I-♭VII-IV. La derecha va en quintas, sin tercera."

def rock_organo(ton):
    """8 compases. Comping de órgano en semicorcheas sobre pedal de izquierda."""
    prog = [0,0,5,5, 7,7,0,0]
    rej = [0, 0.75, 1.5, 1.75, 2.5, 3, 3.75]      # semicorcheas sincopadas
    izq, der = [], []
    for c, g in enumerate(prog):
        izq.append((c*4, 4.0, ton + 36 + g, 78))
        for p in rej:
            for iv in tonos(0, "maj"):
                der.append((c*4 + p, 0.22, ton + 60 + g + iv, 80))
    return izq, der, 8, (4,4), 0.5, \
        "La izquierda sostiene el pedal y la derecha pica. El silencio entre golpes es el patrón."

def montuno(ton):
    """8 compases. Guajeo de corcheas continuas sobre ii-V-I-I."""
    prog = [(2,"min7"), (7,"7"), (0,"maj7"), (0,"maj7"),
            (2,"min7"), (7,"7"), (0,"maj7"), (0,"maj7")]
    # celda de dos compases: los índices apuntan a los tonos del acorde
    celda = [2,0,1,2, 0,1,2,0,  1,2,0,1, 2,0,1,2]
    izq, der = [], []
    for c, (g, tipo) in enumerate(prog):
        t = tonos(ton + 60 + g, tipo)[:3]
        izq.append((c*4, 1.0, ton + 36 + g, 82))
        izq.append((c*4 + 2.5, 1.0, ton + 36 + g + 7, 74))
        for i in range(8):
            idx = celda[(c % 2)*8 + i]
            alt = t[idx] + (12 if i >= 4 else 0)
            der.append((c*4 + i*0.5, 0.45, alt, 86 if i % 2 == 0 else 70))
    return izq, der, 8, (4,4), 0.5, \
        "Celda básica de guajeo, repetida. Un montuno real varía compás a compás — esto es el punto de partida."

def bossa(ton):
    """8 compases. Comping sincopado de dos compases sobre Imaj7-vi7-ii7-V7."""
    prog = [(0,"maj7"), (9,"min7"), (2,"min7"), (7,"7"),
            (0,"maj7"), (9,"min7"), (2,"min7"), (7,"7")]
    par, impar = [0, 1.5, 3], [0.5, 2, 3.5]
    izq, der = [], []
    for c, (g, tipo) in enumerate(prog):
        izq.append((c*4, 1.2, ton + 36 + g, 76))
        izq.append((c*4 + 2.5, 1.2, ton + 36 + g + 7, 68))
        for p in (par if c % 2 == 0 else impar):
            for iv in tonos(0, tipo)[1:]:            # sin fundamental: la tiene la izquierda
                der.append((c*4 + p, 0.55, ton + 60 + g + iv, 72))
    return izq, der, 8, (4,4), 0.5, \
        "Patrón de dos compases: los golpes se corren en el segundo. Sin fundamental en la derecha."

def chacarera(ton):
    """8 compases en 6/8. Bajo en 1 y 4, acordes en la hemiola."""
    prog = [0,0,10,7, 0,0,10,7]                   # i - i - VII - V
    izq, der = [], []
    for c, g in enumerate(prog):
        tipo = "min" if g in (0,) else "maj"
        base = ton + 36 + g
        izq.append((c*3, 0.9, base, 84))
        izq.append((c*3 + 1.5, 0.9, base + 7, 74))
        for p in (0.5, 1.0, 2.0, 2.5):            # el 3 contra 2 característico
            for iv in tonos(0, tipo):
                der.append((c*3 + p, 0.4, ton + 60 + g + iv, 76))
    return izq, der, 8, (6,8), 0.5, \
        "6/8 con la hemiola de tres contra dos. La izquierda va en 1 y 4, la derecha cruza."

PATRONES = {
    "blues-shuffle": (blues_shuffle, 100, "Blues shuffle, 12 compases"),
    "blues-lento":   (blues_lento,    60, "Blues lento en tresillos, 12 compases"),
    "rock-octavas":  (rock_octavas,  132, "Rock en octavas, mixolidio"),
    "rock-organo":   (rock_organo,   116, "Comping de órgano en semicorcheas"),
    "montuno":       (montuno,       160, "Guajeo de salsa, celda básica"),
    "bossa":         (bossa,          132, "Bossa, comping de dos compases"),
    "chacarera":     (chacarera,     100, "Chacarera en 6/8, hemiola"),
}

def generar(estilo, tono, tempo, repeticiones, destino):
    fn, tempo_def, desc = PATRONES[estilo]
    ton = NOTAS[tono]
    izq, der, comps, compas, sw, pie = fn(ton)
    negras = comps * compas[0] * (4 / compas[1])
    ai, ad = [], []
    for r in range(repeticiones):
        off = r * negras
        ai += [(i + off, d, a, v) for i, d, a, v in izq]
        ad += [(i + off, d, a, v) for i, d, a, v in der]
    ruta = os.path.join(destino, f"{estilo}-{tono.replace('#','s')}-{tempo}bpm.mid")
    escribir(ruta, tempo, compas,
             [(notas_a_eventos(ai, CH_IZQ), "mano izquierda"),
              (notas_a_eventos(ad, CH_DER), "mano derecha")])
    return ruta, len(ai) + len(ad), comps * repeticiones, pie

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--estilo", default="todos", choices=["todos"] + list(PATRONES))
    ap.add_argument("--tono", default="C", choices=list(NOTAS))
    ap.add_argument("--tempo", type=int, default=0, help="por defecto, el propio del estilo")
    ap.add_argument("--repeticiones", type=int, default=4)
    ap.add_argument("--destino", default=".")
    ap.add_argument("--listar", action="store_true")
    a = ap.parse_args()

    if a.listar:
        for k, (_, t, d) in PATRONES.items():
            print(f"  {k:15} {t:3} bpm   {d}")
        raise SystemExit

    os.makedirs(a.destino, exist_ok=True)
    estilos = list(PATRONES) if a.estilo == "todos" else [a.estilo]
    for e in estilos:
        tempo = a.tempo or PATRONES[e][1]
        ruta, n, comps, pie = generar(e, a.tono, tempo, a.repeticiones, a.destino)
        print(f"{os.path.basename(ruta):42} {n:4} notas  {comps:3} compases")
        print(f"  {pie}")
