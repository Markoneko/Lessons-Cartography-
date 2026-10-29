# Journal du projet

Décisions et constats, du plus récent au plus ancien.

## 2026-10-29 — Arborescence rationalisée

**Demande de Marc**

- Mettre les fichiers produits dans chaque cours, harmoniser les noms des cours, sans casser de liens.
- Les supports d'origine et les sorties dans chaque cours ; PDF automatiques ; pas de numéro d'ordre ; pas encore de fusion dans `main` ; pas de skill.

**Renommé**

| Avant | Après |
|---|---|
| `cours/de-la-terre-a-la-carte/` | `cours/earth-to-map/` |
| `cours/geotraitements/` | `cours/gis-geoprocessing/` |
| `sources/Reference-*.ppt` | `cours/<cours>/source/` (Géodésie et Histoire de la cartographie : `earth-to-map`) |
| `sources/ModelPPT-GeodataParis_2026.pptx` | `_charte/` |
| `outils/schemas-cartography.py`, `outils/territoire-fictif.py` | `cours/cartography-basics/outils/schemas.py`, `…/territoire-fictif.py` |
| `outils/schemas-geotraitements.py` | `cours/gis-geoprocessing/outils/schemas.py` |
| `_sortie/cours/<cours>/index.html` | `cours/<cours>/_sortie/<Titre>.html`, `<Titre>-EN.html`, et leurs PDF |

`gis-basics` et `cartography-basics` gardent leur nom. Les déplacements sont faits avec `git mv` : l'historique de chaque fichier suit (`git log --follow`).

**Ajouté**

- `outils/sorties.py`, lancé par Quarto après chaque rendu : il range le HTML dans le `_sortie/` du cours, sous le nom du titre (« -EN » pour l'anglais), et imprime le PDF corrigé. Le nom vient du titre : les en-têtes des cours, donc les couvertures figées, n'ont pas à changer. Pendant un aperçu, il copie au lieu de déplacer, et n'imprime pas. `SANS_PDF=1` pour un rendu rapide.
- `outils/pdf.py` : l'impression seule, avec `--vierge` pour la version sans réponses.
- `outils/controle.py` : débordements réponses ouvertes, erreurs JavaScript, captures et planches. Ces outils n'existaient jusqu'ici que dans l'espace de travail des sessions.
- Les générateurs de schémas trouvent seuls leur cours : plus d'argument à donner.

**Vérifié**

- Les liens internes des cours sont tous relatifs à leur dossier ; le registre des diapos figées ne contient aucun chemin. Rien n'a cassé.
- `quarto render` produit les huit supports et leurs huit PDF (41, 54, 55, 40 pages par langue) ; aucun débordement, aucune erreur ; les générateurs relancés redonnent des fichiers identiques ; aucune diapo figée modifiée.
- `plan.md` de « GIS : Basics » est régénéré sans les caractères abîmés (« � ») qu'il portait.
- Les noms anciens restent dans les entrées précédentes de ce journal : c'est l'historique.

## 2026-10-15 — « Cartography : Basics », retours de Marc sur la V0

Numéros de diapo de la V0 (39 diapos) ; la V1 en compte 41. Chaque correction est reportée dans la version anglaise.

**Appliqué**

- Fichiers produits nommés d'après le titre : `Cartography-Basics.html` / `-EN.html` et leurs PDF (`output-file:` dans l'en-tête).
- 3 (0.3) : quatre objectifs, avec « structurer l'information… du plus important au moins important » en troisième ; la mise en page « donne aussi les clefs de compréhension du message ».
- 6 (1.1) : cartes du test des cinq secondes agrandies (hauteur 250 → 350 px, surface ×1,96) ; la phrase d'introduction passe dans le bouton et la question.
- Nouvelle 1.2 « Voir, puis comprendre » : compréhension graphique (voir, signifiant) et mentale (regarder, signifié), avec le « WTF » dessiné : un petit lecteur aux yeux en spirale, des paillettes qui scintillent.
- 8 (1.3, « La sémiologie graphique ») : figure recadrée par Marc, en grand ; bonus vers la page de K. Viswanathan (2015). La réponse est corrigée : la figure montre des échanges de marchandises entre une métropole américaine et d'autres régions (Brookings, *Metro Freight*), pas des flux ferroviaires en Floride. L'ordre de la partie 1 devient : cinq secondes, voir puis comprendre, sémiologie, rédiger et mettre en page.
- 10 (2.1) : trois seuils, avec les figurés de l'ancien support : être vu (huit figurés et leur taille minimale), être séparé (0,2 mm), être distingué (surfaces dans un rapport de 2, épaisseurs à 0,1 et 0,3 mm d'écart). Le curseur règle la taille en multiple du seuil. Lien vers la généralisation.
- 20 et 25 (comparer) : décalage corrigé. La marge par défaut des images de reveal.js étirait la couche du dessus ; correction dans `_briques/briques.css`, donc aussi pour les autres cours.
- 21 (3.8) : l'image d'orientation est nettoyée (agrandie ×3, niveaux, netteté) : `orientation.png`.
- Nouvelle 4.1 « La lumière et l'encre » : brique `synthese`, cercles RVB sur du noir et CMJ sur du blanc, un curseur par couleur ; la question sur la carte imprimée plus terne y passe.
- 23 (4.2) : solide TSV en grand, curseurs crantés, solide coupé à la valeur choisie, case soulevée et cernée ; plus de rotation automatique ; plus de bonus, la conclusion est dans la diapo ; nouvelle question (RVB, CMJN ou TSV ?). L'image `s26_9d1ec19a.jpg` ne montre qu'une valeur : on ne peut pas y placer la valeur. Le solide calculé, coupé à la valeur choisie, en reprend l'aspect.
- 24 (4.3) : quatre codes d'autres cultures, révélés avec la réponse : rouge en Chine, Japon, Corée (prospérité, hausse en bourse) ; blanc du deuil en Asie de l'Est ; rouge et bleu aux États-Unis ; vert de l'islam. Source pour les deux premiers usages de la liste : data.europa.eu, « Colour connotations ».
- 25 (4.4) : bonus « Le jeu vidéo a de l'avance », avec la capture de Fortnite.
- 27 (5.1) : chaque donnée porte un exemple ou son unité ; consigne : nature, ordre ou quantité ?
- 33 (6.1) : carte des JO à droite, sur toute la hauteur.
- 34 (6.2) : recommandation « Maximiser la place de la carte… Jouez avec ! » en troisième ; la mise en page A du schéma intègre la légende dans la carte.
- 35 (6.3) : la légende devient un puzzle (brique `puzzle-legende`) : onze pièces justes, six fausses commentées (unité, figuré, taille des cercles, titre « Divers », classes qui se chevauchent).
- Fin (7.2) : « clairement, honnêtement, esthétiquement », à la place du renvoi au TP. Style de la diapo de fin complété pour accepter une liste (`_charte/geodata.css`).
- Sources : graphe circulaire, Fortnite, codes de couleur ; le solide des couleurs est désormais calculé.

**Données de l'atelier**

- Marc n'aura pas le temps de fournir les données des Vosges : le territoire fictif reste.

**Vérifié**

- 41 diapos par langue, aucun débordement réponses ouvertes, aucune erreur JavaScript ; puzzle joué de bout en bout ; PDF de 41 pages, puzzle terminé dans le corrigé.

## 2026-10-15 — « Cartography : Basics », V0 FR et EN

**Demande de Marc**

- Marc a repris le plan dans `index.qmd` et y a placé ses cartes et celles de ses étudiants.
- La carte vivante devra, à terme, être la carte du TP : les coupes rases des Vosges. Marc la prépare ; elle servira aussi de corrigé. En attendant, une carte élaborée par Claude.
- Deux versions, FR et EN.

**Réalisé**

- `index.qmd` et `index-en.qmd` : 39 diapos chacun, fiches `a-revoir`, aucun débordement, aucune erreur JavaScript. PDF de 39 pages par langue.
- Trois briques nouvelles, documentées dans le README : « atelier » (carte vivante avec discrétisation, classes, palette, histogramme), « flash » (image visible quelques secondes), « couleur3d » (solide des couleurs en 3D, à la place des trois curseurs sur un aplat prévus au plan).
- Un territoire fictif de 110 communes (`outils/territoire-fictif.py`, graine 2026), avec un foyer de coupes au nord-est ; annoncé comme fictif sur la diapo.
- `outils/schemas-cartography.py` : 16 schémas FR et EN (cartes en cercles et en aplats, piège du rayon, échelle des cercles, seuils, Ebbinghaus, Adelson avec l'image d'origine, mot rouge, paliers, tableau des variables, mises en page, simulation du daltonisme selon Machado 2009).
- Chiffres calculés : sextiles des taux pour la légende à remettre en ordre ; 96× contre 9,8× pour le piège du rayon ; 72 communes sur 110 en classe claire en amplitudes égales, 44 en classes foncées en effectifs égaux.
- Citation de l'ancien support vérifiée : Éric Blin et Jean-Paul Bord, *Initiation géo-graphique*, 2e éd. 1995.

**À trancher ou fournir par Marc**

- Les données des Vosges pour l'atelier : par commune, surface forestière et surface en coupes rases, avec la source. Le format attendu est décrit dans le README.
- La version « avant » de la carte du Sahel, pour un vrai avant / après sur la diapo 6.4.
- Les crédits « à compléter » : Gaza, Irma, comtés américains, flux circulaire, images de l'ancien support, auteurs des autres cartes d'étudiants.
- « Un homme sur douze, une femme sur deux cents » pour le daltonisme rouge-vert en Europe : ordre de grandeur courant, non vérifié à la source.

## 2026-10-15 — Nouveau cours : « Cartography : Basics », le plan

**Demande de Marc**

- Quatrième refonte, d'après le PPT « DDMEG-03 Sémiologie » (58 diapos, presque toutes du texte). Synthétiser fortement, éviter les diapos de texte.
- Travailler beaucoup plus les interactions : des activités qui font éprouver les conséquences des choix cartographiques.
- Mettre en valeur des cartes de Marc et de ses étudiants ; le choix se fera ensemble.

**Réalisé : le plan seul, en attente de validation**

- `cours/cartography-basics/index.qmd` : 39 fiches, toutes `a-realiser`, six parties : une carte est un message, ce que l'œil peut voir, les variables visuelles, la couleur, les conséquences des choix, la mise en page.
- Les emplacements prévus pour les cartes de Marc portent la mention « [carte de Marc ?] » dans la fiche.
- PPT d'origine dans `sources/Reference-Semiologie.ppt`, 29 images dans `images/originaux/`.

**Ajouts par rapport au support d'origine**

- Une partie « Les conséquences des choix », absente de l'ancien support : variable selon la donnée, stock ou taux, discrétisation, faire mentir une carte.
- Le piège du rayon des symboles proportionnels, le daltonisme, le test des cinq secondes.

**Briques nouvelles nécessaires**

- « atelier » : une carte vivante, recolorée selon la méthode de discrétisation, le nombre de classes et la palette, avec l'histogramme et ses seuils. C'est la brique principale du cours.
- « flash » : une image qui s'efface au bout de quelques secondes.
- « couleur » : trois curseurs teinte, saturation, valeur sur un aplat.
- Le reste se fait avec les briques existantes : curseur qui pilote un schéma, QCM qui modifie le schéma, comparer, classer, ordre, zones.

**À trancher par Marc**

- Les cartes à exploiter, et leur emplacement.
- Les données de l'atelier : réelles (fournies par Marc) ou un territoire fictif annoncé comme tel.
- Deux versions FR et EN, comme pour les deux autres cours : supposées.
- L'ancien support cite « Blind & Bord » : il s'agit sans doute d'Élisabeth Blin et Jean-Paul Bord, *Initiation géo-graphique* ; à confirmer.

## 2026-10-14 — « GIS : Geoprocessing », retours de Marc sur la V0

Numéros de diapo de la V0 française ; chaque correction est reportée dans la version anglaise.

**Appliqué**

- Partie 4 (traitements raster) : toutes les diapos passent en appui, le cours portant d'abord sur le vecteur.
- Couverture datée du 14 octobre ; la mention du support d'origine est retirée, de la couverture comme des sources : Marc refait ces contenus lui-même.
- 2 (0.2) : plus d'allusion au système de révision (`?niveau=socle`), qui n'est pas prêt.
- 14 (2.2) : un seul schéma, `jointure.svg`. La colonne « essence » apparaît à droite de la table au moment de la réponse, avec une flèche venue des peuplements. Le schéma passe en pleine largeur, la question et la réponse côte à côte dessous.
- 16 (3.1) : trois panneaux séparés. Le chemin passe par les points d'origine, et ne se mêle plus à l'enveloppe convexe.
- 24 (4.3) : le curseur du NDVI est retiré. On donne le seuil d'environ 0,3 entre végétation et absence de végétation.
- 27 (4.6) : la maison est posée sur le sol. Le MNS est désormais calculé à partir du MNT : il le rejoint exactement là où il n'y a ni arbre ni bâtiment.

**Ajouté au gabarit**

- Dans un schéma, la classe `s-apparait` cache un élément jusqu'à l'ouverture de la réponse de la diapo. L'élément figure dans le PDF corrigé, pas dans la version vierge. Documenté dans le README.

**Vérifié**

- 40 diapos par langue, aucun débordement ; colonne cachée avant la réponse, visible après, présente dans le PDF.

**Remarque**

- « GIS : Basics » mentionne encore `?niveau=socle` dans sa diapo « Comment lire ce support » : à retirer aussi si le système de révision n'est pas prêt.

## 2026-10-13 (nuit) — « GIS : Geoprocessing », V0 en français et en anglais

**Décidé par Marc**

- Titre : « GIS : Geoprocessing » (« GIS: Geoprocessing » en anglais). Deux versions. Le cours est présenté avant le TP, puis relu seul.

**Réalisé**

- `index.qmd` et `index-en.qmd` : les 40 diapos du plan, mêmes numéros de fiche, toutes « à revoir ».
- 24 schémas dessinés (et doublés en anglais), produits par `outils/schemas-geotraitements.py`. Les réponses des exercices y sont calculées, pas recopiées : jointure (placettes 1 et 3 dans P1), fusion (3 zones), condition (7 pixels à 1), moyenne 3 × 3 (5), zone B (6), placette 3 (412 m). Pour changer un schéma ou une valeur : modifier le script et le relancer.
- 13 images reprises du support d'origine.
- Vérifié : aucun débordement, réponses affichées comprises, dans les deux langues ; PDF de 40 pages.

**Écarts par rapport au plan**

- 1.2 : la requête est écrite en liste, plus lisible qu'un bloc de code.
- 3.2 : la question ne montre que les trois tampons ; le schéma séparés / fusionnés / multiples passe en bonus, sinon il donnait la réponse.
- 4.1 : cinq traitements à classer au lieu de quatre.
- 5.2 : MAUP illustré par les deux cartes européennes du support d'origine.

**À vérifier par Marc**

- MNE (ancien support) devient MNS, le terme de l'IGN.
- Stan Openshaw, 1984, pour le MAUP : de mémoire, non vérifié en ligne.
- Les images reprises sont petites (230 à 680 pixels de large) ; plusieurs crédits restent « à compléter ».
- Les noms d'outils QGIS ne sont cités qu'une fois (Sélectionner par expression) : à compléter si le TP en a besoin.

## 2026-10-13 (soir) — Nouveau cours : « Géotraitements », le plan

**Demande de Marc**

- Troisième cours sur le même principe, assez court, d'après le PPT « DDMEG-04 Géotraitements » (44 diapos, dont 28 masquées sur le raster ; support d'origine de Malika Madelin).
- Les 16 premières diapos, puis un résumé de tous les traitements raster avec de petits schémas, puis les traitements à cheval entre raster et vecteur.

**Réalisé : le plan seul, en attente de validation**

- `cours/geotraitements/index.qmd` : 40 fiches, toutes `a-realiser`, cinq parties : interroger, enrichir les attributs, créer des objets, les traitements raster (résumé en neuf diapos), entre raster et vecteur.
- La diapo 11 d'origine (rasterisation, vectorisation, MAUP) passe dans la dernière partie, avec la diapo 41.
- Exemples forestiers prévus partout : peuplements, placettes d'inventaire, pistes, pentes non mécanisables, hauteur de canopée (MNS − MNT), NDVI.
- PPT d'origine dans `sources/Reference-Geotraitements.ppt`, 58 images extraites dans `images/originaux/`.

**À trancher par Marc**

- Les deux versions FR et EN, et le support consulté seul (comme « GIS : Basics ») : supposés, à confirmer.
- La diapo finale renvoie au TP géotraitements en préparation.

## 2026-10-13 (fin) — « GIS : Basics », retours de Marc sur la V0

Numéros de diapo de la V0 française. Chaque correction est reportée dans la version anglaise.

**Appliqué**

- 7 (1.2) : schéma de la fusion redessiné. La base de données est faite de trois tables reliées par leurs clefs (peuplements, parcelles, propriétaires), à la manière d'un schéma conceptuel. Une couche raster s'ajoute aux couches vecteur, et le repère passe en 3D : X et Y parallèles aux couches, Z vertical.
- 13 (2.3) : schéma du vocabulaire. Repère en 3D. Le lien part de la ligne en surbrillance et arrive sur le polygone. Le MNT est dessiné en TIN, le raster en grille de valeurs différentes.
- 19 (3.5) : TIN agrandi. « Un tronçon » est écrit parallèle à son segment.
- 20 (3.6) : raster et vecteur défilent en grand, l'un après l'autre.
- 26 (3.12) : images 3D agrandies (rééchantillonnées, donc floues : de meilleurs originaux restent à trouver) ; colonne d'images élargie.
- 33 (4.5) : l'orientation n'est plus exigée. On peut l'enlever quand elle est évidente pour tous, comme une carte de France pour des Français.
- 38 (5.1) : flèches et légende fixes, sous le titre. Nouvelle option de la brique : `::: {.defiler commande="haut"}`. Sans l'option, rien ne change : le premier cours n'est pas touché.
- 39 (5.2) : le classement est supprimé. Il est remplacé par ce qui doit ressortir le plus dans chaque usage : la clarté du résultat pour communiquer, la pertinence du processus pour analyser, le lien entre intrants et extrants pour simuler. Une question s'ajoute : une simulation publiée sans ses hypothèses. La conclusion est gardée.
- 40 (5.3) : « etc. » à la fin des deux listes.
- 45 (6.4) : pont recalé sur la route. Le nœud du terrain nominal suit.
- 46 (6.5) : la question devient « Vous réalisez une base routière pour un outil de guidage routier… ».
- 47 (6.6) : les principes et les exemples sont séparés, en deux blocs : nomenclature, règles de sélection.
- 49 (6.8) : bonus supprimé. Une illustration montre un tronçon d'autoroute et onze objets que gère son SIG, chacun avec son thème.
- Nouvelle diapo 6.8b, « Qu'est-ce qu'un modèle de données ? » : les trois niveaux, conceptuel, logique et physique, sans détail ; la modélisation a son propre cours. La diapo 6.9 s'y réfère.

**Vérifié**

- 55 diapos dans chaque langue, aucun débordement, réponses affichées comprises ; les sept liens du schéma ; PDF de 55 pages.
- Le premier cours compile toujours ; aucune diapo figée n'a été modifiée.

## 2026-10-13 (suite) — « GIS : Basics », V0 en français et en anglais

**Décidé par Marc**

- Deux versions, française et anglaise. Les diapos 50-51 (types de SIG), masquées dans le PPT, sont gardées. Des exemples forestiers, pour FIRS. Les cartes d'exemple seront revues à partir de cette V0.

**Réalisé**

- `index.qmd` et `index-en.qmd` (« GIS: Basics ») : les 54 diapos du plan, mêmes numéros de fiche. Toutes les fiches passent de « à réaliser » à « à revoir », avec la ligne Demande vide : c'est Marc qui fige.
- Exemples forestiers : table d'attributs de peuplements (essence, surface, âge), classements (piste forestière, arbre remarquable, parcelle), types de valeurs (tiges par hectare, certification PEFC), requête sur les chênes de plus de 5 ha, croisement peuplements × cours d'eau, lidar sous la canopée, départs de feux dans le Var, BD Forêt à Nancy, situations de gestion (coupes, scolytes, desserte), une forêt dans le terrain nominal.
- 15 schémas dessinés aux couleurs de la charte, doublés en anglais dans `images/schemas/en/`. Le schéma « vocabulaire » est cliquable : sept mots mènent à leur diapo (identifiants explicites sur ces diapos : `#raster`, `#mnt`, `#vecteur`, `#attributs`, `#types-valeurs`, `#couches`, `#ou-et-quoi`).
- 29 images légères dans `images/`, avec `correspondance.csv` ; la BD Forêt de Nancy est reprise du premier cours.
- Vérifié : aucun débordement sur les 54 diapos, réponses affichées comprises, dans les deux langues ; les sept liens du schéma ; les bonus ; le curseur du terrain nominal ; PDF de 54 pages avec corrigés.
- La réponse du croisement (P1, P3, P4, P5) a été calculée, pas estimée : une première estimation à l'œil était fausse.

**Écarts par rapport au plan**

- 2.2 : le schéma des composantes devient un bandeau horizontal, sinon illisible à côté de l'exercice.
- 3.10 : une question remplace le classement, que le schéma donnait déjà.
- 6.9 : un classement (classe, attribut, relation, objet) remplace la remise en ordre, qui ne convient pas à des paires.
- 4.2 « Consulter » et 6.5 « Un rond-point » passent du socle à l'appui : avec 19 diapos, la carte du cours débordait.

**Faits vérifiés pour ce cours**

- CGIS : Roger Tomlinson, années 1960, pour l'inventaire des terres du Canada (agriculture, forêt, faune). QGIS : commencé en 2002 par Gary Sherman.
- BD Forêt V2 : une formation est décrite à partir de 0,5 ha. LiDAR HD : au moins 10 impulsions par m², MNT au pas de 50 cm, licence ouverte.

**À vérifier par Marc**

- Deux liens n'ont pas pu être ouverts : la page BD TOPO de geoservices.ign.fr (6.7) et l'article sur les parasites, dont l'adresse a été transposée de eps.revues.org vers journals.openedition.org (6.9).
- ARC/INFO « au début des années 1980 », Esri fondée par Jack et Laura Dangermond : de mémoire, non vérifié en ligne.
- Les règles de sélection (cimetières de plus de 2 ha, gares) et la modélisation des ronds-points viennent de l'ancien support : à confirmer avec la BD TOPO actuelle.
- Les crédits des images d'exemple : plusieurs « à compléter » ; Articque pour Bourges et Bordeaux est une supposition tirée des logos.
- Les images 3D (extrusion, drapé, relief) font environ 250 pixels de large : floues en grand.
- Le plan du métro (RATP) et plusieurs cartes ont des droits incertains, comme signalé pour le dépôt public.

## 2026-10-13 — Nouveau cours : « GIS : Basics »

**Demande de Marc**

- Reprendre le PPT « DDMEG-01 Initiation aux SIG » (IGN, 2016, 83 diapos) selon le même procédé, en garder la logique et retirer les diapos inutiles.
- Différence avec le premier cours : ce support ne sera pas projeté. C'est une référence que les étudiants consultent seuls.

**Réalisé : le plan seul, comme convenu, pas encore les diapos**

- `cours/gis-basics/index.qmd` : 54 fiches, toutes `a-realiser`. Chaque intention se termine par les numéros des diapos d'origine (numérotation PowerPoint, diapos masquées comprises).
- Le PPT d'origine est rangé dans `sources/Reference-IntroSIG.ppt` ; ses 65 images, extraites telles quelles, dans `cours/gis-basics/images/originaux/`.

**Choix proposés, à valider par Marc**

- Six parties, dans l'ordre de l'ancien support : d'où vient le SIG, qu'est-ce qu'un SIG, les données, les fonctions, les usages, la conception.
- Pour un usage autonome : une diapo « Comment lire ce support », les notes orales passées sur les diapos, chaque brainstorm devenu un exercice avec sa réponse, un glossaire à la place de « Présenter le glossaire ».
- Les quatre diapos de l'exemple autoroutier tiennent en une ; les neuf diapos d'exemples (enjeux) deviennent une galerie et un exercice de classement.
- Coordonnées et projections : renvoi au cours « De la Terre à la carte », sans les répéter.
- Mise à jour : QGIS et ArcGIS Pro à la place de Géoconcept et MapInfo, Géoplateforme et flux WMS / WMTS / WFS, LiDAR HD ; la table à digitaliser disparaît.
- Historique : l'ancien support (diapo 9, masquée) fait d'Esri l'inventeur du SIG. Le premier SIG est généralement attribué à Roger Tomlinson (CGIS, Canada, années 1960). À vérifier au moment de la réalisation.
- Les diapos 50 et 51 (types de SIG) étaient masquées : gardées en 4.8, niveau veille, à confirmer.

**Constats**

- Les images d'origine sont petites (souvent moins de 700 pixels) et beaucoup datent de 2009 à 2014 (captures de logiciels, cartes INSEE). Sept schémas sont à redessiner aux couleurs de la charte.
- Le titre est en anglais, le contenu prévu en français : langue du cours à confirmer.

## 2026-10-11 (fin) — Deux retouches et version anglaise

**Retouches demandées par Marc**

- 2.1 : nouvelle brique `loupe`. Un clic sur la table de Peutinger l'agrandit trois fois dans son cadre, la souris déplace la zone vue, un second clic revient à l'ensemble. La diapo était à revoir, son état n'a pas été changé.
- 1.4 : l'éclipse de Lune est redessinée, Lune claire et ombre ronde sombre. La diapo est figée ; seul le fichier `images/schemas/rotondite.svg` a changé, à la demande explicite de Marc, et le texte de la diapo n'a pas bougé (le script le confirme).

**Version anglaise**

- `index-en.qmd`, « From the Earth to the Map » : les 54 diapos, mêmes numéros de fiche, toutes à l'état « à revoir » puisque Marc ne l'a pas encore relue.
- Le gabarit lit `lang` dans l'en-tête du cours : libellés, messages des exercices, format des nombres et rose des vents existent en français et en anglais. La typographie française n'est plus appliquée hors du français.
- Neuf schémas doublés dans `images/schemas/en/`.
- `plan-en.md` et `figes-en.json` sont tenus à part des fichiers français.

**Choix faits, confirmés par Marc le 11 octobre**

- Niveaux : Core, Support, Further. Les initiales S, A, V sont perdues ; les pictogrammes ne changent pas.
- « Les trois regards » : Looking up, Looking at the horizon, Looking from above.
- Altitude et hauteur : *elevation* (au-dessus du géoïde) et *height* (au-dessus de l'ellipsoïde).
- Intercalaire 4 : « Which shape do we mean? », plus court que la traduction littérale, qui passait sur deux lignes.

**Limites**

- L'image de la table de Peutinger ne faisait que 720 pixels de large. Réglé le jour même : Marc a déposé un scan de 4 218 pixels sous le même nom, les noms d'étapes se lisent à la loupe. Le fichier HTML passe de 18 à 21 Mo.
- Les images qui contiennent du texte français ne sont pas traduites.
- Les deux versions sont deux fichiers indépendants : toute correction est à faire deux fois.

## 2026-10-11 (suite) — Premier passage de corrections par les fiches

Marc a dégelé 27 diapos, écrit ses demandes dans les fiches et retouché des textes directement. Le script a confirmé qu'aucune des 27 diapos restées figées n'a été modifiée, ni par lui ni par ce passage.

**Appliqué**

- 0.1 : plus d'illustration en couverture.
- 0.5 : QCM resserré ; il ne déborde plus, toutes réponses ouvertes.
- 0.6 : douze champs cliquables au lieu d'un ; zone des maisons élargie ; chemin inchangé.
- 1.1 : plus de zones à cliquer (fiche : « Expérience : aucune ») ; bonus sur Edith Horsley et la vidéo d'Irving Finkel.
- 1.5 : la distance Syène – Alexandrie reste fixe, c'est la Terre qui change de taille.
- 1.8 : la réponse s'obtient en cliquant le mot « Oriens » sur la carte, agrandie de 15 %.
- 2.1 : table de Peutinger agrandie de moitié, centrée.
- 2.2 : la flèche du cap part du nœud de rhumbs à l'ouest du Portugal.
- 2.5 : le principe du triangle (trois mesures connues, dont un côté, donnent les trois autres).
- 2.7 : les trois cartes défilent en grand ; mention du musée de l'Armée.
- 2.9 et 3.4 : nouvelles images de Nancy, ramenées à la même taille.
- 3.1 : photo aérienne agrandie ; bonus photogrammétrie et CO3D.
- 3.5 : neuf étiquettes à classer.
- 4.1 : schéma en largeur, question et réponse dessous, formule signalée comme approchée.
- 4.3 : le globe se déforme selon la réponse choisie.
- 4.4 : coupe du champ de pesanteur ajoutée.
- 4.6 : le curseur est remplacé par un schéma des trois ordres de grandeur.
- 5.1 : nouvelle diapo sur les coordonnées cartésiennes géocentriques ; « Dans quel ordre ? » passe après « Projeter, c'est choisir » et porte le numéro 5.5b.
- 5.6 : Mercator et Peters à la même largeur.
- 5.8 : image corrigée (le fond transparent était devenu noir) ; 5.9 supprimée et devenue son bonus.

**Ajouté au gabarit**

- Brique « défiler », hauteur réglable des images cliquables, commentaire de zones déplaçable, QCM resserré, contenu révélé après un choix.

**Corrigé au passage, à valider par Marc**

- Trois fiches abîmées à la saisie (guillemet manquant en 2.7, fermeture manquante en 3.1, « a revoir » en 5.1).
- 2.3 : « fin du 21eme siècle » écrit « fin du XX^e^ siècle » ; « un sixième d'arc » écrit « un sixième de cercle ».
- 0.2 : « MAry Cassat » écrit « Mary Cassatt ».

**Non fait, ou à vérifier**

- 2.1 : la table n'occupe pas toute la largeur ; il faudrait la rogner ou supprimer du texte.
- 2.2 : la demande annonçait deux ajustements, un seul était écrit.
- 1.1 : la vidéo n'a pas pu être ouverte ; son éditeur (BBC ou British Museum) n'est pas cité sur la diapo.
- 6.3 : la diapo des sources est figée ; le musée de l'Armée n'y est pas reporté.
- Les commentaires des QCM sont un peu plus petits partout, y compris sur les diapos figées : « Quel système en France ? » débordait une fois toutes les réponses ouvertes.

## 2026-10-11 — Le plan fusionne avec le cours

**Le problème**

Deux fichiers de référence, `plan.md` et `index.qmd`, et un écart entre les deux : la réalisation avait réinterprété le plan. Marc veut pouvoir changer des diapos entières, sans que tout soit réinventé à chaque passage, et que ce qui est bon reste figé.

**Décidé**

- Une seule source par cours : `index.qmd`. Chaque diapo porte une fiche (intention, expérience, demande) et un état : `fige`, `a-revoir`, `a-realiser`.
- `plan.md` devient une vue, régénérée à chaque compilation. Le plan annoté d'origine est archivé dans `plan-initial.md`.
- Un assistant ne travaille que sur les diapos `a-revoir` et `a-realiser`, jamais sur le fichier entier.
- Les 54 diapos partent figées : Marc dégèle ce qu'il veut changer.

**Réalisé**

- 54 fiches posées, à partir du plan annoté. Le contenu des diapos n'a pas changé.
- `outils/figer.py` : une empreinte par diapo figée ; testé sur une virgule changée, détectée.
- `CONSIGNES-IA.md` : les règles et le déroulé d'un passage, pour tout assistant, en ligne ou local.
- Les fichiers HTML et PDF déposés dans le dossier d'un cours ne sont plus envoyés sur GitHub.

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
