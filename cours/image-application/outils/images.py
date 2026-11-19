#!/usr/bin/env python3
"""Versions web des images de Marc, pour le cours « Image & Application ».

    python3 cours/image-application/outils/images.py

Lit images/originaux/, écrit les versions légères dans images/ et récrit images/correspondance.csv
(original ; version web ; largeur ; hauteur). Les originaux ne sont pas touchés.
Pour une nouvelle image : la déposer dans images/originaux/, puis ajouter une ligne à TRAVAUX.
"""
import csv
import os
import shutil

from PIL import Image

COURS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(COURS, 'images')
ORIG = os.path.join(IMG, 'originaux')
CSV = os.path.join(IMG, 'correspondance.csv')
LARGEUR_MAX = 1600

# (original, version web) ; une version .jpg est recompressée, un .png gardé sans perte, un .gif copié tel quel
TRAVAUX = [
    ('EMwithRadarLidar.png', 'spectre-xkcd.png'),
    ('MartianDune.png', 'mars-dunes.jpg'),
    ('PleiadesNeo-Arcachon-Octobre2021.png', 'pleiades-neo-arcachon.jpg'),
    ('OilSpillDetection.png', 'maree-noire-radar.jpg'),
    ('Grace.jpeg', 'grace.jpg'),
    ('2026-09-01-Sentinel-1_IW_RGB_Ratio.jpg', 'manche-sentinel-1.jpg'),
    ('IGN-FrocalquierCenter.png', 'forcalquier-ortho.jpg'),
    ('NightAcquisition.jpg', 'denver-nuit.jpg'),
    ('abc2992-f1.jpeg', 'chine-no2-covid.jpg'),
    ('Sahara-RVB.png', 'sahara-rvb.jpg'),
    ('Sahara-BIOMASS.png', 'sahara-biomass.jpg'),
    ('MayanCity.png', 'cite-maya-lidar.jpg'),
    ('soloti.gif', 'soloti.gif'),
    ('sargasses-overview-screenshot.jpg', 'sargasses.jpg'),
    ('ArgoSensor.png', 'flotteur-argo.jpg'),
    ('S2-Bresil.png', 'bolivie-sentinel-2.jpg'),
    ('S2-Biomass.png', 'bolivie-biomass.jpg'),
]


def reduire(im, cote=LARGEUR_MAX):
    if max(im.size) > cote:
        f = cote / max(im.size)
        im = im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)
    return im


def main():
    with open(CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['originale', 'version_web', 'largeur', 'hauteur'])
        for source, cible in TRAVAUX:
            src, dst = os.path.join(ORIG, source), os.path.join(IMG, cible)
            if cible.endswith('.gif'):
                shutil.copyfile(src, dst)
                im = Image.open(dst)
            else:
                im = reduire(Image.open(src))
                if cible.endswith('.jpg'):
                    im.convert('RGB').save(dst, quality=86, optimize=True)
                else:
                    im.save(dst, optimize=True)
            w.writerow([source, cible, im.width, im.height])
            print(f'{cible:30s} {im.width} × {im.height}  {os.path.getsize(dst) // 1024} ko')


if __name__ == '__main__':
    main()
