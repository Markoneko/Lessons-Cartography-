#!/usr/bin/env python3
"""Imprime le PDF de chaque support, à côté de son HTML et du cours.

Lancé tout seul par Quarto après chaque rendu (« post-render » dans _quarto.yml) :

    cours/gis-basics/GIS-Basics.qmd     →  cours/gis-basics/GIS-Basics.html    (+ GIS-Basics.pdf)
    cours/gis-basics/GIS-Basics-EN.qmd  →  cours/gis-basics/GIS-Basics-EN.html (+ GIS-Basics-EN.pdf)

Le HTML est celui que produit Quarto, au nom du fichier du cours ; le PDF prend le même nom.
Le PDF est le support avec le corrigé ; il demande Playwright (voir outils/pdf.py). Sans lui, le
rendu se fait quand même, et un message le signale.

Pendant un aperçu (quarto preview), le PDF n'est pas imprimé. Pour un rendu rapide, sans PDF :
SANS_PDF=1 quarto render …
"""
import os
import re
import subprocess
import sys

# Quarto lit la sortie de ce script en UTF-8 ; sous Windows, Python écrirait en cp1252, et le premier « é »
# ferait échouer le rendu (« Windows stdio in console mode does not support writing non-UTF-8 byte sequences »).
for flux in (sys.stdout, sys.stderr):
    try:
        flux.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdf as imprimante  # noqa: E402


def processus_windows():
    """Sous Windows (pas de « ps ») : {pid: (pid du parent, ligne de commande)}, en un seul appel à PowerShell."""
    import json
    commande = ("Get-CimInstance Win32_Process | Select-Object ProcessId,ParentProcessId,CommandLine"
                " | ConvertTo-Json -Compress")
    sortie = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", commande],
                            capture_output=True, text=True, timeout=30).stdout
    liste = json.loads(sortie)
    if isinstance(liste, dict):
        liste = [liste]
    return {p["ProcessId"]: (p["ParentProcessId"], p.get("CommandLine") or "") for p in liste}


def en_apercu():
    """Vrai si l'un des processus parents est un « quarto preview »."""
    pid = os.getppid()
    if os.name == "nt":
        try:
            table = processus_windows()
        except (OSError, ValueError, subprocess.SubprocessError):
            print("Aperçu ou rendu ? Impossible de le savoir (PowerShell) : on fait comme pour un rendu.")
            return False
        for _ in range(12):
            if pid not in table:
                return False
            parent, commande = table[pid]
            if re.search(r"\bpreview\b", commande):
                return True
            pid = parent
        return False
    for _ in range(12):
        try:
            sortie = subprocess.run(["ps", "-o", "ppid=", "-o", "command=", "-p", str(pid)],
                                    capture_output=True, text=True, timeout=5).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            print("Aperçu ou rendu ? Impossible de le savoir (ps) : on fait comme pour un rendu.")
            return False
        if not sortie:
            return False
        parent, _, commande = sortie.partition(" ")
        if re.search(r"\bpreview\b", commande):
            return True
        if not parent.strip().isdigit() or int(parent) <= 1:
            return False
        pid = int(parent)
    return False


def main():
    racine = os.environ.get("QUARTO_PROJECT_DIR") or os.getcwd()
    sorties = [s for s in os.environ.get("QUARTO_PROJECT_OUTPUT_FILES", "").split("\n") if s.strip()]
    produits = []
    for rel in sorties:
        html = os.path.join(racine, rel)
        if html.endswith(".html") and os.path.exists(html):
            produits.append(html)
            print("Sortie :", os.path.relpath(html, racine))
    if not produits:
        return
    if os.environ.get("SANS_PDF"):
        print("SANS_PDF : PDF non imprimés.")
        return
    if en_apercu():
        print("Aperçu (quarto preview) : PDF non imprimés.")
        return
    if not imprimante.disponible():
        print("PDF non imprimés : Playwright n'est pas installé pour ce Python (" + sys.executable + ").")
        print("  Pour l'installer :  " + ("py" if os.name == "nt" else "python3") + " -m pip install playwright"
              + "  puis  " + ("py" if os.name == "nt" else "python3") + " -m playwright install chromium")
        return
    for p in imprimante.imprimer(produits):
        print("PDF :", os.path.relpath(p, racine))


if __name__ == "__main__":
    main()
