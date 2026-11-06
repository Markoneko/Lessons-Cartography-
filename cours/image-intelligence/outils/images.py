#!/usr/bin/env python3
"""Versions web des images de Marc, pour le cours « Image Intelligence ».

    python3 cours/image-intelligence/outils/images.py

Lit images/originaux/ et images/quizz/, écrit les versions légères dans images/ et complète
images/correspondance.csv (original ; version web ; largeur ; hauteur). Les originaux ne sont pas touchés.
"""
import csv
import os
import shutil

import numpy as np
from PIL import Image, ImageDraw, ImageFont

COURS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(COURS, 'images')
ORIG = os.path.join(IMG, 'originaux')
CSV = os.path.join(IMG, 'correspondance.csv')
LARGEUR_MAX = 1600


def police(taille, gras=True):
    nom = 'DejaVuSans-Bold.ttf' if gras else 'DejaVuSans.ttf'
    try:
        return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/' + nom, taille)
    except OSError:
        return ImageFont.load_default()


def reduire(im, cote=LARGEUR_MAX):
    if max(im.size) > cote:
        f = cote / max(im.size)
        im = im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)
    return im


def sans_curseur(im, boite):
    """Efface un pointeur de souris resté dans une capture de carte : dans sa boîte, tout pixel dont la
    couleur n'est pas une couleur de la légende (présente sur plus de 300 pixels) prend la couleur la plus
    fréquente de son voisinage."""
    a = np.array(im.convert('RGB')).astype(int)
    x0, y0, x1, y1 = boite
    codes = a[..., 0] * 65536 + a[..., 1] * 256 + a[..., 2]
    valeurs, comptes = np.unique(codes, return_counts=True)
    legende = set(valeurs[comptes > 300].tolist())
    masque = np.zeros(codes.shape, bool)
    bloc = codes[y0:y1, x0:x1]
    masque[y0:y1, x0:x1] = ~np.isin(bloc, list(legende))
    for _ in range(12):
        ys, xs = np.nonzero(masque)
        if not len(ys):
            break
        for y, x in zip(ys, xs):
            vois = [tuple(a[yy, xx]) for yy in range(y - 2, y + 3) for xx in range(x - 2, x + 3)
                    if 0 <= yy < a.shape[0] and 0 <= xx < a.shape[1] and not masque[yy, xx]]
            if vois:
                a[y, x] = max(set(vois), key=vois.count)
                masque[y, x] = False
    return Image.fromarray(a.astype(np.uint8))


def centre_equestre(im):
    """Retire les commandes de la visionneuse (zoom, vignette, échelle écrite) et redessine l'échelle :
    20 m font 130 pixels sur la capture (barre « 0 — 20 m » de la visionneuse, mesurée)."""
    im = im.convert('RGB').crop((60, 0, 1204, 712))
    d = ImageDraw.Draw(im)
    x0, y0, l = 24, im.height - 34, 130
    d.rectangle((x0 - 10, y0 - 26, x0 + l + 64, y0 + 18), fill=(255, 255, 255))
    d.line((x0, y0, x0 + l, y0), fill=(40, 40, 50), width=4)
    for x in (x0, x0 + l):
        d.line((x, y0 - 7, x, y0 + 7), fill=(40, 40, 50), width=3)
    d.text((x0 + l + 8, y0 - 12), '20 m', fill=(40, 40, 50), font=police(18))
    d.text((x0, y0 - 25), '0', fill=(40, 40, 50), font=police(14, False))
    return im


# (original, version web, traitement)
TRAVAUX = [
    ('originaux/PlanPennemunde.jpg', 'peenemunde-plan.jpg', lambda im: reduire(im.convert('RGB'), 1500)),
    ('originaux/Frise-Intelligence.png', 'frise-intelligence.png', lambda im: im),
    ('originaux/Star-City.png', 'star-city.jpg', lambda im: reduire(im.convert('RGB'))),
    ('originaux/Colin_Powell_official_Secretary_of_State_photo.jpg', 'colin-powell.jpg', lambda im: im.convert('RGB')),
    ('originaux/IsleAdamCLC.png', 'isle-adam-clc.png', lambda im: sans_curseur(im, (330, 160, 352, 190))),
    ('originaux/IsleAdamBDForetV2.png', 'isle-adam-bdforet.png', lambda im: sans_curseur(im, (330, 115, 352, 145))),
    ('originaux/flair1_ortho.png', 'flair-ortho.png', lambda im: im.convert('RGB')),
    ('originaux/flair1_labels.png', 'flair-etiquettes.png', lambda im: im.convert('RGB')),
    ('originaux/Unet-DetectBati.png', 'unet-reference.png', lambda im: im.convert('RGB')),
    ('originaux/Unet-Detection.png', 'unet-prediction.png', lambda im: im.convert('RGB')),
    ('originaux/AngkorVAt_Lidar.png', 'angkor-lidar.png', lambda im: im.convert('RGB')),
    ('originaux/Centre_equestre.png', 'centre-equestre.jpg', centre_equestre),
    ('originaux/Cambrai-1917.jpg', 'cambrai-1917.jpg', lambda im: reduire(im.convert('RGB'))),
    ('originaux/PXL_20250930_173652676~2.jpg', 'ia-emotion.jpg', lambda im: reduire(im.convert('RGB'))),
    ('originaux/PXL_20261006_182859009.jpg', 'ia-textures-1.jpg', lambda im: reduire(im.convert('RGB'))),
    ('originaux/PXL_20261006_182903643.jpg', 'ia-textures-2.jpg', lambda im: reduire(im.convert('RGB'))),
    ('originaux/IMG-20261029-WA0000.jpg', 'reel-etrange.jpg', lambda im: reduire(im.convert('RGB'), 1400)),
    # deuxième salve
    ('originaux/TourRosny.png', 'tour-rosny.jpg', lambda im: reduire(im.convert('RGB'))),
    ('quizz/Base27.jfif', 'base-27.jpg', lambda im: reduire(im.convert('RGB'))),
    ('originaux/YEUXDOR.jfif', 'yeux-dor.jpg', lambda im: reduire(im.convert('RGB'), 1000)),
    # la même emprise que flamanville.jpg (images/quizz/11.JPG), en infrarouge couleur, 2015 : on la cale sur sa taille
    ('quizz/BDotho2015-Flamanville.png', 'flamanville-irc-2015.jpg',
     lambda im: im.convert('RGB').resize(Image.open(os.path.join(IMG, 'flamanville.jpg')).size, Image.LANCZOS)),
    ('originaux/MottefeodaleRely-sciographie.png', 'motte-rely.jpg', lambda im: im.convert('RGB')),
    ('originaux/mississippi_meanders_etm_1999265.jpg', 'mississippi-meandres.jpg', lambda im: im.convert('RGB')),
    ('originaux/CoerusNoirs.png', 'fiction-coeurs-noirs.jpg', lambda im: reduire(im.convert('RGB'), 900)),
    ('originaux/Bureaudeslegendes.png', 'fiction-bureau-des-legendes.jpg', lambda im: reduire(im.convert('RGB'), 1100)),
    ('originaux/GoldenEye.jpg', 'fiction-goldeneye.jpg', lambda im: reduire(im.convert('RGB'), 900)),
    ('originaux/Al_ouestriendenouveaux.jpg', 'fiction-a-l-ouest.jpg', lambda im: reduire(im.convert('RGB'), 900)),
    ('originaux/Wonder_Woman._2017.png', 'fiction-wonder-woman.jpg', lambda im: reduire(im.convert('RGB'), 1100)),
    # les animations sont copiées telles quelles (Pillow ne garderait qu'une image)
    ('originaux/Novoozernoye.gif', 'novoozernoye.gif', None),
    ('originaux/CampSoleti.gif', 'soloti.gif', None),
    # images de la V0, recadrées sur la partie utile (sans le cadre ni les mentions de l'application)
    ('quizz/IA-progressandlimits/1641941583914.jpg', 'ia-2022-vue-aerienne.jpg',
     lambda im: reduire(im.convert('RGB').crop((88, 205, 1000, 1640)), 1400)),
]


def main():
    lignes = {}
    if os.path.exists(CSV):
        with open(CSV, encoding='utf-8') as f:
            for r in csv.reader(f, delimiter=';'):
                if r and r[0] != 'originale':
                    lignes[r[1]] = r
    for source, cible, traitement in TRAVAUX:
        if traitement is None:
            shutil.copyfile(os.path.join(IMG, source), os.path.join(IMG, cible))
            im = Image.open(os.path.join(IMG, cible))
            lignes[cible] = [source, cible, str(im.width), str(im.height)]
            print(f'{cible:28s} {im.width} × {im.height} (copie, {getattr(im, "n_frames", 1)} image(s))')
            continue
        im = traitement(Image.open(os.path.join(IMG, source)))
        chemin = os.path.join(IMG, cible)
        if cible.endswith('.jpg'):
            im.convert('RGB').save(chemin, quality=86, optimize=True)
        else:
            im.save(chemin, optimize=True)
        lignes[cible] = [source, cible, str(im.width), str(im.height)]
        print(f'{cible:28s} {im.width} × {im.height}')
    with open(CSV, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['originale', 'version_web', 'largeur', 'hauteur'])
        for r in lignes.values():
            w.writerow(r)


if __name__ == '__main__':
    main()
