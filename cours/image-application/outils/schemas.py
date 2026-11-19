"""Schémas du cours « Image Application ».

    python3 cours/image-application/outils/schemas.py

Produit, dans images/schemas/ :
  - couverture.svg : la mosaïque d'hexagones de la couverture, aux couleurs des familles de l'atelier ;
  - spectre.svg    : les signaux de la télédétection, placés sur le spectre ;
  - chaine.svg     : la chaîne type, de la commande au résultat ;
  - resolutions.svg : les quatre résolutions, chacune en deux réglages ;
  - limites.svg    : les trois limites physiques (lumière, orbite, données), allumées tour à tour.
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


def resolutions():
    """Les quatre résolutions, chacune en deux réglages : grossier, puis fin."""
    L, H = 1150, 330
    m = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {L} {H}">']
    titres = ["Spatiale", "Temporelle", "Spectrale", "Radiométrique"]
    larg = 270
    for k, t in enumerate(titres):
        x0 = k * (larg + 23)
        m.append(f'<rect x="{x0}" y="0" width="{larg}" height="{H}" rx="12" fill="#F4F5FB"/>')
        m.append(f'<text x="{x0 + larg / 2}" y="32" text-anchor="middle" {TITRE} font-size="21" fill="{BLEU}">{t}</text>')

    # 1. spatiale : la même scène, échantillonnée en gros puis en petits pixels
    def scene(u, v):
        if 0.55 < u < 0.8 and 0.2 < v < 0.45:
            return (190, 70, 60)            # un toit
        if abs(u - v * 0.6 - 0.15) < 0.07:
            return (150, 150, 155)          # une route
        if (u - 0.3) ** 2 + (v - 0.72) ** 2 < 0.02:
            return (40, 110, 60)            # un bosquet
        return (150, 190, 110)              # un champ

    def echantillon(x, y, cote, n):
        out = []
        c = cote / n
        for i in range(n):
            for j in range(n):
                acc = [0, 0, 0]
                for a in range(4):
                    for b in range(4):
                        r, g, bb = scene((i + (a + 0.5) / 4) / n, (j + (b + 0.5) / 4) / n)
                        acc[0] += r; acc[1] += g; acc[2] += bb
                col = "#%02X%02X%02X" % tuple(int(v / 16) for v in acc)
                out.append(f'<rect x="{x + i * c:.1f}" y="{y + j * c:.1f}" width="{c + 0.3:.1f}" height="{c + 0.3:.1f}" fill="{col}"/>')
        return "".join(out)
    m.append(echantillon(18, 70, 110, 5))
    m.append(echantillon(142, 70, 110, 22))
    for xx, lib in [(73, "gros pixels"), (197, "petits pixels")]:
        m.append(f'<text x="{xx}" y="204" text-anchor="middle" {TEXTE} font-size="14" fill="{ENCRE}">{lib}</text>')
    m.append(f'<text x="135" y="245" text-anchor="middle" {TEXTE} font-size="14" fill="{GRIS}">le plus petit détail visible</text>')
    m.append(f'<text x="135" y="264" text-anchor="middle" {TEXTE} font-size="14" fill="{GRIS}">au sol</text>')

    # 2. temporelle : les passages sur un mois
    x0 = 293
    for row, (pas, lib) in enumerate([(5, "tous les 5 jours"), (1, "chaque jour")]):
        y = 100 + row * 75
        m.append(f'<line x1="{x0 + 20}" y1="{y}" x2="{x0 + 250}" y2="{y}" stroke="{GRIS}" stroke-width="2"/>')
        for d in range(0, 31, pas):
            xx = x0 + 20 + d * 230 / 30
            m.append(f'<circle cx="{xx:.1f}" cy="{y}" r="{5 if pas > 1 else 3}" fill="{ORANGE}"/>')
        m.append(f'<text x="{x0 + 135}" y="{y + 28}" text-anchor="middle" {TEXTE} font-size="14" fill="{ENCRE}">{lib}</text>')
    m.append(f'<text x="{x0 + 135}" y="245" text-anchor="middle" {TEXTE} font-size="14" fill="{GRIS}">le temps entre deux images</text>')
    m.append(f'<text x="{x0 + 135}" y="264" text-anchor="middle" {TEXTE} font-size="14" fill="{GRIS}">du même lieu (sur un mois)</text>')

    # 3. spectrale : une signature de végétation, vue par 3 larges bandes ou par 60 bandes étroites
    x0 = 586
    def refl(lam):           # allure qualitative d'une végétation saine
        if lam < 0.5: r = 0.05
        elif lam < 0.6: r = 0.05 + 0.08 * math.sin((lam - 0.5) / 0.1 * math.pi)
        elif lam < 0.68: r = 0.05
        elif lam < 0.75: r = 0.05 + (lam - 0.68) / 0.07 * 0.4
        elif lam < 1.3: r = 0.45
        else: r = 0.3
        for c, w, d in [(1.45, 0.06, 0.18), (1.95, 0.08, 0.22)]:
            r -= d * math.exp(-((lam - c) / w) ** 2)
        return max(r, 0.02)
    def X(lam): return x0 + 20 + (lam - 0.4) / 2.1 * 230
    pts = " ".join(f"{X(0.4 + i * 0.01):.1f},{150 - refl(0.4 + i * 0.01) * 160:.1f}" for i in range(211))
    m.append(f'<polyline points="{pts}" fill="none" stroke="#2E7D6B" stroke-width="2.5"/>')
    m.append(f'<line x1="{X(0.4)}" y1="152" x2="{X(2.5)}" y2="152" stroke="{GRIS}" stroke-width="1.5"/>')
    for a, b in [(0.45, 0.7), (0.75, 1.0), (1.55, 1.75)]:
        m.append(f'<rect x="{X(a):.1f}" y="168" width="{X(b) - X(a):.1f}" height="14" fill="{BLEU}" opacity="0.8"/>')
    for i in range(60):
        a = 0.42 + i * 0.035
        m.append(f'<rect x="{X(a):.1f}" y="194" width="{max(X(a + 0.02) - X(a), 1.5):.1f}" height="14" fill="{PRUNE}" opacity="0.8"/>')
    m.append(f'<text x="{x0 + 135}" y="62" text-anchor="middle" {TEXTE} font-size="13" fill="{GRIS}">signature d\'une végétation</text>')
    m.append(f'<text x="{x0 + 135}" y="226" text-anchor="middle" {TEXTE} font-size="13" fill="{ENCRE}"><tspan fill="{BLEU}">3 larges bandes</tspan>, puis <tspan fill="{PRUNE}">60 étroites</tspan></text>')
    m.append(f'<text x="{x0 + 135}" y="250" text-anchor="middle" {TEXTE} font-size="14" fill="{GRIS}">le nombre et la largeur</text>')
    m.append(f'<text x="{x0 + 135}" y="269" text-anchor="middle" {TEXTE} font-size="14" fill="{GRIS}">des bandes</text>')

    # 4. radiométrique : le même dégradé, en 4 niveaux puis en 256
    x0 = 879
    for row, (n, lib) in enumerate([(4, "4 niveaux (2 bits)"), (256, "256 niveaux (8 bits)")]):
        y = 80 + row * 80
        for i in range(n):
            v = int(255 * (i / (n - 1)))
            w = 230 / n
            m.append(f'<rect x="{x0 + 20 + i * w:.2f}" y="{y}" width="{w + 0.4:.2f}" height="34" fill="#{v:02X}{v:02X}{v:02X}"/>')
        m.append(f'<text x="{x0 + 135}" y="{y + 54}" text-anchor="middle" {TEXTE} font-size="14" fill="{ENCRE}">{lib}</text>')
    m.append(f'<text x="{x0 + 135}" y="245" text-anchor="middle" {TEXTE} font-size="14" fill="{GRIS}">la finesse des nuances</text>')
    m.append(f'<text x="{x0 + 135}" y="264" text-anchor="middle" {TEXTE} font-size="14" fill="{GRIS}">d\'intensité</text>')
    m.append("</svg>")
    (SORTIE / "resolutions.svg").write_text("".join(m), encoding="utf-8")


def limites():
    """Les trois limites physiques et leur effet sur l'image, qui se succèdent dans un même cadre (4 s chacune).
    À l'impression, les trois sont posées côte à côte, en petit."""
    L, H = 360, 330
    random.seed(3)
    m = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {L} {H}">',
         '<style>.lim-p{opacity:0;animation:lim-tour 12s infinite}.lim-p1{animation-delay:0s}.lim-p2{animation-delay:-8s}'
         '.lim-p3{animation-delay:-4s}@keyframes lim-tour{0%,30%{opacity:1}34%,96%{opacity:0}100%{opacity:1}}'
         '@media print{.lim-p{animation:none;opacity:1}.lim-p1{transform:scale(.333)}'
         '.lim-p2{transform:translate(120px,0) scale(.333)}.lim-p3{transform:translate(240px,0) scale(.333)}}'
         '@media (prefers-reduced-motion:reduce){.lim-p{animation:none;opacity:1}.lim-p2,.lim-p3{display:none}}</style>']
    larg = 360

    def cadre(k, titre, cause, effet):
        x0 = 0
        if k:
            m.append('</g>')      # chaque mécanisme dans son propre groupe, sinon l'animation les emporte tous
        m.append(f'<g class="lim-p lim-p{k + 1}">')
        m.append(f'<rect x="{x0}" y="0" width="{larg}" height="{H}" rx="14" fill="#F4F5FB" stroke="{FILET}" stroke-width="2"/>')
        m.append(f'<text x="{x0 + 22}" y="34" {TITRE} font-size="22" fill="{BLEU}">{titre}</text>')
        for d in range(3):   # où l'on en est : trois pastilles
            m.append(f'<circle cx="{larg - 70 + d * 20}" cy="28" r="6" fill="{ORANGE if d == k else FILET}"/>')
        m.append(f'<text x="{x0 + larg / 2}" y="296" text-anchor="middle" {TEXTE} font-size="15" fill="{ENCRE}">{cause}</text>')
        m.append(f'<text x="{x0 + larg / 2}" y="317" text-anchor="middle" {TEXTE} font-size="15" font-weight="700" fill="{PRUNE}">{effet}</text>')
        return x0

    # 1. la lumière : peu de lumière par petit pixel, donc du bruit
    x0 = cadre(0, "La lumière", "petit pixel, bande étroite : peu de lumière", "l'image devient bruitée")
    m.append(f'<circle cx="{x0 + 50}" cy="80" r="18" fill="#F2C94C"/>')
    for i in range(8):
        a = i * math.pi / 4
        m.append(f'<line x1="{x0 + 50 + 23 * math.cos(a):.1f}" y1="{80 + 23 * math.sin(a):.1f}" x2="{x0 + 50 + 31 * math.cos(a):.1f}" y2="{80 + 31 * math.sin(a):.1f}" stroke="#F2C94C" stroke-width="3"/>')
    # deux pixels qui reçoivent des photons
    for (px, cote, n) in [(x0 + 105, 80, 34), (x0 + 225, 34, 6)]:
        m.append(f'<rect x="{px}" y="{70}" width="{cote}" height="{cote}" fill="none" stroke="{BLEU}" stroke-width="2"/>')
        for _ in range(n):
            m.append(f'<circle cx="{px + random.uniform(4, cote - 4):.1f}" cy="{70 + random.uniform(4, cote - 4):.1f}" r="2.4" fill="{ORANGE}"/>')
    m.append(f'<text x="{x0 + 145}" y="168" text-anchor="middle" {TEXTE} font-size="13" fill="{GRIS}">grand pixel</text>')
    m.append(f'<text x="{x0 + 242}" y="122" text-anchor="middle" {TEXTE} font-size="13" fill="{GRIS}">petit pixel</text>')
    # l'image : lisse à gauche, bruitée à droite
    for (gx, bruit) in [(x0 + 70, 0), (x0 + 200, 70)]:
        for i in range(8):
            for j in range(5):
                v = 90 + i * 15 + random.uniform(-bruit, bruit)
                v = max(0, min(255, int(v)))
                m.append(f'<rect x="{gx + i * 11}" y="{185 + j * 11}" width="11" height="11" fill="#{v:02X}{v:02X}{v:02X}"/>')

    # 2. l'orbite : voir fin, c'est voir proche, donc voir étroit
    x0 = cadre(1, "L'orbite", "voir fin, c'est voir proche, donc étroit", "l'image est étroite, la revisite rare")
    m.append(f'<path d="M{x0 + 20} 250 Q{x0 + larg / 2} 215 {x0 + larg - 20} 250" fill="#DDE8D3" stroke="{GRIS}" stroke-width="1.5"/>')
    for (sx, sy, demi, coul, lib) in [(x0 + 110, 150, 22, PRUNE, "basse : fin, étroit"), (x0 + 245, 70, 80, BLEU, "haute : grossier, large")]:
        m.append(f'<polygon points="{sx},{sy} {sx - demi},{232} {sx + demi},{232}" fill="{coul}" opacity="0.18"/>')
        m.append(f'<rect x="{sx - 11}" y="{sy - 9}" width="22" height="14" rx="2" fill="{coul}"/>')
        m.append(f'<rect x="{sx - 27}" y="{sy - 5}" width="13" height="6" fill="{coul}" opacity="0.6"/><rect x="{sx + 14}" y="{sy - 5}" width="13" height="6" fill="{coul}" opacity="0.6"/>')
        m.append(f'<line x1="{sx - demi}" y1="236" x2="{sx + demi}" y2="236" stroke="{coul}" stroke-width="4"/>')
        m.append(f'<text x="{min(sx, x0 + larg - 80)}" y="{sy - 18}" text-anchor="middle" {TEXTE} font-size="13" fill="{coul}">{lib}</text>')
    m.append(f'<text x="{x0 + larg / 2}" y="268" text-anchor="middle" {TEXTE} font-size="13" fill="{GRIS}">la fauchée : la largeur de l\'image au sol</text>')

    # 3. les données : pixels × bandes × passages, par un tuyau étroit
    x0 = cadre(2, "Les données", "pixels × bandes × passages", "trop pour le lien vers le sol")
    cx, cy = x0 + 95, 95
    for b in range(6):
        d = b * 9
        m.append(f'<rect x="{cx + d}" y="{cy - d}" width="90" height="90" fill="{["#9AB6E8", "#7E8FCF", "#C9A3D6", "#E3A86E", "#D9705B", "#8FBF9F"][b]}" stroke="#FFFFFF" stroke-width="1.5"/>')
    m.append(f'<text x="{cx + 70}" y="{cy + 112}" text-anchor="middle" {TEXTE} font-size="13" fill="{GRIS}">une bande par couche</text>')
    # le tuyau vers la station
    m.append(f'<path d="M{cx + 160} {cy + 20} C{cx + 200} {cy + 40}, {cx + 200} {cy + 90}, {cx + 215} {cy + 115}" fill="none" stroke="{ORANGE}" stroke-width="5" stroke-dasharray="9 6"/>')
    m.append(f'<path d="M{cx + 200} {cy + 150} l15 -30 l15 30 z" fill="{BLEU}"/><line x1="{cx + 215}" y1="{cy + 150}" x2="{cx + 215}" y2="{cy + 162}" stroke="{BLEU}" stroke-width="3"/>')
    m.append(f'<text x="{cx + 205}" y="{cy + 180}" text-anchor="middle" {TEXTE} font-size="13" fill="{GRIS}">station au sol</text>')
    m.append('</g>')
    m.append("</svg>")
    (SORTIE / "limites.svg").write_text("".join(m), encoding="utf-8")


if __name__ == "__main__":
    couverture()
    spectre()
    chaine()
    resolutions()
    limites()
    print("Schémas écrits dans", SORTIE)
