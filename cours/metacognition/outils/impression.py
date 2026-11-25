#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Le PDF du jeu de cartes, prêt à porter chez l'imprimeur.

    python3 outils/impression.py                 le jeu entier, un seul fichier
    python3 outils/impression.py --groupe cap    un groupe à part

Écrit dans impression/ un PDF au format A6 (105 × 148 mm), une face par page,
dans l'ordre recto, verso, recto, verso : en tirage recto-verso, chaque feuille
A6 donne une carte.

Le tirage se fait sur papier blanc, en couleurs. Le groupe n'est donc plus porté
par la teinte du papier mais par celle de l'encre : un bandeau de tête, les
filets, le picto de famille et les étoiles prennent la couleur du groupe.
Rien n'est imposé sur A4 — le massicot s'en charge mieux que nous, et quatre A6
mélangés sur une A4 se retrouvent dans le désordre dès qu'une carte est ajoutée.
"""
import argparse
import pathlib
import subprocess
import sys

from playwright.sync_api import sync_playwright

ICI = pathlib.Path(__file__).resolve().parent.parent


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--groupe", default="",
                    help="contexte, cap ou outil ; vide = le jeu entier")
    args = ap.parse_args()

    sortie = ICI / "impression"
    sortie.mkdir(exist_ok=True)
    if not args.groupe:
        # un seul fichier : on efface les tirages par groupe pour ne pas
        # laisser traîner deux découpages du même jeu
        for vieux in list(sortie.glob("A4-*.pdf")) + list(sortie.glob("Cartes-*-sur-*.pdf")):
            vieux.unlink()

    nom = args.groupe or "jeu-complet"
    html = sortie / f"{nom}.html"
    commande = [sys.executable, str(ICI / "outils" / "cartes.py"),
                "--blanc", "--sortie", str(html)]
    if args.groupe:
        commande += ["--groupe", args.groupe]

    # On lit la sortie de cartes.py au lieu de l'avaler : quand il échoue, c'est
    # lui qui sait pourquoi — un JSON mal formé, le plus souvent — et son message
    # vaut mille fois mieux qu'un « returned non-zero exit status 1 ».
    fait = subprocess.run(commande, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    if fait.returncode != 0:
        raise SystemExit("\nLa fabrication des cartes a échoué. Ce que cartes.py "
                         "en dit :\n"
                         + (fait.stderr or fait.stdout or "(aucun message)").rstrip()
                         + "\n\nCorrigez cela, puis relancez l'impression.\n")
    print((fait.stdout or "").rstrip())

    pdf = sortie / f"Cartes-{nom}.pdf"
    with sync_playwright() as p:
        nav = p.chromium.launch()
        page = nav.new_page()
        page.goto(html.as_uri())
        page.wait_for_timeout(1600)      # le temps que les polices arrivent
        page.pdf(path=str(pdf), prefer_css_page_size=True, print_background=True)
        nav.close()
    html.unlink()
    print(f"{pdf.name} — {pdf.stat().st_size // 1024} Ko")


if __name__ == "__main__":
    main()
