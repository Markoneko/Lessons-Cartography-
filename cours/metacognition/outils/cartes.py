#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fabrique le jeu de cartes A6 à partir de donnees/fiches.json.

    python3 outils/cartes.py                  → le jeu complet
    python3 outils/cartes.py --groupe outil   → un seul groupe

Le fichier produit s'imprime en A6, une face par page, dans l'ordre
recto / verso : en recto-verso, chaque feuille donne une carte.
Quatre A6 par A4, soit six feuilles par jeu.

IMPRESSION EN UNE SEULE ENCRE, SUR PAPIER DE COULEUR.
Le groupe n'est pas signalé par un aplat mais par la couleur du papier :
contexte sur jaune, cap sur rose, outils sur vert. Tout le dessin est donc
en une seule encre sombre, sans fond ni réserve blanche — ce qui coûte
aussi beaucoup moins cher à tirer en soixante exemplaires.

    python3 outils/cartes.py --groupe contexte   → à tirer sur jaune
    python3 outils/cartes.py --groupe cap        → à tirer sur rose
    python3 outils/cartes.py --groupe outil      → à tirer sur vert
"""

import argparse
import html
import json
import pathlib
import re

ICI = pathlib.Path(__file__).resolve().parent.parent

ENCRE = "232968"   # bleu nuit Géodata : l'encre unique
GRIS = "6E6F7A"

GROUPES = {
    "contexte": ("Contexte", "jaune"),
    "cap": ("Cap", "rose"),
    "outil": ("Outil", "vert"),
}

# Les quatre marques de famille. Elles ne sont jamais légendées : les étudiants
# construisent leur propre classement, puis écrivent le nom qu'ils ont choisi.
MARQUES = {
    "extraire": '<path d="M9 5 h-6 v22 h6"/><path d="M12 16 h15"/><path d="M21 10 l6 6 l-6 6"/>',
    "revenir": '<path d="M24 11 a10 10 0 1 0 2.4 8"/><path d="M26 4 v8 h-8"/>',
    "se-regarder": '<circle cx="16" cy="16" r="11"/><circle cx="16" cy="16" r="3.5"/>',
    "respirer": '<path d="M2 16 q5 -9 10 0 t10 0"/><path d="M26 9 v14"/>',
}

# ---------------------------------------------------------------- les schémas
# Dessinés au trait, sans aplat : ils doivent tenir sur un papier teinté.
SCHEMAS = {

    "lune": """<svg viewBox="0 0 120 70"><g class="t">
      <path d="M62 8 a27 27 0 1 0 0 54 a21 21 0 1 1 0 -54 z"/>
      <circle cx="92" cy="18" r="1.6" class="p"/><circle cx="101" cy="31" r="1.2" class="p"/>
      <circle cx="86" cy="42" r="1.2" class="p"/>
    </g></svg>""",

    "sablier": """<svg viewBox="0 0 120 76"><g class="t">
      <path d="M44 6 h32 M44 70 h32"/>
      <path d="M47 6 c0 16 13 24 13 32 c0 8 -13 16 -13 32"/>
      <path d="M73 6 c0 16 -13 24 -13 32 c0 8 13 16 13 32"/>
      <path d="M52 62 h16" class="e"/>
    </g></svg>""",

    # Quatre places tenues, trois qui débordent
    "cases-memoire": """<svg viewBox="0 0 220 60"><g class="t">
      <rect x="4" y="14" width="30" height="30" rx="3"/>
      <rect x="40" y="14" width="30" height="30" rx="3"/>
      <rect x="76" y="14" width="30" height="30" rx="3"/>
      <rect x="112" y="14" width="30" height="30" rx="3"/>
      <rect x="152" y="14" width="30" height="30" rx="3" class="f"/>
      <rect x="188" y="14" width="28" height="30" rx="3" class="f"/>
      <text x="73" y="57" text-anchor="middle" class="l">ce que vous tenez</text>
      <text x="186" y="57" text-anchor="middle" class="l">ce qui déborde</text>
    </g></svg>""",

    # En blocs, puis mélangé
    "alternance": """<svg viewBox="0 0 230 74"><g class="t">
      <text x="2" y="14" class="l">en blocs</text>
      <rect x="54" y="4" width="26" height="14" rx="2"/><rect x="82" y="4" width="26" height="14" rx="2"/>
      <rect x="110" y="4" width="26" height="14" rx="2"/>
      <rect x="140" y="4" width="26" height="14" rx="2" class="h"/><rect x="168" y="4" width="26" height="14" rx="2" class="h"/>
      <rect x="196" y="4" width="26" height="14" rx="2" class="h"/>
      <text x="2" y="48" class="l">mélangé</text>
      <rect x="54" y="38" width="26" height="14" rx="2"/><rect x="82" y="38" width="26" height="14" rx="2" class="h"/>
      <rect x="110" y="38" width="26" height="14" rx="2"/>
      <rect x="140" y="38" width="26" height="14" rx="2" class="h"/><rect x="168" y="38" width="26" height="14" rx="2"/>
      <rect x="196" y="38" width="26" height="14" rx="2" class="h"/>
      <path d="M54 64 h168" class="e"/>
      <text x="138" y="72" text-anchor="middle" class="l">même temps de travail</text>
    </g></svg>""",

    # Une notion au centre, trois prises autour, à remplir
    "etoile-liens": """<svg viewBox="0 0 220 118"><g class="t">
      <circle cx="110" cy="78" r="20"/>
      <path d="M90 78 h-38 M130 78 h38 M110 58 v-16"/>
      <circle cx="34" cy="78" r="16" class="f"/>
      <circle cx="186" cy="78" r="16" class="f"/>
      <circle cx="110" cy="26" r="16" class="f"/>
    </g></svg>""",

    # La zone utile : ni trop facile, ni trop dur
    "cloche": """<svg viewBox="0 0 230 86"><g class="t">
      <path d="M8 70 h214" class="e"/>
      <path d="M14 70 C60 70 62 12 115 12 C168 12 170 70 216 70"/>
      <path d="M78 70 v-22" class="e"/><path d="M152 70 v-22" class="e"/>
      <text x="42" y="82" text-anchor="middle" class="l">trop facile</text>
      <text x="115" y="82" text-anchor="middle" class="l">la zone</text>
      <text x="190" y="82" text-anchor="middle" class="l">trop dur</text>
      <text x="115" y="30" text-anchor="middle" class="l">ce qui s'apprend</text>
    </g></svg>""",

    # Le village : des toits, et une bannière vide à remplir
    "village": """<svg viewBox="0 0 230 96"><g class="t">
      <path d="M6 88 h218" class="e"/>
      <path d="M16 88 v-20 l16 -14 l16 14 v20 z"/><path d="M28 88 v-11 h8 v11"/>
      <path d="M58 88 v-15 l13 -11 l13 11 v15 z"/>
      <path d="M152 88 v-17 l14 -12 l14 12 v17 z"/><path d="M163 88 v-10 h7 v10"/>
      <path d="M192 88 v-13 l11 -10 l11 10 v13 z"/>
      <path d="M100 88 v-34"/><path d="M134 88 v-34"/>
      <rect x="96" y="40" width="42" height="24" rx="2"/>
      <path d="M96 52 h42" class="f"/>
      <path d="M117 40 v-10 l9 5 l-9 5" class="e"/>
    </g></svg>""",
}


def propre(texte):
    """Échappe le HTML et retire le balisage [[mot|id]] des termes cliquables."""
    texte = re.sub(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", r"\1", texte or "")
    return html.escape(texte)


def zone_visuelle(v):
    """Compose l'activité du recto : un schéma, une échelle, des cases,
    des jalons, des colonnes, un cadre à dessiner ou des lignes à remplir."""
    if not v:
        return ""
    bouts = []
    if v.get("palette"):
        bouts.append('<p class="palette">' + " · ".join(propre(m) for m in v["palette"]) + "</p>")
    if v.get("consigne"):
        bouts.append(f'<p class="consigne">{propre(v["consigne"])}</p>')
    if v.get("schema"):
        bouts.append(f'<div class="schema">{SCHEMAS.get(v["schema"], "")}</div>')
    if v.get("echelle"):
        g, dr = v["echelle"]
        bouts.append(
            '<div class="echelle"><span class="bout">' + propre(g) + "</span>"
            '<span class="rail"><i></i><i></i><i></i><i></i><i></i></span>'
            '<span class="bout">' + propre(dr) + "</span></div>")
    if v.get("cases"):
        bouts.append('<p class="cases">' + "".join(
            f'<span class="case">▢ {propre(c)}</span>' for c in v["cases"]) + "</p>")
    if v.get("jalons"):
        bouts.append('<div class="jalons">' + "".join(
            f'<span class="jalon"><b>{propre(j)}</b><i></i></span>' for j in v["jalons"]) + "</div>")
    if v.get("colonnes"):
        bouts.append('<div class="colonnes">' + "".join(
            f'<span class="col"><b>{propre(c)}</b><i></i><i></i></span>' for c in v["colonnes"]) + "</div>")
    if v.get("va-avec"):
        bouts.append(f'<p class="va-avec"><b>ne marche qu\'avec</b> {propre(v["va-avec"])}</p>')
    if v.get("cadre"):
        bouts.append('<div class="cadre"></div>')
    if v.get("lignes"):
        amorces = v.get("amorces") or []
        lignes = ""
        for i in range(v["lignes"]):
            a = f'<b>{propre(amorces[i])}</b>' if i < len(amorces) else ""
            lignes += f'<span class="ligne">{a}</span>'
        bouts.append(f'<div class="lignes">{lignes}</div>')
    return f'<div class="visuel">{"".join(bouts)}</div>'


def carte(f, numero, total):
    nom_groupe, _papier = GROUPES[f["groupe"]]
    rang = f'{numero:02d}<span class="sur">/{total}</span>'

    emotions = f.get("emotions") or ([f["emotion"]] if f.get("emotion") else [])
    bloc_emotions = ""
    if emotions:
        bloc_emotions = (
            '<p class="emotions">' + " · ".join(propre(e) for e in emotions) + "</p>"
            '<p class="mention">rayez les mentions inutiles</p>')

    recto = f"""
<article class="carte recto">
  <header><span class="groupe">{nom_groupe}</span><span class="rang">{rang}</span></header>
  <div class="corps">
    <h1>{propre(f['nom'])}</h1>
    <p class="geste">{propre(f['recto'])}</p>
    {zone_visuelle(f.get('visuel'))}
  </div>
  <footer>
    <div class="ressenti">{bloc_emotions}</div>
    <div class="jauge"><span class="mention">ce que ça vaut pour moi</span><span class="etoiles">☆☆☆☆☆</span></div>
  </footer>
</article>"""

    fam = f.get("famille") or ""
    bloc_famille = ""
    if fam in MARQUES:
        bloc_famille = (
            '<div class="famille">'
            f'<svg viewBox="0 0 32 32" aria-hidden="true">{MARQUES[fam]}</svg>'
            '<span class="nommer"><i></i><b>ma famille</b></span></div>')

    chiffre = f.get("chiffre") or ""
    bloc_chiffre = (
        f'<p class="chiffre">{propre(chiffre)}</p>' if chiffre
        else '<p class="chiffre sans">pas de chiffre reconnu</p>')

    verso = f"""
<article class="carte verso">
  <header><span class="groupe">{propre(f['nom'])}</span><span class="rang">{rang}</span></header>
  <div class="corps">
    {bloc_famille}
    <p class="aussi">{propre(f.get('aussi') or '—')}</p>
    {bloc_chiffre}
    <p class="ampleur">{propre(f.get('ampleur', ''))}</p>
    <section class="ia">
      <h2>Ce que l'IA ampute</h2>
      <p>{propre(f.get('ia-ampute', ''))}</p>
    </section>
    <section class="ia retour">
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
  :root { --encre:#%(encre)s; --gris:#%(gris)s; --papier:%(papier)s; }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: #DCDEE8; color: var(--encre);
    font-family: Roboto, system-ui, sans-serif;
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
  }

  .carte {
    position: relative; width: 105mm; height: 148mm; background: var(--papier);
    display: flex; flex-direction: column; overflow: hidden;
    padding: 6mm 7mm 5mm; border-top: 2.6mm solid var(--encre);
  }
  .carte header {
    display: flex; justify-content: space-between; align-items: baseline;
    font-family: 'IBM Plex Mono', monospace; font-size: 6.4pt;
    letter-spacing: .15em; text-transform: uppercase; color: var(--encre);
    border-bottom: .3mm solid var(--encre); padding-bottom: 1.6mm;
  }
  .carte header .rang { letter-spacing: .05em; }
  .carte header .rang .sur { opacity: .55; }
  .carte .corps { flex: 1 1 auto; display: flex; flex-direction: column; min-height: 0; padding-top: 4.5mm; }
  .carte footer { border-top: .3mm solid var(--encre); padding-top: 1.8mm; }

  /* ------------------------------- recto */
  .recto h1 {
    font-family: Quicksand, sans-serif; font-weight: 700; font-size: 16.5pt;
    line-height: 1.06; letter-spacing: -.015em; margin: 0;
  }
  .recto .geste { font-size: 8.4pt; line-height: 1.5; margin: 3mm 0 0; }

  /* La zone d'activité occupe tout ce qui reste sous le texte : les champs à
     remplir sont généreux, parce qu'on écrit dessus à la main. */
  .visuel { flex: 1 1 auto; display: flex; flex-direction: column; justify-content: flex-end; gap: 2.5mm; padding-top: 4mm; }
  .visuel > * { flex: 0 0 auto; }
  .visuel .consigne { margin-bottom: 0; }
  .visuel .consigne {
    font-family: 'IBM Plex Mono', monospace; font-size: 6.4pt; line-height: 1.4;
    letter-spacing: .04em; color: var(--encre); margin: 0 0 2mm;
  }
  .visuel .palette {
    font-size: 6.6pt; line-height: 1.5; color: var(--gris); margin: 0 0 1.6mm;
  }
  .visuel .schema { margin: 0 0 2mm; }
  .visuel .schema svg { display: block; width: 100%%; height: auto; max-height: 42mm; }
  .visuel .schema .t { fill: none; stroke: var(--encre); stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; }
  .visuel .schema .e { stroke-width: .9; }
  .visuel .schema .f { stroke-dasharray: 3 2.4; }
  .visuel .schema .h { fill: var(--encre); opacity: .18; }
  .visuel .schema .l {
    font-family: 'IBM Plex Mono', monospace; font-size: 7px; fill: var(--encre);
    stroke: none; letter-spacing: .04em;
  }

  .echelle { display: flex; align-items: center; gap: 2mm; padding: 2mm 0; }
  .echelle .bout { font-size: 6.2pt; color: var(--gris); white-space: nowrap; }
  .echelle .rail {
    flex: 1 1 auto; display: flex; justify-content: space-between; align-items: center;
    border-bottom: .3mm solid var(--encre); height: 7mm;
  }
  .echelle .rail i { width: .3mm; height: 2.4mm; background: var(--encre); }

  .cases { display: flex; flex-wrap: wrap; gap: 3mm 4mm; margin: 0; }
  .cases .case { font-size: 7.4pt; white-space: nowrap; }

  .jalons { display: flex; gap: 2.5mm; }
  .jalons .jalon { flex: 1 1 0; }
  .jalons b {
    display: block; font-family: 'IBM Plex Mono', monospace; font-size: 6.2pt;
    color: var(--gris); font-weight: 400; margin-bottom: .8mm;
  }
  .jalons i { display: block; height: 11mm; border: .3mm solid var(--encre); border-radius: .8mm; }

  .colonnes { display: flex; gap: 4mm; flex: 1 1 auto; }
  .colonnes .col { flex: 1 1 0; }
  .colonnes b {
    display: block; font-family: 'IBM Plex Mono', monospace; font-size: 6.2pt;
    color: var(--gris); font-weight: 400; margin-bottom: 2mm;
  }
  .colonnes i { display: block; height: .25mm; background: var(--encre); opacity: .45; margin-bottom: 6mm; }

  .va-avec {
    font-size: 7pt; line-height: 1.4; margin: 0; padding: 1.6mm 2.4mm;
    border: .3mm solid var(--encre); border-radius: 1mm;
  }
  .va-avec b {
    font-family: 'IBM Plex Mono', monospace; font-size: 5.8pt; font-weight: 400;
    letter-spacing: .1em; text-transform: uppercase; color: var(--gris);
  }
  .cadre { flex: 1 1 auto; min-height: 26mm; border: .3mm dashed var(--encre); border-radius: 1mm; }

  .lignes { flex: 1 1 auto; display: flex; flex-direction: column; justify-content: space-between; min-height: 18mm; }
  .lignes .ligne {
    display: block; border-bottom: .25mm solid var(--encre);
    opacity: .9; flex: 1 1 0; min-height: 7mm; position: relative;
  }
  .lignes .ligne b {
    font-family: 'IBM Plex Mono', monospace; font-size: 6pt; font-weight: 400;
    color: var(--gris); position: absolute; bottom: .6mm;
  }

  .recto footer { display: flex; align-items: flex-end; justify-content: space-between; gap: 3mm; }
  .recto .emotions { font-size: 7.4pt; font-style: italic; line-height: 1.3; margin: 0; }
  .recto .mention {
    font-family: 'IBM Plex Mono', monospace; font-size: 5.4pt; letter-spacing: .06em;
    color: var(--gris); margin: .6mm 0 0;
  }
  .recto .jauge { text-align: right; flex: 0 0 auto; }
  .recto .jauge .mention { display: block; margin: 0 0 .4mm; }
  .recto .etoiles { display: block; }
  .recto .etoiles { font-size: 11pt; letter-spacing: .1em; }

  /* ------------------------------- verso */
  .verso header .groupe { font-weight: 500; }
  .verso .famille { display: flex; align-items: center; gap: 2.5mm; margin-bottom: 3.5mm; }
  .verso .famille svg {
    width: 7mm; height: 7mm; flex: 0 0 auto; fill: none; stroke: var(--encre);
    stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round;
  }
  .verso .nommer { flex: 1 1 auto; }
  .verso .nommer i { display: block; border-bottom: .25mm solid var(--encre); height: 3.6mm; }
  .verso .nommer b {
    font-family: 'IBM Plex Mono', monospace; font-size: 5.4pt; font-weight: 400;
    letter-spacing: .06em; color: var(--gris);
  }
  .verso .aussi { font-family: Quicksand, sans-serif; font-weight: 600; font-size: 9pt; margin: 0; }
  .verso .chiffre {
    font-family: 'IBM Plex Mono', monospace; font-weight: 500; font-size: 13pt;
    letter-spacing: .02em; margin: 1mm 0 1mm;
  }
  .verso .chiffre.sans {
    font-size: 6.4pt; letter-spacing: .1em; text-transform: uppercase; color: var(--gris);
    font-weight: 400; margin: 1.4mm 0 1.4mm;
  }
  .verso .ampleur { font-size: 7.8pt; line-height: 1.5; margin: 0 0 4.5mm; }
  .verso .ia { margin-bottom: 4mm; padding-left: 3mm; border-left: .6mm solid var(--encre); }
  .verso .ia.retour { border-left-style: double; border-left-width: 1mm; }
  .verso .ia h2 {
    font-family: 'IBM Plex Mono', monospace; font-weight: 400; font-size: 5.8pt;
    letter-spacing: .12em; text-transform: uppercase; color: var(--gris); margin: 0 0 .8mm;
  }
  .verso .ia p { font-size: 7.8pt; line-height: 1.5; margin: 0; }
  .verso .source { font-family: 'IBM Plex Mono', monospace; font-size: 5.6pt; line-height: 1.38; color: var(--gris); }

  /* ------------------------------- écran : planche de contact */
  @media screen {
    main { display: flex; flex-wrap: wrap; gap: 7mm; padding: 7mm; justify-content: center; }
    .carte { box-shadow: 0 2mm 6mm rgba(35,41,104,.2); }
  }

  /* ------------------------------- impression : une face par page */
  @page { size: 105mm 148mm; margin: 0; }
  @media print {
    body { background: #fff; }
    main { display: block; }
    .carte { break-after: page; page-break-after: always; box-shadow: none; }
    .carte:last-child { break-after: auto; page-break-after: auto; }
  }
</style>
</head>
<body>
<main>
%(cartes)s
</main>
</body>
</html>
"""

# Teintes d'aperçu seulement : à l'impression le papier est déjà coloré,
# donc on tire sur fond blanc et c'est le papier qui fait la couleur.
APERCU = {"contexte": "#FBF3CC", "cap": "#FBE4EC", "outil": "#DFF0DC", "": "#FFFFFF"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--groupe", default="", help="contexte, cap, outil ; vide = tout le jeu")
    ap.add_argument("--sortie", default="")
    ap.add_argument("--blanc", action="store_true",
                    help="aperçu sur fond blanc, comme à l'impression sur papier de couleur")
    args = ap.parse_args()

    jeu = json.loads((ICI / "donnees" / "fiches.json").read_text(encoding="utf-8"))
    fiches = [f for f in jeu["fiches"] if not args.groupe or f["groupe"] == args.groupe]
    if not fiches:
        raise SystemExit(f"aucune fiche pour le groupe « {args.groupe} »")

    rangs = {f["id"]: i + 1 for i, f in enumerate(jeu["fiches"])}
    total = len(jeu["fiches"])
    corps = "\n".join(carte(f, rangs[f["id"]], total) for f in fiches)
    papier = "#FFFFFF" if args.blanc else APERCU.get(args.groupe, "#FFFFFF")

    page = FEUILLE % {"encre": ENCRE, "gris": GRIS, "papier": papier, "cartes": corps}
    nom = args.groupe or "Jeu-complet"
    sortie = args.sortie or str(ICI / f"Cartes-{nom.capitalize()}.html")
    pathlib.Path(sortie).write_text(page, encoding="utf-8")

    tire = len(fiches)
    feuilles = -(-tire * 2 // 8)
    chiffres = sum(1 for f in fiches if f.get("chiffre"))
    print(f"{tire} cartes ({tire * 2} faces) → {sortie}")
    print(f"{feuilles} feuilles A4 en recto-verso, 4 cartes par feuille")
    print(f"{chiffres} cartes portent une ampleur d'effet chiffrée, {tire - chiffres} n'en ont pas")


if __name__ == "__main__":
    main()
