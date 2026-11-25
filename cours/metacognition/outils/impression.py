#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Les PDF du jeu de cartes, prêts à porter chez l'imprimeur.

    python3 outils/impression.py

Écrit dans impression/ un PDF par groupe, au format A6 (105 × 148 mm),
une face par page, dans l'ordre recto, verso, recto, verso : en tirage
recto-verso, chaque feuille A6 donne une carte.

    Cartes-contexte-sur-jaune.pdf   à tirer sur le papier jaune
    Cartes-cap-sur-rose.pdf         sur le rose
    Cartes-outil-sur-vert.pdf       sur le vert

Les PDF sont tirés sur fond blanc : c'est le papier qui fait la couleur,
et l'encre est unique. Rien n'est imposé sur A4 — le massicot et la photo-
copieuse s'en chargent mieux que nous, et quatre A6 mélangés sur une A4
se retrouvent dans le désordre dès qu'une carte est ajoutée.
"""
import pathlib
import subprocess
import sys

from playwright.sync_api import sync_playwright

ICI = pathlib.Path(__file__).resolve().parent.parent
PAPIERS = {"contexte": "jaune", "cap": "rose", "outil": "vert"}


def main():
    sortie = ICI / "impression"
    sortie.mkdir(exist_ok=True)
    for vieux in sortie.glob("A4-*.pdf"):   # on ne garde pas deux formats côte à côte
        vieux.unlink()

    faits = []
    with sync_playwright() as p:
        nav = p.chromium.launch()
        page = nav.new_page()
        for groupe, papier in PAPIERS.items():
            html = sortie / f"{groupe}.html"
            subprocess.run(
                [sys.executable, str(ICI / "outils" / "cartes.py"),
                 "--groupe", groupe, "--blanc", "--sortie", str(html)],
                check=True, capture_output=True)
            page.goto(html.as_uri())
            page.wait_for_timeout(1200)      # le temps que les polices arrivent
            pdf = sortie / f"Cartes-{groupe}-sur-{papier}.pdf"
            page.pdf(path=str(pdf), prefer_css_page_size=True, print_background=True)
            html.unlink()
            faits.append(pdf)
        nav.close()

    for f in faits:
        print(f"{f.name} — {f.stat().st_size // 1024} Ko")


if __name__ == "__main__":
    main()
