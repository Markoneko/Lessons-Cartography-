#!/usr/bin/env python3
"""Images de l'atelier Saumos : versions web, dans images/saumos/.

    python3 cours/image-application/outils/images-saumos.py

Sources :
  - images/originaux/saumos/ : les images de la séance prépa (saumos-seance.html), extraites telles quelles
    (photo d'accroche, dNBR) ; l'emprise du dNBR est GEO ci-dessous ;
  - source/Cas1-Saumos/ : les images de Marc
      * MSG-0/ : Meteosat (MSG, 0°), couleurs naturelles renforcées, du 21 juillet 12 h au 22 juillet 23 h UTC,
        exports d'EUMETView avec leur légende (logo et heure) ;
      * Browser_imagesS2-*/ : exports du Copernicus Browser (21 juillet, 26 juillet, 4 septembre ; quatre compositions),
        tous sur la même grille, recadrés ici sur FENETRE ;
      * Terra/ : anomalies thermiques (21 au 28 juillet) ;
      * le contexte Reuters / EMSR899.
  - la courbe de réflectance « 8 bits » que montre Elikia est dessinée ici (reflectance.svg).
Le dNBR reste en PNG sans perte.
"""
import base64
import glob
import os
import re
import shutil

from PIL import Image

Image.MAX_IMAGE_PIXELS = None
COURS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RACINE = os.path.dirname(os.path.dirname(COURS))
ORIG = os.path.join(COURS, "images", "originaux", "saumos")
SRC = os.path.join(COURS, "source", "Cas1-Saumos")
SORTIE = os.path.join(COURS, "images", "saumos")

# Emprise du dNBR de la séance prépa (1212 × 732 px), en degrés WGS 84
GEO = dict(lon0=-1.239395, lon1=-0.803229, lat0=44.715026, lat1=44.9784)
# Fenêtre des exports du Browser : un peu plus large que GEO, pour garder le panache de fumée
FENETRE = dict(lon0=-1.32, lon1=-0.72, lat0=44.66, lat1=45.03)
# Grille commune des exports du Browser (coin nord-ouest et pas, en degrés)
X0, Y0, DX, DY = -2.04895, 45.734943, 0.0008668212, 0.0006127846683893188
COMPOS = {
    "Highlight_Optimized_Natural_Color_": "naturelles",
    "False_color": "infrarouge",
    "SWIR": "swir",
    "Wildfires": "feux",
}
DATES_S2 = [("07-21", "Browser_imagesS2-21Juill2026"), ("07-26", "Browser_imagesS2-26Juill2026"),
            ("09-04", "Browser_imagesS2-04Sept2026")]


def jpeg(im, chemin, cote=None, qualite=85):
    if cote and max(im.size) > cote:
        f = cote / max(im.size)
        im = im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)
    im.convert("RGB").save(chemin, quality=qualite, optimize=True)
    print(f"{os.path.relpath(chemin, COURS):45s} {im.width} × {im.height}  {os.path.getsize(chemin) // 1024} ko")


def reflectance():
    """Une courbe de réflectance en pixels : forêt saine et forêt brûlée, de 0,4 à 2,5 µm, B8 et B12 marquées.
    Valeurs indicatives (allure des courbes de référence), arrondies pour le dessin."""
    saine = [(0.40, 4), (0.45, 5), (0.50, 6), (0.55, 10), (0.60, 7), (0.65, 5), (0.68, 4), (0.70, 12), (0.72, 28),
             (0.75, 42), (0.80, 45), (0.90, 46), (1.00, 45), (1.10, 44), (1.20, 38), (1.30, 36), (1.40, 22), (1.45, 14),
             (1.50, 20), (1.60, 27), (1.70, 26), (1.80, 18), (1.90, 6), (2.00, 9), (2.10, 14), (2.20, 15), (2.30, 12),
             (2.40, 9), (2.50, 7)]
    brulee = [(0.40, 3), (0.50, 4), (0.60, 5), (0.70, 6), (0.80, 8), (0.90, 9), (1.00, 11), (1.20, 14), (1.40, 15),
              (1.50, 17), (1.60, 20), (1.80, 21), (2.00, 22), (2.20, 23), (2.40, 22), (2.50, 21)]
    W, H, P = 100, 60, 6                      # grille de 100 × 60 « gros pixels » de 6 px
    x0, y0, x1, y1 = 12, 6, 96, 50            # cadre du graphique, en gros pixels

    def lin(x, xs, ys):
        for (a, fa), (b, fb) in zip(zip(xs, ys), zip(xs[1:], ys[1:])):
            if a <= x <= b:
                return fa + (fb - fa) * (x - a) / (b - a)
        return ys[-1]

    def courbe(pts, coul):
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        out, avant = [], None
        for c in range(x0 + 1, x1 + 1):
            lam = 0.4 + (c - x0) / (x1 - x0) * 2.1
            r = lin(lam, xs, ys)
            l = round(y1 - 1 - r / 50 * (y1 - y0 - 1))
            haut, bas = (l, l) if avant is None else (min(l, avant), max(l, avant))
            if bas - haut > 1:                # dans les pentes raides, on remplit la marche
                haut, bas = (haut + 1, bas) if l > avant else (haut, bas - 1)
            out.append(f'<rect x="{c * P}" y="{haut * P}" width="{P}" height="{(bas - haut + 1) * P}" fill="{coul}"/>')
            avant = l
        return "".join(out)

    def colonne(lam, coul, nom):
        c = round(x0 + (lam - 0.4) / 2.1 * (x1 - x0))
        return (f'<rect x="{c * P}" y="{y0 * P}" width="{P}" height="{(y1 - y0) * P}" fill="{coul}" opacity="0.18"/>'
                f'<text x="{c * P + 3}" y="{(y0 - 1) * P}" text-anchor="middle" fill="{coul}" font-size="13">{nom}</text>')

    with open(os.path.join(RACINE, "_charte", "polices", "press-start-2p-latin-400-normal.woff2"), "rb") as f:
        police = base64.b64encode(f.read()).decode()
    axes = (f'<rect x="{x0 * P}" y="{y0 * P}" width="{P}" height="{(y1 - y0 + 1) * P}" fill="#1D2A66"/>'
            f'<rect x="{x0 * P}" y="{y1 * P}" width="{(x1 - x0 + 1) * P}" height="{P}" fill="#1D2A66"/>')
    graduations = "".join(
        f'<text x="{round(x0 + (l - 0.4) / 2.1 * (x1 - x0)) * P}" y="{(y1 + 4) * P}" text-anchor="middle" font-size="11" fill="#1D2A66">{str(l).replace(".", ",")}</text>'
        for l in (0.5, 1.0, 1.5, 2.0, 2.5))
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W * P} {H * P}" shape-rendering="crispEdges">'
           f'<style>@font-face{{font-family:PS2P;src:url(data:font/woff2;base64,{police}) format("woff2")}}'
           f'text{{font-family:PS2P,monospace}}</style>'
           f'<rect width="{W * P}" height="{H * P}" fill="#F4F5FB"/>'
           + colonne(0.842, "#E38226", "B8") + colonne(2.19, "#C2185B", "B12") + axes
           + courbe(saine, "#2E7D32") + courbe(brulee, "#5D4037") + graduations
           + f'<text x="{(x1 - 1) * P}" y="{(y1 + 8) * P}" text-anchor="end" font-size="11" fill="#1D2A66">longueur d\'onde (µm)</text>'
           + f'<text x="{2 * P}" y="{(y0 + 2) * P}" font-size="11" fill="#1D2A66">%</text>'
           + f'<rect x="{50 * P}" y="{(y0 + 3) * P}" width="{2 * P}" height="{2 * P}" fill="#2E7D32"/>'
           + f'<text x="{53 * P}" y="{(y0 + 5) * P}" font-size="11" fill="#1D2A66">forêt saine</text>'
           + f'<rect x="{50 * P}" y="{(y0 + 7) * P}" width="{2 * P}" height="{2 * P}" fill="#5D4037"/>'
           + f'<text x="{53 * P}" y="{(y0 + 9) * P}" font-size="11" fill="#1D2A66">forêt brûlée</text>'
           + '</svg>')
    chemin = os.path.join(SORTIE, "reflectance.svg")
    with open(chemin, "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"{os.path.relpath(chemin, COURS):45s} {os.path.getsize(chemin) // 1024} ko")


def main():
    os.makedirs(SORTIE, exist_ok=True)
    # 1. la séance prépa, sans retouche
    jpeg(Image.open(os.path.join(ORIG, "accroche.jpg")), os.path.join(SORTIE, "accroche.jpg"))
    shutil.copyfile(os.path.join(ORIG, "m_dnbr.png"), os.path.join(SORTIE, "m-dnbr.png"))
    # 2. le contexte Reuters / EMSR899 et les anomalies thermiques Terra
    jpeg(Image.open(os.path.join(SRC, "Contexte-Reuters-EMSR899 Situational Reporting.png")), os.path.join(SORTIE, "contexte-emsr899.jpg"))
    for j in range(21, 29):
        jpeg(Image.open(os.path.join(SRC, "Terra", f"TerraThermalAnomalies-2026-07-{j}.jpeg")), os.path.join(SORTIE, f"terra-07-{j}.jpg"))
    # 3. Meteosat, image par image, légende comprise (le logo et l'heure UTC sont dans l'image)
    for src in sorted(glob.glob(os.path.join(SRC, "MSG-0", "*.png"))):
        m = re.search(r"2026-(\d\d)-(\d\d)T(\d\d)(\d\d)", src)
        jpeg(Image.open(src), os.path.join(SORTIE, f"msg-{m.group(1)}{m.group(2)}-{m.group(3)}{m.group(4)}.jpg"), cote=1000, qualite=76)
    # 4. les exports du Browser, recadrés sur la fenêtre
    boite = (round((FENETRE["lon0"] - X0) / DX), round((Y0 - FENETRE["lat1"]) / DY),
             round((FENETRE["lon1"] - X0) / DX), round((Y0 - FENETRE["lat0"]) / DY))
    for date, dossier in DATES_S2:
        for cle, nom in COMPOS.items():
            src = os.path.join(SRC, dossier, f"2026-{date}-00_00_2026-{date}-23_59_Sentinel-2_L2A_{cle}.tiff")
            jpeg(Image.open(src).crop(boite), os.path.join(SORTIE, f"s2-{date}-{nom}.jpg"))
    # 5. la courbe de réflectance
    reflectance()


if __name__ == "__main__":
    main()
