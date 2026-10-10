# Journal du projet

Décisions et constats, du plus récent au plus ancien.

## 2026-10-10 — Premier cours complet : « De la Terre à la carte »

**Décidé par Marc, sur le plan annoté**

- Lever les yeux est le rapport centrifuge, regarder d'en haut le rapport centripète. Les parties sont nommées par le regard.
- La descente n'est pas le miroir de la montée : géoïde → ellipsoïde → plan.
- Le cours dure environ 1 h 30, à une minute par diapo ; les SIG sont introduits à part, en un quart d'heure.
- Les exemples purs n'ont ni pictogramme ni mention.
- Une nouvelle notion : « Pour aller plus loin », des bonus pour les curieux.
- Les références seront complétées à la fin.

**Réalisé**

- Le cours : 54 diapos dans `cours/de-la-terre-a-la-carte/`, d'après `plan.md`. Le test du bac à sable est supprimé.
- Sept briques nouvelles : pour aller plus loin, pivoter, comparer, curseur, classer, cap, visées. Plus les schémas dessinés.
- Huit schémas vectoriels aux couleurs de la charte.
- Les images : versions légères renommées dans `images/`, originaux conservés dans `images/originaux/`, table de correspondance.
- Vérifié par des clics réels : chaque expérience, les liens de la carte, l'absence de débordement sur les 54 diapos. PDF de 54 pages.

**Écarts par rapport au plan**

- 4.5 : un QCM remplace les zones à cliquer. Les deux figures d'origine n'emploient pas la lettre *h* dans le même sens ; la diapo évite donc les lettres.
- 4.3 : pas d'image trouvée pour la Laponie et le Pérou ; la diapo tient par son QCM.
- 5.11 : un tableau, sans curseur.
- 2.5 : l'activité s'appuie sur le plan des triangles Greenwich – Paris, comme demandé.

**À vérifier par Marc**

- Les zones cliquables de Bedolina et de la tablette de Babylone : placées à l'œil, et leur lecture est une interprétation.
- Le bonus de la diapo Mercator : le document de l'ONU n'a pas pu être ouvert pour vérification ; le texte est celui du plan.
- La carte de 1595 n'est pas en projection de Mercator : c'est un hémisphère de l'atlas. Un planisphère en Mercator a été ajouté à côté.
- Les trois cartes de Nancy ne sont pas calées sur la même emprise : le fondu est approximatif.
- Les coordonnées de la place Stanislas sont calculées pour un point approché.
- La diapo des sources porte encore « à compléter » sur la plupart des lignes.

**Constats**

- Le fichier HTML pèse 16 Mo, images comprises.
- Les formules d'un curseur doivent être écrites entre accents graves, sinon les astérisques sont pris pour de l'italique.

**En attente, pour le suivi de projet**

- Outil de révision embarqué : l'étudiant coche ce qu'il sait, le support lui propose ce qui reste, en remontant aux prérequis.
- Essai d'un modèle local pour la mise en page et les questionnaires, avec un fichier de consignes et un catalogue de modèles.

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
