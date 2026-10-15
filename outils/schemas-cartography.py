#!/usr/bin/env python3
"""Générateur des schémas du cours « Cartography : Basics », en français et en anglais.

    python3 outils/schemas-cartography.py cours/cartography-basics

Lit donnees/territoire.json (outils/territoire-fictif.py) et écrit images/schemas/ (fr)
et images/schemas/en/ (en). Les valeurs citées dans le cours sont calculées ici.
"""
import json
import math
import os
import sys

COURS = sys.argv[1]
OUT = os.path.join(COURS, 'images', 'schemas')
os.makedirs(os.path.join(OUT, 'en'), exist_ok=True)
TERR = json.load(open(os.path.join(COURS, 'donnees', 'territoire.json'), encoding='utf-8'))
COMMUNES = TERR['communes']


def svg(vb, aria, corps, extra=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{aria}"{extra}>\n'
            + '\n'.join(corps) + '\n</svg>\n')


def ecrire(nom, fr, en):
    open(os.path.join(OUT, nom), 'w', encoding='utf-8').write(fr)
    open(os.path.join(OUT, 'en', nom), 'w', encoding='utf-8').write(en)


def T(x, y, s, cls=None, anchor='middle', style=''):
    c = f' class="{cls}"' if cls else ''
    st = f' style="{style}"' if style else ''
    return f'<text{c} x="{x}" y="{y}" text-anchor="{anchor}"{st}>{s}</text>'


def hexrvb(h):
    return [int(h[i:i + 2], 16) for i in (1, 3, 5)]


def rvbhex(c):
    return '#' + ''.join(f'{max(0, min(255, round(v))):02x}' for v in c)


def gamme(ancres, n):
    a = [hexrvb(h) for h in ancres]
    out = []
    for i in range(n):
        t = 0.5 if n == 1 else i / (n - 1)
        p = t * (len(a) - 1)
        k = min(int(p), len(a) - 2)
        f = p - k
        out.append(rvbhex([a[k][j] + (a[k + 1][j] - a[k][j]) * f for j in range(3)]))
    return out


SEQ = ['#FFF4E6', '#F7C08A', '#E38226', '#B5600E', '#5C2C06']
ARC = ['#5E3C99', '#2C7BB6', '#00A884', '#A6D96A', '#FFD92F', '#F46D43', '#D7191C']
RVERT = ['#1A9850', '#91CF60', '#FFFFBF', '#FC8D59', '#D73027']


def quantiles(valeurs, n):
    v = sorted(valeurs)
    N = len(v)
    return [v[0]] + [v[min(N - 1, round(k * N / n) - 1)] for k in range(1, n)] + [v[-1]]


def classe(x, b):
    for k in range(1, len(b) - 1):
        if x <= b[k]:
            return k - 1
    return len(b) - 2


def fr_num(x, d=1):
    s = f'{x:.{d}f}'
    return s.replace('.', ',')


# ------------------------------------------------------------------ carte choroplèthe
def choroplethe(couleurs_par_commune, titre, legende, largeur=None):
    """Une carte du territoire, chaque commune coloriée ; legende = [(couleur, texte)], du haut vers le bas."""
    o = ['<rect width="1000" height="560" fill="#FFFFFF"/>']
    for c, col in zip(COMMUNES, couleurs_par_commune):
        o.append(f'<path d="{c["chemin"]}" fill="{col}" stroke="#FFFFFF" stroke-width="0.9"/>')
    o.append(f'<path d="{TERR["contour"]}" fill="none" stroke="#283B89" stroke-width="2"/>')
    y = 120
    o.append(f'<text x="815" y="{y - 30}" font-family="Raleway, Arial, sans-serif" font-weight="700" font-size="20" fill="#283B89">{titre}</text>')
    for col, txt in legende:
        o.append(f'<rect x="815" y="{y}" width="34" height="22" fill="{col}" stroke="#9A9AA4" stroke-width="1"/>')
        o.append(f'<text x="860" y="{y + 17}" font-family="Roboto, Arial, sans-serif" font-size="17" fill="#2B2B33">{txt}</text>')
        y += 32
    extra = ' width="1000" height="560"'
    return o, extra


TAUX = [c['taux'] for c in COMMUNES]
B6 = quantiles(TAUX, 6)


def carte_taux(ancres, lg, nom_titre):
    cols = gamme(ancres, 6)
    cc = [cols[classe(c['taux'], B6)] for c in COMMUNES]
    leg = [(cols[k], f'{fr_num(B6[k]) if lg == "fr" else f"{B6[k]:.1f}"} – {fr_num(B6[k + 1]) if lg == "fr" else f"{B6[k + 1]:.1f}"} %')
           for k in range(5, -1, -1)]
    o, extra = choroplethe(cc, nom_titre, leg)
    return svg('0 0 1000 560', nom_titre, o, extra)


tt = {'fr': 'Taux de coupes rases', 'en': 'Clear-cut rate'}
ecrire('carte-degrade.svg', carte_taux(SEQ, 'fr', tt['fr']), carte_taux(SEQ, 'en', tt['en']))
ecrire('carte-arc-en-ciel.svg', carte_taux(ARC, 'fr', tt['fr']), carte_taux(ARC, 'en', tt['en']))
ecrire('carte-rouge-vert.svg', carte_taux(RVERT, 'fr', tt['fr']), carte_taux(RVERT, 'en', tt['en']))


# ------------------------------------------------------------------ daltonisme (deutéranopie, Machado et al. 2009, sévérité 1)
MACHADO_D = [[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]]


def lin(v):
    v = v / 255
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def delin(v):
    v = max(0, min(1, v))
    return 255 * (12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055)


def deuteranope(h):
    c = [lin(x) for x in hexrvb(h)]
    return rvbhex([delin(sum(MACHADO_D[i][j] * c[j] for j in range(3))) for i in range(3)])


def carte_dalto(lg):
    nom = {'fr': 'Vu par un œil deutéranope', 'en': 'As seen with deuteranopia'}[lg]
    cols = [deuteranope(h) for h in gamme(RVERT, 6)]
    cc = [cols[classe(c['taux'], B6)] for c in COMMUNES]
    leg = [(cols[k], f'{fr_num(B6[k]) if lg == "fr" else f"{B6[k]:.1f}"} – {fr_num(B6[k + 1]) if lg == "fr" else f"{B6[k + 1]:.1f}"} %')
           for k in range(5, -1, -1)]
    o, extra = choroplethe(cc, tt[lg], leg)
    return svg('0 0 1000 560', nom, o, extra)


ecrire('carte-rouge-vert-dalto.svg', carte_dalto('fr'), carte_dalto('en'))


# ------------------------------------------------------------------ stock en aplats, stock en cercles
STOCK = [c['coupes_ha'] for c in COMMUNES]
BS = quantiles(STOCK, 5)


def stock_aplats(lg):
    cols = gamme(SEQ, 5)
    cc = [cols[classe(v, BS)] for v in STOCK]
    nom = {'fr': 'Coupes rases (ha)', 'en': 'Clear-cuts (ha)'}[lg]
    leg = [(cols[k], f'{BS[k]:.0f} – {BS[k + 1]:.0f} ha') for k in range(4, -1, -1)]
    o, extra = choroplethe(cc, nom, leg)
    return svg('0 0 1000 560', nom, o, extra)


RMAX = 30.0
VMAX = max(STOCK)


def cercles(lg, mode='aire', echelle_css=False):
    """mode = 'aire' (juste) ou 'rayon' (faux) ; echelle_css : le rayon suit la variable --x du curseur."""
    nom = {'fr': 'Coupes rases (ha)', 'en': 'Clear-cuts (ha)'}[lg]
    o = ['<rect width="1000" height="560" fill="#FFFFFF"/>']
    for c in COMMUNES:
        o.append(f'<path d="{c["chemin"]}" fill="#F4F5FB" stroke="#D8DAEC" stroke-width="0.9"/>')
    o.append(f'<path d="{TERR["contour"]}" fill="none" stroke="#283B89" stroke-width="2"/>')
    def r(v):
        return RMAX * (math.sqrt(v / VMAX) if mode == 'aire' else v / VMAX)
    for c in sorted(COMMUNES, key=lambda c: -c['coupes_ha']):
        rr = r(c['coupes_ha'])
        st = ' style="transform: scale(var(--x, 1)); transform-box: fill-box; transform-origin: center;"' if echelle_css else ''
        o.append(f'<circle cx="{c["cx"]}" cy="{c["cy"]}" r="{rr:.2f}" fill="#E38226" fill-opacity="0.75" stroke="#FFFFFF" stroke-width="1"{st}/>')
    o.append(f'<text x="815" y="90" font-family="Raleway, Arial, sans-serif" font-weight="700" font-size="20" fill="#283B89">{nom}</text>')
    y = 130
    for v in (250, 100, 25):
        rr = r(v)
        st = ' style="transform: scale(var(--x, 1)); transform-box: fill-box; transform-origin: center;"' if echelle_css else ''
        o.append(f'<circle cx="845" cy="{y + 30}" r="{rr:.2f}" fill="#E38226" fill-opacity="0.75" stroke="#FFFFFF"{st}/>')
        o.append(f'<text x="890" y="{y + 36}" font-family="Roboto, Arial, sans-serif" font-size="17" fill="#2B2B33">{v} ha</text>')
        y += 70
    titre = {'fr': {'aire': 'Surface proportionnelle', 'rayon': 'Rayon proportionnel'},
             'en': {'aire': 'Area proportional', 'rayon': 'Radius proportional'}}[lg][mode]
    return svg('0 0 1000 560', titre, o, ' width="1000" height="560"')


ecrire('stock-aplats.svg', stock_aplats('fr'), stock_aplats('en'))
ecrire('stock-cercles.svg', cercles('fr'), cercles('en'))
ecrire('cercles-rayon.svg', cercles('fr', 'rayon'), cercles('en', 'rayon'))
ecrire('cercles-echelle.svg', cercles('fr', 'aire', True), cercles('en', 'aire', True))


# ------------------------------------------------------------------ seuils de perception (curseur : x = taille des figurés, en multiple du seuil)
# Valeurs de l'ancien support (d'après É. Blin et J.-P. Bord) : taille minimale, séparation, différenciation.
PX_MM = 5          # échelle d'affichage : 5 px pour 1 mm, à peu près la taille réelle sur un écran de portable


def seuils(lg):
    t = {'fr': ['Les seuils de perception : être vu, être séparé, être distingué',
                ('Être vu', 'taille minimale'), ('Être séparé', '0,2 mm entre deux éléments'), ('Être distingué', 'un écart suffisant'),
                ['0,2 mm', '0,3 mm', '0,4 mm', '0,5 mm', '0,4 × 0,6', '0,6 × 0,8', '1 mm', '0,1 mm'],
                ['deux traits', 'deux carrés', 'deux points'],
                ['surfaces dans un rapport de 2', 'traits rapprochés : 0,1 mm d’écart', 'traits éloignés : 0,3 mm d’écart']],
         'en': ['Perception thresholds: being seen, being separated, being told apart',
                ('Being seen', 'minimum size'), ('Being separated', '0.2 mm between two features'), ('Being told apart', 'a large enough gap'),
                ['0.2 mm', '0.3 mm', '0.4 mm', '0.5 mm', '0.4 × 0.6', '0.6 × 0.8', '1 mm', '0.1 mm'],
                ['two lines', 'two squares', 'two dots'],
                ['areas in a ratio of 2', 'close lines: 0.1 mm apart in width', 'distant lines: 0.3 mm apart in width']]}[lg]
    K = 'var(--x, 4)'
    ENC = '#2B2B33'
    def fig(x, y, corps):      # un figuré dessiné en millimètres autour de (0, 0), agrandi par le curseur
        return f'<g transform="translate({x} {y})"><g style="transform: scale(calc({K} * {PX_MM}))">{corps}</g></g>'
    def trait(x, y, long, ep_mm, dy_mm=0):
        return (f'<path d="M{x - long / 2} {y} H{x + long / 2}" style="stroke:{ENC};'
                f'stroke-width:calc({K} * {ep_mm * PX_MM}px);transform:translateY(calc({K} * {dy_mm * PX_MM}px))"/>')
    o = ['<rect x="0" y="0" width="960" height="330" class="s-fond"/>']
    for r, (titre, sous) in enumerate(t[1:4]):
        y = 34 + r * 105
        o.append(f'<path d="M14 {y + 75} H946" stroke="#D8DAEC" stroke-width="1"/>' if r < 2 else '')
        o.append(T(16, y + 6, titre, 's-titre', 'start'))
        o.append(T(16, y + 28, sous, 's-petit', 'start'))
    # 1. être vu
    y1, xs = 60, [250, 335, 420, 505, 590, 680, 775, 880]
    v = 0.08                                  # épaisseur des contours, en mm
    corps = [f'<circle r="0.1" fill="{ENC}"/>',
             f'<circle r="{0.15 - v / 2}" fill="none" stroke="{ENC}" stroke-width="{v}"/>',
             f'<rect x="-0.2" y="-0.2" width="0.4" height="0.4" fill="{ENC}"/>',
             f'<rect x="{-0.25 + v / 2}" y="{-0.25 + v / 2}" width="{0.5 - v}" height="{0.5 - v}" fill="none" stroke="{ENC}" stroke-width="{v}"/>',
             f'<rect x="-0.3" y="-0.2" width="0.6" height="0.4" fill="{ENC}"/>',
             f'<rect x="{-0.4 + v / 2}" y="{-0.3 + v / 2}" width="{0.8 - v}" height="{0.6 - v}" fill="none" stroke="{ENC}" stroke-width="{v}"/>',
             f'<path d="M0 -0.5 L0.5 0.37 H-0.5 Z" fill="none" stroke="{ENC}" stroke-width="{v}" stroke-linejoin="round"/>']
    for x, c in zip(xs, corps):
        o.append(fig(x, y1, c))
    o.append(trait(xs[7], y1, 60, 0.1))
    for x, lab in zip(xs, t[4]):
        o.append(T(x, y1 + 40, lab, 's-petit'))
    # 2. être séparé : 0,2 mm d'écart
    y2 = 165
    o.append(trait(300, y2, 70, 0.1, -0.15))
    o.append(trait(300, y2, 70, 0.1, 0.15))
    o.append(fig(470, y2, f'<rect x="-0.5" y="-0.2" width="0.4" height="0.4" fill="{ENC}"/><rect x="0.1" y="-0.2" width="0.4" height="0.4" fill="{ENC}"/>'))
    o.append(fig(640, y2, f'<circle cx="-0.2" r="0.1" fill="{ENC}"/><circle cx="0.2" r="0.1" fill="{ENC}"/>'))
    for x, lab in zip([300, 470, 640], t[5]):
        o.append(T(x, y2 + 40, lab, 's-petit'))
    # 3. être distingué
    y3 = 268
    o.append(fig(300, y3, f'<circle cx="-1.05" r="0.5" fill="{ENC}"/><circle cx="1.2" r="{0.5 * math.sqrt(2):.4f}" fill="{ENC}"/>'))
    o.append(trait(520, y3, 90, 0.1, -0.3))
    o.append(trait(520, y3, 90, 0.2, 0.3))
    o.append(trait(735, y3, 70, 0.1))
    o.append(trait(855, y3, 70, 0.4))
    for x, lab in zip([300, 520, 795], t[6]):
        o.append(T(x, y3 + 44, lab, 's-petit'))
    return svg('0 0 960 330', t[0], o)


ecrire('seuils.svg', seuils('fr'), seuils('en'))


# ------------------------------------------------------------------ Ebbinghaus (curseur : x = rayon du cercle de droite)
def ebbinghaus(lg):
    t = {'fr': ['L’illusion d’Ebbinghaus', 'les deux cercles mesurent 30'], 'en': ['The Ebbinghaus illusion', 'both circles measure 30']}[lg]
    o = []
    cx, cy = 220, 170
    for k in range(6):
        a = k * math.pi / 3
        o.append(f'<circle cx="{cx + 110 * math.cos(a):.1f}" cy="{cy + 110 * math.sin(a):.1f}" r="52" fill="#9CA6CF"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="30" fill="#E38226"/>')
    cx2 = 680
    for k in range(8):
        a = k * math.pi / 4
        o.append(f'<circle cx="{cx2 + 62 * math.cos(a):.1f}" cy="{cy + 62 * math.sin(a):.1f}" r="13" fill="#9CA6CF"/>')
    o.append(f'<circle cx="{cx2}" cy="{cy}" style="r: calc(var(--x, 30) * 1px)" fill="#E38226"/>')
    o.append('<g class="s-apparait">')
    o.append(f'<circle cx="{cx2}" cy="{cy}" r="30" fill="none" stroke="#283B89" stroke-width="2.5" stroke-dasharray="5 4"/>')
    o.append(T(450, 335, t[1], 's-titre'))
    o.append('</g>')
    return svg('0 0 900 345', t[0], o)


ecrire('ebbinghaus.svg', ebbinghaus('fr'), ebbinghaus('en'))


# ------------------------------------------------------------------ Adelson : l'image d'origine (E. H. Adelson, 1995), et la révélation
def adelson(lg):
    import base64
    from PIL import Image
    t = {'fr': ['L’échiquier d’Adelson', 'A et B : le même gris (120, 120, 120)'],
         'en': ['Adelson’s checker shadow', 'A and B: the same grey (120, 120, 120)']}[lg]
    chemin = os.path.join(COURS, 'images', 'originaux', 's29_917a22e1.png')
    im = Image.open(chemin).convert('RGB')
    gris = im.getpixel((395, 215))
    assert gris == im.getpixel((385, 345)) == (120, 120, 120)   # A et B, mesurés sur l'image
    b64 = base64.b64encode(open(chemin, 'rb').read()).decode()
    o = [f'<image href="data:image/png;base64,{b64}" x="0" y="0" width="800" height="621"/>',
         '<g class="s-apparait">',
         f'<rect x="383" y="218" width="12" height="118" fill="{rvbhex(gris)}"/>',
         f'<rect x="418" y="214" width="12" height="118" fill="{rvbhex(gris)}"/>',
         f'<rect x="30" y="566" width="470" height="44" rx="8" fill="#FFFFFF" opacity="0.92"/>',
         T(265, 596, t[1], 's-titre', style='font-size:24px'),
         '</g>']
    return svg('0 0 800 621', t[0], o)


ecrire('adelson.svg', adelson('fr'), adelson('en'))


# ------------------------------------------------------------------ contraste : un mot sur un fond qui change (curseur : x = teinte du fond)
def un_mot(lg):
    t = {'fr': ['Un mot rouge sur un fond de teinte variable', 'Un mot'], 'en': ['A red word on a background of changing hue', 'A word']}[lg]
    o = ['<rect x="0" y="0" width="520" height="200" rx="10" style="fill: hsl(calc(var(--x, 90) * 1deg), 70%, 50%)"/>',
         T(260, 125, t[1], style='font-family:Raleway,Arial,sans-serif;font-size:64px;font-weight:700;fill:#D7191C')]
    return svg('0 0 520 200', t[0], o)


ecrire('un-mot.svg', un_mot('fr'), un_mot('en'))


# ------------------------------------------------------------------ combien de paliers ? sept marches, cinq teintes
def paliers(lg):
    t = {'fr': ['Sept paliers de valeur dans cinq teintes', ['Jaune', 'Vert', 'Bleu', 'Rouge', 'Gris']],
         'en': ['Seven value steps in five hues', ['Yellow', 'Green', 'Blue', 'Red', 'Grey']]}[lg]
    teintes = [(52, 95), (120, 55), (215, 70), (0, 75), (0, 0)]
    o = []
    for r, ((h, s), nom) in enumerate(zip(teintes, t[1])):
        y = 10 + r * 64
        o.append(T(80, y + 36, nom, anchor='end', style='font-weight:700'))
        for k in range(7):
            l = 92 - k * 11
            o.append(f'<rect x="{100 + k * 100}" y="{y}" width="100" height="52" style="fill:hsl({h},{s}%,{l}%)"/>')
    return svg('0 0 810 330', t[0], o)


ecrire('paliers.svg', paliers('fr'), paliers('en'))


# ------------------------------------------------------------------ les variables visuelles × implantations (d'après Bertin)
def variables(lg):
    t = {'fr': ['Les variables visuelles et les trois implantations',
                ['Forme', 'Taille', 'Orientation', 'Couleur', 'Valeur', 'Structure'], ['Point', 'Ligne', 'Surface']],
         'en': ['Visual variables and the three implantations',
                ['Shape', 'Size', 'Orientation', 'Colour', 'Value', 'Texture'], ['Point', 'Line', 'Area']]}[lg]
    o = []
    W, Hh = 250, 64
    for j, nom in enumerate(t[2]):
        o.append(T(190 + j * W + W / 2, 26, nom, 's-titre'))
    for i, nom in enumerate(t[1]):
        y = 40 + i * Hh
        o.append(f'<rect x="0" y="{y}" width="{190 + 3 * W}" height="{Hh}" fill="{"#F4F5FB" if i % 2 == 0 else "#FFFFFF"}"/>')
        o.append(T(176, y + 39, nom, anchor='end', style='font-weight:700'))
        for j in range(3):
            x0, cy = 190 + j * W + 40, y + Hh / 2
            for k in range(4):
                x = x0 + k * 48
                if j == 0:       # point
                    if i == 0: o.append([f'<circle cx="{x}" cy="{cy}" r="11" fill="#283B89"/>', f'<rect x="{x-10}" y="{cy-10}" width="20" height="20" fill="#283B89"/>', f'<path d="M{x} {cy-12} L{x+12} {cy+10} L{x-12} {cy+10} Z" fill="#283B89"/>', f'<path d="M{x-11} {cy-3} h22 v6 h-22 z M{x-3} {cy-11} h6 v22 h-6 z" fill="#283B89"/>'][k])
                    if i == 1: o.append(f'<circle cx="{x}" cy="{cy}" r="{4 + k * 3.5}" fill="#283B89"/>')
                    if i == 2: o.append(f'<rect x="{x-3}" y="{cy-13}" width="6" height="26" fill="#283B89" transform="rotate({k * 45} {x} {cy})"/>')
                    if i == 3: o.append(f'<circle cx="{x}" cy="{cy}" r="11" fill="{["#283B89", "#E38226", "#4E8A5A", "#9655A2"][k]}"/>')
                    if i == 4: o.append(f'<circle cx="{x}" cy="{cy}" r="11" fill="{["#DCE1F2", "#9CA6CF", "#5866A8", "#1D2A66"][k]}"/>')
                    if i == 5: o.append(f'<circle cx="{x}" cy="{cy}" r="12" fill="url(#trame{k})" stroke="#283B89" stroke-width="1"/>')
                if j == 1 and k == 0:  # ligne
                    if i == 0:
                        for kk, d in enumerate(['none', '10 6', '2 5', '14 4 2 4']):
                            o.append(f'<path d="M{x0 - 10} {cy - 18 + kk * 12} H{x0 + 170}" stroke="#283B89" stroke-width="3" stroke-dasharray="{d}"/>')
                    if i == 1:
                        for kk in range(4):
                            o.append(f'<path d="M{x0 - 10 + kk * 48} {cy} h38" stroke="#283B89" stroke-width="{1 + kk * 3}"/>')
                    if i == 2:
                        for kk, a in enumerate([0, 90]):
                            xx = x0 + 20 + kk * 100
                            o.append(f'<path d="M{xx - 30} {cy} H{xx + 30}" stroke="#283B89" stroke-width="2"/>')
                            for m in range(-2, 3):
                                o.append(f'<path d="M{xx + m * 12} {cy - 8} v16" stroke="#283B89" stroke-width="2" transform="rotate({45 if kk else 0} {xx + m * 12} {cy})"/>')
                    if i == 3:
                        for kk, col in enumerate(["#283B89", "#E38226", "#4E8A5A", "#9655A2"]):
                            o.append(f'<path d="M{x0 - 10 + kk * 48} {cy} h38" stroke="{col}" stroke-width="5"/>')
                    if i == 4:
                        for kk, col in enumerate(["#DCE1F2", "#9CA6CF", "#5866A8", "#1D2A66"]):
                            o.append(f'<path d="M{x0 - 10 + kk * 48} {cy} h38" stroke="{col}" stroke-width="5"/>')
                    if i == 5:
                        o.append(f'<path d="M{x0 - 10} {cy} H{x0 + 170}" stroke="#283B89" stroke-width="10" stroke-dasharray="2 3"/>')
                if j == 2:  # surface
                    fill = {0: "#283B89", 1: "#283B89", 2: f"url(#hachure{k})", 3: ["#283B89", "#E38226", "#4E8A5A", "#9655A2"][k],
                            4: ["#DCE1F2", "#9CA6CF", "#5866A8", "#1D2A66"][k], 5: f"url(#trame{k})"}[i]
                    if i == 0:
                        o.append(f'<rect x="{x - 18}" y="{cy - 18}" width="36" height="36" fill="url(#motif{k})" stroke="#283B89"/>')
                    elif i == 1:
                        o.append(f'<rect x="{x - 18}" y="{cy - 18}" width="36" height="36" fill="url(#pois{k})" stroke="#283B89"/>')
                    else:
                        o.append(f'<rect x="{x - 18}" y="{cy - 18}" width="36" height="36" fill="{fill}" stroke="#283B89"/>')
    defs = ['<defs>']
    for k in range(4):
        defs.append(f'<pattern id="trame{k}" width="{3 + k * 2}" height="{3 + k * 2}" patternUnits="userSpaceOnUse"><circle cx="1.5" cy="1.5" r="1.2" fill="#283B89"/></pattern>')
        defs.append(f'<pattern id="hachure{k}" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate({k * 45})"><path d="M0 3 H6" stroke="#283B89" stroke-width="1.6"/></pattern>')
        defs.append(f'<pattern id="pois{k}" width="12" height="12" patternUnits="userSpaceOnUse"><circle cx="6" cy="6" r="{1 + k * 1.2}" fill="#283B89"/></pattern>')
        motif = ['<circle cx="6" cy="6" r="2.4" fill="#283B89"/>', '<rect x="3.5" y="3.5" width="5" height="5" fill="#283B89"/>',
                 '<path d="M6 2.5 L9.5 9 H2.5 Z" fill="#283B89"/>', '<path d="M3 6 H9 M6 3 V9" stroke="#283B89" stroke-width="1.6"/>'][k]
        defs.append(f'<pattern id="motif{k}" width="12" height="12" patternUnits="userSpaceOnUse">{motif}</pattern>')
    defs.append('</defs>')
    return svg(f'0 0 {190 + 3 * W} {40 + 6 * Hh}', t[0], defs + o)


ecrire('variables.svg', variables('fr'), variables('en'))


# ------------------------------------------------------------------ des codes de couleur d'autres cultures (sens révélé avec la réponse)
# Sources : data.europa.eu, guide de visualisation des données, « Colour connotations » (rouge en Chine,
# rouge et bleu aux États-Unis) ; le blanc du deuil en Asie de l'Est et le vert de l'islam sont des usages courants.
def codes_ailleurs(lg):
    t = {'fr': ['Quatre codes de couleur venus d’ailleurs',
                [('Rouge', 'Chine, Japon, Corée', ['la prospérité ; en bourse,', 'la hausse'], ['#D7191C']),
                 ('Blanc', 'Asie de l’Est', ['le deuil'], ['#FFFFFF']),
                 ('Rouge, bleu', 'États-Unis', ['républicains, démocrates', '(en France, rouge = gauche)'], ['#D7191C', '#2C5AA0']),
                 ('Vert', 'monde musulman', ['la couleur de l’islam'], ['#11845B'])]],
         'en': ['Four colour codes from elsewhere',
                [('Red', 'China, Japan, Korea', ['prosperity; on the stock', 'market, a rise'], ['#D7191C']),
                 ('White', 'East Asia', ['mourning'], ['#FFFFFF']),
                 ('Red, blue', 'United States', ['Republicans, Democrats', '(in France, red = left)'], ['#D7191C', '#2C5AA0']),
                 ('Green', 'Muslim world', ['the colour of Islam'], ['#11845B'])]]}[lg]
    o = []
    for k, (nom, ou, sens, cols) in enumerate(t[1]):
        x, y = (k % 2) * 300, (k // 2) * 140
        o.append(f'<rect x="{x}" y="{y}" width="290" height="128" rx="10" class="s-fond"/>')
        for j, c in enumerate(cols):
            h = 100 / len(cols)
            o.append(f'<rect x="{x + 12}" y="{y + 14 + j * h:.1f}" width="50" height="{h:.1f}" fill="{c}" stroke="#9A9AA4" stroke-width="1"/>')
        o.append(T(x + 76, y + 36, nom, 's-titre', 'start'))
        o.append(T(x + 76, y + 57, ou, 's-petit', 'start'))
        o.append('<g class="s-apparait">')
        for j, ligne in enumerate(sens):
            o.append(T(x + 76, y + 86 + j * 20, ligne, anchor='start', style='font-size:15px;fill:#2B2B33'))
        o.append('</g>')
    return svg('0 0 590 268', t[0], o)


ecrire('codes-ailleurs.svg', codes_ailleurs('fr'), codes_ailleurs('en'))


# ------------------------------------------------------------------ « WTF » : on voit tout, on ne comprend rien (paillettes animées)
def wtf(lg):
    t = {'fr': 'Un petit lecteur ébloui par une carte : il voit tout, il ne comprend rien',
         'en': 'A little reader dazzled by a map: sees everything, understands nothing'}[lg]
    etoile = 'M0 -1 C0.14 -0.14 0.14 -0.14 1 0 C0.14 0.14 0.14 0.14 0 1 C-0.14 0.14 -0.14 0.14 -1 0 C-0.14 -0.14 -0.14 -0.14 0 -1 Z'
    o = ['<style>'
         '.wtf-p{transform-box:fill-box;transform-origin:center;animation:wtf-scintille 1.8s ease-in-out infinite}'
         '.wtf-q{animation:wtf-flotte 3s ease-in-out infinite}'
         '@keyframes wtf-scintille{0%,100%{opacity:.25;transform:scale(.55) rotate(0deg)}50%{opacity:1;transform:scale(1.1) rotate(25deg)}}'
         '@keyframes wtf-flotte{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}'
         '@media (prefers-reduced-motion: reduce){.wtf-p,.wtf-q{animation:none}}'
         '</style>']
    # le petit lecteur, tout rond
    o.append('<ellipse cx="215" cy="205" rx="98" ry="90" fill="#FDE3CF" stroke="#283B89" stroke-width="3.5"/>')
    o.append('<ellipse cx="160" cy="222" rx="14" ry="9" fill="#F7A1B5" opacity="0.8"/><ellipse cx="270" cy="222" rx="14" ry="9" fill="#F7A1B5" opacity="0.8"/>')
    def spirale(cx, cy):
        pts = []
        for k in range(0, 160):
            a = k * 0.16
            r = 1.1 * a
            pts.append(f'{cx + r * math.cos(a):.1f} {cy + r * math.sin(a):.1f}')
        return f'<path d="M{" L".join(pts)}" fill="none" stroke="#283B89" stroke-width="3" stroke-linecap="round"/>'
    o.append(spirale(178, 182))
    o.append(spirale(252, 182))
    o.append('<path d="M196 240 q7 -8 14 0 t14 0 t14 0" fill="none" stroke="#283B89" stroke-width="3" stroke-linecap="round"/>')
    # la carte, tenue à l'envers, trop chargée
    o.append('<g transform="rotate(-9 215 306)">'
             '<rect x="150" y="262" width="130" height="88" rx="4" fill="#FFFFFF" stroke="#283B89" stroke-width="3"/>'
             '<path d="M158 337 C180 287 200 327 222 282 S262 317 272 273" fill="none" stroke="#E38226" stroke-width="5"/>'
             '<path d="M160 277 C190 307 230 267 270 337" fill="none" stroke="#4FA3D9" stroke-width="4"/>'
             '<circle cx="186" cy="299" r="9" fill="#9655A2"/><circle cx="246" cy="317" r="7" fill="#4E8A5A"/>'
             '<rect x="206" y="287" width="14" height="14" fill="#D7191C"/><path d="M255 282 l8 14 h-16 z" fill="#F2B705"/>'
             '</g>')
    # les mains qui tiennent la carte
    o.append('<ellipse cx="152" cy="318" rx="13" ry="11" fill="#FDE3CF" stroke="#283B89" stroke-width="3"/>')
    o.append('<ellipse cx="280" cy="294" rx="13" ry="11" fill="#FDE3CF" stroke="#283B89" stroke-width="3"/>')
    # la bulle
    o.append('<path d="M330 30 h170 a22 22 0 0 1 22 22 v62 a22 22 0 0 1 -22 22 h-120 l-34 30 l6 -30 h-22 a22 22 0 0 1 -22 -22 v-62 a22 22 0 0 1 22 -22 z" '
             'fill="#FFFFFF" stroke="#283B89" stroke-width="3.5" transform="translate(-24 0)"/>')
    o.append('<text x="391" y="108" text-anchor="middle" style="font-family:Raleway,Arial,sans-serif;font-size:58px;font-weight:800;fill:#283B89">WTF ?!</text>')
    # les points d'interrogation qui flottent
    for k, (x, y, s, col) in enumerate([(70, 90, 40, '#9655A2'), (95, 150, 26, '#E38226'), (330, 210, 34, '#4FA3D9')]):
        o.append(f'<text class="wtf-q" x="{x}" y="{y}" style="animation-delay:{k * 0.7:.1f}s;font-family:Raleway,Arial,sans-serif;font-size:{s}px;font-weight:800;fill:{col}">?</text>')
    # les paillettes
    pail = [(40, 40, 12, '#F2B705'), (130, 60, 8, '#FF6FB5'), (300, 28, 9, '#4FC3F7'), (560, 70, 11, '#F2B705'),
            (545, 170, 8, '#FF6FB5'), (440, 200, 13, '#9655A2'), (360, 300, 10, '#4FC3F7'), (60, 230, 10, '#FF6FB5'),
            (35, 320, 13, '#F2B705'), (320, 165, 7, '#E38226'), (500, 250, 9, '#4FC3F7'), (115, 330, 7, '#9655A2'),
            (585, 300, 12, '#FF6FB5'), (250, 330, 8, '#F2B705'), (420, 300, 6, '#E38226'), (205, 82, 7, '#4FC3F7')]
    for k, (x, y, s, col) in enumerate(pail):
        o.append(f'<g transform="translate({x} {y}) scale({s})"><path class="wtf-p" d="{etoile}" fill="{col}" style="animation-delay:{(k * 0.37) % 1.8:.2f}s"/></g>')
    for k in range(26):   # quelques grains de paillettes
        x = 20 + (k * 157) % 590
        y = 15 + (k * 89) % 335
        col = ['#F2B705', '#FF6FB5', '#4FC3F7', '#9655A2'][k % 4]
        if ((x - 215) / 112) ** 2 + ((y - 215) / 112) ** 2 < 1 or (300 < x < 545 and 20 < y < 175):
            continue          # pas sur le visage ni dans la bulle
        o.append(f'<circle cx="{x}" cy="{y}" r="{1.6 + (k % 3) * 0.8:.1f}" fill="{col}" opacity="0.8"/>')
    return svg('0 0 620 360', t, o, ' width="620" height="360"')


ecrire('wtf.svg', wtf('fr'), wtf('en'))


# ------------------------------------------------------------------ la carte du puzzle de légende (sans légende)
# Aplats : taux de coupes en 4 classes (effectifs égaux) ; cercles : surface coupée ; lignes : routes forestières ;
# carrés : scieries. Les valeurs et les rayons sont imprimés en fin de script, pour les pièces du puzzle.
B4 = quantiles(TAUX, 4)
RMAXL = 16.0
COUL4 = gamme(SEQ, 4)
CERCLE_L = '#3E8FD0'


def legende_carte(lg):
    nom = {'fr': 'Coupes rases et filière bois dans le territoire fictif', 'en': 'Clear-cuts and the timber industry in the fictional territory'}[lg]
    o = ['<rect width="800" height="560" fill="#FFFFFF"/>']
    for c in COMMUNES:
        o.append(f'<path d="{c["chemin"]}" fill="{COUL4[classe(c["taux"], B4)]}" stroke="#FFFFFF" stroke-width="0.9"/>')
    o.append(f'<path d="{TERR["contour"]}" fill="none" stroke="#283B89" stroke-width="2"/>')
    # cercles : la surface coupée
    for c in sorted(COMMUNES, key=lambda c: -c['coupes_ha']):
        if c['coupes_ha'] >= 8:
            r = RMAXL * math.sqrt(c['coupes_ha'] / VMAX)
            o.append(f'<circle cx="{c["cx"]}" cy="{c["cy"]}" r="{r:.2f}" fill="{CERCLE_L}" fill-opacity="0.8" stroke="#FFFFFF" stroke-width="1"/>')
    # routes forestières : par bandes, d'ouest en est, à travers l'est boisé ; un trait blanc cerné de noir
    for y0, y1, x0 in [(140, 215, 330), (290, 365, 360), (405, 470, 450)]:
        pts, dernier = [], -999
        for x, y in sorted([(c['cx'], c['cy']) for c in COMMUNES if y0 <= c['cy'] <= y1 and c['cx'] >= x0]):
            if x - dernier >= 55:
                pts.append((x, y)); dernier = x
        d = 'M' + ' L'.join(f'{x:.0f} {y:.0f}' for x, y in pts)
        o.append(f'<path d="{d}" fill="none" stroke="#1B1B22" stroke-width="5.5" stroke-linejoin="round" stroke-linecap="round"/>')
        o.append(f'<path d="{d}" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>')
    # scieries : sur quatre communes boisées
    boisees = sorted(COMMUNES, key=lambda c: -c['foret_ha'])[:12:3]
    for c in boisees:
        o.append(f'<rect x="{c["cx"] + 9:.0f}" y="{c["cy"] - 14:.0f}" width="11" height="11" fill="#FFFFFF" stroke="#1B1B22" stroke-width="2.2"/>')
    return svg('0 0 800 560', nom, o, ' width="800" height="560"')


ecrire('legende-carte.svg', legende_carte('fr'), legende_carte('en'))


# ------------------------------------------------------------------ quatre mises en page
def mises_en_page(lg):
    t = {'fr': ['Quatre mises en page de la même carte', 'titre', 'légende', 'échelle', 'source'],
         'en': ['Four layouts of the same map', 'title', 'legend', 'scale', 'source']}[lg]
    o = []
    def page(x, lettre, blocs, carte):
        o.append(f'<rect x="{x}" y="10" width="200" height="270" fill="#FFFFFF" stroke="#283B89" stroke-width="2"/>')
        cx, cy, w, h = carte
        o.append(f'<rect x="{x + cx}" y="{10 + cy}" width="{w}" height="{h}" rx="16" fill="#C9D3B8"/>')
        for bx, by, bw, bh, col in blocs:
            o.append(f'<rect x="{x + bx}" y="{10 + by}" width="{bw}" height="{bh}" fill="{col}"/>')
        o.append(T(x + 100, 310, lettre, 's-titre', style='font-size:26px'))
    TI, LE, EC = '#283B89', '#E38226', '#6E6F7A'
    # A : la carte occupe la page et accueille la légende (recommandation : maximiser la carte)
    page(20, 'A', [(12, 14, 176, 22, TI), (128, 150, 54, 76, LE), (12, 246, 60, 8, EC), (110, 256, 78, 6, EC)], (12, 46, 176, 190))
    o.append('<rect x="148" y="160" width="54" height="76" fill="none" stroke="#FFFFFF" stroke-width="2"/>')
    page(270, 'B', [(150, 230, 40, 14, TI), (10, 14, 60, 40, LE), (12, 120, 30, 8, EC), (140, 18, 50, 6, EC)], (40, 60, 120, 150))
    page(520, 'C', [(12, 14, 176, 22, TI), (12, 210, 176, 50, LE), (160, 50, 30, 8, EC), (40, 50, 100, 6, EC), (12, 64, 20, 20, LE), (166, 160, 24, 30, LE)], (40, 80, 120, 120))
    page(770, 'D', [(12, 14, 176, 22, TI), (14, 200, 80, 60, LE), (120, 230, 68, 8, EC), (120, 250, 68, 6, EC)], (70, 70, 60, 50))
    return svg('0 0 990 320', t[0], o)


ecrire('mises-en-page.svg', mises_en_page('fr'), mises_en_page('en'))

# Valeurs citées dans le cours
print('seuils sextiles du taux :', [round(b, 1) for b in B6])
print('stock max :', VMAX, 'ha ; communes :', len(COMMUNES))
print('rapport des surfaces de cercles, max / 25 ha : rayon', round((VMAX / 25) ** 2, 1), 'fois ; aire', round(VMAX / 25, 1), 'fois')
print('deutéranope :', [deuteranope(h) for h in gamme(RVERT, 6)])
print('puzzle de légende : quartiles du taux', [round(b, 1) for b in B4], '; couleurs', COUL4,
      '; rayons 245/100/25 ha :', [round(RMAXL * math.sqrt(v / VMAX), 1) for v in (VMAX, 100, 25)])
