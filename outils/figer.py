#!/usr/bin/env python3
"""Garde-fou des diapos figées.

Chaque diapo dont la fiche porte etat="fige" reçoit une empreinte. Toute
modification, même d'un caractère, est signalée.

    python3 outils/figer.py verifier    cours/mon-cours/index.qmd
    python3 outils/figer.py enregistrer cours/mon-cours/index.qmd

« verifier » compare le cours aux empreintes enregistrées ; il échoue s'il
trouve une diapo figée modifiée ou disparue. « enregistrer » prend l'état
actuel comme nouvelle référence.
"""
import hashlib
import json
import os
import re
import sys


def diapos(texte):
    """Découpe le cours en diapos. Le début du fichier (en-tête) compte pour la couverture."""
    morceaux, courant, titre = [], [], "Couverture"
    for ligne in texte.split("\n"):
        if ligne.startswith("## "):
            morceaux.append((titre, courant))
            courant, titre = [], ligne[3:].split("{")[0].strip()
        courant.append(ligne.rstrip())
    morceaux.append((titre, courant))
    resultat = []
    for titre, lignes in morceaux:
        while lignes and lignes[-1] == "":
            lignes = lignes[:-1]
        bloc = "\n".join(lignes)
        fiche = re.search(r":::\s*\{\.fiche([^}]*)\}", bloc)
        if not fiche:
            continue
        attributs = dict(re.findall(r'([\w-]+)="([^"]*)"', fiche.group(1)))
        resultat.append({
            "n": attributs.get("n", ""),
            "etat": attributs.get("etat", "a-revoir"),
            "titre": titre,
            "empreinte": hashlib.sha256(bloc.encode("utf-8")).hexdigest()[:16],
        })
    return resultat


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("verifier", "enregistrer"):
        print(__doc__)
        return 2
    commande, cours = sys.argv[1], sys.argv[2]
    # index.qmd donne figes.json ; index-en.qmd donne figes-en.json
    suffixe = os.path.basename(cours)[len("index"):-len(".qmd")] if os.path.basename(cours).startswith("index") else ""
    registre = os.path.join(os.path.dirname(cours), "figes" + suffixe + ".json")
    with open(cours, encoding="utf-8") as f:
        actuelles = diapos(f.read())
    figees = {d["n"]: d for d in actuelles if d["etat"] == "fige"}

    if commande == "enregistrer":
        contenu = {n: {"titre": d["titre"], "empreinte": d["empreinte"]} for n, d in figees.items()}
        with open(registre, "w", encoding="utf-8") as f:
            json.dump(contenu, f, ensure_ascii=False, indent=1, sort_keys=True)
            f.write("\n")
        print(f"{len(contenu)} diapos figées enregistrées dans {registre}")
        return 0

    if not os.path.exists(registre):
        print("Aucune empreinte enregistrée : lancer d'abord « enregistrer ».")
        return 1
    with open(registre, encoding="utf-8") as f:
        reference = json.load(f)
    presentes = {d["n"]: d for d in actuelles}
    ecarts = []
    for n, ref in reference.items():
        d = presentes.get(n)
        if d is None:
            ecarts.append(f"  {n} {ref['titre']} : diapo figée disparue")
        elif d["etat"] != "fige":
            pass  # dégelée volontairement : on a le droit de la modifier
        elif d["empreinte"] != ref["empreinte"]:
            ecarts.append(f"  {n} {d['titre']} : diapo figée modifiée")
    nouvelles = [n for n in figees if n not in reference]
    degelees = [n for n, ref in reference.items() if n in presentes and presentes[n]["etat"] != "fige"]
    print(f"{len(reference)} diapos figées en référence, {len(figees)} figées dans le cours.")
    if degelees:
        print("Dégelées depuis la référence : " + ", ".join(sorted(degelees)))
    if nouvelles:
        print("Figées depuis la référence, pas encore enregistrées : " + ", ".join(nouvelles))
    if ecarts:
        print("ÉCARTS :")
        print("\n".join(ecarts))
        return 1
    print("Aucune diapo figée n'a été modifiée.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
