#!/usr/bin/env python3
"""Images de l'atelier Saumos : versions web, dans images/saumos/.

    python3 cours/image-application/outils/images-saumos.py

Sources :
  - images/originaux/saumos/ : les images de la séance prépa (saumos-seance.html), extraites telles quelles
    (photo d'accroche, 37 images Meteosat, compositions SWIR des 26 juillet et 4 septembre, bandes B8A et B12,
    dNBR) ; leur emprise est GEO ci-dessous ;
  - source/Cas1-Saumos/ : les exports du Copernicus Browser de Marc (21 et 26 juillet, quatre compositions),
    les anomalies thermiques Terra (21 au 28 juillet), le contexte Reuters / EMSR899.
Le dNBR reste en PNG sans perte : l'atelier lit la couleur de ses pixels pour donner la classe de sévérité.
"""
import os
import shutil

from PIL import Image

Image.MAX_IMAGE_PIXELS = None
COURS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIG = os.path.join(COURS, "images", "originaux", "saumos")
SRC = os.path.join(COURS, "source", "Cas1-Saumos")
SORTIE = os.path.join(COURS, "images", "saumos")

# Emprise des images de la séance prépa (1212 × 732 px), en degrés WGS 84
GEO = dict(lon0=-1.239395, lon1=-0.803229, lat0=44.715026, lat1=44.9784)
# Fenêtre des exports du Browser : un peu plus large que GEO, pour garder le panache de fumée
FENETRE = dict(lon0=-1.32, lon1=-0.72, lat0=44.66, lat1=45.03)
COMPOS = {
    "Highlight_Optimized_Natural_Color_": "naturelles",
    "False_color": "infrarouge",
    "SWIR": "swir",
    "Wildfires": "feux",
}


def jpeg(im, chemin, cote=None, qualite=85):
    if cote and max(im.size) > cote:
        f = cote / max(im.size)
        im = im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)
    im.convert("RGB").save(chemin, quality=qualite, optimize=True)
    print(f"{os.path.relpath(chemin, COURS):45s} {im.width} × {im.height}  {os.path.getsize(chemin) // 1024} ko")


def main():
    os.makedirs(SORTIE, exist_ok=True)
    # 1. la séance prépa, sans retouche
    for nom in ["accroche", "s2_26_swir", "s2_04_swir", "m_b8a", "m_b12"]:
        jpeg(Image.open(os.path.join(ORIG, nom + ".jpg")), os.path.join(SORTIE, nom.replace("_", "-") + ".jpg"))
    shutil.copyfile(os.path.join(ORIG, "m_dnbr.png"), os.path.join(SORTIE, "m-dnbr.png"))
    for k in range(37):
        jpeg(Image.open(os.path.join(ORIG, f"mtg_{k:02d}.jpg")), os.path.join(SORTIE, f"mtg-{k:02d}.jpg"), qualite=78)
    # 2. le contexte Reuters / EMSR899 et les anomalies thermiques Terra
    jpeg(Image.open(os.path.join(SRC, "Contexte-Reuters-EMSR899 Situational Reporting.png")), os.path.join(SORTIE, "contexte-emsr899.jpg"))
    for j in range(21, 29):
        jpeg(Image.open(os.path.join(SRC, "Terra", f"TerraThermalAnomalies-2026-07-{j}.jpeg")), os.path.join(SORTIE, f"terra-07-{j}.jpg"))
    # 3. les exports du Browser, recadrés sur la fenêtre
    for date, dossier in [("21", "Browser_imagesS2-21Juill2026"), ("26", "Browser_imagesS2-26Juill2026")]:
        for cle, nom in COMPOS.items():
            src = os.path.join(SRC, dossier, f"2026-07-{date}-00_00_2026-07-{date}-23_59_Sentinel-2_L2A_{cle}.tiff")
            im = Image.open(src)
            x0, y0, dx, dy = -2.04895, 45.734943, 0.0008668212, 0.0006127846683893188
            boite = (round((FENETRE["lon0"] - x0) / dx), round((y0 - FENETRE["lat1"]) / dy),
                     round((FENETRE["lon1"] - x0) / dx), round((y0 - FENETRE["lat0"]) / dy))
            jpeg(im.crop(boite), os.path.join(SORTIE, f"s2-07-{date}-{nom}.jpg"))


if __name__ == "__main__":
    main()
