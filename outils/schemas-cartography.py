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


# ------------------------------------------------------------------ seuils de perception (curseur : x = épaisseur en mm sur papier)
def seuils(lg):
    t = {'fr': ['Un trait et un point, à l’épaisseur choisie', 'trait', 'point (diamètre double)', 'seuil du trait : 0,1 mm', 'seuil du point : 0,2 mm'],
         'en': ['A line and a point, at the chosen width', 'line', 'point (twice the width)', 'line threshold: 0.1 mm', 'point threshold: 0.2 mm']}[lg]
    o = ['<rect x="0" y="0" width="900" height="220" class="s-fond"/>']
    o.append('<path d="M60 70 C 250 30 420 120 620 60 S 800 50 840 80" style="fill:none;stroke:#2B2B33;stroke-width:calc(var(--x, 0.3) * 6px)"/>')
    for k, x in enumerate([90, 230, 370, 510, 650, 790]):
        o.append(f'<circle cx="{x}" cy="150" style="r: calc(var(--x, 0.3) * 6px); fill:#2B2B33"/>')
    o.append(T(60, 112, t[1], 's-petit', 'start'))
    o.append(T(60, 195, t[2], 's-petit', 'start'))
    return svg('0 0 900 220', t[0], o)


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
    page(20, 'A', [(12, 14, 176, 22, TI), (130, 50, 58, 150, LE), (12, 240, 60, 8, EC), (110, 252, 78, 6, EC)], (12, 50, 110, 180))
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
