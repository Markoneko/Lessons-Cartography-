"""Schémas du cours « Image Application ».

    python3 cours/image-application/outils/schemas.py

Produit, dans images/schemas/ :
  - couverture.svg : la mosaïque d'hexagones de la couverture, aux couleurs des familles de l'atelier ;
  - spectre.svg    : les signaux de la télédétection, placés sur le spectre ;
  - chaine.svg     : la chaîne type, de la commande au résultat.
Les couleurs des familles sont lues dans donnees/atelier.json : un seul endroit à changer.
"""
import json
import math
import random
from pathlib import Path

ICI = Path(__file__).resolve().parent.parent
SORTIE = ICI / "images" / "schemas"
SORTIE.mkdir(parents=True, exist_ok=True)
FAMILLES = json.loads((ICI / "donnees" / "atelier.json").read_text(encoding="utf-8"))["familles"]
BLEU, ORANGE, PRUNE, ENCRE, GRIS, FILET = "#283B89", "#E38226", "#541C5B", "#2B2B33", "#6E6F7A", "#D8DAEC"
TEXTE = 'font-family="Roboto, Arial, sans-serif"'
TITRE = 'font-family="Raleway, Trebuchet MS, sans-serif" font-weight="700"'


def hexagone(cx, cy, r):
    """Hexagone à pointe en haut, de rayon r."""
    pts = []
    for k in range(6):
        a = math.radians(60 * k - 90)
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return " ".join(pts)


def couverture():
    random.seed(7)
    r = 46
    w, h = math.sqrt(3) * r, 1.5 * r
    morceaux = []
    for rang in range(9):
        for col in range(9):
            cx = col * w + (w / 2 if rang % 2 else 0)
            cy = rang * h
            # une diagonale plus dense, qui s'efface vers la gauche
            p = 0.15 + 0.75 * (col / 8)
            if random.random() > p:
                continue
            f = random.choice(FAMILLES)
            plein = random.random() < 0.55
            if plein:
                morceaux.append(f'<polygon points="{hexagone(cx, cy, r - 3)}" fill="{f["fond"]}" opacity="0.92"/>')
            else:
                morceaux.append(f'<polygon points="{hexagone(cx, cy, r - 4)}" fill="none" stroke="{f["fond"]}" stroke-width="3"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-60 -60 {9 * w + 80:.0f} {8 * h + 120:.0f}">'
           + "".join(morceaux) + "</svg>")
    (SORTIE / "couverture.svg").write_text(svg, encoding="utf-8")


def spectre():
    """Une échelle logarithmique des longueurs d'onde, de 0,4 µm à 1 m."""
    L, H = 1100, 270
    x0, x1 = 40, L - 40

    def x(lam_um):
        a, b = math.log10(0.4), math.log10(1e6)
        return x0 + (x1 - x0) * (math.log10(lam_um) - a) / (b - a)

    m = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {L} {H}">']
    # trois familles d'origine du signal
    groupes = [
        (0.4, 3, "#F4E7B0", "Le soleil éclaire, la surface renvoie"),
        (3, 1000, "#F6D3B4", "La surface émet"),
        (1000, 1e6, "#D9DDF2", "L'instrument émet et reçoit"),
    ]
    for a, b, coul, nom in groupes:
        m.append(f'<rect x="{x(a):.1f}" y="40" width="{x(b) - x(a):.1f}" height="70" fill="{coul}"/>')
        m.append(f'<text x="{(x(a) + x(b)) / 2:.1f}" y="30" text-anchor="middle" {TITRE} font-size="17" fill="{PRUNE}">{nom}</text>')
    bandes = [
        (0.4, 0.7, "Visible", "#9AB6E8"),
        (0.7, 1.3, "Proche IR", "#C9A3D6"),
        (1.3, 3, "IR moyen", "#E3A86E"),
        (8, 14, "IR thermique", "#D9705B"),
        (10000, 1e6, "Micro-ondes : radar", "#7E8FCF"),
    ]
    # les trois bandes solaires sont étroites : leurs noms s'étagent, reliés par un filet
    etages = {"Visible": 132, "Proche IR": 152, "IR moyen": 172}
    for a, b, nom, coul in bandes:
        xm = math.sqrt(a * b)
        m.append(f'<rect x="{x(a):.1f}" y="62" width="{max(x(b) - x(a), 6):.1f}" height="26" rx="4" fill="{coul}"/>')
        y = etages.get(nom, 132)
        if nom in etages:
            m.append(f'<line x1="{x(xm):.1f}" y1="90" x2="{x(xm):.1f}" y2="{y - 13}" stroke="{coul}" stroke-width="2"/>')
            m.append(f'<text x="{x(xm) + 4:.1f}" y="{y}" {TEXTE} font-size="15" font-weight="700" fill="{ENCRE}">{nom}</text>')
        else:
            m.append(f'<text x="{x(xm):.1f}" y="{y}" text-anchor="middle" {TEXTE} font-size="15" font-weight="700" fill="{ENCRE}">{nom}</text>')
    # repères
    reperes = [(1.064, "laser du LiDAR", -1), (55000, "radar en bande C", 1), (240000, "bande L", 1)]
    for lam, nom, sens in reperes:
        xx = x(lam)
        m.append(f'<line x1="{xx:.1f}" y1="56" x2="{xx:.1f}" y2="94" stroke="{BLEU}" stroke-width="2.5"/>')
        m.append(f'<text x="{xx:.1f}" y="106" text-anchor="middle" {TEXTE} font-size="13" fill="{BLEU}">{nom}</text>')
    # graduation
    for lam, lib in [(0.4, "0,4 µm"), (1, "1 µm"), (10, "10 µm"), (100, "100 µm"), (1000, "1 mm"), (10000, "1 cm"), (100000, "10 cm"), (1e6, "1 m")]:
        xx = x(lam)
        m.append(f'<line x1="{xx:.1f}" y1="206" x2="{xx:.1f}" y2="214" stroke="{GRIS}" stroke-width="1.5"/>')
        m.append(f'<text x="{xx:.1f}" y="232" text-anchor="middle" {TEXTE} font-size="13" fill="{GRIS}">{lib}</text>')
    m.append(f'<line x1="{x0}" y1="210" x2="{x1}" y2="210" stroke="{GRIS}" stroke-width="1.5"/>')
    m.append(f'<text x="{x1}" y="258" text-anchor="end" {TEXTE} font-size="13" fill="{GRIS}">longueur d\'onde, échelle logarithmique</text>')
    m.append("</svg>")
    (SORTIE / "spectre.svg").write_text("".join(m), encoding="utf-8")


def chaine():
    r = 52
    w = math.sqrt(3) * r
    L, H = int(9 * (w + 14) + 20), 150
    m = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {L} {H}">']
    for k, f in enumerate(FAMILLES):
        cx, cy = 10 + w / 2 + k * (w + 14), 70
        m.append(f'<polygon points="{hexagone(cx, cy, r)}" fill="{f["fond"]}"/>')
        m.append(f'<text x="{cx:.1f}" y="{cy + 5:.1f}" text-anchor="middle" {TITRE} font-size="17" fill="{f["texte"]}">{f["nom"]}</text>')
        if k < len(FAMILLES) - 1:
            xa = cx + w / 2 + 1
            m.append(f'<path d="M{xa:.1f} {cy} l11 0 m-5 -5 l5 5 l-5 5" fill="none" stroke="{GRIS}" stroke-width="2"/>')
    m.append(f'<text x="{10 + w / 2 + 3 * (w + 14):.1f}" y="140" text-anchor="middle" {TEXTE} font-size="13" fill="{GRIS}">facultatif</text>')
    m.append(f'<text x="{10 + w / 2 + 5 * (w + 14):.1f}" y="140" text-anchor="middle" {TEXTE} font-size="13" fill="{GRIS}">facultatif</text>')
    m.append(f'<text x="{10 + w / 2 + 7 * (w + 14):.1f}" y="140" text-anchor="middle" {TEXTE} font-size="13" font-weight="700" fill="{PRUNE}">jamais facultatif</text>')
    m.append("</svg>")
    (SORTIE / "chaine.svg").write_text("".join(m), encoding="utf-8")


if __name__ == "__main__":
    couverture()
    spectre()
    chaine()
    print("Schémas écrits dans", SORTIE)
