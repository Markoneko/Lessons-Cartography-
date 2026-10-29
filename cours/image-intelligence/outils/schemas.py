#!/usr/bin/env python3
"""Schémas et données du cours « Image Intelligence », en français et en anglais.

    python3 cours/image-intelligence/outils/schemas.py

Écrit images/schemas/ (fr), images/schemas/en/ (en), les trois images de l'unité minimale de
collecte dans images/, et le profil du radiotélescope FAST dans donnees/.
Les valeurs citées dans le cours sont calculées ici et imprimées à la fin.
"""
import json
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


# ------------------------------------------------------------------ trois raisonnements
def raisonnements(lg):
    t = {'fr': ['Induction, déduction, abduction',
                [('Induction', ['des cas observés', '→ une règle'], 'Chaque dôme vu jusqu’ici', 'abritait un réacteur.'),
                 ('Déduction', ['une règle + un cas', '→ une conséquence'], 'Un réacteur rejette de la chaleur :', 'il lui faut de l’eau froide.'),
                 ('Abduction', ['un indice surprenant', '→ la meilleure explication'], 'Des remous en mer, loin du bord :', 'sans doute un rejet d’eau.')],
                'Le faisceau d’indices', 'hypothèse', ['forme', 'site', 'association', 'temps']],
         'en': ['Induction, deduction, abduction',
                [('Induction', ['observed cases', '→ a rule'], 'Every dome seen so far', 'housed a reactor.'),
                 ('Deduction', ['a rule + a case', '→ a consequence'], 'A reactor gives off heat:', 'it needs cold water.'),
                 ('Abduction', ['a surprising clue', '→ the best explanation'], 'Boils at sea, far from shore:', 'probably a water outfall.')],
                'The bundle of clues', 'hypothesis', ['shape', 'site', 'association', 'time']]}[lg]
    o = []
    for k, (nom, def_, ex1, ex2) in enumerate(t[1]):
        x = 10 + k * 250
        o.append(f'<rect x="{x}" y="10" width="236" height="200" rx="12" class="s-fond"/>')
        o.append(T(x + 118, 44, nom, 's-titre', style='font-size:22px'))
        o.append(T(x + 118, 76, def_[0], style=f'font-size:16px;fill:{ENCRE}'))
        o.append(T(x + 118, 98, def_[1], style=f'font-size:16px;fill:{BLEU};font-weight:700'))
        o.append(f'<path d="M{x + 30} 120 H{x + 206}" stroke="#D8DAEC" stroke-width="1.5"/>')
        o.append(T(x + 118, 150, ex1, 's-petit', style='font-size:14px;font-style:italic'))
        o.append(T(x + 118, 172, ex2, 's-petit', style='font-size:14px;font-style:italic'))
    # le faisceau : quatre indices convergent vers une hypothèse
    o.append(T(380, 252, t[2], 's-titre'))
    cx, cy = 380, 330
    for k, mot in enumerate(t[4]):
        x0 = 90 + k * 190
        o.append(f'<path d="M{x0} 290 Q {x0 + (cx - x0) * 0.4} 300 {cx} {cy - 26}" fill="none" stroke="{ORANGE}" stroke-width="3" marker-end="url(#fleche)"/>')
        o.append(f'<circle cx="{x0}" cy="285" r="5" fill="{ORANGE}"/>')
        o.append(T(x0, 278, mot, 's-petit', style='font-size:14px'))
    o.append(f'<rect x="{cx - 80}" y="{cy - 24}" width="160" height="44" rx="22" fill="{BLEU}"/>')
    o.append(T(cx, cy + 5, t[3], style='font-size:18px;font-weight:700;fill:#FFFFFF'))
    defs = (f'<defs><marker id="fleche" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            f'<path d="M0 0 L10 5 L0 10 z" fill="{ORANGE}"/></marker></defs>')
    return svg('0 0 760 370', t[0], [defs] + o)


ecrire('raisonnements.svg', raisonnements('fr'), raisonnements('en'))


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
# PROFIL INDICATIF, à valider par Marc ou à remplacer par une extraction d'un MNT (Copernicus DEM, par exemple).
profil = {
    "source": "Lecture de l'image Pléiades (2 mars 2016) ; profil indicatif, à valider",
    "points": [[0, 0.70], [0.08, 0.78], [0.15, 0.71], [0.22, 0.80], [0.28, 0.62], [0.305, 0.52],
               [0.36, 0.34], [0.40, 0.26], [0.443, 0.22], [0.49, 0.26], [0.53, 0.34], [0.585, 0.52],
               [0.62, 0.70], [0.70, 0.88], [0.76, 0.80], [0.84, 0.62], [0.88, 0.55], [0.95, 0.62], [1, 0.68]]
}
json.dump(profil, open(os.path.join(COURS, 'donnees', 'fast-profil.json'), 'w', encoding='utf-8'), ensure_ascii=False)

# Valeurs citées dans le cours
print('UMC :', [(nom, n, round(pc, 1)) for umc, nom, c, n, pc in resultats])
print('part des classes (brut) :', [round(float((occ == k).mean() * 100), 1) for k in range(4)])
