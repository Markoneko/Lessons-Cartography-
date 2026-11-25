#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Les deux schémas de l'ampleur d'effet.

    python3 outils/schemas-ampleur.py

Écrit dans images/schemas/ :

  ampleur-echelle.svg   trois panneaux, g = 0,2 · 0,5 · 0,8 — ce que vaut un g
  ampleur-dispersion.svg  le même gain brut, sur deux dispersions différentes

Le second est le plus utile en cours : il montre pourquoi on divise par
l'écart-type. La flèche du gain a exactement la même longueur dans les deux
panneaux ; seule la largeur des cloches change, et l'ampleur avec elle.

Les classes sont celles du gabarit (voir README.md) : s-fin, s-accent,
s-tirets, s-titre, s-petit. Les couleurs viennent de la charte, pas d'ici.
"""
import math
import pathlib

ICI = pathlib.Path(__file__).resolve().parent.parent


def cloche(mu, sigma, base, hauteur, x0, x1, pas=2.0):
    """Une gaussienne, échantillonnée : le tracé d'une courbe normale."""
    pts = []
    x = x0
    while x <= x1:
        y = base - hauteur * math.exp(-0.5 * ((x - mu) / sigma) ** 2)
        pts.append(f"{x:.1f},{y:.1f}")
        x += pas
    return "M" + " L".join(pts)


def phi(z):
    """La fonction de répartition de la loi normale : le rang du médian."""
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def panneau(ox, largeur, g, sigma, base, hauteur, titre, sous, med=True):
    """Un panneau : deux cloches décalées de g écarts-types."""
    mu = ox + largeur * 0.42
    mu2 = mu + g * sigma
    x0, x1 = ox + 6, ox + largeur - 6
    el = [f'<line class="s-fin" x1="{ox + 4}" y1="{base}" '
          f'x2="{ox + largeur - 4}" y2="{base}"/>',
          f'<path class="s-fin" d="{cloche(mu, sigma, base, hauteur, x0, x1)}"/>',
          f'<path class="s-accent" d="{cloche(mu2, sigma, base, hauteur, x0, x1)}"/>',
          f'<line class="s-tirets" x1="{mu:.1f}" y1="{base}" '
          f'x2="{mu:.1f}" y2="{base - hauteur - 6:.0f}"/>',
          f'<line class="s-tirets" x1="{mu2:.1f}" y1="{base}" '
          f'x2="{mu2:.1f}" y2="{base - hauteur - 6:.0f}"/>']
    el.append(f'<text class="s-titre" x="{ox + largeur / 2:.0f}" y="{base + 42}" '
              f'text-anchor="middle">{titre}</text>')
    if med:
        el.append(f'<text class="s-petit" x="{ox + largeur / 2:.0f}" y="{base + 66}" '
                  f'text-anchor="middle">{sous}</text>')
    return el, mu, mu2


# ------------------------------------------------- 1. l'échelle des ampleurs

def echelle():
    base, hauteur, sigma = 210, 150, 40
    larg, ecart = 330, 32
    el = []
    for i, g in enumerate((0.2, 0.5, 0.8)):
        ox = 24 + i * (larg + ecart)
        p, mu, mu2 = panneau(
            ox, larg, g, sigma, base, hauteur,
            f"g = {g:.1f}".replace(".", ","),
            f"le médian dépasse {phi(g) * 100:.0f} % du témoin")
        el += p
        # la mesure de l'écart, entre les deux sommets
        y = base - hauteur - 20
        el.append(f'<path class="s-fin" d="M{mu:.1f},{y - 4} V{y + 4} M{mu:.1f},{y} '
                  f'L{mu2:.1f},{y} M{mu2:.1f},{y - 4} V{y + 4}"/>')
        el.append(f'<text class="s-petit" x="{(mu + mu2) / 2:.0f}" y="{y - 12}" '
                  f'text-anchor="middle">{g:.1f}'.replace(".", ",")
                  + ' σ</text>')
    return ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 1120 292\" "
            "role=\"img\" aria-label=\"Trois paires de courbes normales décalées "
            "de 0,2, 0,5 et 0,8 écart-type\">\n  "
            + "\n  ".join(el) + "\n</svg>\n")


# -------------------------------------- 2. pourquoi diviser par l'écart-type

def dispersion():
    base, hauteur = 200, 130
    gain = 52              # le même gain brut, en points, dans les deux cas
    el = []

    for ox, larg, part, sigma, titre, sous in (
            (24, 400, .35, 26, "g = 2,0",
             "une promotion homogène : l'écart saute aux yeux"),
            (520, 576, .31, 95, "g = 0,55",
             "une promotion dispersée : le même gain s'y noie")):
        mu = ox + larg * part
        mu2 = mu + gain
        x0, x1 = ox + 6, ox + larg - 6
        el.append(f'<line class="s-fin" x1="{ox + 4}" y1="{base}" '
                  f'x2="{ox + larg - 4}" y2="{base}"/>')
        el.append(f'<path class="s-fin" d="{cloche(mu, sigma, base, hauteur, x0, x1)}"/>')
        el.append(f'<path class="s-accent" d="{cloche(mu2, sigma, base, hauteur, x0, x1)}"/>')
        for m in (mu, mu2):
            el.append(f'<line class="s-tirets" x1="{m:.1f}" y1="{base}" '
                      f'x2="{m:.1f}" y2="{base - hauteur - 10:.0f}"/>')
        # la flèche du gain, identique de part et d'autre
        y = base - hauteur - 24
        el.append(f'<path class="s-trait" d="M{mu:.1f},{y} L{mu2:.1f},{y} '
                  f'M{mu2 - 9:.1f},{y - 5} L{mu2:.1f},{y} L{mu2 - 9:.1f},{y + 5}"/>')
        el.append(f'<text class="s-petit" x="{(mu + mu2) / 2:.0f}" y="{y - 10}" '
                  f'text-anchor="middle">+ 4 points</text>')
        # l'écart-type, mesuré sous la courbe témoin
        el.append(f'<line class="s-fin" x1="{mu:.1f}" y1="{base + 18}" '
                  f'x2="{mu + sigma:.1f}" y2="{base + 18}"/>')
        el.append(f'<line class="s-fin" x1="{mu:.1f}" y1="{base + 12}" '
                  f'x2="{mu:.1f}" y2="{base + 24}"/>')
        el.append(f'<line class="s-fin" x1="{mu + sigma:.1f}" y1="{base + 12}" '
                  f'x2="{mu + sigma:.1f}" y2="{base + 24}"/>')
        el.append(f'<text class="s-petit" x="{mu + sigma / 2:.0f}" y="{base + 38}" '
                  f'text-anchor="middle">un écart-type</text>')
        el.append(f'<text class="s-titre" x="{ox + larg / 2:.0f}" y="{base + 76}" '
                  f'text-anchor="middle">{titre}</text>')
        el.append(f'<text class="s-petit" x="{ox + larg / 2:.0f}" y="{base + 100}" '
                  f'text-anchor="middle">{sous}</text>')

    el.append('<line class="s-fin" x1="472" y1="20" x2="472" y2="306" '
              'stroke-dasharray="4 6"/>')
    return ("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 1120 316\" "
            "role=\"img\" aria-label=\"Le même gain de quatre points, sur une "
            "promotion homogène puis sur une promotion dispersée\">\n  "
            + "\n  ".join(el) + "\n</svg>\n")


def main():
    dossier = ICI / "images" / "schemas"
    dossier.mkdir(parents=True, exist_ok=True)
    for nom, contenu in (("ampleur-echelle.svg", echelle()),
                         ("ampleur-dispersion.svg", dispersion())):
        (dossier / nom).write_text(contenu, encoding="utf-8")
        print(f"{nom} — {len(contenu)} caractères")
    # le contrôle : g = gain / écart-type, c'est tout ce que dit le schéma
    for sigma, attendu in ((26, "2,0"), (95, "0,55")):
        print(f"  σ = {sigma} → g = {52 / sigma:.2f}".replace(".", ",")
              + f" (annoncé {attendu})")


if __name__ == "__main__":
    main()
