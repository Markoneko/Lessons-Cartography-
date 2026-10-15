#!/usr/bin/env python3
"""Un territoire fictif pour le cours « Cartography : Basics ».

    python3 outils/territoire-fictif.py cours/cartography-basics/donnees/territoire.json

Une centaine de communes inventées (diagramme de Voronoï découpé par un contour),
avec pour chacune une surface forestière et une surface en coupes rases.
Le taux de coupes est asymétrique et forme un foyer au nord-est, comme une attaque
de scolytes. Tout est tiré au hasard avec une graine fixe : le fichier est reproductible.

Ce territoire n'existe pas. Il est annoncé comme tel dans le cours.
Coordonnées en pixels : 800 × 560 ; 1 pixel = 75 m sur le terrain.
"""
import json
import math
import sys

import numpy as np
from scipy.spatial import Voronoi
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union

GRAINE = 2026
L, H = 800, 560
M_PAR_PX = 75.0
HA_PAR_PX2 = M_PAR_PX ** 2 / 10_000

rng = np.random.default_rng(GRAINE)

# Contour : un ovale bosselé
angles = np.linspace(0, 2 * math.pi, 90, endpoint=False)
rayon = 1 + 0.08 * np.sin(3 * angles + 0.7) + 0.05 * np.sin(5 * angles + 2.1) + 0.03 * np.sin(9 * angles)
contour = Polygon([(400 + 335 * r * math.cos(a), 280 + 232 * r * math.sin(a)) for a, r in zip(angles, rayon)])

# Germes : plus serrés à l'ouest (vallées peuplées, petites communes), plus lâches à l'est (montagne)
germes = []
while len(germes) < 110:
    x, y = rng.uniform(20, 780), rng.uniform(15, 545)
    if not contour.contains(Point(x, y)):
        continue
    densite = 1.0 - 0.75 * (x / L)          # 1 à l'ouest, 0,25 à l'est
    if rng.uniform() < densite and all((x - a) ** 2 + (y - b) ** 2 > 26 ** 2 for a, b in germes):
        germes.append((x, y))
# relaxation de Lloyd, deux passes, pour des formes plus régulières
for _ in range(2):
    pts = np.array(germes + [(-2000, -2000), (3000, -2000), (-2000, 3000), (3000, 3000)])
    vor = Voronoi(pts)
    nouveaux = []
    for i in range(len(germes)):
        region = vor.regions[vor.point_region[i]]
        poly = Polygon([vor.vertices[k] for k in region]).intersection(contour)
        nouveaux.append((poly.centroid.x, poly.centroid.y))
    germes = nouveaux

pts = np.array(germes + [(-2000, -2000), (3000, -2000), (-2000, 3000), (3000, 3000)])
vor = Voronoi(pts)
communes = []
for i in range(len(germes)):
    region = vor.regions[vor.point_region[i]]
    poly = Polygon([vor.vertices[k] for k in region]).intersection(contour)
    if poly.geom_type != 'Polygon' or poly.area < 50:
        continue
    communes.append(poly)

# Attributs
foyer = (610, 170)                     # le foyer de scolytes, au nord-est
donnees = []
for n, poly in enumerate(communes, 1):
    cx, cy = poly.centroid.x, poly.centroid.y
    surface_ha = poly.area * HA_PAR_PX2
    part_foret = float(np.clip(0.30 + 0.55 * (cx / L) + rng.normal(0, 0.08), 0.15, 0.92))
    foret_ha = surface_ha * part_foret
    d = math.hypot(cx - foyer[0], cy - foyer[1])
    taux = 1.2 + 16 * math.exp(-(d / 150) ** 2) + rng.gamma(1.3, 1.1)
    if rng.uniform() < 0.04:            # quelques coupes isolées, fortes
        taux += rng.uniform(8, 14)
    taux = round(float(min(taux, 32)), 1)
    coupes_ha = round(foret_ha * taux / 100)
    taux = round(100 * coupes_ha / foret_ha, 1) if foret_ha else 0.0
    xs, ys = poly.exterior.coords.xy
    chemin = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in zip(xs[:-1], ys[:-1])) + ' Z'
    donnees.append({
        'id': n,
        'chemin': chemin,
        'cx': round(cx, 1), 'cy': round(cy, 1),
        'surface_ha': round(surface_ha),
        'foret_ha': round(foret_ha),
        'coupes_ha': coupes_ha,
        'taux': taux,
    })

sortie = {
    'nom': 'Territoire fictif',
    'note': 'Territoire inventé, données simulées (outils/territoire-fictif.py, graine %d).' % GRAINE,
    'largeur': L, 'hauteur': H, 'metres_par_pixel': M_PAR_PX,
    'contour': 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in list(contour.exterior.coords)[:-1]) + ' Z',
    'communes': donnees,
}
chemin = sys.argv[1]
import os
os.makedirs(os.path.dirname(chemin), exist_ok=True)
json.dump(sortie, open(chemin, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
t = sorted(c['taux'] for c in donnees)
print(f"{len(donnees)} communes ; taux de {t[0]} à {t[-1]} % ; médiane {t[len(t)//2]} % ; "
      f"coupes totales {sum(c['coupes_ha'] for c in donnees)} ha ; {os.path.getsize(chemin)//1024} Ko")
