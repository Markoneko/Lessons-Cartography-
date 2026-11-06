#!/usr/bin/env python3
"""Schémas et données du cours « Image Intelligence », en français et en anglais.

    python3 cours/image-intelligence/outils/schemas.py

Écrit images/schemas/ (fr), images/schemas/en/ (en), les trois images de l'unité minimale de
collecte dans images/, et le profil du radiotélescope FAST dans donnees/.
Les valeurs citées dans le cours sont calculées ici et imprimées à la fin.
"""
import csv
import json
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

COURS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(COURS, 'images', 'schemas')
os.makedirs(os.path.join(OUT, 'en'), exist_ok=True)
BLEU, ORANGE, ENCRE, GRIS, FOND = '#283B89', '#E38226', '#2B2B33', '#6E6F7A', '#F4F5FB'


def svg(vb, aria, corps):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{aria}">\n'
            + '\n'.join(corps) + '\n</svg>\n')


def ecrire(nom, fr, en):
    open(os.path.join(OUT, nom), 'w', encoding='utf-8').write(fr)
    open(os.path.join(OUT, 'en', nom), 'w', encoding='utf-8').write(en)


def T(x, y, s, cls=None, anchor='middle', style=''):
    c = f' class="{cls}"' if cls else ''
    st = f' style="{style}"' if style else ''
    return f'<text{c} x="{x}" y="{y}" text-anchor="{anchor}"{st}>{s}</text>'


def fleche(ident, couleur=ORANGE):
    return (f'<defs><marker id="{ident}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            f'<path d="M0 0 L10 5 L0 10 z" fill="{couleur}"/></marker></defs>')


# ------------------------------------------------------------------ trois raisonnements
# Définitions de Marc (retours sur la V0). Les exemples sont sortis des cases : ils forment le faisceau.
def raisonnements(lg):
    t = {'fr': ['Induction, déduction, abduction',
                [('Induction', ['On observe des faits répétés', 'et l’on en dégage une règle.'],
                  ['Forte probabilité,', 'pas de certitude absolue.']),
                 ('Déduction', ['Des règles ou des prémisses', 'mènent à une conclusion.'],
                  ['Si les prémisses sont vraies,', 'la conclusion est certaine.']),
                 ('Abduction', ['Face à un fait observé,', 'on propose des hypothèses.'],
                  ['Aucune certitude : des pistes,', 'surtout quand le fait surprend.'])],
                'Le faisceau d’indices', 'hypothèse : c’est l’ombre de la tour',
                [['Toutes les ombres déjà vues', 'pointent au nord-ouest.'],
                 ['Le soleil est au sud-est : les', 'ombres tombent au nord-ouest.'],
                 ['Une tache sombre, allongée,', 'au pied d’une tour…']]],
         'en': ['Induction, deduction, abduction',
                [('Induction', ['We observe repeated facts', 'and draw a rule from them.'],
                  ['Highly probable,', 'never absolutely certain.']),
                 ('Deduction', ['Rules or premises', 'lead to a conclusion.'],
                  ['If the premises are true,', 'the conclusion is certain.']),
                 ('Abduction', ['Faced with an observed fact,', 'we put forward hypotheses.'],
                  ['No certainty: leads,', 'above all when the fact surprises.'])],
                'The bundle of clues', 'hypothesis: it is the tower’s shadow',
                [['Every shadow seen so far', 'points north-west.'],
                 ['The sun is in the south-east:', 'shadows fall north-west.'],
                 ['A long dark patch', 'at the foot of a tower…']]]}[lg]
    o = []
    for k, (nom, def_, portee) in enumerate(t[1]):
        x = 10 + k * 250
        o.append(f'<rect x="{x}" y="6" width="236" height="164" rx="12" class="s-fond"/>')
        o.append(T(x + 118, 38, nom, 's-titre', style='font-size:22px'))
        o.append(T(x + 118, 68, def_[0], style=f'font-size:15.5px;fill:{ENCRE}'))
        o.append(T(x + 118, 89, def_[1], style=f'font-size:15.5px;fill:{ENCRE}'))
        o.append(f'<path d="M{x + 30} 106 H{x + 206}" stroke="#D8DAEC" stroke-width="1.5"/>')
        o.append(T(x + 118, 132, portee[0], style=f'font-size:15px;fill:{BLEU};font-weight:700'))
        o.append(T(x + 118, 153, portee[1], style=f'font-size:15px;fill:{BLEU};font-weight:700'))
    # le faisceau : un exemple de chaque raisonnement converge vers une hypothèse
    o.append(T(380, 204, t[2], 's-titre'))
    cx, cy = 380, 330
    for k, (l1, l2) in enumerate(t[4]):
        x0 = 128 + k * 250
        o.append(T(x0, 232, l1, 's-petit', style='font-size:14.5px;font-style:italic'))
        o.append(T(x0, 251, l2, 's-petit', style='font-size:14.5px;font-style:italic'))
        o.append(f'<circle cx="{x0}" cy="266" r="5" fill="{ORANGE}"/>')
        o.append(f'<path d="M{x0} 270 Q {x0 + (cx - x0) * 0.3} 292 {cx + (x0 - cx) * 0.18} {cy - 26}" fill="none" '
                 f'stroke="{ORANGE}" stroke-width="3" marker-end="url(#fleche-raison)"/>')
    o.append(f'<rect x="{cx - 160}" y="{cy - 24}" width="320" height="44" rx="22" fill="{BLEU}"/>')
    o.append(T(cx, cy + 5, t[3], style='font-size:17px;font-weight:700;fill:#FFFFFF'))
    return svg('0 0 760 362', t[0], [fleche('fleche-raison')] + o)


ecrire('raisonnements.svg', raisonnements('fr'), raisonnements('en'))


# ------------------------------------------------------------------ ombres portées : déduire l'objet de son ombre
# Vue verticale : d'en haut, chaque objet n'est qu'une petite trace ; son ombre, allongée par un soleil bas au
# sud-est, en donne la silhouette. Les noms n'apparaissent qu'avec la réponse.
OMBRE = '#3B3C47'


def silhouette(nom):
    """Silhouette de l'objet dans un repère local : pied en (0, 0), sommet vers les y négatifs."""
    s = []
    if nom == 'eolienne':
        s.append('<path d="M-2.5 0 L-1.5 -112 L1.5 -112 L2.5 0 Z"/>')
        for a in (90, 210, 330):
            r = math.radians(a)
            x, y = 44 * math.cos(r), -112 - 44 * math.sin(r)
            px, py = 4 * math.sin(r), 4 * math.cos(r)
            s.append(f'<path d="M{px:.1f} {-112 + py:.1f} L{x:.1f} {y:.1f} L{-px:.1f} {-112 - py:.1f} Z"/>')
        s.append('<circle cx="0" cy="-112" r="5"/>')
    elif nom == 'chateau':
        s.append('<path d="M-6 0 L-6 -72 L-30 -96 L-30 -122 Q0 -136 30 -122 L30 -96 L6 -72 L6 0 Z"/>')
    elif nom == 'pylone':
        s.append('<g fill="none" stroke="currentColor" stroke-width="2.6">'
                 '<path d="M-14 0 L-3 -132 M14 0 L3 -132 M-3 -132 L3 -132"/>'
                 '<path d="M-13 -12 L11 -36 M13 -12 L-11 -36 M-11 -36 L9 -62 M11 -36 L-9 -62 M-9 -62 L7 -88 M9 -62 L-7 -88"/>'
                 '<path d="M-38 -96 L38 -96 M-28 -116 L28 -116 M-38 -96 L-5 -108 M38 -96 L5 -108"/></g>')
    elif nom == 'grue':
        s.append('<path d="M-3 0 L-3 -122 L3 -122 L3 0 Z"/>')
        s.append('<path d="M-30 -118 L92 -118 L92 -124 L-30 -124 Z"/>')
        s.append('<rect x="-30" y="-118" width="14" height="12"/>')
        s.append('<path d="M0 -146 L-28 -124 M0 -146 L90 -124" fill="none" stroke="currentColor" stroke-width="1.6"/>')
        s.append('<path d="M-1.5 -146 L-1.5 -124 L1.5 -124 L1.5 -146 Z"/>')
        s.append('<path d="M60 -118 L60 -80" fill="none" stroke="currentColor" stroke-width="1.4"/>')
    return ''.join(s)


def trace_haut(nom):
    """Ce que l'on voit d'en haut, au pied de l'ombre."""
    return {'eolienne': '<path d="M-40 -4 L40 4" stroke="#8A8B95" stroke-width="3"/><circle r="4" fill="#8A8B95"/>',
            'chateau': '<circle r="30" fill="#C9CAD3" stroke="#8A8B95" stroke-width="1.5"/>',
            'pylone': '<rect x="-12" y="-12" width="24" height="24" fill="none" stroke="#8A8B95" stroke-width="2"/>'
                      '<path d="M-12 -12 L12 12 M12 -12 L-12 12 M-36 0 L36 0" stroke="#8A8B95" stroke-width="2"/>',
            'grue': '<path d="M-30 0 L92 0" stroke="#8A8B95" stroke-width="4"/><rect x="-5" y="-5" width="10" height="10" fill="#8A8B95"/>'}[nom]


def ombres(lg):
    noms = {'fr': ['Une éolienne', 'Un château d’eau', 'Un pylône électrique', 'Une grue'],
            'en': ['A wind turbine', 'A water tower', 'A power pylon', 'A crane']}[lg]
    titre = {'fr': 'Quatre ombres portées, vues d’avion', 'en': 'Four cast shadows, seen from the air'}[lg]
    o = []
    for k, nom in enumerate(['eolienne', 'chateau', 'pylone', 'grue']):
        x = 6 + k * 189
        o.append(f'<rect x="{x}" y="6" width="181" height="262" rx="10" fill="#E8ECDB" stroke="#D8DAEC" stroke-width="1.5"/>')
        o.append(T(x + 20, 34, 'ABCD'[k], 's-titre', style='font-size:24px'))
        bx, by = x + 128, 236
        o.append(f'<g transform="translate({bx} {by}) rotate(-50)" fill="{OMBRE}" color="{OMBRE}" opacity="0.88">{silhouette(nom)}</g>')
        o.append(f'<g transform="translate({bx} {by})">{trace_haut(nom)}</g>')
        o.append(f'<g class="s-apparait">{T(x + 90, 292, noms[k], "s-orange", style="font-size:17px")}</g>')
    # le soleil, en bas à droite (sud-est)
    o.append(f'<circle cx="752" cy="290" r="8" fill="{ORANGE}"/>')
    return svg('0 0 760 304', titre, o)


ecrire('ombres-portees.svg', ombres('fr'), ombres('en'))


# ------------------------------------------------------------------ indices de l'archéologie aérienne
def archeo(lg):
    t = {'fr': ['Indices phytographiques et sciographiques', 'Indices phytographiques : la culture, en été sec',
                'fossé comblé : elle pousse mieux,', 'plus haute et plus verte',
                'mur enfoui : elle pousse mal,', 'plus basse, elle jaunit tôt',
                'vu d’avion', 'Indice sciographique', 'lumière rasante :', 'le relief arasé fait une ombre',
                'terre arable', 'sous-sol'],
         'en': ['Crop marks and shadow marks', 'Crop marks: the crop, in a dry summer',
                'filled-in ditch: it grows better,', 'taller and greener',
                'buried wall: it grows poorly,', 'shorter, yellowing early',
                'seen from the air', 'Shadow mark', 'grazing light:', 'the levelled bank casts a shadow',
                'topsoil', 'subsoil']}[lg]
    o = [T(250, 26, t[1], 's-titre', style='font-size:18px')]
    sol, terre = 176, 200
    o.append(f'<rect x="20" y="{sol}" width="460" height="{terre - sol}" fill="#B89B74"/>')
    o.append(f'<rect x="20" y="{terre}" width="460" height="78" fill="#E9E1CC"/>')
    o.append(f'<path d="M110 {terre} L118 262 Q140 274 162 262 L170 {terre} Z" fill="#7A5E3E"/>')
    for i in range(4):
        for j in range(3):
            o.append(f'<rect x="{318 + j * 18}" y="{204 + i * 14}" width="16" height="12" rx="2" fill="#A3A4AE" stroke="#7E7F8A"/>')
    o.append(T(30, 222, t[10], 's-petit', anchor='start', style='font-size:12px'))
    o.append(T(30, 262, t[11], 's-petit', anchor='start', style='font-size:12px'))
    for x in range(28, 478, 9):
        if 104 <= x <= 176:
            h, c = 68, '#3F7A2E'
        elif 306 <= x <= 376:
            h, c = 26, '#D2B85A'
        else:
            h, c = 46, '#9DB46A'
        o.append(f'<path d="M{x} {sol} L{x} {sol - h}" stroke="{c}" stroke-width="3.2" stroke-linecap="round"/>')
        o.append(f'<path d="M{x} {sol - h + 6} l-4 -7 M{x} {sol - h + 6} l4 -7" stroke="{c}" stroke-width="2"/>')
    o.append(T(140, 70, t[2], style=f'font-size:13.5px;fill:{ENCRE}'))
    o.append(T(140, 87, t[3], style=f'font-size:13.5px;fill:{ENCRE};font-weight:700'))
    o.append(T(350, 92, t[4], style=f'font-size:13.5px;fill:{ENCRE}'))
    o.append(T(350, 109, t[5], style=f'font-size:13.5px;fill:{ENCRE};font-weight:700'))
    # vu d'avion : la même bande de champ, vue d'en haut
    y0 = 296
    o.append(f'<rect x="20" y="{y0}" width="460" height="34" fill="#9DB46A"/>')
    o.append(f'<rect x="104" y="{y0}" width="72" height="34" fill="#3F7A2E"/>')
    o.append(f'<rect x="306" y="{y0}" width="70" height="34" fill="#D9C66C"/>')
    o.append(T(250, y0 + 54, t[6], 's-petit', style='font-size:13px;font-style:italic'))
    # indice sciographique
    xs = 520
    o.append(f'<rect x="{xs}" y="6" width="234" height="368" rx="10" class="s-fond"/>')
    o.append(T(xs + 117, 34, t[7], 's-titre', style='font-size:18px'))
    o.append(f'<circle cx="{xs + 206}" cy="96" r="14" fill="{ORANGE}"/>')
    for k in range(3):
        o.append(f'<path d="M{xs + 190} {96 + k * 9} L{xs + 30} {214 + k * 9}" stroke="{ORANGE}" stroke-width="1.4" stroke-dasharray="5 5"/>')
    sol2 = 236
    o.append(f'<path d="M{xs + 12} {sol2} L{xs + 92} {sol2} Q{xs + 117} {sol2 - 16} {xs + 142} {sol2} L{xs + 222} {sol2} L{xs + 222} {sol2 + 50} L{xs + 12} {sol2 + 50} Z" fill="#B89B74"/>')
    o.append(f'<path d="M{xs + 64} {sol2} L{xs + 104} {sol2} Q{xs + 112} {sol2 - 9} {xs + 117} {sol2 - 15} Z" fill="{OMBRE}" opacity="0.75"/>')
    o.append(T(xs + 117, 310, t[8], style=f'font-size:13.5px;fill:{ENCRE}'))
    o.append(T(xs + 117, 328, t[9], style=f'font-size:13.5px;fill:{ENCRE};font-weight:700'))
    return svg('0 0 760 380', t[0], o)


ecrire('indices-archeo.svg', archeo('fr'), archeo('en'))


# ------------------------------------------------------------------ chronologie relative
# Un paysage inventé, vu d'avion : six tracés qui se recoupent. Ce qui recoupe est plus récent.
def chronologie(lg):
    t = {'fr': 'Six tracés qui se recoupent', 'en': 'Six features that cross each other'}[lg]
    o = ['<defs><clipPath id="chrono-cadre"><rect x="4" y="4" width="752" height="332" rx="10"/></clipPath></defs>',
         '<g clip-path="url(#chrono-cadre)">', '<rect x="4" y="4" width="752" height="332" fill="#EEF0E2"/>']
    # A : l'ancien méandre, comblé (une large bande plus humide, aux bords flous)
    o.append('<path d="M-10 70 C 120 30, 160 190, 280 170 S 420 40, 520 110 S 640 300, 780 250" fill="none" '
             'stroke="#C9D8C4" stroke-width="46" stroke-linecap="round"/>')
    # C : des parcelles en lanières, perpendiculaires à la voie B
    import itertools
    ux, uy = 680 / math.hypot(680, 260), -260 / math.hypot(680, 260)     # sens de la voie
    nx, ny = -uy, ux
    teintes = itertools.cycle(['#DDE3C2', '#E9E3C4', '#D3DDB6', '#E3E8CF'])
    for k in range(-14, 30):
        cxp, cyp = 40 + ux * (k * 22 + 11), 300 + uy * (k * 22 + 11)
        for cote in (-1, 1):
            p1 = (cxp - ux * 10 + cote * nx * 6, cyp - uy * 10 + cote * ny * 6)
            p2 = (cxp + ux * 10 + cote * nx * 6, cyp + uy * 10 + cote * ny * 6)
            p3 = (p2[0] + cote * nx * 120, p2[1] + cote * ny * 120)
            p4 = (p1[0] + cote * nx * 120, p1[1] + cote * ny * 120)
            o.append('<path d="M{:.0f} {:.0f} L{:.0f} {:.0f} L{:.0f} {:.0f} L{:.0f} {:.0f} Z" fill="{}" opacity="0.85"/>'
                     .format(*p1, *p2, *p3, *p4, next(teintes)))
    # B : la voie droite
    o.append('<path d="M40 300 L720 40" stroke="#B59C70" stroke-width="7"/>')
    # D : la voie ferrée, qui coupe les lanières sans les suivre
    o.append('<path id="chrono-fer" d="M-10 150 C 200 170, 420 330, 780 250" fill="none" stroke="#55565F" stroke-width="5"/>')
    o.append('<path d="M-10 150 C 200 170, 420 330, 780 250" fill="none" stroke="#EEF0E2" stroke-width="2" stroke-dasharray="3 7"/>')
    # E : l'autoroute, qui passe au-dessus de la voie ferrée (pont)
    o.append('<path d="M470 340 C 520 230, 560 140, 640 -10" fill="none" stroke="#9A9BA6" stroke-width="20"/>')
    o.append('<path d="M470 340 C 520 230, 560 140, 640 -10" fill="none" stroke="#FFFFFF" stroke-width="1.5" stroke-dasharray="10 10"/>')
    o.append('<path d="M512 268 L540 270 M500 290 L530 296" stroke="#2B2B33" stroke-width="2.5"/>')
    # F : le lotissement en chantier, branché sur l'autoroute (terre nue, voies en boucle, quelques maisons)
    o.append('<path d="M640 120 L740 120 L740 200 L640 200 Z" fill="#E2D3B5"/>')
    o.append('<path d="M600 155 L655 160 C 700 125, 735 150, 715 175 C 690 200, 655 180, 655 160" fill="none" stroke="#C8B48E" stroke-width="7"/>')
    for (hx, hy) in [(668, 132), (690, 128), (712, 140), (722, 182), (676, 188)]:
        o.append(f'<rect x="{hx}" y="{hy}" width="11" height="9" fill="#C0504D"/>')
    o.append('</g>')
    o.append(f'<rect x="4" y="4" width="752" height="332" rx="10" fill="none" stroke="#D8DAEC" stroke-width="1.5"/>')
    for lettre, (lx, ly) in zip('ABCDEF', [(160, 66), (318, 202), (188, 300), (88, 186), (596, 72), (740, 104)]):
        o.append(f'<circle cx="{lx}" cy="{ly}" r="14" fill="{BLEU}"/>')
        o.append(T(lx, ly + 6, lettre, style='font-size:16px;font-weight:700;fill:#FFFFFF'))
    return svg('0 0 760 340', t, o)


ecrire('chronologie.svg', chronologie('fr'), chronologie('en'))


# ------------------------------------------------------------------ précision des interprètes et des machines
# Ordres de grandeur donnés par Marc Poupée (retours sur la V0) : ce ne sont pas des mesures de ce cours.
def precision(lg):
    t = {'fr': ['Précision de la production d’information géographique', ['Photo-interprète expert',
                'Classification experte', 'Apprentissage machine', 'Réseau de neurones'], 'très variable', '80 à 85 %'],
         'en': ['Accuracy of geographic information production', ['Expert photo interpreter',
                'Expert classification', 'Machine learning', 'Neural network'], 'highly variable', '80 to 85%']}[lg]
    x0, x1, v0, v1 = 270, 700, 50, 100

    def X(v):
        return x0 + (x1 - x0) * (v - v0) / (v1 - v0)
    o = []
    for v in range(50, 101, 10):
        o.append(f'<path d="M{X(v):.0f} 14 V214" stroke="#E4E5EE" stroke-width="1"/>')
        o.append(T(X(v), 236, f'{v} %' if lg == 'fr' else f'{v}%', 's-petit', style='font-size:13px'))
    o.append('<defs><pattern id="precision-hachure" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
             f'<rect width="8" height="8" fill="#E7E9F5"/><path d="M0 0 V8" stroke="{BLEU}" stroke-width="2" opacity="0.45"/></pattern></defs>')
    for k, nom in enumerate(t[1]):
        y = 22 + k * 50
        o.append(T(x0 - 14, y + 21, nom, anchor='end', style=f'font-size:16px;fill:{ENCRE}'))
        if k == 1:
            o.append(f'<rect x="{X(55):.0f}" y="{y + 4}" width="{X(92) - X(55):.0f}" height="26" rx="4" fill="url(#precision-hachure)"/>')
            o.append(T(X(92) + 10, y + 22, t[2], anchor='start', style=f'font-size:15px;fill:{ENCRE};font-style:italic'))
        elif k == 2:
            o.append(f'<rect x="{x0}" y="{y + 4}" width="{X(80) - x0:.0f}" height="26" rx="4" fill="{BLEU}"/>')
            o.append(f'<rect x="{X(80) + 2:.0f}" y="{y + 4}" width="{X(85) - X(80) - 2:.0f}" height="26" rx="4" fill="{BLEU}" opacity="0.35"/>')
            o.append(T(X(85) + 10, y + 22, t[3], anchor='start', style=f'font-size:15px;fill:{ENCRE};font-weight:700'))
        else:
            v = 95 if k == 0 else 92
            o.append(f'<rect x="{x0}" y="{y + 4}" width="{X(v) - x0:.0f}" height="26" rx="4" fill="{BLEU}"/>')
            o.append(T(X(v) + 10, y + 22, f'{v} %' if lg == 'fr' else f'{v}%', anchor='start', style=f'font-size:15px;fill:{ENCRE};font-weight:700'))
    # le graphique n'apparaît qu'avec la première réponse de la diapo (après le vote)
    return svg('0 0 760 246', t[0], ['<g class="s-apparait">'] + o + ['</g>'])


ecrire('precision.svg', precision('fr'), precision('en'))


# ------------------------------------------------------------------ l'unité minimale de collecte
# Une petite zone de 160 × 100 cellules de 10 m : 160 ha. Quatre occupations du sol, tirées d'un bruit lissé.
# Pour chaque unité minimale, les taches trop petites sont fondues dans la classe voisine la plus présente.
rng = np.random.default_rng(1962)
H, L = 100, 160
bruit = ndimage.gaussian_filter(rng.normal(size=(H, L)), 6.0)
bruit2 = ndimage.gaussian_filter(rng.normal(size=(H, L)), 1.6)
occ = np.digitize(bruit + 0.12 * bruit2, np.quantile(bruit + 0.12 * bruit2, [0.42, 0.68, 0.9]))   # 0..3
COULEURS = {0: (93, 140, 72), 1: (190, 214, 140), 2: (232, 205, 120), 3: (150, 150, 160)}
NOMS = {'fr': ['forêt', 'prairie', 'culture', 'bâti'], 'en': ['forest', 'meadow', 'cropland', 'built-up']}
HA_PAR_CELLULE = 0.01


def generaliser(carte, umc_ha):
    c = carte.copy()
    seuil = umc_ha / HA_PAR_CELLULE
    for _ in range(40):
        change = False
        for classe in range(4):
            etiq, n = ndimage.label(c == classe)
            if n == 0:
                continue
            tailles = ndimage.sum(np.ones_like(c), etiq, index=np.arange(1, n + 1))
            for i, t in enumerate(tailles, 1):
                if t < seuil:
                    tache = etiq == i
                    bord = ndimage.binary_dilation(tache) & ~tache
                    voisins = c[bord]
                    voisins = voisins[voisins != classe]
                    if len(voisins):
                        c[tache] = np.bincount(voisins, minlength=4).argmax()
                        change = True
        if not change:
            break
    return c


def taches(carte):
    return sum(ndimage.label(carte == k)[1] for k in range(4))


UMC = [(0.0, 'brut'), (0.5, '0,5 ha'), (2.25, '2,25 ha'), (25, '25 ha')]
resultats = []
for umc, nom in UMC:
    c = occ if umc == 0 else generaliser(occ, umc)
    resultats.append((umc, nom, c, taches(c), float((c != occ).mean() * 100)))


def image_umc(carte, titre, fichier):
    f = 5
    im = Image.new('RGB', (L * f, H * f + 46), (255, 255, 255))
    px = np.zeros((H, L, 3), dtype=np.uint8)
    for k, col in COULEURS.items():
        px[carte == k] = col
    im.paste(Image.fromarray(px).resize((L * f, H * f), Image.NEAREST), (0, 46))
    d = ImageDraw.Draw(im)
    try:
        police = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 24)
    except OSError:
        police = ImageFont.load_default()
    d.text((12, 10), titre, fill=(40, 59, 137), font=police)
    im.save(os.path.join(COURS, 'images', fichier), optimize=True)


for umc, nom, c, n, pc in resultats[1:]:
    etiq_fr = f'Unité minimale de collecte : {nom} — {n} taches'
    etiq_en = f'Minimum mapping unit: {nom.replace(",", ".")} — {n} patches'
    base = 'umc-' + nom.replace(',', '-').replace(' ', '')
    image_umc(c, etiq_fr, base + '.png')
    image_umc(c, etiq_en, base + '-en.png')


# ------------------------------------------------------------------ le profil du radiotélescope FAST
# Coupe de A (ouest) à B (est) par le centre de la parabole, sur l'image Pléiades du 2 mars 2016.
# Altitudes relatives (0 = le plus bas, 1 = le plus haut), lues sur l'image : ombres, pentes, routes.
# Retours de Marc sur la V0 : départ au milieu ; les lacets de la piste disent une première pente forte jusqu'à une
# crête, puis la descente vers le centre. Un troisième terme « v » marque une crête vive (anguleuse) ; les autres
# points sont arrondis (fonds, épaules).
# PROFIL INDICATIF, à valider par Marc ou à remplacer par une extraction d'un MNT (Copernicus DEM, par exemple).
profil = {
    "source": "Lecture de l'image Pléiades (2 mars 2016) ; profil indicatif, à valider",
    "points": [[0, 0.50], [0.07, 0.62], [0.13, 0.80], [0.17, 0.88, "v"], [0.23, 0.70], [0.28, 0.58],
               [0.31, 0.55, "v"], [0.37, 0.33], [0.443, 0.22], [0.52, 0.33], [0.585, 0.55, "v"],
               [0.64, 0.74], [0.70, 0.90, "v"], [0.77, 0.74], [0.84, 0.58], [0.90, 0.52], [0.96, 0.57], [1, 0.62]]
}
json.dump(profil, open(os.path.join(COURS, 'donnees', 'fast-profil.json'), 'w', encoding='utf-8'), ensure_ascii=False)


# ------------------------------------------------------------------ Flamanville : qui vit à moins de 100 km ?
# Terres : Natural Earth 1:10 m. Population : populations légales des communes (INSEE, via le jeu
# « découpage administratif » d'Etalab, v6), placées au point représentatif de chaque commune ; îles
# Anglo-Normandes : ordres de grandeur arrondis (Jersey, recensement 2021 ; Guernesey, Aurigny, Sercq).
FLAM = (-1.8819, 49.5366)
ILES = [('Jersey', -2.13, 49.21, 103000), ('Guernesey', -2.58, 49.46, 64000),
        ('Aurigny', -2.20, 49.71, 2000), ('Sercq', -2.36, 49.43, 500)]


def km(lon, lat):
    return ((lon - FLAM[0]) * math.cos(math.radians(FLAM[1])) * 111.32, (lat - FLAM[1]) * 110.57)


def carte_flamanville():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle, PathPatch
    from matplotlib.path import Path
    from shapely.geometry import shape, Point

    terres = shape(json.load(open(os.path.join(COURS, 'donnees', 'terres-cotentin.geojson')))['geometry'])
    communes = []
    with open(os.path.join(COURS, 'donnees', 'population-cotentin.csv'), encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter=';'):
            communes.append((r['nom'], float(r['lon']), float(r['lat']), int(r['population'])))
    lieux = communes + [(n, lo, la, p) for n, lo, la, p in ILES]

    # chiffres : population à moins de 100 km, part de terre dans le cercle
    dans = [(n, p) for n, lo, la, p in lieux if math.hypot(*km(lo, la)) <= 100]
    total = sum(p for _, p in dans)
    rng2 = np.random.default_rng(7)
    pts = rng2.uniform(-100, 100, size=(60000, 2))
    pts = pts[np.hypot(pts[:, 0], pts[:, 1]) <= 100]
    lon = FLAM[0] + pts[:, 0] / (math.cos(math.radians(FLAM[1])) * 111.32)
    lat = FLAM[1] + pts[:, 1] / 110.57
    from shapely import contains_xy
    part_terre = float(contains_xy(terres, lon, lat).mean())

    def polys(g):
        return list(g.geoms) if hasattr(g, 'geoms') else [g]

    for lg in ('fr', 'en'):
        fig, ax = plt.subplots(figsize=(8, 8), dpi=150)
        ax.set_facecolor('#DCE6F5')
        fig.patch.set_facecolor('#DCE6F5')
        for p in polys(terres):
            for rang, anneau in enumerate([p.exterior] + list(p.interiors)):
                xy = np.array([km(x, y) for x, y in anneau.coords])
                ax.add_patch(PathPatch(Path(xy), facecolor='#F4F1E8' if rang == 0 else '#DCE6F5',
                                       edgecolor='#9FA3B8', linewidth=0.6, zorder=1 + (rang > 0)))
        xs, ys, ss = [], [], []
        for n, lo, la, p in lieux:
            x, y = km(lo, la)
            xs.append(x); ys.append(y); ss.append(p / 160)
        ax.scatter(xs, ys, s=ss, color=BLEU, alpha=0.55, linewidths=0, zorder=3)
        ax.add_patch(Circle((0, 0), 100, fill=False, edgecolor=ORANGE, linewidth=2.2, linestyle=(0, (6, 4)), zorder=4))
        ax.plot([0], [0], marker='*', markersize=17, color=ORANGE, markeredgecolor='white', zorder=5)
        noms = {'fr': {'Flamanville': 'Flamanville', 'Cherbourg-en-Cotentin': 'Cherbourg', 'Saint-Lô': 'Saint-Lô',
                       'Caen': 'Caen', 'Jersey': 'Jersey', 'Guernesey': 'Guernesey', 'Granville': 'Granville',
                       'Coutances': 'Coutances', 'Bayeux': 'Bayeux', 'La Hague': 'La Hague'},
                'en': {'Flamanville': 'Flamanville', 'Cherbourg-en-Cotentin': 'Cherbourg', 'Saint-Lô': 'Saint-Lô',
                       'Caen': 'Caen', 'Jersey': 'Jersey', 'Guernesey': 'Guernsey', 'Granville': 'Granville',
                       'Coutances': 'Coutances', 'Bayeux': 'Bayeux', 'La Hague': 'La Hague'}}[lg]
        places = {n: (lo, la) for n, lo, la, p in lieux}
        for cle, dx, dy in [('Cherbourg-en-Cotentin', 4, 6), ('Saint-Lô', 4, 4), ('Caen', -6, 6), ('Jersey', -4, -9),
                            ('Guernesey', 3, -9), ('Granville', 5, -3), ('Coutances', 5, 0), ('Bayeux', 3, 5),
                            ('La Hague', -14, 5)]:
            if cle in places:
                x, y = km(*places[cle])
                ax.annotate(noms[cle], (x, y), xytext=(x + dx, y + dy), fontsize=10, color='#2B2B33', zorder=6)
        ax.annotate('Flamanville', (0, 0), xytext=(4, -9), fontsize=12, fontweight='bold', color='#2B2B33', zorder=6)
        ax.text(0, 103, '100 km', color=ORANGE, fontsize=11, fontweight='bold', ha='center', zorder=6)
        # légende des cercles
        for k, (p, txt) in enumerate([(10000, '10 000'), (50000, '50 000'), (100000, '100 000')]):
            ax.scatter([-104], [86 - k * 11], s=p / 160, color=BLEU, alpha=0.55, linewidths=0, zorder=6)
            ax.text(-96, 84 - k * 11, txt + (' hab.' if lg == 'fr' else ' inhab.'), fontsize=9, color='#2B2B33', zorder=6)
        ax.set_xlim(-118, 118); ax.set_ylim(-110, 112)
        ax.set_aspect('equal'); ax.axis('off')
        fig.subplots_adjust(0, 0, 1, 1)
        nom = 'carte-flamanville' + ('' if lg == 'fr' else '-en') + '.png'
        fig.savefig(os.path.join(COURS, 'images', nom), dpi=150, facecolor=fig.get_facecolor())
        plt.close(fig)
    return total, part_terre, sorted(dans, key=lambda x: -x[1])[:6]


flam = carte_flamanville()


# ------------------------------------------------------------------ l'Isle-Adam : CORINE Land Cover et BD Forêt V2
# Les deux captures de Marc couvrent la même emprise (barre d'échelle : 1 000 m = 93 pixels, mesurée).
def isle_adam():
    a = np.array(Image.open(os.path.join(COURS, 'images', 'isle-adam-clc.png')).convert('RGB')).astype(int)
    b = np.array(Image.open(os.path.join(COURS, 'images', 'isle-adam-bdforet.png')).convert('RGB')).astype(int)
    m = np.ones(a.shape[:2], bool); m[680:, 680:] = False          # cadre de l'échelle

    def proche(im, c, t=30):
        return np.abs(im - np.array(c)).sum(2) < t
    clc = proche(a, (128, 255, 0)) | proche(a, (166, 242, 0)) | proche(a, (77, 255, 0)) | proche(a, (0, 166, 0))
    bdf = (b[..., 1] > b[..., 0] + 40) & (b[..., 1] > b[..., 2] + 10)
    m_px = 1000 / 93
    ha = m.sum() * m_px ** 2 / 1e4
    res = {'emprise_km': (round(a.shape[1] * m_px / 1000, 1), round(a.shape[0] * m_px / 1000, 1)),
           'foret_clc': round(clc[m].mean() * 100, 1), 'foret_bdf': round(bdf[m].mean() * 100, 1),
           'seulement_clc_ha': round((clc & ~bdf)[m].mean() * ha, -1), 'seulement_bdf_ha': round((bdf & ~clc)[m].mean() * ha, -1),
           'accord': round(100 * (1 - (clc ^ bdf)[m].mean()), 1),
           'taches_clc': int(ndimage.label(clc & m)[1]), 'taches_bdf': int(ndimage.label(bdf & m)[1])}
    return res


iad = isle_adam()

# Valeurs citées dans le cours
print('UMC :', [(nom, n, round(pc, 1)) for umc, nom, c, n, pc in resultats])
print('part des classes (brut) :', [round(float((occ == k).mean() * 100), 1) for k in range(4)])
print('Flamanville : population à moins de 100 km =', flam[0], '; part de terre dans le cercle =', round(flam[1] * 100), '% ;', flam[2])
print("L'Isle-Adam :", iad)
