"""Générateur des schémas de cours/geotraitements.

    python3 outils/schemas-geotraitements.py cours/geotraitements/images/schemas

Schémas du cours GIS : Geoprocessing, en français et en anglais.
Écrit chaque schéma dans <dossier>/ (fr) et <dossier>/en/ (en).
Les valeurs des exercices sont calculées ici, pas recopiées à la main.
"""
import os, sys

OUT = sys.argv[1]
os.makedirs(os.path.join(OUT, 'en'), exist_ok=True)

def svg(vb, aria, body, extra=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{aria}"{extra}>\n'
            + '\n'.join(body) + '\n</svg>\n')

def ecrire(nom, fr, en):
    open(os.path.join(OUT, nom), 'w', encoding='utf-8').write(fr)
    open(os.path.join(OUT, 'en', nom), 'w', encoding='utf-8').write(en)

def T(x, y, s, cls=None, anchor='middle', style=''):
    c = f' class="{cls}"' if cls else ''
    st = f' style="{style}"' if style else ''
    return f'<text{c} x="{x}" y="{y}" text-anchor="{anchor}"{st}>{s}</text>'

def fleche(x1, y, x2):
    return f'<path class="s-accent" d="M{x1} {y} H{x2-10}"/><path class="s-plein-accent" d="M{x2} {y} l-12 -7 v14 z"/>'

def grille(x, y, vals, c=40, couleur=None, gras=None, police=16):
    """Une grille de valeurs. couleur(v) donne un remplissage ; gras = ensemble de (i, j) surlignés."""
    o = []
    for i, ligne in enumerate(vals):
        for j, v in enumerate(ligne):
            fill = couleur(v) if couleur else '#fff'
            o.append(f'<rect x="{x+j*c}" y="{y+i*c}" width="{c}" height="{c}" style="fill:{fill};stroke:#D8DAEC;stroke-width:1"/>')
            if v is not None and v != '':
                w = 'font-weight:700;' if gras and (i, j) in gras else ''
                o.append(T(x+j*c+c/2, y+i*c+c/2+police*0.35, v, style=f'font-size:{police}px;{w}'))
    n, m = len(vals), len(vals[0])
    o.append(f'<rect class="s-trait" x="{x}" y="{y}" width="{m*c}" height="{n*c}" style="stroke-width:1.8"/>')
    return o

def bleu(v, vmin, vmax):
    t = (v - vmin) / (vmax - vmin) if vmax > vmin else 0
    return f'rgb({int(236-100*t)},{int(240-110*t)},{int(250-60*t)})'

L = lambda fr, en: {'fr': fr, 'en': en}

# ---------------------------------------------------------------- 1.5 relations spatiales
def relations(lg):
    t = {'fr': ['Les relations spatiales : intersecte, contient, à moins de', 'intersecte', 'contient', 'à moins de d', 'la piste traverse', 'le peuplement', 'la placette est dedans', 'tout ce qui touche le cercle'],
         'en': ['Spatial relationships: intersects, contains, within a distance', 'intersects', 'contains', 'within distance d', 'the road crosses', 'the stand', 'the plot is inside', 'all that touches the circle']}[lg]
    o = []
    for k, x in enumerate([20, 400, 780]):
        o.append(f'<rect class="s-fond" x="{x}" y="10" width="350" height="240" rx="12"/>')
    o.append('<path class="s-plein-accent" opacity="0.3" d="M80 70 L260 60 L280 190 L90 200 Z"/><path class="s-trait" d="M80 70 L260 60 L280 190 L90 200 Z"/>')
    o.append('<path class="s-accent" d="M40 220 C 120 160 200 120 340 40" style="stroke-width:5"/>')
    o.append(T(195, 290, t[1], 's-titre')); o.append(T(195, 312, t[4], 's-petit'))
    o.append('<path class="s-plein-accent" opacity="0.3" d="M460 70 L640 60 L660 190 L470 200 Z"/><path class="s-trait" d="M460 70 L640 60 L660 190 L470 200 Z"/>')
    o.append('<circle class="s-plein" cx="560" cy="130" r="9"/>')
    o.append(T(575, 290, t[2], 's-titre')); o.append(T(575, 312, t[6], 's-petit'))
    o.append('<circle cx="955" cy="130" r="80" class="s-tirets" style="stroke:var(--orange);stroke-width:2.5"/>')
    o.append('<circle class="s-plein" cx="955" cy="130" r="8"/><path class="s-fin" d="M955 130 L1035 130"/>')
    o.append(T(995, 122, 'd', style='font-size:18px;font-style:italic'))
    o.append('<path class="s-plein-accent" opacity="0.3" d="M1010 170 L1100 160 L1110 235 L1020 240 Z"/><path class="s-trait" d="M1010 170 L1100 160 L1110 235 L1020 240 Z"/>')
    o.append('<path class="s-trait" d="M810 60 L870 40 L880 90 L820 100 Z" style="stroke:var(--gris)"/>')
    o.append(T(955, 290, t[3], 's-titre')); o.append(T(955, 312, t[7], 's-petit'))
    return svg('0 0 1150 325', t[0], o)
ecrire('relations-spatiales.svg', relations('fr'), relations('en'))

# ---------------------------------------------------------------- 1.6 Venn
def venn(lg):
    t = {'fr': ['Trois opérateurs booléens sur deux critères', 'A : chêne', 'B : plus de 5 ha'],
         'en': ['Three Boolean operators on two criteria', 'A: oak', 'B: over 5 ha']}[lg]
    o = ['<defs><clipPath id="vA"><circle cx="0" cy="0" r="70"/></clipPath></defs>']
    for k, (x, op) in enumerate([(190, 'AND'), (575, 'OR'), (960, 'NOT')]):
        a, b = x - 45, x + 45
        if op == 'AND':
            o.append(f'<clipPath id="cA{k}"><circle cx="{a}" cy="120" r="75"/></clipPath>')
            o.append(f'<circle cx="{b}" cy="120" r="75" clip-path="url(#cA{k})" class="s-plein-accent" opacity="0.7"/>')
        elif op == 'OR':
            o.append(f'<circle cx="{a}" cy="120" r="75" class="s-plein-accent" opacity="0.7"/><circle cx="{b}" cy="120" r="75" class="s-plein-accent" opacity="0.7"/>')
        else:
            o.append(f'<mask id="mN{k}"><rect x="0" y="0" width="1150" height="300" fill="#fff"/><circle cx="{b}" cy="120" r="75" fill="#000"/></mask>')
            o.append(f'<circle cx="{a}" cy="120" r="75" mask="url(#mN{k})" class="s-plein-accent" opacity="0.7"/>')
        o.append(f'<circle class="s-trait" cx="{a}" cy="120" r="75"/><circle class="s-trait" cx="{b}" cy="120" r="75"/>')
        o.append(T(a - 35, 125, 'A', style='font-weight:700')); o.append(T(b + 35, 125, 'B', style='font-weight:700'))
        o.append(T(x, 240, f'A {op} B', 's-titre', style='font-family:var(--police-mono)'))
    o.append(T(575, 280, f'{t[1]}   ·   {t[2]}', 's-petit', style='font-size:16px'))
    return svg('0 0 1150 295', t[0], o)
ecrire('venn.svg', venn('fr'), venn('en'))

# ---------------------------------------------------------------- 2.2 jointure spatiale
PEUPL = [('P1', 'M60 40 L330 30 L340 250 L70 260 Z', L('chêne', 'oak')), ('P2', 'M330 30 L560 50 L550 240 L340 250 Z', L('hêtre', 'beech'))]
PLAC = [(1, 160, 110, 32), (2, 450, 150, 45), (3, 230, 200, 28)]
def dans(px, py, d):
    import re
    pts = [tuple(map(float, p.split())) for p in re.findall(r'[\d.]+ [\d.]+', d)]
    c = False
    for i in range(len(pts)):
        x1, y1 = pts[i]; x2, y2 = pts[(i + 1) % len(pts)]
        if (y1 > py) != (y2 > py) and px < (x2 - x1) * (py - y1) / (y2 - y1) + x1: c = not c
    return c
JOINT = {n: next(p for p in PEUPL if dans(x, y, p[1])) for n, x, y, _ in PLAC}
def table(x, y, entetes, lignes, largeurs, surligne=None):
    o, h = [], 34
    tot = sum(largeurs)
    o.append(f'<rect class="s-blanc" x="{x}" y="{y}" width="{tot}" height="{h*(len(lignes)+1)}"/>')
    o.append(f'<rect class="s-plein" x="{x}" y="{y}" width="{tot}" height="{h}" opacity="0.15"/>')
    cx = x
    for k, (e, w) in enumerate(zip(entetes, largeurs)):
        st = 'font-weight:700' + (';fill:var(--orange-texte)' if surligne == k else '')
        o.append(T(cx + w / 2, y + 23, e, style=st))
        for r, l in enumerate(lignes):
            st2 = 'fill:var(--orange-texte);font-weight:700' if surligne == k else ''
            o.append(T(cx + w / 2, y + h * (r + 1) + 23, l[k], style=st2))
        cx += w
        if k < len(largeurs) - 1:
            o.append(f'<path class="s-fin" d="M{cx} {y} V{y+h*(len(lignes)+1)}"/>')
    for r in range(len(lignes)):
        o.append(f'<path class="s-fin" d="M{x} {y+h*(r+1)} H{x+tot}"/>')
    return o
def jointure(lg, resultat):
    t = {'fr': ['Jointure spatiale : chaque placette reçoit les attributs du peuplement où elle tombe', 'Peuplements', 'Placettes', 'placette', 'diamètre', 'essence', 'Résultat de la jointure'],
         'en': ['Spatial join: each plot receives the attributes of the stand it falls in', 'Stands', 'Plots', 'plot', 'diameter', 'species', 'Result of the join']}[lg]
    o = []
    for nom, d, ess in PEUPL:
        o.append(f'<path d="{d}" class="s-plein-accent" opacity="{0.25 if nom=="P1" else 0.12}"/><path class="s-trait" d="{d}"/>')
    o.append(T(110, 75, f'P1 · {PEUPL[0][2][lg]}', style='font-weight:700', anchor='start'))
    o.append(T(380, 75, f'P2 · {PEUPL[1][2][lg]}', style='font-weight:700', anchor='start'))
    for n, x, y, _ in PLAC:
        o.append(f'<circle class="s-plein" cx="{x}" cy="{y}" r="8"/>'); o.append(T(x + 18, y + 6, str(n), style='font-weight:700', anchor='start'))
    o.append(T(310, 295, f'{t[1]} + {t[2]}', 's-titre'))
    if not resultat:
        o += table(640, 70, [t[3], t[4]], [[str(n), f'{d} cm'] for n, _, _, d in PLAC], [110, 150])
        o.append(T(770, 40, t[2], 's-titre'))
    else:
        o += table(620, 70, [t[3], t[4], t[5]], [[str(n), f'{d} cm', JOINT[n][2][lg]] for n, _, _, d in PLAC], [100, 140, 140], surligne=2)
        o.append(T(810, 40, t[6], 's-titre'))
    return svg('0 0 1150 310', t[0], o)
ecrire('jointure-entrees.svg', jointure('fr', False), jointure('en', False))
ecrire('jointure-resultat.svg', jointure('fr', True), jointure('en', True))

# ---------------------------------------------------------------- 3.1 implantation
def implantation(lg):
    t = {'fr': ["Changer d'implantation : chemin, enveloppe convexe, centroïde", 'Chemin', 'des points à la ligne', 'Enveloppe convexe', 'des points au polygone', 'Centroïde', 'du polygone au point'],
         'en': ['Changing the geometry type: path, convex hull, centroid', 'Path', 'from points to a line', 'Convex hull', 'from points to a polygon', 'Centroid', 'from a polygon to a point']}[lg]
    o = []
    pts = [(40, 150), (90, 110), (140, 130), (190, 80), (240, 100)]
    for x, y in pts: o.append(f'<circle class="s-plein" cx="{x}" cy="{y}" r="6"/>')
    o.append(fleche(260, 115, 300))
    o.append('<path class="s-accent" d="M' + ' L'.join(f'{x+280} {y}' for x, y in pts) + '"/>')
    o.append(T(260, 230, t[1], 's-titre')); o.append(T(260, 252, t[2], 's-petit'))
    pts2 = [(430, 120), (470, 70), (520, 100), (500, 160), (450, 170), (480, 120)]
    for x, y in pts2: o.append(f'<circle class="s-plein" cx="{x}" cy="{y}" r="6"/>')
    o.append(fleche(540, 115, 580))
    hull = [(430, 120), (470, 70), (520, 100), (500, 160), (450, 170)]
    d = 'M' + ' L'.join(f'{x+170} {y}' for x, y in hull) + ' Z'
    o.append(f'<path class="s-plein-accent" opacity="0.35" d="{d}"/><path class="s-trait" d="{d}"/>')
    for x, y in pts2: o.append(f'<circle cx="{x+170}" cy="{y}" r="4" style="fill:var(--gris)"/>')
    o.append(T(560, 230, t[3], 's-titre')); o.append(T(560, 252, t[4], 's-petit'))
    poly = [(770, 80), (850, 60), (880, 130), (830, 170), (760, 150)]
    d = 'M' + ' L'.join(f'{x} {y}' for x, y in poly) + ' Z'
    o.append(f'<path class="s-plein-accent" opacity="0.35" d="{d}"/><path class="s-trait" d="{d}"/>')
    o.append(fleche(895, 115, 935))
    cx = sum(x for x, _ in poly) / 5; cy = sum(y for _, y in poly) / 5
    o.append(f'<path class="s-fin" d="M{poly[0][0]+210} {poly[0][1]}' + ''.join(f' L{x+210} {y}' for x, y in poly[1:]) + ' Z" style="stroke-dasharray:4 4"/>')
    o.append(f'<circle class="s-plein" cx="{cx+210:.0f}" cy="{cy:.0f}" r="8"/>')
    o.append(T(930, 230, t[5], 's-titre')); o.append(T(930, 252, t[6], 's-petit'))
    return svg('0 0 1150 265', t[0], o)
ecrire('implantation.svg', implantation('fr'), implantation('en'))

# ---------------------------------------------------------------- 3.2 tampons
TP = [(150, 140), (230, 120), (195, 200)]
def tampons(lg, mode):
    t = {'fr': ['Trois tampons qui se chevauchent', 'Trois placettes, un tampon de 50 m', 'Séparés : 3 objets', 'Fusionnés : 1 objet', 'Multiples : des anneaux'],
         'en': ['Three overlapping buffers', 'Three plots, a 50 m buffer', 'Separate: 3 features', 'Dissolved: 1 feature', 'Multiple: rings']}[lg]
    o = []
    if mode == 'question':
        for x, y in TP:
            o.append(f'<circle cx="{x}" cy="{y}" r="70" class="s-tirets" style="stroke:var(--orange);stroke-width:2.5"/>')
            o.append(f'<circle class="s-plein" cx="{x}" cy="{y}" r="7"/>')
        o.append(T(190, 315, t[1], 's-titre'))
        return svg('0 0 380 330', t[0], o)
    for x, y in TP:
        o.append(f'<circle cx="{x}" cy="{y}" r="70" class="s-plein-accent" opacity="0.28"/><circle cx="{x}" cy="{y}" r="70" class="s-trait"/>')
        o.append(f'<circle class="s-plein" cx="{x}" cy="{y}" r="6"/>')
    o.append(T(190, 315, t[2], 's-titre'))
    o.append('<g transform="translate(380,0)">')
    o.append('<mask id="mFus"><rect width="380" height="330" fill="#fff"/>' + ''.join(f'<circle cx="{x}" cy="{y}" r="68.5" fill="#000"/>' for x, y in TP) + '</mask>')
    for x, y in TP: o.append(f'<circle cx="{x}" cy="{y}" r="70" style="fill:#F5D3B0"/>')
    for x, y in TP: o.append(f'<circle cx="{x}" cy="{y}" r="71.5" style="fill:var(--bleu)" mask="url(#mFus)"/>')
    for x, y in TP: o.append(f'<circle class="s-plein" cx="{x}" cy="{y}" r="6"/>')
    o.append(T(190, 315, t[3], 's-titre')); o.append('</g>')
    o.append('<g transform="translate(760,0)">')
    for r, op in [(110, 0.12), (80, 0.22), (50, 0.35)]:
        o.append(f'<circle cx="190" cy="150" r="{r}" class="s-plein-accent" opacity="{op}"/><circle cx="190" cy="150" r="{r}" class="s-trait" style="stroke-width:1.5"/>')
    o.append('<circle class="s-plein" cx="190" cy="150" r="6"/>')
    o.append(T(190, 315, t[4], 's-titre')); o.append('</g>')
    return svg('0 0 1140 330', t[0], o)
ecrire('tampons-question.svg', tampons('fr', 'question'), tampons('en', 'question'))
ecrire('tampons.svg', tampons('fr', 'tout'), tampons('en', 'tout'))

# ---------------------------------------------------------------- 3.3 superposition
PA = ['M30 40 L150 30 L160 150 L40 160 Z', 'M150 30 L260 45 L250 170 L160 150 Z']   # peuplements
PB = 'M110 90 L320 90 L320 230 L110 230 Z'                                           # zone (commune, Natura 2000)
def superposition(lg):
    t = {'fr': ['Superposer : découper, unir, intersecter', 'Peuplements', 'Zone', 'Découper', 'la géométrie de la zone, les attributs des peuplements', 'Unir', 'toute la surface des deux couches', 'Intersecter', 'la partie commune, les attributs des deux'],
         'en': ['Overlaying: clip, union, intersect', 'Stands', 'Zone', 'Clip', 'the zone shape, the stand attributes', 'Union', 'the whole area of both layers', 'Intersect', 'the common part, attributes of both']}[lg]
    o = ['<defs><clipPath id="cB"><path d="' + PB + '"/></clipPath></defs>']
    def entree(dx):
        r = [f'<g transform="translate({dx},0)">']
        for d, op in zip(PA, [0.35, 0.18]): r.append(f'<path d="{d}" class="s-plein-accent" opacity="{op}"/><path class="s-trait" d="{d}"/>')
        r.append(f'<path d="{PB}" style="fill:#9655A2;opacity:0.18"/><path d="{PB}" class="s-violet" style="stroke-dasharray:7 5"/>')
        r.append('</g>')
        return r
    o += entree(0)
    o.append(T(175, 270, f'{t[1]} + {t[2]}', 's-titre'))
    # découper
    o.append('<g transform="translate(380,-10) scale(0.75)">')
    for d, op in zip(PA, [0.45, 0.25]): o.append(f'<path d="{d}" clip-path="url(#cB)" class="s-plein-accent" opacity="{op}"/><path class="s-trait" d="{d}" clip-path="url(#cB)"/>')
    for d in PA: o.append(f'<path d="{d}" class="s-fin" style="stroke-dasharray:4 4"/>')
    o.append(f'<path d="{PB}" class="s-fin" style="stroke-dasharray:4 4"/>')
    o.append('</g>')
    o.append(T(490, 230, t[3], 's-titre')); o.append(T(490, 252, t[4], 's-petit', style='font-size:12px'))
    # unir
    o.append('<g transform="translate(640,-10) scale(0.75)">')
    o.append(f'<path d="{PB}" style="fill:#9655A2;opacity:0.18"/>')
    for d, op in zip(PA, [0.35, 0.18]): o.append(f'<path d="{d}" class="s-plein-accent" opacity="{op}"/>')
    for d in PA: o.append(f'<path class="s-trait" d="{d}"/>')
    o.append(f'<path d="{PB}" class="s-trait"/>')
    o.append('</g>')
    o.append(T(760, 230, t[5], 's-titre')); o.append(T(760, 252, t[6], 's-petit', style='font-size:12px'))
    # intersecter
    o.append('<g transform="translate(900,-10) scale(0.75)">')
    for d, op in zip(PA, [0.55, 0.35]): o.append(f'<path d="{d}" clip-path="url(#cB)" class="s-plein-accent" opacity="{op}"/><path class="s-trait" d="{d}" clip-path="url(#cB)"/>')
    for d in PA: o.append(f'<path d="{d}" clip-path="url(#cB)" style="fill:#9655A2;opacity:0.22"/>')
    o.append(f'<path d="{PB}" class="s-fin" style="stroke-dasharray:4 4"/>')
    o.append('</g>')
    o.append(T(1020, 230, t[7], 's-titre')); o.append(T(1020, 252, t[8], 's-petit', style='font-size:12px'))
    o.append('<path class="s-tirets" d="M345 20 V260"/>')
    return svg('0 0 1150 285', t[0], o)
ecrire('superposition.svg', superposition('fr'), superposition('en'))

# ---------------------------------------------------------------- 3.4 fusion selon un attribut
PARC = [(1, 0, 0, 'X'), (3, 0, 1, 'X'), (2, 0, 2, 'Y'), (4, 1, 0, 'Z'), (5, 1, 1, 'Z'), (6, 1, 2, 'Y')]
COUL = {'X': '#F2D2B0', 'Y': '#DCE6F5', 'Z': '#E4D3E8'}
def dissolve(lg, apres):
    t = {'fr': ['Six parcelles et leur zone', 'Après la fusion sur « zone »', 'parcelle', 'zone'],
         'en': ['Six parcels and their zone', 'After dissolving on "zone"', 'parcel', 'zone']}[lg]
    o, c = [], 110
    x0, y0 = 30, 30
    for n, i, j, z in PARC:
        o.append(f'<rect x="{x0+j*c}" y="{y0+i*c}" width="{c}" height="{c}" style="fill:{COUL[z]};stroke:{COUL[z] if apres else "var(--bleu)"};stroke-width:1.5"/>')
        if not apres: o.append(T(x0 + j * c + c / 2, y0 + i * c + c / 2 + 6, f'{n} · {z}', style='font-weight:700'))
    if apres:
        zones = {}
        for n, i, j, z in PARC: zones.setdefault(z, []).append((i, j))
        # contours : on trace les arêtes entre cellules de zones différentes, et le bord
        for n, i, j, z in PARC:
            for di, dj, ax in [(-1, 0, 'h'), (1, 0, 'h'), (0, -1, 'v'), (0, 1, 'v')]:
                v = next((p[3] for p in PARC if p[1] == i + di and p[2] == j + dj), None)
                if v != z:
                    if ax == 'h':
                        yy = y0 + (i + (1 if di == 1 else 0)) * c
                        o.append(f'<path class="s-trait" d="M{x0+j*c} {yy} h{c}"/>')
                    else:
                        xx = x0 + (j + (1 if dj == 1 else 0)) * c
                        o.append(f'<path class="s-trait" d="M{xx} {y0+i*c} v{c}"/>')
        for z, cells in zones.items():
            cx = sum(x0 + j * c + c / 2 for i, j in cells) / len(cells); cy = sum(y0 + i * c + c / 2 for i, j in cells) / len(cells)
            o.append(T(cx, cy + 7, z, style='font-weight:700;font-size:22px'))
        o.append(T(195, 290, t[1], 's-titre'))
    else:
        o.append(T(195, 290, t[0], 's-titre'))
    return svg('0 0 390 305', t[1] if apres else t[0], o)
ecrire('dissolve-avant.svg', dissolve('fr', False), dissolve('en', False))
ecrire('dissolve-apres.svg', dissolve('fr', True), dissolve('en', True))
NB_ZONES = len(set(p[3] for p in PARC))

# ---------------------------------------------------------------- 4.1 trois familles
def familles(lg):
    t = {'fr': ['Trois familles d’opérations raster : locale, focale, zonale', 'Locale', 'pixel à pixel', 'Focale', 'selon les voisins', 'Zonale', 'selon une zone'],
         'en': ['Three families of raster operations: local, focal, zonal', 'Local', 'cell by cell', 'Focal', 'from the neighbours', 'Zonal', 'by zone']}[lg]
    o = []
    def g(x, y, hl, coul='#fff'):
        r = []
        for i in range(5):
            for j in range(5):
                f = hl(i, j) or coul
                r.append(f'<rect x="{x+j*34}" y="{y+i*34}" width="34" height="34" style="fill:{f};stroke:#D8DAEC"/>')
        r.append(f'<rect class="s-trait" x="{x}" y="{y}" width="170" height="170" style="stroke-width:1.5"/>')
        return r
    o += g(70, 20, lambda i, j: '#E38226' if (i, j) == (2, 2) else None)
    o += g(70, 210, lambda i, j: '#F2AE6D' if (i, j) == (2, 2) else None)
    o.append('<path class="s-tirets" d="M155 105 V295"/>')
    o.append(T(155, 410, t[1], 's-titre')); o.append(T(155, 432, t[2], 's-petit'))
    o += g(470, 115, lambda i, j: '#E38226' if (i, j) == (2, 2) else ('#F2D2B0' if abs(i-2) <= 1 and abs(j-2) <= 1 else None))
    o.append('<rect x="504" y="149" width="102" height="102" class="s-accent" style="fill:none"/>')
    o.append(T(555, 410, t[3], 's-titre')); o.append(T(555, 432, t[4], 's-petit'))
    Z = lambda i, j: '#E4D3E8' if j < 2 else ('#F2D2B0' if i < 2 else '#DCE6F5')
    o += g(870, 115, Z)
    o.append('<path class="s-violet" d="M870 115 h68 v170 h-68 z" style="stroke-width:3.5;fill:none"/>')
    o.append(T(955, 410, t[5], 's-titre')); o.append(T(955, 432, t[6], 's-petit'))
    return svg('0 0 1110 445', t[0], o)
ecrire('familles-raster.svg', familles('fr'), familles('en'))

# ---------------------------------------------------------------- 4.2 condition sur la pente
PENTES = [[12, 18, 25, 33], [15, 28, 35, 41], [22, 31, 38, 45], [9, 14, 27, 36]]
SEUIL = 30
BIN = [[1 if v > SEUIL else 0 for v in l] for l in PENTES]
def condition(lg, sortie):
    t = {'fr': ['Une grille de pentes, en %', 'Pente > 30 : 1, sinon 0', 'pente (%)', 'masque'],
         'en': ['A grid of slopes, in %', 'Slope > 30: 1, otherwise 0', 'slope (%)', 'mask']}[lg]
    o = grille(20, 20, PENTES, c=56, couleur=lambda v: bleu(v, 0, 50), police=18)
    o.append(T(132, 270, t[2], 's-petit'))
    if sortie:
        o = grille(20, 20, BIN, c=56, couleur=lambda v: '#E38226' if v else '#fff', police=18)
        o.append(T(132, 270, t[3], 's-petit'))
        return svg('0 0 270 285', t[1], o)
    return svg('0 0 270 285', t[0], o)
ecrire('condition-entree.svg', condition('fr', False), condition('en', False))
ecrire('condition-sortie.svg', condition('fr', True), condition('en', True))

# ---------------------------------------------------------------- 4.3 algèbre raster
A = [[2, 4, 4], [1, 3, 5], [0, 2, 6]]
B = [[1, 1, 2], [3, 1, 0], [2, 2, 1]]
S = [[a + b for a, b in zip(la, lb)] for la, lb in zip(A, B)]
def algebre(lg):
    t = {'fr': ['Algèbre raster : deux couches additionnées pixel à pixel'], 'en': ['Raster algebra: two layers added cell by cell']}[lg]
    o = grille(20, 20, A, c=50); o.append(T(195, 105, '+', 's-titre', style='font-size:34px'))
    o += grille(230, 20, B, c=50); o.append(T(405, 105, '=', 's-titre', style='font-size:34px'))
    o += grille(440, 20, S, c=50, couleur=lambda v: bleu(v, 0, 8))
    return svg('0 0 610 190', t[0], o)
ecrire('algebre.svg', algebre('fr'), algebre('en'))

# ---------------------------------------------------------------- 4.4 cohérence
def coherence(lg):
    t = {'fr': ['Deux grilles de résolution et de calage différents', 'couche 1 : 30 m', 'couche 2 : 10 m, décalée', 'quel pixel de la couche 2 pour ce pixel de la couche 1 ?'],
         'en': ['Two grids with different resolution and alignment', 'layer 1: 30 m', 'layer 2: 10 m, shifted', 'which layer-2 cell for this layer-1 cell?']}[lg]
    o = []
    for i in range(10):
        for j in range(10):
            o.append(f'<rect x="{80+j*24}" y="{45+i*24}" width="24" height="24" style="fill:none;stroke:#9CC3E6;stroke-width:1"/>')
    for i in range(4):
        for j in range(4):
            o.append(f'<rect x="{40+j*72}" y="{20+i*72}" width="72" height="72" style="fill:none;stroke:var(--bleu);stroke-width:2"/>')
    o.append('<rect x="112" y="92" width="72" height="72" style="fill:#E38226;opacity:0.35"/>')
    o.append(T(420, 80, t[1], anchor='start', style='fill:var(--bleu);font-weight:700'))
    o.append(T(420, 110, t[2], anchor='start', style='fill:#4A7CC2;font-weight:700'))
    o.append(T(420, 170, t[3], 's-petit', anchor='start'))
    return svg('0 0 860 320', t[0], o)
ecrire('coherence.svg', coherence('fr'), coherence('en'))

# ---------------------------------------------------------------- 4.5 fenêtre glissante
FEN = [[4, 6, 5, 7, 8], [5, 3, 6, 9, 7], [6, 4, 8, 5, 6], [7, 7, 2, 1, 5], [8, 6, 5, 4, 3]]
VOIS = [FEN[i][j] for i in range(1, 4) for j in range(1, 4)]
MOY = sum(VOIS) / 9
assert MOY == int(MOY)
def fenetre(lg):
    t = {'fr': ['Une fenêtre de 3 × 3 autour du pixel central', 'fenêtre 3 × 3', 'pixel central'],
         'en': ['A 3 × 3 window around the centre cell', '3 × 3 window', 'centre cell']}[lg]
    o = grille(20, 20, FEN, c=52, couleur=lambda v: '#fff', gras={(2, 2)}, police=18)
    o.insert(0, '<rect x="72" y="72" width="156" height="156" style="fill:#F2D2B0"/>')
    o = [o[0]] + [x.replace('fill:#fff', 'fill:none') for x in o[1:]]
    o.append('<rect x="124" y="124" width="52" height="52" style="fill:none;stroke:var(--orange);stroke-width:3"/>')
    o.append('<rect x="72" y="72" width="156" height="156" class="s-accent" style="fill:none"/>')
    o.append(T(300, 90, t[1], 's-orange', anchor='start'))
    o.append('<rect x="300" y="112" width="22" height="22" style="fill:none;stroke:var(--orange);stroke-width:3"/>')
    o.append(T(332, 129, t[2], 's-petit', anchor='start'))
    return svg('0 0 460 300', t[0], o)
ecrire('fenetre.svg', fenetre('fr'), fenetre('en'))

# ---------------------------------------------------------------- 4.6 MNS - MNT
def mns(lg):
    t = {'fr': ['MNS, MNT et hauteur de canopée', 'MNS : le sol et le sursol', 'MNT : le sol', 'hauteur = MNS − MNT'],
         'en': ['DSM, DTM and canopy height', 'DSM: ground and above-ground', 'DTM: bare ground', 'height = DSM − DTM']}[lg]
    o = []
    sol = 'M20 250 C 200 230 380 270 560 240 S 900 220 1080 245'
    o.append(f'<path d="{sol} L1080 300 L20 300 Z" style="fill:#E7E1D0"/>')
    for x, h in [(140, 95), (200, 120), (260, 105), (320, 130), (380, 115), (440, 100), (500, 125)]:
        yb = 252 if x < 300 else 250
        o.append(f'<path d="M{x} {yb} V{yb-h+30}" style="stroke:#8C6E4A;stroke-width:5"/>')
        o.append(f'<ellipse cx="{x}" cy="{yb-h+20}" rx="34" ry="30" style="fill:#7FA86A"/>')
    o.append('<rect x="700" y="170" width="90" height="70" style="fill:#F3E2C7;stroke:#6E6F7A;stroke-width:2"/>')
    o.append('<path class="s-accent" d="M20 225 C 80 215 110 140 140 128 S 220 100 260 118 S 330 92 380 108 S 470 100 530 102 S 590 220 640 228 S 690 165 700 168 H790 S 820 225 860 228 S 1000 222 1080 230" style="stroke-width:3.5"/>')
    o.append(f'<path class="s-trait" d="{sol}" style="stroke-width:3.5"/>')
    o.append('<path class="s-plein" d="M320 110 V244" style="stroke:var(--violet);stroke-width:3"/><path d="M320 104 l-7 12 h14 z M320 250 l-7 -12 h14 z" style="fill:var(--violet)"/>')
    o.append(T(330, 62, t[3], anchor='start', style='fill:var(--violet);font-weight:700'))
    o.append(T(880, 205, t[1], 's-orange', anchor='start')); o.append(T(880, 270, t[2], anchor='start', style='fill:var(--bleu);font-weight:700'))
    return svg('0 0 1100 300', t[0], o)
ecrire('mns-mnt.svg', mns('fr'), mns('en'))

# ---------------------------------------------------------------- 4.8 zonal
ZON = [['A', 'A', 'B', 'B'], ['A', 'A', 'B', 'B'], ['A', 'C', 'C', 'B'], ['C', 'C', 'C', 'B']]
VAL = [[2, 4, 6, 8], [3, 5, 7, 9], [1, 2, 3, 5], [2, 4, 6, 1]]
def moy(z):
    v = [VAL[i][j] for i in range(4) for j in range(4) if ZON[i][j] == z]
    return sum(v) / len(v)
MOY_B = moy('B'); assert MOY_B == int(MOY_B)
CZ = {'A': '#E4D3E8', 'B': '#F2D2B0', 'C': '#DCE6F5'}
def zonal(lg):
    t = {'fr': ['Des valeurs et des zones', 'valeurs', 'zones'], 'en': ['Values and zones', 'values', 'zones']}[lg]
    o = grille(20, 20, VAL, c=52, police=18); o.append(T(124, 250, t[1], 's-petit'))
    o += grille(290, 20, ZON, c=52, couleur=lambda z: CZ[z], police=18); o.append(T(394, 250, t[2], 's-petit'))
    return svg('0 0 520 265', t[0], o)
ecrire('zonal.svg', zonal('fr'), zonal('en'))

# ---------------------------------------------------------------- 4.9 rééchantillonner
def reech(lg):
    t = {'fr': ['Rééchantillonner : quatre pixels deviennent un', 'résolution 10 m', 'résolution 20 m (moyenne)'],
         'en': ['Resampling: four cells become one', '10 m resolution', '20 m resolution (mean)']}[lg]
    V = [[2, 4, 6, 8], [4, 6, 8, 10], [1, 3, 5, 7], [3, 5, 7, 9]]
    R = [[sum(V[2*i+a][2*j+b] for a in (0, 1) for b in (0, 1)) // 4 for j in range(2)] for i in range(2)]
    o = grille(20, 20, V, c=44, couleur=lambda v: bleu(v, 0, 10)); o.append(T(108, 215, t[1], 's-petit'))
    o.append(fleche(215, 108, 265))
    o += grille(285, 20, R, c=88, couleur=lambda v: bleu(v, 0, 10), police=20); o.append(T(373, 215, t[2], 's-petit'))
    return svg('0 0 480 230', t[0], o)
ecrire('reechantillonner.svg', reech('fr'), reech('en'))

# ---------------------------------------------------------------- 5.1 parcelles vecteur / raster (pour le curseur : couleurs écrites en dur)
PV = [('M40 40 L330 30 L360 230 L60 250 Z', '#F2D2B0'), ('M330 30 L620 60 L600 260 L360 230 Z', '#C9D3B8'), ('M60 250 L360 230 L380 420 L50 410 Z', '#DCE6F5'), ('M360 230 L600 260 L620 420 L380 420 Z', '#E4D3E8')]
def parcelles(lg, raster):
    titre = {'fr': ['Les parcelles en vecteur', 'Les parcelles rasterisées, pixels de 40 m'], 'en': ['Parcels as vector', 'Parcels rasterised, 40 m cells']}[lg][1 if raster else 0]
    o = ['<rect width="660" height="450" fill="#FFFFFF"/>']
    if not raster:
        for d, c in PV: o.append(f'<path d="{d}" fill="{c}" stroke="#283B89" stroke-width="2.5"/>')
    else:
        c = 30
        for i in range(0, 450, c):
            for j in range(0, 660, c):
                cx, cy = j + c / 2, i + c / 2
                col = next((col for d, col in PV if dans(cx, cy, d)), None)
                if col: o.append(f'<rect x="{j}" y="{i}" width="{c}" height="{c}" fill="{col}" stroke="#FFFFFF" stroke-width="0.8"/>')
        for d, _ in PV: o.append(f'<path d="{d}" fill="none" stroke="#283B89" stroke-width="1.2" stroke-dasharray="5 5" opacity="0.6"/>')
    return svg('0 0 660 450', titre, o, extra=' width="660" height="450"')
ecrire('parcelles-vecteur.svg', parcelles('fr', False), parcelles('en', False))
ecrire('parcelles-raster.svg', parcelles('fr', True), parcelles('en', True))

# ---------------------------------------------------------------- 5.4 masque
def masque(lg):
    t = {'fr': ['Découper un MNT par le contour d’une forêt', 'MNT', 'forêt', 'MNT de la forêt'], 'en': ['Clipping a DTM by a forest boundary', 'DTM', 'forest', 'DTM of the forest']}[lg]
    FOR = 'M60 60 L200 40 L230 150 L170 220 L50 190 Z'
    o = []
    def g(dx, garder):
        r = []
        for i in range(8):
            for j in range(8):
                cx, cy = 20 + j * 30 + 15, 20 + i * 30 + 15
                v = 300 + 12 * i + 8 * j
                inside = dans(cx, cy, FOR)
                if garder and not inside: continue
                r.append(f'<rect x="{dx+20+j*30}" y="{20+i*30}" width="30" height="30" style="fill:{bleu(v,300,450)};stroke:#fff"/>')
        return r
    o += g(0, False); o.append(T(140, 285, t[1], 's-petit'))
    o.append(T(300, 145, '+', 's-titre', style='font-size:30px'))
    o.append(f'<g transform="translate(320,0)"><path d="{FOR}" class="s-plein-accent" opacity="0.3"/><path d="{FOR}" class="s-trait"/></g>')
    o.append(T(460, 285, t[2], 's-petit'))
    o.append(fleche(620, 145, 670))
    o += g(680, True)
    o.append(f'<g transform="translate(680,0)"><path d="{FOR}" class="s-trait" style="stroke-dasharray:5 4"/></g>')
    o.append(T(820, 285, t[3], 's-petit'))
    return svg('0 0 960 300', t[0], o)
ecrire('masque.svg', masque('fr'), masque('en'))

# ---------------------------------------------------------------- 5.5 échantillonner
ALT = [[380, 395, 410, 425], [388, 402, 418, 431], [396, 412, 426, 440], [405, 420, 433, 448]]
PTS = [(1, 0, 2), (2, 1, 3), (3, 2, 1)]
VAL_P3 = ALT[2][1]
def echant(lg):
    t = {'fr': ['Trois placettes sur un MNT', 'altitude (m)'], 'en': ['Three plots on a DTM', 'elevation (m)']}[lg]
    c = 70
    o = grille(20, 20, ALT, c=c, couleur=lambda v: bleu(v, 370, 450), police=15)
    for n, i, j in PTS:
        x, y = 20 + j * c + c * 0.85, 20 + i * c + c * 0.2
        o.append(f'<circle cx="{x}" cy="{y}" r="9" style="fill:#E38226;stroke:#fff;stroke-width:2"/>')
        o.append(T(x, y + 5, str(n), style='fill:#fff;font-weight:700;font-size:12px'))
    o.append(T(160, 324, t[1], 's-petit'))
    return svg('0 0 320 335', t[0], o)
ecrire('echantillonner.svg', echant('fr'), echant('en'))

# Valeurs à reporter dans le cours
print('jointure :', {n: JOINT[n][0] for n in JOINT})
print('zones après fusion :', NB_ZONES)
print('condition :', BIN)
print('moyenne 3x3 :', MOY, 'centre avant :', FEN[2][2])
print('moyenne zone B :', MOY_B)
print('placette 3 :', VAL_P3)
print('algèbre :', S)
