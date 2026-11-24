#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fabrique le jeu de cartes A5 à partir de donnees/fiches.json.

    python3 outils/cartes.py                       → A5, le jeu complet
    python3 outils/cartes.py --format a6
    python3 outils/cartes.py --groupe outil

Le fichier produit s'imprime une face par page, dans l'ordre recto / verso :
en recto-verso, chaque feuille donne une carte.

Deux formats, et ce n'est pas un choix cosmétique.
  A5 (148 x 210) : carte de travail. Elle porte une zone où l'étudiant écrit
      quand et où il appliquera le geste. Deux par A4, douze feuilles par jeu.
  A6 (105 x 148) : jeu à trier. Pas de zone d'écriture, tout tient à la main et
      sur une table. Quatre par A4, six feuilles par jeu.
"""

import argparse
import html
import json
import pathlib
import re

ICI = pathlib.Path(__file__).resolve().parent.parent

# Charte Géodata Paris
BLEU, BLEU_NUIT, ORANGE = "#2E3387", "#232968", "#E17E0A"
VIOLET, POURPRE = "#62538B", "#9C5099"
ENCRE, GRIS, FILET, FOND = "#2B2B33", "#6E6F7A", "#D8DAEC", "#F4F5FB"

GROUPES = {
    "contexte": ("Contexte", VIOLET, "ce qui doit tenir avant toute méthode"),
    "cap":      ("Cap",      ORANGE, "ce qui donne une direction au travail"),
    "outil":    ("Outil",    BLEU,   "ce que l'on fait, concrètement, pour apprendre"),
}

ECHELLE = {
    5: "effet large, plusieurs méta-analyses",
    4: "effet solide, bien établi",
    3: "effet modéré, très dépendant du contexte",
    2: "effet faible, ou contesté",
    0: "condition, pas une technique",
}

# Les quatre familles. La marque ne figure qu'au verso : au recto, elle donnerait
# la réponse de l'activité où les étudiants rangent les cartes eux-mêmes.
MARQUES = {
    "extraire": """<path d="M7 6 h-5 v20 h5" /><path d="M10 16 h16" /><path d="M20 10 l6 6 l-6 6" />""",
    "revenir": """<path d="M24 11 a10 10 0 1 0 2.4 8" /><path d="M26 4 v8 h-8" />""",
    "se-regarder": """<circle cx="16" cy="16" r="11" /><circle cx="16" cy="16" r="3.5" />""",
    "respirer": """<path d="M2 16 q5 -9 10 0 t10 0" /><path d="M26 9 v14" />""",
}
NOMS_FAMILLE = {
    "extraire": "Extraire", "revenir": "Revenir",
    "se-regarder": "Se regarder", "respirer": "Respirer",
}


def propre(texte):
    """Échappe le HTML et retire le balisage [[mot|id]] des termes cliquables."""
    texte = re.sub(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", r"\1", texte or "")
    return html.escape(texte)


def etoiles(n):
    if not n:
        return '<span class="condition">condition</span>'
    plein = '<span class="pleine">★</span>' * n
    return plein + '<span class="vide">★</span>' * (5 - n)


def carte(f, numero, total, fmt="a5"):
    nom_groupe, couleur, _ = GROUPES[f["groupe"]]
    fam = f.get("famille") or ""
    marque = ""
    if fam in MARQUES:
        marque = (
            '<div class="famille">'
            f'<svg viewBox="0 0 32 32" aria-hidden="true">{MARQUES[fam]}</svg>'
            f'<span>{NOMS_FAMILLE[fam]}</span></div>'
        )

    rang = f'{numero:02d}<span class="sur">/{total}</span>'
    aussi = f'<p class="aussi">{propre(f["aussi"])}</p>' if f.get("aussi") else ""

    # En A5, la carte est un objet de travail : l'étudiant y écrit quand et où
    # il appliquera le geste. C'est ce qui remplit le bas de la carte, et c'est
    # la matière de son plan d'action. En A6, il n'y a pas la place : le jeu
    # sert alors à trier, pas à écrire.
    protocole = ""
    if fmt == "a5":
        protocole = (
            '<div class="protocole">'
            '<h2>Chez moi, ce sera <span>quand · où · pour quelle difficulté</span></h2>'
            '<span class="ligne"></span><span class="ligne"></span><span class="ligne"></span>'
            '</div>'
        )

    recto = f"""
<article class="carte recto" style="--teinte:{couleur}">
  <header><span class="groupe">{nom_groupe}</span><span class="rang">{rang}</span></header>
  <div class="corps">
    <h1>{propre(f['nom'])}</h1>
    <p class="geste">{propre(f['recto'])}</p>
    {protocole}
  </div>
  <footer>
    <span class="emotion">{propre(f.get('emotion', ''))}</span>
    <span class="jauge">{etoiles(f.get('etoiles', 0))}</span>
  </footer>
</article>"""

    verso = f"""
<article class="carte verso" style="--teinte:{couleur}">
  <header><span class="groupe">{propre(f['nom'])}</span><span class="rang">{rang}</span></header>
  <div class="corps">
    {marque}
    {aussi}
    <p class="echelle">{ECHELLE.get(f.get('etoiles', 0), '')}</p>
    <p class="ampleur">{propre(f.get('ampleur', ''))}</p>
    <section class="ia ampute">
      <h2>Ce que l'IA ampute</h2>
      <p>{propre(f.get('ia-ampute', ''))}</p>
    </section>
    <section class="ia inversion">
      <h2>Comment le retourner</h2>
      <p>{propre(f.get('ia-inversion', ''))}</p>
    </section>
  </div>
  <footer><span class="source">{propre(f.get('source', ''))}</span></footer>
</article>"""
    return recto + verso


FEUILLE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Apprendre à apprendre — jeu de cartes</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=Roboto:ital,wght@0,300;0,400;0,500;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {
    --bleu:%(bleu)s; --bleu-nuit:%(bleu_nuit)s; --orange:%(orange)s;
    --encre:%(encre)s; --gris:%(gris)s; --filet:%(filet)s; --fond:%(fond)s;
    --larg:%(larg)smm; --haut:%(haut)smm;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: #E9EAF2; color: var(--encre);
    font-family: Roboto, system-ui, sans-serif;
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
  }

  .carte {
    position: relative; width: var(--larg); height: var(--haut); background: #fff;
    display: flex; flex-direction: column; overflow: hidden;
    border-top: 4.5mm solid var(--teinte);
  }
  .carte header {
    display: flex; justify-content: space-between; align-items: baseline;
    font-family: 'IBM Plex Mono', monospace; letter-spacing: .14em;
    text-transform: uppercase; color: var(--teinte);
    border-bottom: .35mm solid var(--filet);
  }
  .carte .rang { color: var(--gris); letter-spacing: .06em; }
  .carte .rang .sur { opacity: .6; }
  .carte .corps { flex: 1 1 auto; display: flex; flex-direction: column; }
  .carte footer {
    display: flex; justify-content: space-between; align-items: baseline;
    border-top: .35mm solid var(--filet);
  }

  /* ---- recto ---- */
  .recto h1 {
    font-family: Quicksand, sans-serif; font-weight: 700;
    line-height: 1.06; letter-spacing: -.015em; color: var(--bleu-nuit); margin: 0;
  }
  .recto .geste { color: var(--encre); margin: 0; }
  .recto .emotion { font-style: italic; color: var(--gris); }
  .recto .jauge { letter-spacing: .07em; white-space: nowrap; }
  .recto .pleine { color: var(--orange); }
  .recto .vide { color: var(--filet); }
  .recto .condition {
    font-family: 'IBM Plex Mono', monospace; letter-spacing: .11em;
    text-transform: uppercase; color: var(--teinte);
    border: .35mm solid var(--teinte); border-radius: 1mm; padding: .8mm 2.2mm;
  }

  /* La zone d'écriture, en A5 seulement */
  .protocole { flex: 1 1 auto; display: flex; flex-direction: column; padding-top: 12mm; }
  .protocole h2 {
    font-family: 'IBM Plex Mono', monospace; font-weight: 500; font-size: 7.5pt;
    letter-spacing: .12em; text-transform: uppercase; color: var(--teinte); margin: 0;
  }
  .protocole .ligne { display: block; height: .3mm; background: var(--filet); margin-top: auto; }
  .protocole h2 span { color: var(--gris); text-transform: none; letter-spacing: .06em; }

  /* ---- verso ---- */
  .verso header .groupe { color: var(--gris); letter-spacing: .09em; }
  .verso .famille {
    display: flex; align-items: center; gap: 2.6mm;
    font-family: Quicksand, sans-serif; font-weight: 600; color: var(--teinte);
  }
  .verso .famille svg {
    flex: 0 0 auto; fill: none; stroke: var(--teinte);
    stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round;
  }
  .verso .aussi {
    font-family: Quicksand, sans-serif; font-weight: 600;
    color: var(--bleu-nuit); margin: 0;
  }
  .verso .echelle {
    font-family: 'IBM Plex Mono', monospace; letter-spacing: .1em;
    text-transform: uppercase; color: var(--orange); margin: 0;
  }
  .verso .ampleur { color: var(--encre); margin: 0; }
  .verso .ia { border-left: .8mm solid var(--filet); }
  .verso .ia.ampute { border-left-color: var(--orange); }
  .verso .ia.inversion { border-left-color: var(--bleu); }
  .verso .ia h2 {
    font-family: 'IBM Plex Mono', monospace; font-weight: 500;
    letter-spacing: .12em; text-transform: uppercase; color: var(--gris); margin: 0;
  }
  .verso .ia p { margin: 0; }
  .verso .source { font-family: 'IBM Plex Mono', monospace; color: var(--gris); line-height: 1.4; }

  /* ---- échelles propres à chaque format ---- */
  .fmt-a5 .carte { padding: 11mm 13mm 9mm; }
  .fmt-a5 .carte header { font-size: 8.5pt; padding-bottom: 2.5mm; }
  .fmt-a5 .carte footer { padding-top: 3mm; }
  .fmt-a5 .recto .corps { padding-top: 10mm; }
  .fmt-a5 .recto h1 { font-size: 31pt; }
  .fmt-a5 .recto .geste { font-size: 13.5pt; line-height: 1.62; margin-top: 7mm; max-width: 108mm; }
  .fmt-a5 .recto .emotion { font-size: 11pt; }
  .fmt-a5 .recto .jauge { font-size: 14pt; }
  .fmt-a5 .recto .condition { font-size: 8pt; }
  .fmt-a5 .verso .corps { padding-top: 7mm; }
  .fmt-a5 .verso .famille { font-size: 12pt; margin-bottom: 6mm; }
  .fmt-a5 .verso .famille svg { width: 9mm; height: 9mm; }
  .fmt-a5 .verso .aussi { font-size: 12pt; margin-bottom: 1.5mm; }
  .fmt-a5 .verso .echelle { font-size: 7.5pt; margin-bottom: 2mm; }
  .fmt-a5 .verso .ampleur { font-size: 10.5pt; line-height: 1.5; margin-bottom: 7mm; }
  .fmt-a5 .verso .ia { padding-left: 4mm; margin-bottom: 5mm; }
  .fmt-a5 .verso .ia h2 { font-size: 7.5pt; margin-bottom: 1.5mm; }
  .fmt-a5 .verso .ia p { font-size: 10.5pt; line-height: 1.5; }
  .fmt-a5 .verso .source { font-size: 7.5pt; }

  .fmt-a6 .carte { padding: 7mm 8.5mm 6mm; border-top-width: 3.5mm; }
  .fmt-a6 .carte header { font-size: 6.5pt; padding-bottom: 1.8mm; }
  .fmt-a6 .carte footer { padding-top: 2mm; }
  .fmt-a6 .recto .corps { padding-top: 6mm; }
  .fmt-a6 .recto h1 { font-size: 18pt; }
  .fmt-a6 .recto .geste { font-size: 9pt; line-height: 1.5; margin-top: 4.5mm; }
  .fmt-a6 .recto .emotion { font-size: 8pt; }
  .fmt-a6 .recto .jauge { font-size: 9.5pt; }
  .fmt-a6 .recto .condition { font-size: 6pt; }
  .fmt-a6 .verso .corps { padding-top: 4mm; }
  .fmt-a6 .verso .famille { font-size: 8.5pt; margin-bottom: 3.5mm; }
  .fmt-a6 .verso .famille svg { width: 6mm; height: 6mm; }
  .fmt-a6 .verso .aussi { font-size: 8.5pt; margin-bottom: 1mm; }
  .fmt-a6 .verso .echelle { font-size: 5.8pt; margin-bottom: 1.5mm; }
  .fmt-a6 .verso .ampleur { font-size: 7.4pt; line-height: 1.42; margin-bottom: 4mm; }
  .fmt-a6 .verso .ia { padding-left: 2.8mm; margin-bottom: 3mm; }
  .fmt-a6 .verso .ia h2 { font-size: 5.8pt; margin-bottom: 1mm; }
  .fmt-a6 .verso .ia p { font-size: 7.4pt; line-height: 1.42; }
  .fmt-a6 .verso .source { font-size: 5.8pt; }

  /* ---- écran : planche de contact ---- */
  @media screen {
    main { display: flex; flex-wrap: wrap; gap: 8mm; padding: 8mm; justify-content: center; }
    .carte { box-shadow: 0 2mm 7mm rgba(35,41,104,.17); }
  }

  /* ---- impression : une face par page, recto puis verso ---- */
  @page { size: var(--larg) var(--haut); margin: 0; }
  @media print {
    body { background: #fff; }
    main { display: block; }
    .carte { break-after: page; page-break-after: always; box-shadow: none; }
    .carte:last-child { break-after: auto; page-break-after: auto; }
  }
</style>
</head>
<body class="fmt-%(fmt)s">
<main>
%(cartes)s
</main>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--groupe", default="", help="contexte, cap, outil ; vide = tout le jeu")
    ap.add_argument("--format", default="a5", choices=["a5", "a6"])
    ap.add_argument("--sortie", default="")
    args = ap.parse_args()

    jeu = json.loads((ICI / "donnees" / "fiches.json").read_text(encoding="utf-8"))
    fiches = [f for f in jeu["fiches"] if not args.groupe or f["groupe"] == args.groupe]

    total = len(fiches)
    corps = "\n".join(carte(f, i + 1, total, args.format) for i, f in enumerate(fiches))
    larg, haut = (148, 210) if args.format == "a5" else (105, 148)
    page = FEUILLE % {
        "bleu": BLEU, "bleu_nuit": BLEU_NUIT, "orange": ORANGE,
        "encre": ENCRE, "gris": GRIS, "filet": FILET, "fond": FOND,
        "larg": larg, "haut": haut, "fmt": args.format, "cartes": corps,
    }
    sortie = args.sortie or str(ICI / f"Metacognition-Cartes-{args.format.upper()}.html")
    pathlib.Path(sortie).write_text(page, encoding="utf-8")
    par_a4 = 2 if args.format == "a5" else 4
    print(f"{total} cartes ({total * 2} faces) en {args.format.upper()} → {sortie}")
    print(f"soit {-(-total * 2 // (par_a4 * 2))} feuilles A4 en recto-verso par jeu")


if __name__ == "__main__":
    main()
