#!/usr/bin/env python3
"""Range les fichiers produits dans le dossier _sortie/ de chaque cours, et imprime les PDF.

Lancé tout seul par Quarto après chaque rendu (« post-render » dans _quarto.yml) :

    cours/gis-basics/index.qmd     →  cours/gis-basics/_sortie/GIS-Basics.html    (+ GIS-Basics.pdf)
    cours/gis-basics/index-en.qmd  →  cours/gis-basics/_sortie/GIS-Basics-EN.html (+ GIS-Basics-EN.pdf)

Le nom vient du titre du cours ; « -EN » s'ajoute à la version anglaise (lang: en).
Le PDF est le support avec le corrigé ; il demande Playwright (voir outils/pdf.py). Sans lui, le
rendu se fait quand même, et un message le signale.

Pendant un aperçu (quarto preview), le fichier est copié et non déplacé, pour ne pas couper l'aperçu,
et le PDF n'est pas imprimé. Pour un rendu rapide, sans PDF :  SANS_PDF=1 quarto render …
"""
import os
import re
import shutil
import subprocess
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdf as imprimante  # noqa: E402


def en_apercu():
    """Vrai si l'un des processus parents est un « quarto preview »."""
    pid = os.getppid()
    for _ in range(12):
        try:
            sortie = subprocess.run(["ps", "-o", "ppid=", "-o", "command=", "-p", str(pid)],
                                    capture_output=True, text=True, timeout=5).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            return True                     # dans le doute, on copie : rien ne se perd
        if not sortie:
            return False
        parent, _, commande = sortie.partition(" ")
        if re.search(r"\bpreview\b", commande):
            return True
        if not parent.strip().isdigit() or int(parent) <= 1:
            return False
        pid = int(parent)
    return False


def en_tete(qmd):
    """Le titre et la langue, lus dans l'en-tête YAML du cours."""
    titre, langue = None, None
    with open(qmd, encoding="utf-8") as f:
        lignes = f.read().split("\n")
    if not lignes or lignes[0].strip() != "---":
        return titre, langue
    for ligne in lignes[1:]:
        if ligne.strip() == "---":
            break
        m = re.match(r'^title:\s*["\']?(.*?)["\']?\s*$', ligne)
        if m:
            titre = m.group(1)
        m = re.match(r'^lang:\s*["\']?([\w-]+)', ligne)
        if m:
            langue = m.group(1)
    return titre, langue


def nom_de_fichier(titre, langue, defaut):
    if not titre:
        return defaut
    t = titre.replace("&nbsp;", " ")
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    t = re.sub(r"[^A-Za-z0-9]+", "-", t).strip("-")
    return (t or defaut) + ("-EN" if (langue or "").startswith("en") else "")


def main():
    racine = os.environ.get("QUARTO_PROJECT_DIR") or os.getcwd()
    sorties = [s for s in os.environ.get("QUARTO_PROJECT_OUTPUT_FILES", "").split("\n") if s.strip()]
    apercu = en_apercu()
    produits = []
    for rel in sorties:
        html = os.path.join(racine, rel)
        if not html.endswith(".html") or not os.path.exists(html):
            continue
        dossier, fichier = os.path.split(html)
        if os.path.basename(dossier) == "_sortie":
            continue
        qmd = os.path.join(dossier, os.path.splitext(fichier)[0] + ".qmd")
        titre, langue = en_tete(qmd) if os.path.exists(qmd) else (None, None)
        cible_dossier = os.path.join(dossier, "_sortie")
        os.makedirs(cible_dossier, exist_ok=True)
        cible = os.path.join(cible_dossier, nom_de_fichier(titre, langue, os.path.splitext(fichier)[0]) + ".html")
        if apercu:
            shutil.copyfile(html, cible)
        else:
            os.replace(html, cible)
        produits.append(cible)
        print("Sortie :", os.path.relpath(cible, racine))
    if apercu or not produits or os.environ.get("SANS_PDF"):
        return
    if not imprimante.disponible():
        print("PDF non imprimés : Playwright n'est pas installé (voir outils/pdf.py).")
        return
    for p in imprimante.imprimer(produits):
        print("PDF :", os.path.relpath(p, racine))


if __name__ == "__main__":
    main()
