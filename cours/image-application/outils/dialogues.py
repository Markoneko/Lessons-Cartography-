#!/usr/bin/env python3
"""La carte des dialogues de l'atelier Saumos, pour la relecture : un script lisible et un graphe.

    python3 cours/image-application/outils/dialogues.py

Lit donnees/saumos.json et écrit, dans source/Cas1-Saumos/ :
  - dialogues-saumos.md  : chaque enquête, expert par expert, accueil, options, questions, conditions et effets ;
  - graphe-saumos.svg    : le graphe, façon Twine (une boîte par réplique, une couleur par expert ;
                           flèches pleines : « il faut avoir entendu » ; pointillés : « débloque » ;
                           flèches doubles orange : le relais entre coéquipiers). Il faut Graphviz (dot).
"""
import json
import os
import re
import shutil
import subprocess
import textwrap

COURS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(COURS, "donnees", "saumos.json"), encoding="utf-8"))
SORTIE = os.path.join(COURS, "source", "Cas1-Saumos")
EXP = {x["id"]: x for x in D["experts"]}
POST = {p["id"]: p for p in D["postures"]}
TERMES = D.get("termes", {})
MOTIF = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")


def ty(t):
    """Le texte pour le script : les termes cliquables entre ⟪ ⟫, comme le jeu les colore."""
    return MOTIF.sub(lambda m: "⟪" + m.group(1) + "⟫", t or "")


def plat(t):
    return MOTIF.sub(lambda m: m.group(1), t or "")


def options(L, opts, retrait=""):
    for o in opts:
        juste = "" if "juste" not in o else (" ✓" if o["juste"] else " ✗")
        L.append(f"{retrait}- ◆ *« {ty(o['dit'])} »*{juste} → {ty(o['r'])}{effets(o)}")
        options(L, o.get("options", []), retrait + "  ")


def effets(o):
    e = []
    if o.get("indices"):
        e.append("carnet : " + ", ".join(D["indices"][i]["titre"] for i in o["indices"]))
    if o.get("clefs"):
        e.append("🔑 " + ", ".join(D["clefs"][c] for c in o["clefs"]))
    if o.get("debloque"):
        e.append("débloque " + ", ".join(o["debloque"]))
    if o.get("cout"):
        e.append(f"−{o['cout']} confiance")
    if o.get("image"):
        e.append("montre : " + o["image"])
    return (" — *" + " ; ".join(e) + "*") if e else ""


def conditions(n):
    c = []
    for cle, mot in (("si", "si"), ("sauf", "sauf si")):
        d = n.get(cle) or {}
        morceaux = []
        if d.get("noeuds"):
            morceaux.append("entendu " + ", ".join(d["noeuds"]))
        if d.get("essais"):
            morceaux.append("déjà tenté " + ", ".join(d["essais"]))
        if d.get("indices"):
            morceaux.append("carnet " + ", ".join(D["indices"][i]["titre"] for i in d["indices"]))
        if d.get("clefs"):
            morceaux.append("clef " + ", ".join(d["clefs"]))
        if morceaux:
            c.append(mot + " " + (" et " if cle == "si" else " ou ").join(morceaux))
    if n.get("cache"):
        c.append("caché tant qu'on ne l'a pas débloqué")
    return (" `" + " ; ".join(c) + "`") if c else ""


def script():
    L = ["# Atelier Saumos — les dialogues, tels que le jeu les joue", "",
         "Fichier produit par `outils/dialogues.py` à partir de `donnees/saumos.json` : ne pas le modifier à la main,",
         "modifier le JSON puis relancer. ▶ question, ✦ aparté, ✎ réponse tapée, ◆ choix ; *effets* en italique, `conditions` en code ;",
         "⟪ ⟫ : terme technique cliquable (en couleur dans le jeu, il ouvre un aparté et s'ajoute au lexique du carnet).", ""]
    for k, E in D["enquetes"].items():
        P = POST[E["posture"]]
        L += [f"## Enquête {k} — {E['titre']}", "", f"Jouée par **{P['nom'].lower()}** ; labo : {D['labos'][E['labo']]['titre']}.", ""]
        for x in D["experts"]:
            a = E["accueils"].get(x["id"])
            L += [f"### {x['prenom']} ({x['specialite']})", ""]
            if a:
                L.append(f"**Accueil.** {ty(a['r'])}{effets(a)}")
                options(L, a.get("options", []))
                if a.get("retour"):
                    L.append(f"- ↩ au retour : {ty(a['retour'])}")
                L.append("")
            for n in E["noeuds"]:
                if n["expert"] != x["id"]:
                    continue
                signe = {"ouverte": "✎", "aparte": "✦"}.get(n.get("type"), "▶")
                L.append(f"**{n['id']}** {signe} *« {ty(n['q'])} »*{conditions(n)}  ")
                L.append(f"{ty(n['r'])}{effets(n)}")
                options(L, n.get("options", []))
                for a2 in n.get("attendu", []):
                    L.append(f"- ✎ si la réponse contient `{' + '.join(a2['motifs'])}`{' **(bonne réponse)**' if a2.get('fin') else ''} → {ty(a2['r'])}{effets(a2)}")
                if n.get("sinon"):
                    L.append(f"- ✎ sinon → {ty(n['sinon']['r'])}")
                if n.get("relais"):
                    L.append(f"- ⇄ relais : {ty(n['relais']['texte'])}")
                L.append("")
    L += ["## Le carnet", ""] + [f"- **{v['titre']}** : {ty(v['texte'])}" for v in D["indices"].values()]
    # le lexique : chaque terme, l'expert qui l'explique et les répliques où il apparaît
    ou = {}
    texte = json.dumps(D["enquetes"], ensure_ascii=False) + json.dumps(D.get("paris", []), ensure_ascii=False) + json.dumps(D.get("cadrage", {}), ensure_ascii=False) + json.dumps(D["indices"], ensure_ascii=False)
    for m in MOTIF.finditer(texte):
        ou.setdefault(m.group(2) or m.group(1), 0)
        ou[m.group(2) or m.group(1)] += 1
    noms = {x["id"]: x["prenom"] for x in D["experts"]}
    L += ["", "## Le lexique (termes cliquables)", ""]
    for k, v in TERMES.items():
        L.append(f"- **{v['mot']}** (`{k}`, expliqué par {noms.get(v.get('qui'), v.get('qui', '?'))}, {ou.get(k, 0)} occurrence(s)) : {v['texte']}")
    orphelins = sorted(set(ou) - set(TERMES))
    if orphelins:
        L.append("")
        L.append("Termes marqués dans les dialogues mais absents du lexique : " + ", ".join(orphelins))
    with open(os.path.join(SORTIE, "dialogues-saumos.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def graphe():
    def etiquette(t, n=26):
        return "\\n".join(textwrap.wrap(plat(t).replace('"', "'"), n)[:4])
    G = ['digraph saumos {', 'rankdir=LR; newrank=true; node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=10];',
         'edge [color="#6E6F7A", arrowsize=0.6];']
    for k, E in D["enquetes"].items():
        G.append(f'subgraph cluster_{k} {{ label="Enquête {k} — {POST[E["posture"]]["nom"].lower()}"; fontname="Helvetica-Bold"; color="#283B89";')
        for x, a in E["accueils"].items():
            G.append(f'"{k}:{x}" [label="{EXP[x]["prenom"]}\\naccueil", fillcolor="{EXP[x]["couleur"]}", fontcolor="white"];')
        for n in E["noeuds"]:
            forme = {"ouverte": "box3d", "aparte": "note"}.get(n.get("type"), "box")
            G.append(f'"{n["id"]}" [label="{n["id"]}\\n{etiquette(n["q"])}", shape={forme}, fillcolor="{EXP[n["expert"]]["couleur"]}33", color="{EXP[n["expert"]]["couleur"]}"];')
            G.append(f'"{k}:{n["expert"]}" -> "{n["id"]}" [color="#C9CDE6"];')
            for r in (n.get("si") or {}).get("noeuds", []):
                G.append(f'"{r}" -> "{n["id"]}";')
            for r in (n.get("si") or {}).get("essais", []):
                G.append(f'"{r}" -> "{n["id"]}" [style=dotted, label="après un essai", fontsize=8];')
            for d in n.get("debloque", []) + [d for a2 in n.get("attendu", []) for d in a2.get("debloque", [])]:
                G.append(f'"{n["id"]}" -> "{d}" [style=dashed];')
            for c in n.get("clefs", []) + [c for a2 in n.get("attendu", []) for c in a2.get("clefs", [])]:
                G.append(f'"{n["id"]}" -> "clef {c}" [color="#E38226"];')
            for c in (n.get("si") or {}).get("clefs", []):
                G.append(f'"clef {c}" -> "{n["id"]}" [color="#E38226"];')
        G.append("}")
    for c in D["clefs"]:
        G.append(f'"clef {c}" [shape=cds, fillcolor="#FFE0B2", label="🔑 {c}"];')
    for k, E in D["enquetes"].items():
        for n in E["noeuds"]:
            for s in (n.get("relais") or {}).get("depuis", []):
                G.append(f'"{s}" -> "{n["id"]}" [color="#E38226", penwidth=2.2, style=bold, label="relais", fontsize=9, fontcolor="#E38226"];')
    G.append("}")
    dot = "\n".join(G)
    if not shutil.which("dot"):
        print("Graphviz absent : graphe non produit.")
        return
    svg = subprocess.run(["dot", "-Tsvg"], input=dot, capture_output=True, text=True, check=True).stdout
    with open(os.path.join(SORTIE, "graphe-saumos.svg"), "w", encoding="utf-8") as f:
        f.write(svg)


if __name__ == "__main__":
    script()
    graphe()
    print("dialogues-saumos.md et graphe-saumos.svg écrits dans", os.path.relpath(SORTIE, COURS))
