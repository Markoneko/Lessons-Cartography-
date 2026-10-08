# Journal du projet

Décisions et constats, du plus récent au plus ancien.

## 2026-10-08 (suite) — Retours de Marc sur le premier test

**Décidé**

- PowerPoint sort du processus. Deux sorties seulement : le HTML pour l'interaction avec les étudiants, le PDF comme support de cours.
- Le niveau se lit devant le titre, plus en haut à droite.
- Nouveau code des niveaux, proposé par Marc : trois formes tirées des strates du logo, qui évoquent chacune l'initiale du niveau.
  Socle : trois strates à décrochement, gras, bleu (S). Appui : deux strates en crête, moyen, orange (A). Veille : une strate en creux, fin, violet (V).
  Le code combine forme, nombre, épaisseur et couleur.

**Ajouté**

- Carte du cours cliquable : chaque ligne mène à sa diapo, chaque pictogramme ramène à la carte, et une pastille indique la partie.
- Le PDF porte le corrigé des exercices ; `&reponses=non` donne la version vierge. Il est maintenant paginé.
- Espaces insécables de la typographie française posées automatiquement.

**À trancher par Marc**

- Deux variantes de pictogramme sont montrées sur la diapo « Le code des niveaux » : un A barré, un V double.
- « Faire des liens » dans la carte : aujourd'hui ce sont des liens de navigation. Des liens de prérequis entre concepts, comme dans la Canopée, demanderaient de déclarer ces prérequis sur chaque diapo.

**Ensuite**

- Marc installe Quarto pour vérifier la prise en main sans assistance.
- Organiser la production : un plan de cours comme point de départ, et un stockage propre des images.

## 2026-10-08 — Premier test du processus

**Décidé**

- Source en Markdown, compilée avec Quarto. PowerPoint et LaTeX écartés comme formats maîtres : le premier se propage mal d'un cours à l'autre, le second est pénible pour des supports riches en images.
- Sorties : HTML pour projeter (un seul fichier, hors ligne), PDF par impression du HTML, PowerPoint en secours.
- Charte tirée du gabarit officiel `ModelPPT-GeodataParis_2026.pptx` : bleu `#283B89`, orange `#E38226`, prune `#541C5B`, titres en Raleway, texte en Roboto. Mise en page personnelle : titre en haut à gauche, niveau en haut à droite, logo en pied.
- Trois niveaux de maîtrise : socle, appui, veille.
- Code visuel retenu pour le test : les strates du logo, par quantité (trois pleines, deux, une en contour), toujours accompagnées du mot. Les niveaux sont ordonnés, donc on joue sur la valeur et non sur la teinte ; le code reste lisible en noir et blanc.
- Le test est une tranche de 17 diapos, pas la fusion complète des deux cours. Il vit dans `bac-a-sable/` et ne sert pas de référence de contenu.
- Pas d'agents : une conversation et un dépôt suffisent.

**Testé et fonctionnel**

- Repère de niveau sur chaque diapo, et « carte du cours » générée automatiquement.
- Quatre briques d'exercice : question/réponse, QCM, remise en ordre, zones à cliquer.
- Tri par niveau et masquage des diapos optionnelles, à la compilation ou par l'adresse de la page.
- PDF de 18 pages, une par diapo.

**Constats**

- La sortie PowerPoint est modifiable mais dégradée : deux colonnes au plus, exercices aplatis, charte simplifiée. Le gabarit officiel n'est pas utilisable tel quel par le convertisseur (noms et emplacements des zones incompatibles) ; un gabarit dérivé est fabriqué par `_charte/outils/fabriquer-gabarit-pptx.py`.
- Les images récupérées des anciens PPT sont petites (300 à 800 pixels de large). Lisibles, mais à remplacer par des originaux pour la version définitive.

**À trancher par Marc**

- Le code des niveaux : A (quantité), B (position) ou C (pastille). Les trois sont comparés sur l'avant-dernière diapo du test.
- Les niveaux attribués aux diapos du test sont des suppositions, à corriger.
- Aplatissement de la Terre : l'ancien support dit 22 km ; l'écart entre les deux rayons est d'environ 21 km. Le test écrit « une vingtaine ».
- Lien avec la Canopée : l'attribut `perle="…"` existe, avec un code fictif (`EXEMPLE-01`). Il reste à y mettre les vrais identifiants.
- Dépôt public : il contient des scans de livres et de cartes aux droits incertains. À passer en privé avant d'y verser tous les cours.

**Ensuite**

- Valider la forme, puis déplacer le gabarit de `bac-a-sable/` vers un vrai premier cours dans `cours/`.
- Décider si la sortie PowerPoint vaut d'être maintenue.
- Publication pour les étudiants (GitHub Pages) : non testée.
