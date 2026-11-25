#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fabrique le jeu de cartes A6 à partir de donnees/fiches.json.

    python3 outils/cartes.py                  → le jeu complet
    python3 outils/cartes.py --groupe outil   → un seul groupe

Le fichier produit s'imprime en A6, une face par page, dans l'ordre
recto / verso : en recto-verso, chaque feuille donne une carte.
Quatre A6 par A4, soit six feuilles par jeu.

IMPRESSION EN COULEURS, SUR PAPIER BLANC.
Le groupe n'est plus porté par la teinte du papier mais par celle de l'encre :
bandeau de tête, filets, picto de famille et étoiles prennent sa couleur.

    contexte → violet · cap → orange · outil → bleu

Le reste — texte courant, dessins, lignes à remplir — garde le bleu nuit de la
charte. Les petits textes utilisent une version assombrie de l'accent : l'orange
vif ne tient pas la lecture à six points sur du blanc.
"""

import argparse
import html
import json
import pathlib
import re

ICI = pathlib.Path(__file__).resolve().parent.parent

ENCRE = "232968"   # bleu nuit Géodata : l'encre unique
GRIS = "6E6F7A"

# Le tirage se fait désormais sur papier blanc : le groupe n'est plus porté par
# la couleur de la feuille mais par celle de l'encre. Chaque groupe prend une
# couleur de la charte, déclinée en deux valeurs — la vive pour les bandeaux et
# les filets, une plus sombre pour les petits textes, qui ne tiendraient pas la
# lecture en orange vif à six points.
GROUPES = {
    "contexte": ("Contexte", "jaune", "#62538B", "#52447A"),   # violet
    "cap": ("Cap", "rose", "#E17E0A", "#B5660A"),              # orange
    "outil": ("Outil", "vert", "#2E3387", "#2E3387"),          # bleu
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

    "lune": """<svg viewBox="0 0 120 72"><g class="t">
      <path class="pl" d="M64 8 A28 28 0 1 0 64 64 A34 34 0 0 1 64 8 Z"/>
      <circle class="pl" cx="94" cy="20" r="2.2"/>
      <circle class="pl" cx="103" cy="35" r="1.6"/>
      <circle class="pl" cx="90" cy="48" r="1.6"/>
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

    # Un village perché de Provence : maisons mitoyennes, toits décalés,
    # clocher au point haut, deux cyprès — et une bannière vide au premier
    # plan, où l'étudiant écrit le rôle qu'il se donne.
    # Le mouvement ouvert : « prendre du recul sur nos mécaniques propres ».
    # Un boîtier dont on a ôté le fond. Les roues sont des jantes à rayons,
    # comme en horlogerie : l'encre fait la pièce, le papier fait le vide.
    "rouages": """<svg viewBox="0 0 122 112">
      <g class="a">
      <path d="M103.0,50.0 h11 a3,3 0 0 1 0,12 h-11 Z"/>
      <path fill-rule="evenodd" d="M55.0,6.0 A50.0,50.0 0 1 1 54.9,6.0 ZM55.0,9.0 A47.0,47.0 0 1 0 55.1,9.0 Z"/>
      <path d="M63.1,56.2 L66.0,56.9 L66.0,59.1 L63.1,59.8 L62.9,60.9 L65.6,62.2 L65.1,64.3 L62.1,64.3 L61.7,65.3 L64.0,67.3 L63.0,69.2 L60.1,68.4 L59.4,69.3 L61.2,71.8 L59.7,73.4 L57.1,72.0 L56.3,72.7 L57.4,75.5 L55.6,76.7 L53.4,74.7 L52.4,75.2 L52.8,78.2 L50.8,78.9 L49.1,76.4 L48.0,76.7 L47.7,79.7 L45.6,79.9 L44.6,77.1 L43.4,77.1 L42.4,79.9 L40.3,79.7 L40.0,76.7 L38.9,76.4 L37.2,78.9 L35.2,78.2 L35.6,75.2 L34.6,74.7 L32.4,76.7 L30.6,75.5 L31.7,72.7 L30.9,72.0 L28.3,73.4 L26.8,71.8 L28.6,69.3 L27.9,68.4 L25.0,69.2 L24.0,67.3 L26.3,65.3 L25.9,64.3 L22.9,64.3 L22.4,62.2 L25.1,60.9 L24.9,59.8 L22.0,59.1 L22.0,56.9 L24.9,56.2 L25.1,55.1 L22.4,53.8 L22.9,51.7 L25.9,51.7 L26.3,50.7 L24.0,48.7 L25.0,46.8 L27.9,47.6 L28.6,46.7 L26.8,44.2 L28.3,42.6 L30.9,44.0 L31.7,43.3 L30.6,40.5 L32.4,39.3 L34.6,41.3 L35.6,40.8 L35.2,37.8 L37.2,37.1 L38.9,39.6 L40.0,39.3 L40.3,36.3 L42.4,36.1 L43.4,38.9 L44.6,38.9 L45.6,36.1 L47.7,36.3 L48.0,39.3 L49.1,39.6 L50.8,37.1 L52.8,37.8 L52.4,40.8 L53.4,41.3 L55.6,39.3 L57.4,40.5 L56.3,43.3 L57.1,44.0 L59.7,42.6 L61.2,44.2 L59.4,46.7 L60.1,47.6 L63.0,46.8 L64.0,48.7 L61.7,50.7 L62.1,51.7 L65.1,51.7 L65.6,53.8 L62.9,55.1 Z"/>
      <path d="M87.3,41.4 L89.0,42.3 L88.8,44.3 L87.0,44.8 L86.6,45.8 L87.9,47.2 L86.9,49.0 L85.1,48.8 L84.4,49.6 L85.0,51.4 L83.4,52.7 L81.8,51.7 L80.8,52.2 L80.7,54.1 L78.8,54.7 L77.6,53.2 L76.6,53.3 L75.7,55.0 L73.7,54.8 L73.2,53.0 L72.2,52.6 L70.8,53.9 L69.0,52.9 L69.2,51.1 L68.4,50.4 L66.6,51.0 L65.3,49.4 L66.3,47.8 L65.8,46.8 L63.9,46.7 L63.3,44.8 L64.8,43.6 L64.7,42.6 L63.0,41.7 L63.2,39.7 L65.0,39.2 L65.4,38.2 L64.1,36.8 L65.1,35.0 L66.9,35.2 L67.6,34.4 L67.0,32.6 L68.6,31.3 L70.2,32.3 L71.2,31.8 L71.3,29.9 L73.2,29.3 L74.4,30.8 L75.4,30.7 L76.3,29.0 L78.3,29.2 L78.8,31.0 L79.8,31.4 L81.2,30.1 L83.0,31.1 L82.8,32.9 L83.6,33.6 L85.4,33.0 L86.7,34.6 L85.7,36.2 L86.2,37.2 L88.1,37.3 L88.7,39.2 L87.2,40.4 Z"/>
      <path d="M79.8,73.2 L80.9,74.0 L80.5,75.9 L79.2,76.2 L78.7,77.1 L79.2,78.4 L78.0,79.8 L76.6,79.3 L75.8,79.9 L75.6,81.3 L73.8,81.8 L72.8,80.8 L71.8,80.8 L71.0,81.9 L69.1,81.5 L68.8,80.2 L67.9,79.7 L66.6,80.2 L65.2,79.0 L65.7,77.6 L65.1,76.8 L63.7,76.6 L63.2,74.8 L64.2,73.8 L64.2,72.8 L63.1,72.0 L63.5,70.1 L64.8,69.8 L65.3,68.9 L64.8,67.6 L66.0,66.2 L67.4,66.7 L68.2,66.1 L68.4,64.7 L70.2,64.2 L71.2,65.2 L72.2,65.2 L73.0,64.1 L74.9,64.5 L75.2,65.8 L76.1,66.3 L77.4,65.8 L78.8,67.0 L78.3,68.4 L78.9,69.2 L80.3,69.4 L80.8,71.2 L79.8,72.2 Z"/>
      </g>
      <g class="r">
      <circle cx="44.0" cy="58.0" r="17.2"/>
      <circle cx="76.0" cy="42.0" r="10.1"/>
      <circle cx="72.0" cy="73.0" r="7.0"/>
      </g>
      <g class="a">
      <rect x="43.1" y="42.6" width="1.7" height="30.9" transform="rotate(45.0 44.0 58.0)"/>
      <rect x="43.1" y="42.6" width="1.7" height="30.9" transform="rotate(135.0 44.0 58.0)"/>
      <rect x="43.1" y="42.6" width="1.7" height="30.9" transform="rotate(225.0 44.0 58.0)"/>
      <rect x="43.1" y="42.6" width="1.7" height="30.9" transform="rotate(315.0 44.0 58.0)"/>
      <circle cx="44.0" cy="58.0" r="3.7"/>
      <rect x="75.2" y="32.9" width="1.6" height="18.3" transform="rotate(45.0 76.0 42.0)"/>
      <rect x="75.2" y="32.9" width="1.6" height="18.3" transform="rotate(135.0 76.0 42.0)"/>
      <rect x="75.2" y="32.9" width="1.6" height="18.3" transform="rotate(225.0 76.0 42.0)"/>
      <rect x="75.2" y="32.9" width="1.6" height="18.3" transform="rotate(315.0 76.0 42.0)"/>
      <circle cx="76.0" cy="42.0" r="2.2"/>
      <circle cx="72.0" cy="73.0" r="2.0"/>
      </g>
      </svg>""",
    "village": """<svg viewBox="0 0 250 148">
      <path class="t e" d="M14,125 C38,122 58,118 86,115 C120,111 150,109 180,112 C208,115 228,120 238,122"/>
      <path class="m" d="M54,101 L54,60 L80,57 L80,101 Z"/>
      <path class="m" d="M80,101 L80,52 L104,50 L104,101 Z"/>
      <path class="m" d="M134,101 L134,50 L158,53 L158,101 Z"/>
      <path class="m" d="M158,101 L158,58 L182,56 L182,101 Z"/>
      <path class="m" d="M182,101 L182,64 L204,66 L204,101 Z"/>
      <path class="a" d="M51,60.3 L80,57.0 L80,61.2 L51,64.5 Z"/>
      <path class="a" d="M80,52.0 L104,50.0 L104,54.2 L80,56.2 Z"/>
      <path class="a" d="M134,50.0 L158,53.0 L158,57.2 L134,54.2 Z"/>
      <path class="a" d="M158,58.0 L182,56.0 L182,60.2 L158,62.2 Z"/>
      <path class="a" d="M182,64.0 L207,66.3 L207,70.5 L182,68.2 Z"/>
      <path class="m" d="M104,101 L104,26 L134,26 L134,101 Z"/>
      <path class="a" d="M99,28.4 L119,15 L139,28.4 L139,32.6 L119,19.2 L99,32.6 Z"/>
      <path class="t e" d="M112,56 L112,44 A7,7 0 0 1 126,44 L126,56 Z"/>
      <path class="a" d="M117,46 h4 v7 h-4 Z"/>
      <path class="m" d="M18,122 L18,86 L48,83 L48,122 Z"/>
      <path class="m" d="M48,122 L48,74 L76,76 L76,122 Z"/>
      <path class="m" d="M76,122 L76,80 L104,78 L104,122 Z"/>
      <path class="m" d="M104,122 L104,70 L134,72 L134,122 Z"/>
      <path class="m" d="M134,122 L134,82 L162,80 L162,122 Z"/>
      <path class="m" d="M162,122 L162,76 L192,78 L192,122 Z"/>
      <path class="m" d="M192,122 L192,86 L218,84 L218,122 Z"/>
      <path class="m" d="M218,122 L218,92 L238,94 L238,122 Z"/>
      <path class="a" d="M15,86.3 L48,83.0 L48,87.2 L15,90.5 Z"/>
      <path class="a" d="M48,74.0 L76,76.0 L76,80.2 L48,78.2 Z"/>
      <path class="a" d="M76,80.0 L104,78.0 L104,82.2 L76,84.2 Z"/>
      <path class="a" d="M104,70.0 L134,72.0 L134,76.2 L104,74.2 Z"/>
      <path class="a" d="M134,82.0 L162,80.0 L162,84.2 L134,86.2 Z"/>
      <path class="a" d="M162,76.0 L192,78.0 L192,82.2 L162,80.2 Z"/>
      <path class="a" d="M192,86.0 L218,84.0 L218,88.2 L192,90.2 Z"/>
      <path class="a" d="M218,92.0 L241,94.3 L241,98.5 L218,96.2 Z"/>
      <g class="a">
      <rect x="60.7" y="86" width="4" height="5.4"/>
      <rect x="69.3" y="86" width="4" height="5.4"/>
      <rect x="86.0" y="86" width="4" height="5.4"/>
      <rect x="94.0" y="86" width="4" height="5.4"/>
      <rect x="86.0" y="71" width="4" height="5.4"/>
      <rect x="94.0" y="71" width="4" height="5.4"/>
      <rect x="140.0" y="86" width="4" height="5.4"/>
      <rect x="148.0" y="86" width="4" height="5.4"/>
      <rect x="140.0" y="71" width="4" height="5.4"/>
      <rect x="148.0" y="71" width="4" height="5.4"/>
      <rect x="164.0" y="86" width="4" height="5.4"/>
      <rect x="172.0" y="86" width="4" height="5.4"/>
      <rect x="164.0" y="71" width="4" height="5.4"/>
      <rect x="172.0" y="71" width="4" height="5.4"/>
      <rect x="187.3" y="86" width="4" height="5.4"/>
      <rect x="194.7" y="86" width="4" height="5.4"/>
      <rect x="23.5" y="100" width="4" height="5.4"/>
      <rect x="31.0" y="100" width="4" height="5.4"/>
      <rect x="38.5" y="100" width="4" height="5.4"/>
      <rect x="53.0" y="100" width="4" height="5.4"/>
      <rect x="60.0" y="100" width="4" height="5.4"/>
      <rect x="67.0" y="100" width="4" height="5.4"/>
      <rect x="81.0" y="100" width="4" height="5.4"/>
      <rect x="88.0" y="100" width="4" height="5.4"/>
      <rect x="95.0" y="100" width="4" height="5.4"/>
      <rect x="109.5" y="100" width="4" height="5.4"/>
      <rect x="117.0" y="100" width="4" height="5.4"/>
      <rect x="124.5" y="100" width="4" height="5.4"/>
      <rect x="109.5" y="85" width="4" height="5.4"/>
      <rect x="117.0" y="85" width="4" height="5.4"/>
      <rect x="124.5" y="85" width="4" height="5.4"/>
      <rect x="139.0" y="100" width="4" height="5.4"/>
      <rect x="146.0" y="100" width="4" height="5.4"/>
      <rect x="153.0" y="100" width="4" height="5.4"/>
      <rect x="167.5" y="100" width="4" height="5.4"/>
      <rect x="175.0" y="100" width="4" height="5.4"/>
      <rect x="182.5" y="100" width="4" height="5.4"/>
      <rect x="198.7" y="100" width="4" height="5.4"/>
      <rect x="207.3" y="100" width="4" height="5.4"/>
      <rect x="117" y="66" width="4" height="5.4"/>
      <rect x="117" y="81" width="4" height="5.4"/>
      </g>
      <g class="a">
      <path d="M11,67 C14.5,86 15.5,107 13.6,125 L8.4,125 C6.5,107 7.5,86 11,67 Z"/>
      <path d="M245,80 C248,95 249,112 247.4,126 L242.6,126 C241,112 242,95 245,80 Z"/>
      </g>
      <path class="a" d="M52,104 L198,104 L198,106.8 L52,106.8 Z"/>
      <path class="m" d="M58,106.8 L192,106.8 L192,134 L125,145 L58,134 Z"/>
      </svg>""",

    "cairns": """<svg viewBox="0 0 120 106"><g class="a">
  <rect x="4" y="98" width="112" height="1.6" rx=".8" opacity=".5"/>
  <ellipse cx="22" cy="92" rx="15" ry="6"/><ellipse cx="22" cy="80" rx="11.5" ry="5.5"/>
  <ellipse cx="21" cy="69" rx="8.5" ry="5"/><ellipse cx="22" cy="60" rx="5.5" ry="4"/>
  <ellipse cx="60" cy="92" rx="17" ry="6.5"/><ellipse cx="60" cy="79" rx="13" ry="6"/>
  <ellipse cx="59" cy="67" rx="10" ry="5.5"/><ellipse cx="60" cy="57" rx="7.5" ry="4.5"/>
  <ellipse cx="60" cy="48" rx="5" ry="3.5"/>
  <ellipse cx="97" cy="92" rx="13" ry="6"/><ellipse cx="97" cy="81" rx="9.5" ry="5"/>
  <ellipse cx="96" cy="72" rx="6.5" ry="4"/>
</g></svg>""",
    # Deux têtes empruntées au jeu de l'atelier Saumos (Image-Application),
    # reprises en une seule encre : celle de gauche parle, celle de droite
    # écoute. Le jeu alterne déjà bouche fermée et bouche ouverte.
    "pair": """<svg viewBox="0 0 48 20" shape-rendering="crispEdges"><g class="a">
      <rect x="6" y="2" width="1" height="1"/>
      <rect x="8" y="2" width="1" height="1"/>
      <rect x="10" y="2" width="2" height="1"/>
      <rect x="13" y="2" width="1" height="1"/>
      <rect x="5" y="3" width="10" height="1"/>
      <rect x="4" y="4" width="3" height="1"/>
      <rect x="7" y="4" width="1" height="1" opacity="0.55"/>
      <rect x="8" y="4" width="8" height="1"/>
      <rect x="4" y="5" width="1" height="1"/>
      <rect x="5" y="5" width="10" height="1"/>
      <rect x="15" y="5" width="1" height="1"/>
      <rect x="4" y="6" width="1" height="1"/>
      <rect x="5" y="6" width="1" height="1"/>
      <rect x="14" y="6" width="1" height="1"/>
      <rect x="15" y="6" width="1" height="1"/>
      <rect x="4" y="7" width="1" height="1"/>
      <rect x="15" y="7" width="1" height="1"/>
      <rect x="4" y="8" width="1" height="1"/>
      <rect x="15" y="8" width="1" height="1"/>
      <rect x="4" y="9" width="1" height="1"/>
      <rect x="6" y="9" width="2" height="1"/>
      <rect x="12" y="9" width="2" height="1"/>
      <rect x="15" y="9" width="1" height="1"/>
      <rect x="4" y="10" width="1" height="1"/>
      <rect x="15" y="10" width="1" height="1"/>
      <rect x="4" y="11" width="1" height="1"/>
      <rect x="9" y="11" width="2" height="1" opacity="0.14"/>
      <rect x="15" y="11" width="1" height="1"/>
      <rect x="4" y="12" width="1" height="1"/>
      <rect x="15" y="12" width="1" height="1"/>
      <rect x="5" y="13" width="1" height="1"/>
      <rect x="14" y="13" width="1" height="1"/>
      <rect x="6" y="14" width="1" height="1"/>
      <rect x="13" y="14" width="1" height="1"/>
      <rect x="7" y="15" width="1" height="1"/>
      <rect x="8" y="15" width="4" height="1" opacity="0.14"/>
      <rect x="12" y="15" width="1" height="1"/>
      <rect x="5" y="16" width="3" height="1" opacity="0.22"/>
      <rect x="8" y="16" width="4" height="1" opacity="0.14"/>
      <rect x="12" y="16" width="3" height="1" opacity="0.22"/>
      <rect x="3" y="17" width="14" height="1" opacity="0.22"/>
      <rect x="2" y="18" width="16" height="1" opacity="0.22"/>
      <rect x="2" y="19" width="16" height="1" opacity="0.22"/>
      <rect x="8" y="12" width="4" height="1"/>
      <rect x="9" y="13" width="2" height="1"/>
      <rect x="21" y="1" width="6" height="1"/>
      <rect x="20" y="2" width="1" height="3"/>
      <rect x="27" y="2" width="1" height="3"/>
      <rect x="21" y="5" width="6" height="1"/>
      <rect x="22" y="6" width="2" height="1"/>
      <rect x="22" y="7" width="1" height="1"/>
      <rect x="21" y="3" width="1" height="1"/>
      <rect x="23" y="3" width="1" height="1"/>
      <rect x="25" y="3" width="1" height="1"/>
      <rect x="33" y="0" width="10" height="1"/>
      <rect x="31" y="1" width="7" height="1"/>
      <rect x="38" y="1" width="1" height="1" opacity="0.55"/>
      <rect x="39" y="1" width="6" height="1"/>
      <rect x="30" y="2" width="16" height="1"/>
      <rect x="30" y="3" width="3" height="1"/>
      <rect x="33" y="3" width="1" height="1" opacity="0.55"/>
      <rect x="34" y="3" width="12" height="1"/>
      <rect x="30" y="4" width="12" height="1"/>
      <rect x="42" y="4" width="1" height="1" opacity="0.55"/>
      <rect x="43" y="4" width="3" height="1"/>
      <rect x="30" y="5" width="16" height="1"/>
      <rect x="30" y="6" width="2" height="1"/>
      <rect x="32" y="6" width="1" height="1"/>
      <rect x="43" y="6" width="1" height="1"/>
      <rect x="44" y="6" width="2" height="1"/>
      <rect x="30" y="7" width="2" height="1"/>
      <rect x="32" y="7" width="1" height="1"/>
      <rect x="43" y="7" width="1" height="1"/>
      <rect x="44" y="7" width="2" height="1"/>
      <rect x="30" y="8" width="2" height="1"/>
      <rect x="32" y="8" width="1" height="1"/>
      <rect x="43" y="8" width="1" height="1"/>
      <rect x="44" y="8" width="2" height="1"/>
      <rect x="30" y="9" width="2" height="1"/>
      <rect x="32" y="9" width="1" height="1"/>
      <rect x="34" y="9" width="2" height="1"/>
      <rect x="40" y="9" width="2" height="1"/>
      <rect x="43" y="9" width="1" height="1"/>
      <rect x="44" y="9" width="2" height="1"/>
      <rect x="32" y="10" width="1" height="1"/>
      <rect x="43" y="10" width="1" height="1"/>
      <rect x="32" y="11" width="1" height="1"/>
      <rect x="37" y="11" width="2" height="1" opacity="0.14"/>
      <rect x="43" y="11" width="1" height="1"/>
      <rect x="32" y="12" width="1" height="1"/>
      <rect x="43" y="12" width="1" height="1"/>
      <rect x="33" y="13" width="1" height="1"/>
      <rect x="42" y="13" width="1" height="1"/>
      <rect x="34" y="14" width="1" height="1"/>
      <rect x="41" y="14" width="1" height="1"/>
      <rect x="35" y="15" width="1" height="1"/>
      <rect x="36" y="15" width="4" height="1" opacity="0.14"/>
      <rect x="40" y="15" width="1" height="1"/>
      <rect x="33" y="16" width="3" height="1" opacity="0.22"/>
      <rect x="36" y="16" width="4" height="1" opacity="0.14"/>
      <rect x="40" y="16" width="3" height="1" opacity="0.22"/>
      <rect x="31" y="17" width="14" height="1" opacity="0.22"/>
      <rect x="30" y="18" width="16" height="1" opacity="0.22"/>
      <rect x="30" y="19" width="16" height="1" opacity="0.22"/>
      <rect x="37" y="12" width="2" height="1"/>
      </g></svg>""",

    "spirale": """<svg viewBox="0 0 92 92"><g class="a"><path d="M46.0,39.8L46.8,39.6L47.7,39.4L48.7,39.4L49.6,39.6L50.6,39.8L51.6,40.2L52.5,40.8L53.4,41.5L54.2,42.4L54.9,43.4L55.5,44.5L55.9,45.7L56.2,47.0L56.3,48.4L56.2,49.8L55.9,51.3L55.4,52.7L54.7,54.0L53.8,55.3L52.7,56.5L51.5,57.6L50.0,58.5L48.4,59.2L46.7,59.8L44.9,60.1L43.1,60.1L41.2,60.0L39.3,59.5L37.4,58.8L35.6,57.9L34.0,56.6L32.4,55.2L31.1,53.5L29.9,51.7L29.0,49.6L28.4,47.4L28.0,45.1L27.9,42.8L28.2,40.4L28.8,38.0L29.6,35.7L30.9,33.5L32.4,31.4L34.2,29.5L36.2,27.8L38.5,26.4L41.0,25.3L43.7,24.5L46.5,24.1L49.3,24.0L52.2,24.3L55.1,24.9L57.9,26.0L60.5,27.4L63.0,29.2L65.3,31.3L67.3,33.8L69.0,36.5L70.4,39.4L71.3,42.6L71.9,45.8L72.0,49.2L71.7,52.6L71.0,56.0L69.8,59.2L68.1,62.4L66.1,65.3L63.6,68.0L60.8,70.3L57.7,72.3L54.3,74.0L50.7,75.1L47.0,75.8L43.1,76.0L39.2,75.7L35.3,74.9L31.6,73.6L28.0,71.8L24.6,69.5L21.5,66.8L18.7,63.6L16.4,60.1L14.5,56.3L13.1,52.3L12.3,48.0L12.0,43.7L12.2,39.2L13.1,34.9L14.5,30.6L16.4,26.5L18.9,22.6L21.9,19.1L25.4,16.0L29.3,13.3L33.5,11.1L38.0,9.4L42.7,8.4L47.6,7.9L52.5,8.1L57.4,9.0L62.2,10.4L66.8,12.5L71.1,15.2L75.1,18.5L78.7,22.3L78.0,22.7L74.5,19.1L70.6,15.9L66.3,13.3L61.8,11.3L57.1,9.9L52.3,9.2L47.5,9.0L42.8,9.5L38.3,10.6L33.9,12.2L29.8,14.4L26.1,17.0L22.8,20.1L20.0,23.5L17.6,27.3L15.8,31.2L14.5,35.4L13.8,39.6L13.6,43.8L13.9,47.9L14.8,51.9L16.2,55.8L18.0,59.4L20.3,62.6L22.9,65.6L25.9,68.1L29.1,70.2L32.5,71.8L36.1,73.0L39.7,73.7L43.3,73.9L46.9,73.6L50.4,72.9L53.7,71.7L56.8,70.2L59.6,68.3L62.1,66.1L64.3,63.6L66.1,60.9L67.5,58.0L68.5,55.0L69.1,51.9L69.3,48.9L69.1,45.9L68.5,42.9L67.6,40.2L66.3,37.6L64.7,35.3L62.9,33.2L60.9,31.4L58.6,29.9L56.3,28.7L53.8,27.9L51.3,27.4L48.8,27.2L46.4,27.4L44.0,27.9L41.8,28.7L39.8,29.7L37.9,31.0L36.3,32.4L34.9,34.1L33.7,35.8L32.8,37.7L32.2,39.6L31.9,41.5L31.8,43.5L32.0,45.3L32.4,47.1L33.0,48.8L33.8,50.3L34.8,51.6L35.9,52.8L37.2,53.8L38.5,54.6L39.9,55.2L41.3,55.5L42.7,55.7L44.0,55.7L45.3,55.5L46.5,55.1L47.6,54.6L48.6,54.0L49.4,53.2L50.1,52.4L50.6,51.5L51.0,50.6L51.3,49.7L51.4,48.8L51.3,48.0L51.2,47.2L50.9,46.5L50.5,45.9L50.1,45.4L49.6,44.9L49.1,44.7L48.6,44.5L48.0,44.4L47.5,44.4L47.1,44.6L46.7,44.8L46.4,45.1L46.2,45.4L46.0,45.8L46.0,46.2Z"/></g></svg>""",
    # Le compas : rien n'apparaît si on ne le fait pas tourner soi-même.
    # Une pointe qui pivote, une mine qui trace, et l'arc déjà parcouru.
    "compas": """<svg viewBox="19 0 74 109">
      <path class="t" d="M89.6,71.8
      A33.2,33.2 0 0 1 23.5,76.4"/>
      <g class="a">
      <path d="M68.4,10.7 L56.9,65.7 L56.4,71.8 L59.1,66.3 L77.6,13.3 Z"/>
      <path d="M68.4,13.3 L86.9,66.3 L89.6,71.8 L89.1,65.7 L77.6,10.7 Z"/>
      <circle cx="73" cy="12" r="7"/>
      </g>
      <circle class="m" cx="73" cy="12" r="2.6"/>
      </svg>""",

    "plomb": """<svg viewBox="0 0 100 100"><g class="a">
  <path fill-rule="evenodd" d="M50,1a5,5 0 1,0 .1,0ZM50,4a2,2 0 1,1 -.1,0Z"/>
  <rect x="49.1" y="9" width="1.8" height="50" rx=".9"/>
  <path d="M41,59h18v11l-9,21l-9,-21Z"/>
  <path d="M10,96 L90,88 90,90.4 10,98.4Z" opacity=".45"/>
</g></svg>""",

    "niveau": """<svg viewBox="0 0 120 56"><g class="a">
  <path fill-rule="evenodd" d="M4,15h112a5,5 0 0,1 5,5v17a5,5 0 0,1 -5,5h-112a5,5 0 0,1 -5,-5v-17a5,5 0 0,1 5,-5Z
     M26,21h68a7.5,7.5 0 0,1 0,15h-68a7.5,7.5 0 0,1 0,-15Z"/>
  <circle cx="79" cy="28.5" r="5.6"/>
  <rect x="53" y="21" width="1.5" height="15"/><rect x="65" y="21" width="1.5" height="15"/>
  <rect x="12" y="46" width="24" height="1.6" rx=".8" opacity=".45"/>
  <rect x="84" y="46" width="24" height="1.6" rx=".8" opacity=".45"/>
</g></svg>""",
    # La courbe de l'oubli, échantillonnée sur la vraie exponentielle. Chaque
    # retour double la constante de temps : la pente de départ est divisée par
    # deux d'un segment à l'autre, et la dernière décroissance est presque plate.
    # Le pointillé est le même début de courbe, poursuivi sans jamais revenir.
    "oubli": """<svg viewBox="0 0 250 112"><g class="t">
      <path d="M26 96 h214 M26 96 v-82" class="e"/>
      <path d="M26.0,14.0 L28.0,20.1 L30.0,25.7 L32.0,30.9 L34.0,35.7 L36.0,40.2 L38.0,44.3 L40.0,48.1 L42.0,51.7 L44.0,55.0 L46.0,58.0 L48.0,60.8 L50.0,63.4 L52.0,65.8 L54.0,68.1 L56.0,70.1 L58.0,72.1 L60.0,73.8 L62.0,75.5 L64.0,77.0 L66.0,78.4 L68.0,79.7 L70.0,80.9 L72.0,82.0 L74.0,83.1 L76.0,84.0 L78.0,84.9 L80.0,85.7 L82.0,86.5 L84.0,87.2 L86.0,87.8 L88.0,88.4 L90.0,89.0 L92.0,89.5 L94.0,90.0 L96.0,90.4 L98.0,90.9 L100.0,91.2 L102.0,91.6 L104.0,91.9 L106.0,92.2 L108.0,92.5 L110.0,92.8 L112.0,93.0 L114.0,93.2 L116.0,93.4 L118.0,93.6 L120.0,93.8 L122.0,94.0 L124.0,94.1 L126.0,94.2 L128.0,94.4 L130.0,94.5 L132.0,94.6 L134.0,94.7 L136.0,94.8 L138.0,94.9 L140.0,95.0 L142.0,95.1 L144.0,95.1 L146.0,95.2 L148.0,95.2 L150.0,95.3 L152.0,95.4 L154.0,95.4 L156.0,95.4 L158.0,95.5 L160.0,95.5 L162.0,95.6 L164.0,95.6 L166.0,95.6 L168.0,95.7 L170.0,95.7 L172.0,95.7 L174.0,95.7 L176.0,95.7 L178.0,95.8 L180.0,95.8 L182.0,95.8 L184.0,95.8 L186.0,95.8 L188.0,95.8 L190.0,95.9 L192.0,95.9 L194.0,95.9 L196.0,95.9 L198.0,95.9 L200.0,95.9 L202.0,95.9 L204.0,95.9 L206.0,95.9 L208.0,95.9 L210.0,95.9 L212.0,95.9 L214.0,95.9 L216.0,95.9 L218.0,95.9 L220.0,96.0 L222.0,96.0 L224.0,96.0 L226.0,96.0 L228.0,96.0 L230.0,96.0 L232.0,96.0 L234.0,96.0 L236.0,96.0 L238.0,96.0 L240.0,96.0 L242.0,96.0" class="f"/>
      <path d="M26.0,14.0 L28.0,20.1 L30.0,25.7 L32.0,30.9 L34.0,35.7 L36.0,40.2 L38.0,44.3 L40.0,48.1 L42.0,51.7 L44.0,55.0 L46.0,58.0 L48.0,60.8 L50.0,63.4 L52.0,65.8 L54.0,68.1 L56.0,70.1 L58.0,72.1 L60.0,73.8 L62.0,75.5 L64.0,77.0 L66.0,78.4 L68.0,79.7 L70.0,80.9 L72.0,82.0 L74.0,83.1"/>
      <path d="M74.0,83.1 V14"/>
      <path d="M74.0,14.0 L76.0,17.1 L78.0,20.1 L80.0,22.9 L82.0,25.7 L84.0,28.3 L86.0,30.9 L88.0,33.4 L90.0,35.7 L92.0,38.0 L94.0,40.2 L96.0,42.3 L98.0,44.3 L100.0,46.3 L102.0,48.1 L104.0,49.9 L106.0,51.7 L108.0,53.4 L110.0,55.0 L112.0,56.5 L114.0,58.0 L116.0,59.4 L118.0,60.8 L120.0,62.1 L122.0,63.4 L124.0,64.7 L126.0,65.8 L128.0,67.0"/>
      <path d="M128.0,67.0 V14"/>
      <path d="M128.0,14.0 L130.0,15.5 L132.0,17.0 L134.0,18.4 L136.0,19.9 L138.0,21.3 L140.0,22.6 L142.0,24.0 L144.0,25.3 L146.0,26.6 L148.0,27.9 L150.0,29.1 L152.0,30.3 L154.0,31.5 L156.0,32.7 L158.0,33.9 L160.0,35.0 L162.0,36.1 L164.0,37.2 L166.0,38.3 L168.0,39.4 L170.0,40.4 L172.0,41.4 L174.0,42.4 L176.0,43.4 L178.0,44.4 L180.0,45.3 L182.0,46.3 L184.0,47.2 L186.0,48.1 L188.0,49.0 L190.0,49.8 L192.0,50.7 L194.0,51.5 L196.0,52.3"/>
      <path d="M196.0,52.3 V14"/>
      <path d="M196.0,14.0 L198.0,14.7 L200.0,15.4 L202.0,16.1 L204.0,16.8 L206.0,17.5 L208.0,18.2 L210.0,18.8 L212.0,19.5 L214.0,20.2 L216.0,20.8 L218.0,21.5 L220.0,22.1 L222.0,22.8 L224.0,23.4 L226.0,24.0 L228.0,24.7 L230.0,25.3 L232.0,25.9 L234.0,26.5 L236.0,27.1 L238.0,27.7 L240.0,28.3 L242.0,28.9"/>
      <text x="22" y="18" text-anchor="end" class="l">tout</text>
      <text x="22" y="99" text-anchor="end" class="l">rien</text>
      <text x="238" y="108" text-anchor="end" class="l">le temps</text>
      <text x="150" y="92" class="l">sans retour</text>
      <text x="80" y="10" class="l">chaque retour relance</text>
      </g></svg>""",

}

SCHEMAS["profils"] = SCHEMAS["pair"]
SCHEMAS["main"] = SCHEMAS["compas"]


RANGS = {}


def propre(texte):
    """Échappe le HTML et retire le balisage [[mot|id]] des termes cliquables."""
    texte = re.sub(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", r"\1", texte or "")
    return html.escape(texte)


def zone_visuelle(v, paire=""):
    """Compose l'activité du recto : un schéma, une échelle, des cases,
    des jalons, des colonnes, un cadre à dessiner ou des lignes à remplir."""
    if not v and not paire:
        return ""
    v = v or {}
    bouts = []
    if v.get("palette"):
        # Un nuage de mots. Tous les mots ont la même taille et la même graisse :
        # aucun n'est proposé avant un autre, c'est à l'étudiant de choisir. Seule
        # la position varie — un peu haut, un peu bas, un peu de biais — pour que
        # l'œil se promène au lieu de lire une liste.
        decal = [0, -1.5, 1.1, -0.7, 1.6, -1.2, .5, -1.7, 1.3, -.4, .9, -1]
        tourne = [-3, 2, -1.5, 3, -2.5, 1, -3.5, 2.5, -1, 1.5, -2, 3.5]
        mots = "".join(
            f'<span style="transform:translateY({decal[i % len(decal)]}mm)'
            f' rotate({tourne[i % len(tourne)]}deg)">{propre(m)}</span>'
            for i, m in enumerate(v["palette"]))
        bouts.append(f'<div class="nuage">{mots}</div>')
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
    nom_groupe = GROUPES[f["groupe"]][0]
    rang = f'{numero:02d}<span class="sur">/{total}</span>'

    emotions = f.get("emotions") or ([f["emotion"]] if f.get("emotion") else [])
    bloc_emotions = ""
    if emotions:
        bloc_emotions = (
            '<p class="emotions">' + " · ".join(propre(e) for e in emotions) + "</p>"
            '<p class="mention">rayez les mentions inutiles</p>')

    va_avec = (f.get("visuel") or {}).get("va-avec") or f.get("va-avec") or ""
    paire = (f'<p class="va-avec"><b>ne marche qu\'avec :</b> {propre(va_avec)}</p>'
             if va_avec else "")

    groupe = f["groupe"]
    recto = f"""
<article class="carte recto" data-groupe="{groupe}">
  <header><span class="groupe">{nom_groupe}</span><span class="rang">{rang}</span></header>
  <div class="corps">
    <h1>{propre(f['nom'])}</h1>
    <p class="geste">{propre(f['recto'])}</p>
    {zone_visuelle(f.get('visuel'))}
    {paire}
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

    sv = f.get("schema-verso") or ""
    schema_verso = (f'<div class="schema schema-verso">{SCHEMAS.get(sv, "")}</div>'
                    if sv in SCHEMAS else "")

    renvoi = f.get("renvoi-ia") or ""
    if renvoi and renvoi in RANGS:
        n, titre = RANGS[renvoi]
        bloc_ia = ('<section class="renvoi"><h2>Le versant IA de ce geste</h2>'
                   f'<p>est traité sur la carte {n:02d} · {propre(titre)}</p></section>')
    else:
        bloc_ia = f"""<section class="ia">
      <h2>Ce que l'IA ampute</h2>
      <p>{propre(f.get('ia-ampute', ''))}</p>
    </section>
    <section class="ia retour">
      <h2>Comment le retourner</h2>
      <p>{propre(f.get('ia-inversion', ''))}</p>
    </section>"""

    chiffre = f.get("chiffre") or ""
    bloc_chiffre = (
        f'<p class="chiffre">{propre(chiffre)}</p>' if chiffre
        else '<p class="chiffre sans">pas de chiffre reconnu</p>')

    verso = f"""
<article class="carte verso" data-groupe="{groupe}">
  <header><span class="groupe">{propre(f['nom'])}</span><span class="rang">{rang}</span></header>
  <div class="corps">
    {bloc_famille}
    <p class="aussi">{propre(f.get('aussi') or '—')}</p>
    {bloc_chiffre}
    <p class="ampleur">{propre(f.get('ampleur', ''))}</p>
    {schema_verso}
    {bloc_ia}
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
  /* l'accent vaut l'encre tant qu'aucun groupe n'est déclaré */
  .carte { --accent: var(--encre); --accent-texte: var(--encre); }
  .carte[data-groupe="contexte"] { --accent: #62538B; --accent-texte: #52447A; }
  .carte[data-groupe="cap"] { --accent: #E17E0A; --accent-texte: #B5660A; }
  .carte[data-groupe="outil"] { --accent: #2E3387; --accent-texte: #2E3387; }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: #DCDEE8; color: var(--encre);
    font-family: Roboto, system-ui, sans-serif;
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
  }

  .carte {
    position: relative; width: 105mm; height: 148mm; background: var(--papier);
    display: flex; flex-direction: column; overflow: hidden;
    padding: 6mm 7mm 5mm; border-top: 2.6mm solid var(--accent);
  }
  .carte header {
    display: flex; justify-content: space-between; align-items: baseline;
    font-family: 'IBM Plex Mono', monospace; font-size: 6.4pt;
    letter-spacing: .15em; text-transform: uppercase; color: var(--accent-texte);
    border-bottom: .3mm solid var(--accent); padding-bottom: 1.6mm;
  }
  .carte header .rang { letter-spacing: .05em; }
  .carte header .rang .sur { opacity: .55; }
  .carte .corps { flex: 1 1 auto; display: flex; flex-direction: column; min-height: 0; padding-top: 4.5mm; }
  .carte footer { border-top: .3mm solid var(--accent); padding-top: 1.8mm; }

  /* ------------------------------- recto */
  .recto h1 {
    font-family: Quicksand, sans-serif; font-weight: 700; font-size: 16.5pt;
    line-height: 1.06; letter-spacing: -.015em; margin: 0;
  }
  .recto .geste { font-size: 8.4pt; line-height: 1.5; margin: 3mm 0 0; }

  /* La zone d'activité occupe tout ce qui reste sous le texte : les champs à
     remplir sont généreux, parce qu'on écrit dessus à la main. */
  .visuel { flex: 1 1 0; min-height: 0; overflow: hidden; display: flex; flex-direction: column; justify-content: center; gap: 2.5mm; padding: 5mm 0 4mm; }
  .visuel > * { flex: 0 0 auto; min-height: 0; }
  .visuel .schema { flex: 0 1 auto; overflow: hidden; }
  .visuel .consigne { margin-bottom: 0; }
  .visuel .consigne {
    font-family: 'IBM Plex Mono', monospace; font-size: 6.4pt; line-height: 1.4;
    letter-spacing: .04em; color: var(--encre); margin: 0 0 2mm;
  }
  .nuage {
    display: flex; flex-wrap: wrap; align-items: center; justify-content: center;
    gap: 1.4mm 3.4mm; font-family: Quicksand, sans-serif; font-weight: 600;
    font-size: 10.5pt; line-height: 1.18; text-align: center; padding: 1.4mm 0;
  }
  .nuage span { display: inline-block; }
  .schema { margin: 0 0 2mm; }
  .schema svg { display: block; width: 100%%; height: auto; max-height: 44mm; }
  .schema .t { fill: none; stroke: var(--encre); stroke-width: 1.5; stroke-linecap: round; stroke-linejoin: round; }
  .schema .e { stroke-width: .9; }
  .schema .f { stroke-dasharray: 3 2.4; }
  .schema .h { fill: var(--encre); opacity: .18; }
  .schema .pl { fill: var(--encre); stroke: none; }
  .schema .a { fill: var(--encre); stroke: none; }
  /* un volume plein : le papier à l'intérieur, l'encre au pourtour. Ce qui est
     derrière est masqué — un mur n'est jamais coupé par ce qu'il cache. */
  .schema .m {
    fill: var(--papier); stroke: var(--encre); stroke-width: 1.1;
    stroke-linejoin: round;
  }
  /* la réserve seule : le papier, sans contour — pour évider une masse d'encre */
  .schema .r { fill: var(--papier); stroke: none; }
  .schema .l {
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
    flex: 0 0 auto; margin: 0 0 1.5mm; font-size: 7pt; line-height: 1.4; padding: 1.6mm 2.4mm;
    border: .3mm solid var(--accent); border-radius: 1mm;
  }
  .va-avec b {
    font-family: 'IBM Plex Mono', monospace; font-size: 5.8pt; font-weight: 400;
    letter-spacing: .1em; text-transform: uppercase; color: var(--gris);
  }
  .cadre { flex: 1 1 auto; min-height: 26mm; border: .3mm dashed var(--encre); border-radius: 1mm; }

  .lignes { flex: 0 0 auto; display: flex; flex-direction: column; gap: 2mm; }
  .lignes .ligne {
    display: block; border-bottom: .25mm solid var(--encre);
    opacity: .9; flex: 0 0 auto; height: 8mm; position: relative;
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
  .recto .etoiles { font-size: 11pt; letter-spacing: .1em; color: var(--accent); }

  /* ------------------------------- verso */
  .verso header .groupe { font-weight: 500; }
  .verso .famille { display: flex; align-items: center; gap: 2.5mm; margin-bottom: 3.5mm; }
  .verso .famille svg {
    width: 7mm; height: 7mm; flex: 0 0 auto; fill: none; stroke: var(--accent);
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
  .verso .ampleur { font-size: 7.8pt; line-height: 1.5; margin: 0 0 3mm; }
  .verso .schema-verso { margin: 0 0 4mm; }
  .verso .schema-verso svg { max-height: 30mm; }
  .verso .ia { margin-bottom: 4mm; padding-left: 3mm; border-left: .6mm solid var(--accent); }
  .verso .ia.retour { border-left-style: double; border-left-width: 1mm; }
  .verso .ia h2 {
    font-family: 'IBM Plex Mono', monospace; font-weight: 400; font-size: 5.8pt;
    letter-spacing: .12em; text-transform: uppercase; color: var(--gris); margin: 0 0 .8mm;
  }
  .verso .ia p { font-size: 7.8pt; line-height: 1.5; margin: 0; }
  .verso .renvoi {
    border: .3mm solid var(--accent); border-radius: 1mm; padding: 2.4mm 3mm; margin-bottom: 4mm;
  }
  .verso .renvoi h2 {
    font-family: 'IBM Plex Mono', monospace; font-weight: 400; font-size: 5.8pt;
    letter-spacing: .12em; text-transform: uppercase; color: var(--gris); margin: 0 0 .8mm;
  }
  .verso .renvoi p { font-size: 8.2pt; line-height: 1.4; margin: 0; }
  .verso .source { font-family: 'IBM Plex Mono', monospace; font-size: 5.6pt; line-height: 1.38; color: var(--gris); }

  /* ------------------------------- imposition : 4 cartes par A4 */
  .planche {
    width: 210mm; height: 296mm; display: grid;
    grid-template-columns: 105mm 105mm; grid-template-rows: 148mm 148mm;
    background: var(--papier);
  }
  .planche .carte { box-shadow: none !important; }
  .carte.vide { border-top: 0; background: var(--papier); }
  body.a4 main { display: block; padding: 0; }
  @media screen { body.a4 .planche { margin: 0 auto 8mm; box-shadow: 0 2mm 7mm rgba(35,41,104,.22); } }
  @media print {
    body.a4 .planche { break-after: page; page-break-after: always; box-shadow: none; }
    body.a4 .planche:last-child { break-after: auto; page-break-after: auto; }
    body.a4 .carte { break-after: auto !important; page-break-after: auto !important; }
  }

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


def derniere_version():
    """Le fichier de fiches le plus récent : fichesV12 l'emporte sur fichesV9,
    et fiches.json ne sert que si aucune version numérotée n'existe. Marc
    travaille en versions successives ; le générateur suit sans rien à régler."""
    dossier = ICI / "donnees"
    versions = []
    for f in dossier.glob("fichesV*.json"):
        m = re.fullmatch(r"fichesV(\d+)", f.stem)
        if m:
            versions.append((int(m.group(1)), f))
    if versions:
        return max(versions)[1]
    simple = dossier / "fiches.json"
    if simple.exists():
        return simple
    raise SystemExit("aucun fichier de fiches dans donnees/")


def impose_a4(corps):
    """Quatre cartes A6 par page A4, prêtes à tirer en recto-verso.

    Les faces arrivent en recto, verso, recto, verso. On remplit d'abord une
    page de quatre rectos, puis la page des quatre versos correspondants, en
    inversant les colonnes : avec un retournement sur le bord long, chaque
    verso retombe derrière son recto.
    """
    morceaux = [m for m in corps.split("<article") if m.strip()]
    morceaux = ["<article" + m for m in morceaux]
    rectos = morceaux[0::2]
    versos = morceaux[1::2]

    pages = []
    for d in range(0, len(rectos), 4):
        r = rectos[d:d + 4]
        v = versos[d:d + 4]
        while len(r) < 4:
            r.append('<article class="carte vide"></article>')
            v.append('<article class="carte vide"></article>')
        # colonnes inversées au verso : 2,1,4,3
        v = [v[1], v[0], v[3], v[2]]
        pages.append('<section class="planche">' + "".join(r) + "</section>")
        pages.append('<section class="planche">' + "".join(v) + "</section>")
    return "\n".join(pages)


def lire_fiches(source):
    """Charge le fichier de fiches, et explique l'erreur plutôt que de la jeter.

    Un JSON à la main se casse toujours de la même façon : une virgule oubliée
    entre deux entrées, une virgule en trop avant une accolade fermante, ou un
    guillemet droit tapé au milieu d'un texte. Le message de Python donne une
    ligne et une colonne, mais pas la ligne elle-même ; on la montre.
    """
    texte = source.read_text(encoding="utf-8")
    try:
        return json.loads(texte)
    except json.JSONDecodeError as e:
        lignes = texte.splitlines()
        debut = max(0, e.lineno - 3)
        vu = []
        for n in range(debut, min(len(lignes), e.lineno + 2)):
            marque = "→" if n + 1 == e.lineno else " "
            vu.append(f"  {marque} {n + 1:>4} | {lignes[n]}")
            if n + 1 == e.lineno:
                vu.append("       " + " " * (len(str(e.lineno)) + e.colno) + "^")
        raise SystemExit(
            f"\n{source.name} n'est pas un JSON valide.\n"
            f"  ligne {e.lineno}, colonne {e.colno} : {e.msg}\n\n"
            + "\n".join(vu)
            + "\n\n  Trois causes, par ordre de fréquence :\n"
              "  · une virgule manque à la fin de la ligne précédente ;\n"
              "  · une virgule est restée avant un } ou un ] ;\n"
              "  · un guillemet droit \" a été tapé dans un texte — il faut\n"
              "    l'écrire \\\" ou utiliser des guillemets français « ».\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fiches", default="",
                    help="fichier de fiches ; par défaut la version la plus récente de donnees/")
    ap.add_argument("--groupe", default="", help="contexte, cap, outil ; vide = tout le jeu")
    ap.add_argument("--sortie", default="")
    ap.add_argument("--a4", action="store_true",
                    help="impose quatre cartes par page A4, prêt à tirer en recto-verso")
    ap.add_argument("--blanc", action="store_true",
                    help="aperçu sur fond blanc, comme à l'impression sur papier de couleur")
    args = ap.parse_args()

    source = args.fiches and pathlib.Path(args.fiches) or derniere_version()
    jeu = lire_fiches(source)
    fiches = [f for f in jeu["fiches"] if not args.groupe or f["groupe"] == args.groupe]
    if not fiches:
        raise SystemExit(f"aucune fiche pour le groupe « {args.groupe} »")

    RANGS.update({f["id"]: (i + 1, f["nom"]) for i, f in enumerate(jeu["fiches"])})
    rangs = {i: n for i, (n, _t) in RANGS.items()}
    total = len(jeu["fiches"])
    corps = "\n".join(carte(f, rangs[f["id"]], total) for f in fiches)
    papier = "#FFFFFF" if args.blanc else APERCU.get(args.groupe, "#FFFFFF")

    if args.a4:
        corps = impose_a4(corps)
    page = FEUILLE % {"encre": ENCRE, "gris": GRIS, "papier": papier, "cartes": corps}
    if args.a4:
        page = page.replace("@page { size: 105mm 148mm; margin: 0; }",
                            "@page { size: 210mm 297mm; margin: 0; }")
        page = page.replace("<body>", '<body class="a4">', 1)
    nom = args.groupe or "Jeu-complet"
    sortie = args.sortie or str(ICI / f"Cartes-{nom.capitalize()}.html")
    pathlib.Path(sortie).write_text(page, encoding="utf-8")

    tire = len(fiches)
    feuilles = -(-tire * 2 // 8)
    chiffres = sum(1 for f in fiches if f.get("chiffre"))
    print(f"source : {source.name}")
    print(f"{tire} cartes ({tire * 2} faces) → {sortie}")
    print(f"{feuilles} feuilles A4 en recto-verso, 4 cartes par feuille")
    print(f"{chiffres} cartes portent une ampleur d'effet chiffrée, {tire - chiffres} n'en ont pas")


if __name__ == "__main__":
    main()
