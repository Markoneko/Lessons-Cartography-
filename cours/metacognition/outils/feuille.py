#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""La feuille A4 du cours « Apprendre à apprendre ».

    python3 outils/feuille.py [--papier jaune|rose|vert|blanc]

Deux faces, une seule encre.

Recto — les deux activités d'introduction, puis un tableau à trois colonnes :
ce qu'ils notent, cinq étoiles vides, et la carte qu'ils mettront en face.

Verso — le plan d'action sous forme de carte marine. L'île du contexte en bas
à gauche, la rose des vents du site Alidade en bas à droite pour le cap, et
entre les deux les îlots des gestes qu'ils s'engagent à essayer en décembre.
Chaque îlot porte un pavillon vide : c'est là qu'ils écrivent le nom du geste,
et c'est ce qui leur donne une raison de garder les cartes. La feuille se plie
et part dans l'enveloppe.

Les deux consignes du recto sont celles de Marc, reprises mot pour mot de ses
notes du 23 novembre.
"""
import argparse
import math
import pathlib
import subprocess
import sys

# Sous Windows, la sortie d'un script appelé par un autre passe par un tuyau, et
# Python l'encode alors dans la page de code locale, pas en UTF-8 : une flèche
# « → » suffit à faire échouer le script entier. On force l'UTF-8 quand c'est
# possible, sans rien casser ailleurs.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ICI = pathlib.Path(__file__).resolve().parent.parent
ENCRE = "232968"
GRIS = "6E6F7A"
PAPIERS = {"jaune": "#FBF3CC", "rose": "#F9DDE4", "vert": "#DFF0DC",
           "blanc": "#FFFFFF"}

# --------------------------------------------------------------------- recto

ACTIVITE_1 = ("Commencez par noter vos stratégies d'apprentissage. Identifiez "
              "les outils que vous utilisez à l'heure actuelle. Notez-les avec "
              "des étoiles : 5 étoiles du top, 1 étoile pas mal mais un peu "
              "gadget, 3 c'est du solide.")
ACTIVITE_2 = ("Identifiez ce qui ne fonctionne pas, ou ce qui vous pose des "
              "questions, vous insécurise. Par exemple : je n'ose pas poser de "
              "questions en cours ; j'ai l'impression de manquer de certains "
              "concepts clefs ; je dors mal.")

ETOILES = "☆☆☆☆☆"


def tableau(titre, numero, consigne, jauge, lignes):
    rangs = "".join(
        f'<tr><td class="point"></td><td class="note">{ETOILES}</td>'
        f'<td class="carte"></td></tr>' for _ in range(lignes))
    return f"""
  <section class="activite">
    <h2><span class="num">{numero}</span>{titre}</h2>
    <p class="consigne">{consigne}</p>
    <table>
      <thead><tr>
        <th class="point">dans vos mots</th>
        <th class="note">{jauge}</th>
        <th class="carte">la carte qui lui répond</th>
      </tr></thead>
      <tbody>{rangs}</tbody>
    </table>
  </section>"""


def recto():
    return f"""
<article class="page recto">
  <header><span>Géodata Paris · Ing1</span><span>Apprendre à apprendre</span></header>
  <h1>Ce qui fonctionne, ce qui bloque</h1>
  <p class="chapeau">Avant d'ouvrir le jeu de cartes. Écrivez d'abord, vous
    chercherez les correspondances ensuite : la troisième colonne ne se remplit
    qu'une fois les cartes en main.</p>
  {tableau("Ce qui fonctionne déjà", "1", ACTIVITE_1, "ce que ça vaut", 7)}
  {tableau("Ce qui bloque", "2", ACTIVITE_2, "ce que ça me coûte", 6)}
  <footer>Gardez cette feuille : son verso part dans l'enveloppe à la fin de la séance.</footer>
</article>"""


# --------------------------------------------------------------------- verso
# La rose des vents est celle du site Alidade : trois rangs de pointes
# (quarts, demi-vents, vents), chacune fendue en deux moitiés, l'une pleine,
# l'autre évidée. On garde la graduation, on laisse tomber les chiffres :
# à 22 mm de rayon ils ne se liraient pas.

def rose(cx, cy, rayon):
    k = rayon / 124.0
    out = [f'<circle class="fin" cx="{cx}" cy="{cy}" r="{124 * k:.2f}"/>',
           f'<circle class="fin" cx="{cx}" cy="{cy}" r="{117 * k:.2f}"/>']
    for d in range(0, 360, 5):
        th = math.radians(d - 90)
        lg = 8 if d % 30 == 0 else 5 if d % 10 == 0 else 3
        x1, y1 = cx + math.cos(th) * 124 * k, cy + math.sin(th) * 124 * k
        x2, y2 = (cx + math.cos(th) * (124 - lg) * k,
                  cy + math.sin(th) * (124 - lg) * k)
        out.append(f'<line class="fin" x1="{x1:.2f}" y1="{y1:.2f}" '
                   f'x2="{x2:.2f}" y2="{y2:.2f}"/>')

    def pointe(ang, long_, larg):
        th = math.radians(ang - 90)
        px, py = math.cos(th), math.sin(th)
        qx, qy = -py, px
        t = f"{cx + px * long_ * k:.2f},{cy + py * long_ * k:.2f}"
        g = f"{cx + qx * larg * k:.2f},{cy + qy * larg * k:.2f}"
        d = f"{cx - qx * larg * k:.2f},{cy - qy * larg * k:.2f}"
        return (f'<path class="creuse" d="M{cx},{cy} L{g} L{t} Z"/>'
                f'<path class="pleine" d="M{cx},{cy} L{d} L{t} Z"/>')

    for i in range(16):
        if i % 2:
            out.append(pointe(i * 22.5, 46, 5))
    for i in range(8):
        if i % 2:
            out.append(pointe(i * 45, 72, 10))
    for i in range(4):
        out.append(pointe(i * 90, 104, 13))
    out.append(f'<circle class="pleine" cx="{cx}" cy="{cy}" r="{6 * k:.2f}"/>')
    for nom, ang in (("N", 0), ("E", 90), ("S", 180), ("O", 270)):
        th = math.radians(ang - 90)
        out.append(f'<text class="card" x="{cx + math.cos(th) * 142 * k:.2f}" '
                   f'y="{cy + math.sin(th) * 142 * k + 1.4:.2f}">{nom}</text>')
    return "".join(out)


# Les côtes sont tirées de la même recette qu'Alidade : un cercle déformé par
# quelques harmoniques, puis lissé. Le tirage est reproductible, donc la carte
# est la même sur toutes les feuilles.

def des(graine):
    etat = graine

    def suivant():
        nonlocal etat
        etat = (etat + 0x6D2B79F5) & 0xFFFFFFFF
        x = (etat ^ (etat >> 15)) * (1 | etat) & 0xFFFFFFFF
        x = (x + ((x ^ (x >> 7)) * (61 | x) & 0xFFFFFFFF)) & 0xFFFFFFFF
        x ^= x >> 14
        return (x & 0xFFFFFFFF) / 4294967296
    return suivant


def cote(cx, cy, rayon, graine, n=48, ampleur=1.0):
    """Une côte : un cercle déformé par quelques harmoniques, puis lissé.
    Plus l'île est petite, plus on calme les harmoniques — sinon elle tourne
    au nuage au lieu de la terre."""
    r = des(graine)
    comps = [(k, a * (0.5 + r()) * ampleur, r() * 6.2832)
             for k, a in ((2, .14), (3, .10), (4, .07), (5, .05), (7, .03),
                          (11, .018))]
    pts = []
    for i in range(n):
        th = i / n * 6.2832
        f = 1 + sum(a * math.sin(k * th + p) for k, a, p in comps)
        pts.append((cx + math.cos(th) * rayon * f,
                    cy + math.sin(th) * rayon * f * .82))
    return lisse(pts)


def lisse(p):
    n = len(p)
    d = ""
    for i in range(n):
        a, b, c, e = p[(i - 1) % n], p[i], p[(i + 1) % n], p[(i + 2) % n]
        if i == 0:
            d += f"M{b[0]:.2f} {b[1]:.2f}"
        d += (f"C{b[0] + (c[0] - a[0]) / 6:.2f} {b[1] + (c[1] - a[1]) / 6:.2f} "
              f"{c[0] - (e[0] - b[0]) / 6:.2f} {c[1] - (e[1] - b[1]) / 6:.2f} "
              f"{c[0]:.2f} {c[1]:.2f}")
    return d + "Z"


def route_lissee(p):
    """Une route ouverte qui passe par tous les points, sans boucler."""
    n = len(p)
    d = f"M{p[0][0]:.1f},{p[0][1]:.1f}"
    for i in range(n - 1):
        a = p[i - 1] if i else p[0]
        b, c = p[i], p[i + 1]
        e = p[i + 2] if i + 2 < n else p[-1]
        d += (f"C{b[0] + (c[0] - a[0]) / 6:.1f},{b[1] + (c[1] - a[1]) / 6:.1f} "
              f"{c[0] - (e[0] - b[0]) / 6:.1f},{c[1] - (e[1] - b[1]) / 6:.1f} "
              f"{c[0]:.1f},{c[1]:.1f}")
    return d


# Les sept îlots, posés à la main : (x, y, rayon, pavillon à droite).
# L'escale se lit dans le sens de la route, du contexte vers le cap.
ILOTS = [(34, 128, 6.2, True), (30, 86, 5.4, True), (60, 52, 6.0, True),
         (100, 34, 5.6, True), (140, 58, 6.2, False), (152, 98, 5.4, False),
         (100, 106, 5.8, False)]

MAT, PAV_L, PAV_H = 13.0, 30.0, 7.2


def ilot(cx, cy, rayon, graine, cote_droit=True):
    """Un îlot et son pavillon vide : le nom du geste s'écrit dessus."""
    x = cx + 1.0 if cote_droit else cx - 1.0 - PAV_L
    pic = cy - rayon * .72 - MAT
    return (f'<path class="terre" d="{cote(cx, cy, rayon, graine)}"/>'
            f'<path class="laisse" d="{cote(cx, cy, rayon * .78, graine)}"/>'
            f'<line class="mat" x1="{cx:.1f}" y1="{cy - rayon * .72:.1f}" '
            f'x2="{cx:.1f}" y2="{pic:.1f}"/>'
            f'<rect class="pavillon" x="{x:.1f}" y="{pic:.1f}" '
            f'width="{PAV_L}" height="{PAV_H}" rx="0.5"/>')


def carte_marine():
    el = []
    # la neatline : deux filets et des amorces de graduation entre les deux
    el.append('<rect class="trait" x="1.2" y="1.2" width="179.6" height="209.6"/>')
    el.append('<rect class="fin" x="4" y="4" width="174" height="204"/>')
    for x in range(14, 180, 10):
        el.append(f'<line class="fin" x1="{x}" y1="1.2" x2="{x}" y2="4"/>')
        el.append(f'<line class="fin" x1="{x}" y1="208" x2="{x}" y2="210.8"/>')
    for y in range(14, 210, 10):
        el.append(f'<line class="fin" x1="1.2" y1="{y}" x2="4" y2="{y}"/>')
        el.append(f'<line class="fin" x1="178" y1="{y}" x2="180.8" y2="{y}"/>')

    # la route, en pointillé : de l'île du contexte au dernier îlot. Elle ne
    # rejoint pas la rose — un cap n'est pas une destination, c'est ce par quoi
    # on s'oriente. La rose reste l'instrument, dans son coin.
    passage = [(48, 146)] + [(x, y) for x, y, _, _ in ILOTS]
    el.append(f'<path class="route" d="{route_lissee(passage)}"/>')

    # sept îlots : un par geste retenu pour décembre
    for i, (cx, cy, r, droite) in enumerate(ILOTS):
        el.append(ilot(cx, cy, r, 1700 + i * 37, droite))
        el.append(f'<text class="rang" x="{cx:.0f}" y="{cy + 1.4:.1f}">{i + 1}</text>')

    # l'île du contexte, et ses lignes à l'intérieur : c'est votre sol
    el.append(f'<path class="terre" d="{cote(48, 166, 23, 404, 48, .8)}"/>')
    el.append(f'<path class="laisse" d="{cote(48, 166, 20, 404, 48, .8)}"/>')
    for y in (158, 168, 178):
        el.append(f'<line class="ecrire" x1="30" y1="{y}" x2="66" y2="{y}"/>')
    el.append('<text class="zone" x="48" y="196">LE CONTEXTE</text>')
    el.append('<text class="aide" x="48" y="201.5">ce qui vous rend serein, ou pas</text>')

    # le cap : la rose des vents, et autour d'elle de quoi noter ce qu'elle oriente
    for y in (118, 128, 138):
        el.append(f'<line class="ecrire" x1="104" y1="{y}" x2="172" y2="{y}"/>')
    el.append(rose(140, 164, 19.5))
    el.append('<text class="zone" x="140" y="196">LE CAP</text>')
    el.append('<text class="aide" x="140" y="201.5">pourquoi je suis là, où je vais</text>')
    return "".join(el)


def verso():
    return f"""
<article class="page verso">
  <header><span>Géodata Paris · Ing1</span><span>Apprendre à apprendre</span></header>
  <h1>Votre plan d'action</h1>
  <p class="chapeau">Sept gestes au plus, ceux que vous vous engagez à essayer
    d'ici janvier : un par îlot, son nom sur le pavillon. Cette face part dans
    l'enveloppe ; les cartes restent avec vous.
    <span class="ident">Nom <span class="trou"></span> Date <span class="trou"></span></span></p>
  <div class="chart"><svg viewBox="0 0 182 212">{carte_marine()}</svg></div>
</article>"""


# ----------------------------------------------------------------- la feuille

def page(papier):
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Apprendre à apprendre — la feuille</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=Roboto:ital,wght@0,300;0,400;0,500;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {{ --encre:#{ENCRE}; --gris:#{GRIS}; --papier:{papier}; }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; background: #DCDEE8; color: var(--encre);
    font-family: Roboto, system-ui, sans-serif;
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
  }}
  .page {{
    position: relative; width: 210mm; height: 297mm; background: var(--papier);
    padding: 11mm 14mm 9mm; display: flex; flex-direction: column;
    overflow: hidden; border-top: 2.6mm solid var(--encre); margin: 0 auto 6mm;
  }}
  .page header {{
    display: flex; justify-content: space-between; align-items: baseline;
    font-family: 'IBM Plex Mono', monospace; font-size: 7pt;
    letter-spacing: .15em; text-transform: uppercase;
    border-bottom: .3mm solid var(--encre); padding-bottom: 1.8mm;
  }}
  h1 {{
    font-family: Quicksand, sans-serif; font-weight: 700; font-size: 22pt;
    line-height: 1.04; letter-spacing: -.015em; margin: 5mm 0 0;
  }}
  .chapeau {{ font-size: 9pt; line-height: 1.45; margin: 2.5mm 0 0; max-width: 150mm; }}
  .ident {{
    display: block; margin-top: 3mm; font-family: 'IBM Plex Mono', monospace;
    font-size: 8pt; letter-spacing: .06em;
  }}
  .trou {{
    display: inline-block; width: 42mm; border-bottom: .3mm solid var(--encre);
    margin: 0 6mm 0 1.5mm;
  }}

  /* ------------------------------- recto */
  .activite {{ margin-top: 7mm; }}
  .activite h2 {{
    font-family: Quicksand, sans-serif; font-weight: 700; font-size: 12.5pt;
    margin: 0; display: flex; align-items: baseline; gap: 3mm;
  }}
  .activite .num {{
    font-family: 'IBM Plex Mono', monospace; font-size: 9pt; font-weight: 500;
    border: .3mm solid var(--encre); border-radius: 50%; width: 6.5mm;
    height: 6.5mm; display: inline-flex; align-items: center;
    justify-content: center; flex: 0 0 auto;
  }}
  .consigne {{ font-size: 8.6pt; line-height: 1.45; margin: 1.8mm 0 2.5mm; max-width: 165mm; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th {{
    font-family: 'IBM Plex Mono', monospace; font-size: 6.6pt; font-weight: 400;
    letter-spacing: .12em; text-transform: uppercase; color: var(--gris);
    text-align: left; padding: 0 0 1mm 1.5mm; border-bottom: .3mm solid var(--encre);
  }}
  td {{ border-bottom: .25mm solid var(--encre); height: 12.4mm; }}
  th.note, td.note {{ width: 34mm; text-align: center; }}
  th.note {{ text-align: center; }}
  th.carte, td.carte {{ width: 46mm; border-left: .25mm solid var(--encre); }}
  td.note {{ font-size: 11.5pt; letter-spacing: .14em; vertical-align: middle; }}
  .page footer {{
    margin-top: auto; border-top: .3mm solid var(--encre); padding-top: 2mm;
    font-family: 'IBM Plex Mono', monospace; font-size: 7pt; color: var(--gris);
  }}

  /* ------------------------------- verso : la carte marine */
  .chart {{ flex: 1 1 auto; min-height: 0; display: flex; margin-top: 4mm; }}
  .chart svg {{ width: 100%; height: 100%; }}
  .trait {{ fill: none; stroke: var(--encre); stroke-width: .5; }}
  .fin {{ fill: none; stroke: var(--encre); stroke-width: .25; }}
  .fin-plein {{ fill: var(--papier); stroke: var(--encre); stroke-width: .25; }}
  .route {{
    fill: none; stroke: var(--encre); stroke-width: .5;
    stroke-dasharray: 2.4 2.2; opacity: .75;
  }}
  .terre {{ fill: var(--papier); stroke: var(--encre); stroke-width: .6; }}
  .laisse {{ fill: none; stroke: var(--encre); stroke-width: .25; opacity: .5; }}
  .mat {{ stroke: var(--encre); stroke-width: .55; }}
  .pavillon {{ fill: var(--papier); stroke: var(--encre); stroke-width: .45; }}
  .pleine {{ fill: var(--encre); stroke: none; }}
  .creuse {{ fill: var(--papier); stroke: var(--encre); stroke-width: .22; }}
  .ecrire {{ stroke: var(--encre); stroke-width: .3; opacity: .8; }}
  .zone {{
    font-family: Quicksand, sans-serif; font-weight: 700; font-size: 5.2px;
    letter-spacing: .14em; text-anchor: middle; fill: var(--encre);
  }}
  .aide {{
    font-family: 'IBM Plex Mono', monospace; font-size: 3.4px;
    text-anchor: middle; fill: var(--encre); opacity: .72;
  }}
  .card {{
    font-family: 'IBM Plex Mono', monospace; font-size: 4px;
    text-anchor: middle; fill: var(--encre);
  }}
  /* le numéro d'escale, posé sur l'îlot : il dit l'ordre de la route */
  .rang {{
    font-family: 'IBM Plex Mono', monospace; font-size: 4.4px; font-weight: 500;
    text-anchor: middle; fill: var(--encre); opacity: .8;
  }}

  @page {{ size: 210mm 297mm; margin: 0; }}
  @media print {{
    body {{ background: none; }}
    .page {{ margin: 0; break-after: page; }}
    .page:last-child {{ break-after: auto; }}
  }}
</style>
</head>
<body>{recto()}{verso()}</body>
</html>
"""


def imprimer(html, pdf, attente=1400):
    """Imprime une page en PDF, et dit quoi faire si l'outil manque.

    Playwright et son navigateur s'installent en deux commandes, une fois pour
    toutes. Tant qu'ils ne sont pas là, autant le dire franchement plutôt que
    de laisser une trace d'appels Python en guise d'explication.
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit(
            "\nPlaywright n'est pas installé : c'est lui qui imprime les PDF.\n"
            "  Windows :        py -m pip install --user -r requirements.txt\n"
            "                   py -m playwright install chromium\n"
            "  macOS, Linux :   python3 -m pip install --user -r requirements.txt\n"
            "                   python3 -m playwright install chromium\n"
            f"\nLa page HTML, elle, est déjà écrite : {html}\n")
    try:
        with sync_playwright() as p:
            nav = p.chromium.launch()
            pg = nav.new_page()
            pg.goto(html.as_uri())
            pg.wait_for_timeout(attente)      # le temps que les polices arrivent
            pg.pdf(path=str(pdf), prefer_css_page_size=True, print_background=True)
            nav.close()
    except Exception as e:
        raise SystemExit(
            "\nLe navigateur qui imprime les PDF n'a pas démarré.\n"
            "  S'il n'est pas encore installé, une seule commande suffit :\n"
            "  Windows :        py -m playwright install chromium\n"
            "  macOS, Linux :   python3 -m playwright install chromium\n"
            f"\nCe que Playwright en dit : {type(e).__name__} — "
            f"{str(e).strip().splitlines()[0] if str(e).strip() else '(rien)'}\n"
            f"\nLa page HTML, elle, est déjà écrite : {html}\n")
    return pdf


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--papier", default="blanc", choices=sorted(PAPIERS))
    ap.add_argument("--sortie", default=None)
    ap.add_argument("--sans-pdf", action="store_true",
                    help="n'écrire que la page HTML, pour un aperçu rapide")
    a = ap.parse_args()

    html = pathlib.Path(a.sortie) if a.sortie else ICI / "impression" / "Feuille.html"
    html.parent.mkdir(exist_ok=True)
    html.write_text(page(PAPIERS[a.papier]), encoding="utf-8")
    print(f"aperçu : {html}")

    if a.sans_pdf:
        print("PDF non demandé (--sans-pdf).")
        return
    pdf = imprimer(html, html.parent / "Feuille-plan-action.pdf")
    print(f"{pdf.name} — {pdf.stat().st_size // 1024} Ko")


if __name__ == "__main__":
    main()
