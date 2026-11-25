#!/usr/bin/env python3
"""Têtes en pixel art (8 bits, esprit JRPG) des personnages de l'atelier Saumos.

    python3 cours/image-application/outils/pixels.py

Écrit donnees/pixels.json : { "elikia": "<svg…>", … }. Chaque tête a deux bouches, fermée et ouverte :
l'atelier les alterne quand le personnage parle. Dessins originaux, sur une grille de 20 × 22 pixels.

Lettres de la grille : K contour, S peau, s ombre de peau, E yeux, H cheveux, h reflet, A et a accessoires,
G lunettes, W blanc, T vêtement, t ombre du vêtement, L lèvres. Un point : transparent.
"""
import json
import os

COURS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L, H = 20, 22

BASE = [
    "....................",
    "....................",
    "....................",
    "....................",
    "......KKKKKKKK......",
    ".....KSSSSSSSSK.....",
    "....KSSSSSSSSSSK....",
    "....KSSSSSSSSSSK....",
    "....KSSSSSSSSSSK....",
    "....KSEESSSSEESK....",
    "....KSSSSSSSSSSK....",
    "....KSSSSssSSSSK....",
    "....KSSSSSSSSSSK....",
    ".....KSSSSSSSSK.....",
    "......KSSSSSSK......",
    ".......KssssK.......",
    ".....TTTssssTTT.....",
    "...TTTTTTTTTTTTTT...",
    "..TTTTTTTTTTTTTTTT..",
    "..TTTTTTTTTTTTTTTT..",
    "..TTTTTTTTTTTTTTTT..",
    "..TTTTTTTTTTTTTTTT..",
]

# Morceaux réutilisables ------------------------------------------------------------------
LUNETTES = {8: ".....GGGG..GGGG.....", 9: "....KGEEGGGGEEGK....", 10: ".....GGGG..GGGG....."}


def fusion(*couches):
    """Plusieurs couches en une : la dernière l'emporte, caractère par caractère."""
    out = {}
    for c in couches:
        for r, ligne in c.items():
            if r in out:
                ligne = "".join(b if b != "." else a for a, b in zip(out[r], ligne))
            out[r] = ligne
    return out


def cote(rangs, gauche, droite, car="H"):
    """Mèches ou rabats sur les côtés du visage, rang par rang."""
    out = {}
    for r in rangs:
        ligne = ["."] * L
        for c in gauche + droite:
            ligne[c] = car
        out[r] = "".join(ligne)
    return out


PERSOS = {
    # Elikia : foulard noué haut, lunettes rondes, blouse blanche
    "elikia": dict(
        pal=dict(S="#7A4A2E", s="#5E3720", H="#1F1612", G="#D4AF37", A="#E38226", a="#F2C94C", T="#F4F4F0", t="#D8DAE4", M="#4A2418"),
        couches=[{0: ".......AAAAA........", 1: "......AaAAAaA.......", 2: ".....AAAaAAAAA......",
                  3: "....AAAAAAaAAAA.....", 4: "....AaAAAAAAAaA.....", 5: "....AAAAaAAAAAA.....",
                  6: "....KAAAAAAAAAAK...."},
                 LUNETTES,
                 {16: ".....TTTaaaaTTT.....", 17: "...TTTTTaaaaTTTTT...", 18: "..TTTTTTaaaaTTTTTT..",
                  19: "..TTTTTTTKKTTTTTTT..", 20: "..TTTTTTTTTTTTTTTT.."}]),
    # Bastien : béret, lunettes rondes, moustache, gilet
    "bastien": dict(
        pal=dict(S="#F1C9A5", s="#D9A47E", H="#5A3A22", G="#9A6B3A", A="#1F2A55", a="#1F2A55", T="#8A5264", t="#6B3E4D", W="#F4F4F0", M="#8A4A3A"),
        couches=[{2: ".........A..........", 3: ".....AAAAAAAAAA.....", 4: "....AAAAAAAAAAAA....",
                  5: "....KAAAAAAAAAAK....", 6: "....KHSSSSSSSSHK....", 7: "....KHSSSSSSSSHK...."},
                 LUNETTES,
                 {11: "....KSSHHHHHHSSK...."},
                 {16: ".....TTTWWWWTTT.....", 17: "...TTTTTWWWWTTTTT..."}]),
    # Inès : queue de cheval, casque audio, chemise bleue et insigne orange
    "ines": dict(
        pal=dict(S="#E8B48F", s="#C98E68", H="#2A1A14", h="#4A3226", A="#6E6F7A", a="#E38226", T="#283B89", t="#1D2A66", M="#8A3B3B"),
        couches=[{3: ".....HHHHHHHHHH.....", 4: "....HHHhHHHHHHHH....", 5: "....HHHHHHHHHHHH....",
                  6: "....KHHSSSSSSHHK.HH.", 7: "....KHSSSSSSSSHKHHH.", 8: "................HH..",
                  9: "................HH..", 10: "................H..."},
                 {4: "...AAAAAAAAAAAAAA...", 8: "...A................", 9: "..AA................",
                  10: "..AA................", 11: "...AA...............", 12: "....AAA............."},
                 {18: "..TTTaTTTTTTTTTTTT.."}]),
    # Youri : chapka, sourcil levé, barbe, manteau vert
    "youri": dict(
        pal=dict(S="#F3D2BC", s="#D8AE93", H="#B9784A", A="#5B4636", a="#C8B6A2", T="#2E7D6B", t="#22604F", M="#7A4A3A"),
        couches=[{1: ".....AAAAAAAAAA.....", 2: "....AaaaaaaaaaaA....", 3: "...AAAAAAAAAAAAAA...",
                  4: "...AAAAAAAAAAAAAA...", 5: "...AAKSSSSSSSSKAA..."},
                 cote(range(6, 13), [3], [16], "A"),
                 {7: "............HH......", 8: "......HH............"},
                 {12: "....KHHSSSSSSHHK....", 13: ".....KHHHHHHHHK.....", 14: "......KHHHHHHK......"},
                 {16: ".....aaassssaaa.....", 17: "...TTaaaaaaaaaaTT..."}]),
    # Rose : carré noir à frange, boucles d'oreilles, trench et foulard rose
    "rose": dict(
        pal=dict(S="#F6D5C4", s="#E0B3A0", H="#15151C", h="#33334A", A="#C2185B", W="#F4F4F0", T="#C9AE86", t="#A88C66", M="#B3123A"),
        couches=[{3: ".....HHHHHHHHHH.....", 4: "....HHHhHHHHHHHH....", 5: "....HHHHHHHHHHHH....",
                  6: "...HHHHHHHHHHHHHH...", 7: "...HHSSSSSSSSSSHH..."},
                 cote(range(8, 14), [3, 4], [15, 16]),
                 {14: "...W..KSSSSSSK..W..."},
                 {16: ".....AAAAAAAAAA.....", 17: "...TTTAAAAAAAATTT..."}]),
    # Le préfet : képi à feuilles de chêne, moustache grise, uniforme
    "prefet": dict(
        pal=dict(S="#F0C8A8", s="#D6A684", H="#9A9AA4", A="#1D2A66", a="#D4AF37", T="#1D2A66", t="#141D4A", M="#7A4A3A"),
        couches=[{1: ".....AAAAAAAAAA.....", 2: ".....AAAAAAAAAA.....", 3: ".....aaaaaaaaaa.....",
                  4: "....aAaAaAaAaAaa....", 5: "...KKKKKKKKKKKKKK...", 6: "....KHSSSSSSSSHK...."},
                 {11: "....KSSHHHHHHSSK...."},
                 {17: "..aaaTTTTTTTTTTaaa..", 18: "..TTTTTTTaaTTTTTTT..", 20: "..TTTTTTTaaTTTTTTT.."}]),
}

# Les héros des étudiants : coupes et accessoires variés, teintes de peau variées
COIFFES = {
    "epis": {2: "......H.H.HH.H......", 3: ".....HHHHHHHHHH.....", 4: "....HHHhHHHHHHHH....",
             5: "....KHHHHHHHHHHK....", 6: "....KHSSSSSSSSHK...."},
    "longs": fusion({3: ".....HHHHHHHHHH.....", 4: "....HHHhHHHHHHHH....", 5: "...HHHHHHHHHHHHHH...",
                   6: "...HHHSSSSSSSSHHH..."}, cote(range(7, 18), [3, 4], [15, 16])),
    "afro": fusion({0: ".....HHHHHHHHHH.....", 1: "...HHHHHHHhHHHHHH...", 2: "..HHHHHHHHHHHHHHHH..",
                  3: "..HHHhHHHHHHHHHHHH..", 4: "..HHHHHHHHHHHHhHHH..", 5: "..HHHHHHHHHHHHHHHH..",
                  6: "..HHKSSSSSSSSSSKHH.."}, cote(range(7, 10), [2, 3], [16, 17])),
    "chignon": {0: "........HHHH........", 1: ".......HHhHHH.......", 2: "........HHHH........",
                3: ".....HHHHHHHHHH.....", 4: "....HHHHHHHHHHHH....", 5: "....KHHHHHHHHHHK....",
                6: "....KHSSSSSSSSHK...."},
    "casquette": {3: ".....AAAAAAAAAA.....", 4: "....AAAAAAAaAAAA....", 5: "..AAKAAAAAAAAAAK....",
                  6: "....KHSSSSSSSSHK...."},
    "foulard": fusion({3: ".....AAAAAAAAAA.....", 4: "....AAAAAAAAAAAA....", 5: "...AAAAAAAAAAAAAA...",
                     6: "...AAKSSSSSSSSKAA...", 14: "...AAAKSSSSSSKAAA...", 15: "...AAAAAAAAAAAAAA...",
                     16: "..AAAAAAAAAAAAAAAA.."}, cote(range(7, 14), [3, 4], [15, 16], "A")),
    "bonnet": {1: ".........a..........", 2: "........AAA.........", 3: ".....AAAAAAAAAA.....",
               4: "....AAAAAAAAAAAA....", 5: "....aaaaaaaaaaaa....", 6: "....KHSSSSSSSSHK...."},
    "boucles": {3: ".....H.HH.HH.H......", 4: "....HHHHHHHhHHHH....", 5: "....HHhHHHHHHHHH....",
                6: "....KHHSSSSSSHHK...."},
    "ras": {4: "......HHHHHHHH......", 5: ".....KhhhhhhhhK....."},
}
HEROS = [
    ("heros-1", "epis", False, dict(S="#F1C9A5", s="#D9A47E", H="#6B4423", h="#8C5A30", T="#E38226", t="#B8661C")),
    ("heros-2", "longs", False, dict(S="#F6D5C4", s="#E0B3A0", H="#D9B44A", h="#F0D27A", T="#541C5B", t="#3E1443")),
    ("heros-3", "afro", False, dict(S="#6B4028", s="#52301D", H="#1A1210", h="#33241C", T="#2E7D6B", t="#22604F")),
    ("heros-4", "chignon", True, dict(G="#4F6BC4", S="#F3D2BC", s="#D8AE93", H="#B5462A", h="#D26A45", T="#283B89", t="#1D2A66")),
    ("heros-5", "casquette", False, dict(S="#C68B5E", s="#A86F46", H="#2A1A14", A="#D8D33A", a="#B0AB24", T="#8A5264", t="#6B3E4D")),
    ("heros-6", "foulard", False, dict(S="#D9A37E", s="#BD8561", A="#9655A2", a="#7A4086", T="#9655A2", t="#7A4086")),
    ("heros-7", "bonnet", False, dict(S="#F1C9A5", s="#D9A47E", H="#3A2A20", A="#2E7D6B", a="#F4F4F0", T="#6E6F7A", t="#54555E")),
    ("heros-8", "boucles", True, dict(G="#D8D33A", S="#8C5A3C", s="#6E432A", H="#1F1612", h="#3A2A20", T="#E38226", t="#B8661C")),
    ("heros-9", "ras", False, dict(S="#E8B48F", s="#C98E68", H="#2A1A14", h="#4A3226", T="#283B89", t="#1D2A66")),
]
for nom, coiffe, lunettes, pal in HEROS:
    couches = [COIFFES[coiffe]] + ([LUNETTES] if lunettes else [])
    PERSOS[nom] = dict(pal=dict(pal, M=pal.get("M", "#8A3B3B")), couches=couches)

COMMUN = dict(K="#1E1A24", E="#16161E", G="#2B2B33", W="#F4F4F0", m="#D46A6A")


def grille(couches):
    g = [list(r) for r in BASE]
    for couche in couches:
        for r, ligne in couche.items():
            for c, car in enumerate(ligne):
                if car != ".":
                    g[r][c] = car
    return g


def rects(g, pal):
    """Une ligne de pixels de même couleur devient un seul rectangle."""
    out = []
    for r, ligne in enumerate(g):
        c = 0
        while c < L:
            car = ligne[c]
            if car == ".":
                c += 1
                continue
            d = c
            while d + 1 < L and ligne[d + 1] == car:
                d += 1
            coul = pal.get(car) or COMMUN.get(car)
            if coul:
                out.append(f'<rect x="{c}" y="{r}" width="{d - c + 1}" height="1" fill="{coul}"/>')
            c = d + 1
    return "".join(out)


def bouches(pal):
    m = pal.get("M", "#8A3B3B")
    fermee = f'<rect x="9" y="12" width="2" height="1" fill="{m}"/>'
    ouverte = (f'<rect x="8" y="12" width="4" height="1" fill="{m}"/>'
               f'<rect x="9" y="12" width="2" height="1" fill="{COMMUN["m"]}"/>'
               f'<rect x="9" y="13" width="2" height="1" fill="{m}"/>')
    return f'<g class="px-ferme">{fermee}</g><g class="px-ouvert">{ouverte}</g>'


def main():
    out = {}
    for nom, p in PERSOS.items():
        pal = p["pal"]
        corps = rects(grille(p["couches"]), pal)
        out[nom] = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {L} {H}" shape-rendering="crispEdges" '
                    f'class="px">{corps}{bouches(pal)}</svg>')
    chemin = os.path.join(COURS, "donnees", "pixels.json")
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=0)
    print(f"{len(out)} têtes écrites dans {chemin}")


if __name__ == "__main__":
    main()
