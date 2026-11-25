#!/usr/bin/env python3
"""La petite carte 8 bits de la commande du préfet : la région de Saumos, en gros pixels.

    python3 cours/image-application/outils/carte-saumos.py

Source : l'export Copernicus Browser du 21 juillet 2026 en fausses couleurs (Sentinel-2 L2A, B8-B4-B3),
grille commune des exports (voir images-saumos.py). Chaque gros pixel prend la classe dominante de ses pixels :
eau (le proche infrarouge s'effondre, ou le rouge le dépasse), bâti (proche infrarouge et rouge voisins),
forêt (proche infrarouge fort, rouge faible), terres ouvertes (le reste). Les noms de lieux sont posés
par la page, en police pixel, à partir de leurs coordonnées (donnees/saumos.json, clé « carte »).
"""
import os

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
COURS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(COURS, "source", "Cas1-Saumos", "Browser_imagesS2-21Juill2026",
                   "2026-07-21-00_00_2026-07-21-23_59_Sentinel-2_L2A_False_color.tiff")
X0, Y0, DX, DY = -2.04895, 45.734943, 0.0008668212, 0.0006127846683893188
EMPRISE = dict(lon0=-1.45, lon1=-0.45, lat0=44.55, lat1=45.25)
CASE = 16                                   # pixels de l'export par gros pixel (environ 1,1 km)
PALETTE = {"eau": (46, 86, 170), "eau-claire": (79, 130, 214), "bati": (150, 150, 162),
           "foret": (34, 102, 52), "ouvert": (138, 178, 74), "sable": (232, 214, 150)}


def main():
    im = Image.open(SRC).convert("RGB")
    E = EMPRISE
    boite = (round((E["lon0"] - X0) / DX), round((Y0 - E["lat1"]) / DY), round((E["lon1"] - X0) / DX), round((Y0 - E["lat0"]) / DY))
    a = np.asarray(im.crop(boite)).astype(int)
    pir, rouge, vert = a[..., 0], a[..., 1], a[..., 2]
    classe = np.full(pir.shape, 3)                          # 3 : terres ouvertes
    classe[(pir > 1.9 * rouge) & (pir < 185)] = 2           # 2 : forêt
    classe[(abs(pir - rouge) < 28) & (pir > 70)] = 1        # 1 : bâti, sol nu
    classe[(pir > 175) & (rouge > 150)] = 4                 # 4 : sable des dunes, très clair
    classe[(pir < 48) | (rouge - pir > 10)] = 0             # 0 : eau
    h, w = classe.shape[0] // CASE, classe.shape[1] // CASE
    noms = ["eau", "bati", "foret", "ouvert", "sable"]
    sortie = Image.new("RGB", (w, h))
    px = sortie.load()
    for j in range(h):
        for i in range(w):
            bloc = classe[j * CASE:(j + 1) * CASE, i * CASE:(i + 1) * CASE]
            n = np.bincount(bloc.ravel(), minlength=5)
            k = int(n.argmax())
            if k != 0 and n[0] > 0.35 * bloc.size:          # une côte, un lac : l'eau gagne dès un bon tiers
                k = 0
            nom = noms[k]
            if nom == "eau" and n[0] < 0.7 * bloc.size:
                nom = "eau-claire"
            px[i, j] = PALETTE[nom]
    chemin = os.path.join(COURS, "images", "saumos", "carte-8bit.png")
    sortie.save(chemin)
    # l'emprise exacte des gros pixels, à reporter dans donnees/saumos.json (clé « carte »)
    lon0, lat1 = X0 + boite[0] * DX, Y0 - boite[1] * DY
    exacte = dict(lon0=round(lon0, 5), lon1=round(lon0 + w * CASE * DX, 5), lat0=round(lat1 - h * CASE * DY, 5), lat1=round(lat1, 5))
    print(os.path.relpath(chemin, COURS), sortie.size, "emprise", exacte)


if __name__ == "__main__":
    main()
