# Supports de cours — Géodata Paris / FIRS

Un cours = un fichier texte, qui porte le nom du cours (`GIS-Basics.qmd`), et un dossier d'images.
La mise en page, la charte et les exercices sont fournis par le gabarit : on ne s'occupe que du contenu.

Aucune IA n'est nécessaire pour écrire, modifier ou produire un support.

## Ce qu'il faut installer (une fois)

> **Nota bene — reproduire la chaîne sur un autre ordinateur.** Quatre installations, puis une vérification. Les commandes sont données pour Windows (PowerShell) ; sous macOS ou Linux, remplacer `py` par `python3`. Sur un poste sans droits d'administrateur, chaque logiciel existe en version « utilisateur » ou portable, et `--user` suffit pour Python.

1. **Git et le dépôt.** [GitHub Desktop](https://desktop.github.com/) (le plus simple) ou [Git](https://git-scm.com/). Cloner `Markoneko/Lessons-Cartography-`, puis se placer sur la branche de travail, `test-gabarit`.
2. **Quarto**, version 1.8 ou plus récente : [quarto.org](https://quarto.org/docs/get-started/). Vérifier : `quarto --version`.
3. **Un éditeur.** [VS Code](https://code.visualstudio.com/) avec l'extension Quarto ; le Bloc-notes suffit à la rigueur.
4. **Python 3 et ses modules** — pour les PDF, le contrôle des supports et les outils des cours (images, schémas). Sans eux, le HTML se produit quand même.
   - Python : [python.org](https://www.python.org/downloads/) ; sous Windows, cocher « Add python.exe to PATH ». Vérifier : `py --version`.
   - Les modules, depuis la racine du dépôt : `py -m pip install --user -r requirements.txt`
   - Le navigateur qui imprime les PDF, une fois : `py -m playwright install chromium`

**Vérifier.** Depuis la racine du dépôt, dans un terminal (pas avec le bouton de VS Code, qui lance un aperçu, sans PDF) :

```
quarto render cours/gis-basics/GIS-Basics.qmd
```

Les dernières lignes doivent dire « Sortie : … » puis « PDF : … », et les deux fichiers apparaître à côté du `.qmd`. Sinon, le terminal dit pourquoi (Playwright absent, avec la commande à taper ; aperçu en cours ; `SANS_PDF`).

Ce qui a coincé sous Windows, et qui est réglé dans le dépôt : `python3` n'y existe pas (Quarto lance donc `outils/sorties.py` avec le Python qu'il trouve, `py`) ; les messages accentués faisaient échouer Quarto (le script écrit en UTF-8). Si un problème de ce genre revient, voir `JOURNAL.md` (20 novembre 2026).

## Produire un support

Dans un terminal, depuis ce dossier :

```
quarto render cours/mon-cours/Mon-Cours.qmd
```

Le résultat arrive à côté du cours, sous le nom du fichier du cours (`outils/sorties.py` imprime le PDF après chaque rendu) :

- `cours/gis-basics/GIS-Basics.html` et `GIS-Basics-EN.html` : un seul fichier par langue, qui fonctionne sans réseau. Il sert à projeter et à faire manipuler les étudiants. Touche `F` : plein écran. Touche `S` : vue orateur avec les notes.
- `GIS-Basics.pdf` et `GIS-Basics-EN.pdf` : le support de cours, avec le corrigé des exercices, imprimé tout seul si Playwright est installé.

Après le rendu, le terminal dit toujours ce qu'il advient du PDF : « PDF : … » quand il est imprimé, sinon la raison (Playwright absent, `SANS_PDF`, aperçu en cours).

`quarto render`, sans nom de fichier, produit tous les cours. Pour un rendu rapide sans PDF : `SANS_PDF=1 quarto render cours/mon-cours/Mon-Cours.qmd`.

Le PDF sans les réponses : `python3 outils/pdf.py cours/gis-basics/GIS-Basics.html --vierge`. À la main, on obtient les mêmes en ouvrant le HTML dans Chrome, avec `?print-pdf` (ou `?print-pdf&reponses=non`) au bout de l'adresse, puis Imprimer → Enregistrer au format PDF (marges : aucune, graphiques d'arrière-plan : cochés).

Pour contrôler un support (débordements, réponses ouvertes, erreurs JavaScript), et en tirer des planches de captures :

```
python3 outils/controle.py cours/gis-basics/GIS-Basics.html --images /tmp/captures
```

Pour travailler avec un aperçu qui se met à jour à chaque enregistrement :

```
quarto preview cours/mon-cours/Mon-Cours.qmd
```

Pendant l'aperçu, pas de PDF.

## Les supports imprimés (cours « metacognition »)

Ce cours ne se projette pas, il se manipule : un jeu de 23 cartes A6 et une
feuille A4 recto-verso. Les deux se fabriquent depuis la racine du dépôt.

**Changer le contenu des cartes.** Tout est dans un seul fichier de données,
`cours/metacognition/donnees/fichesV7.json` : une fiche par carte, avec son nom,
son texte de recto, ses émotions, son chiffre d'ampleur d'effet, ses deux blocs
« IA » et sa zone d'activité. Le générateur prend **toujours la version numérotée
la plus haute** : pour garder une version de côté, enregistrer sous `fichesV8.json`
et c'est elle qui sera lue, sans rien changer d'autre.

**Voir le résultat tout de suite**, sans PDF ni Playwright — c'est la boucle de
travail, elle prend une seconde :

```
py cours\metacognition\outils\cartes.py                     (Windows)
python3 cours/metacognition/outils/cartes.py                 (macOS, Linux)
```

Sans autre argument, il écrit `cours/metacognition/Cartes-Jeu-complet.html` et
affiche le chemin en clair ; il suffit d'ouvrir ce fichier dans Chrome. Les
options : `--groupe contexte|cap|outil` pour n'en voir qu'un, `--sortie <chemin>`
pour choisir où écrire, `--fiches <chemin>` pour forcer une version précise.

Sous Windows, la commande est **`py`**, jamais `python3` : ce nom n'existe pas,
et `python` ouvre parfois le Store au lieu de lancer quoi que ce soit.

**Produire le PDF d'impression** — 46 pages A6, une face par page, à tirer en
recto-verso :

```
py cours\metacognition\outils\impression.py                  (Windows)
python3 cours/metacognition/outils/impression.py             (macOS, Linux)
```

Il écrit `cours/metacognition/impression/Cartes-jeu-complet.pdf`. Avec
`--groupe cap`, il n'en sort qu'un groupe. Le tirage est prévu **en couleurs sur
papier blanc** : chaque groupe porte sa couleur (contexte violet, cap orange,
outil bleu) sur le bandeau de tête, les filets, le picto de famille et les étoiles.

**La feuille A4** se fabrique de la même façon :

```
py cours\metacognition\outils\feuille.py                    (Windows)
python3 cours/metacognition/outils/feuille.py                (macOS, Linux)
```

Elle écrit `impression/Feuille-plan-action.pdf`, et `impression/Feuille.html`
à côté pour vérifier d'un coup d'œil. `--sans-pdf` s'arrête à l'aperçu.

Son contenu n'est pas dans un JSON mais directement dans `outils/feuille.py` :
les consignes en haut du fichier, le dessin de la carte marine dans
`carte_marine()`. Les deux schémas de l'ampleur d'effet du support projeté
viennent de `outils/schemas-ampleur.py`.

Ces trois outils n'ont besoin que de Python, sauf la sortie PDF qui passe par
Playwright — déjà installé si les PDF de cours fonctionnent.

## Le plan et le cours : un seul fichier

Le plan n'est pas un document à part. Sous chaque titre de diapo, une **fiche** dit ce que la diapo doit faire et où elle en est. Elle n'apparaît ni dans le HTML ni dans le PDF.

```markdown
## Tournez la carte {.socle}

::: {.fiche n="1.9" etat="fige"}
Intention : Al-Idrisi place le sud en haut ; le nord en haut n'est qu'une convention.
Expérience : pivoter la carte jusqu'à reconnaître la Méditerranée.
Demande :
:::
```

| État | Sens | Ce que fait un assistant |
|---|---|---|
| `fige` | la diapo convient | il n'y touche pas |
| `a-revoir` | une demande est écrite | il modifie cette diapo, et elle seule |
| `a-realiser` | la fiche existe, pas le contenu | il construit la diapo |

- **Demander un changement** : passer l'état à `a-revoir` et écrire la ligne « Demande ». Ce qui est entre guillemets « » sera recopié mot pour mot.
- **Ajouter une diapo** : écrire son titre et sa fiche, avec `etat="a-realiser"`.
- **Déplacer ou supprimer une diapo** : couper-coller ou effacer le bloc, du `##` jusqu'au `##` suivant.
- **Figer** : remettre `etat="fige"` quand la diapo convient.

À chaque compilation, `plan.md` est régénéré à côté du cours : le tableau de toutes les diapos, leur état, et la liste des demandes en attente. On le lit, on ne le modifie pas.

Un script garantit que les diapos figées ne bougent pas :

```
python3 outils/figer.py verifier cours/earth-to-map/De-la-Terre-a-la-carte.qmd
```

Les règles que doit suivre un assistant sont dans `CONSIGNES-IA.md`.

## Créer un nouveau cours

1. Copier le dossier `cours/earth-to-map` et le renommer d'après le titre du cours, en anglais, en minuscules et avec des tirets (`gis-basics`, `cartography-basics`…).
2. Renommer le fichier du nom du nouveau cours (`Mon-Cours.qmd`, et `Mon-Cours-EN.qmd` pour l'anglais), remplacer son contenu et les images ; ranger le support d'origine dans `source/`, et supprimer les HTML et PDF copiés avec le dossier.

Un cours contient tout ce qui le concerne :

| Dans le dossier du cours | Contenu |
|---|---|
| `Nom-du-cours.qmd`, `Nom-du-cours-EN.qmd` | le cours, en français et en anglais ; le fichier porte le nom du cours |
| `plan.md`, `plan-en.md`, `figes.json`, `figes-en.json` | produits par la compilation et par `figer.py` |
| `images/` | les images légères, `originaux/` et `schemas/` |
| `donnees/` | les données des exercices, s'il y en a |
| `source/` | le support d'origine (PPT), jamais modifié |
| `outils/` | les générateurs propres au cours (schémas, données) |
| `Nom-du-cours.html`, `Nom-du-cours.pdf` | les fichiers produits, à côté du cours, non versionnés |

## Écrire une diapo

```markdown
## Titre de la diapo {.socle}

Du texte, avec du **gras**.

- une puce
- une autre

![](images/ma-carte.jpg)

::: {.notes}
Ce que je dis à l'oral. Visible seulement dans la vue orateur.
:::
```

Chaque `##` commence une nouvelle diapo.

### Les trois niveaux

On pose une étiquette à côté du titre : `{.socle}`, `{.appui}` ou `{.veille}`.
Le pictogramme s'affiche devant le titre, et la diapo « carte du cours » se met à jour toute seule.

| Étiquette | Pictogramme | Sens |
|-----------|-------------|------|
| `.socle`  | trois strates à décrochement, trait gras, bleu — évoque un S | à maîtriser |
| `.appui`  | deux strates en crête, trait moyen, orange — évoque un A | pour consolider |
| `.veille` | une strate en creux, trait fin, violet — évoque un V | pour aller plus loin |

Forme, nombre de traits, épaisseur et couleur disent la même chose : le code reste lisible en noir et blanc.

Une diapo sans étiquette est un **exemple** : elle n'a pas de pictogramme et n'apparaît pas dans la carte du cours.

Pour relier une diapo à une perle de la Canopée : `{.socle perle="CODE-01"}`.

### La carte du cours

```markdown
## Carte du cours

::: {.carte-du-cours}
:::
```

Elle liste les diapos par niveau. Chaque ligne est un lien vers sa diapo, et le pictogramme de chaque diapo ramène à la carte.

Avec `{.carte-du-cours niveaux="socle"}`, elle ne garde qu'un niveau : c'est la diapo « À retenir ».

### Types de diapo

| Écriture | Résultat |
|----------|----------|
| `## Titre {.intercalaire}` | titre de partie, numéroté et coloré automatiquement |
| `## Titre {.image-pleine}` | une image sur toute la diapo |
| `## Titre {.fin}` | diapo de clôture |
| `## Titre {.optionnel}` | diapo que l'on peut retirer d'un coup |
| `## Titre {visibility="hidden"}` | diapo cachée, mais conservée dans le fichier |

Deux colonnes :

```markdown
:::: {.columns}
::: {.column width="60%"}
À gauche.
:::
::: {.column width="40%"}
À droite.
:::
::::
```

Mises en valeur : `[phrase clef]{.a-retenir}`, `[40 000 km]{.chiffre}`, `[source de l'image]{.legende}`.

## Les exercices

**Question, puis réponse au clic suivant**

```markdown
::: {.question etiquette="Prédiction"}
Que va-t-il se passer si… ?
:::

::: {.reponse}
Voici pourquoi.
:::
```

**QCM** — `[x]` marque la bonne réponse, le sous-point est le commentaire affiché après le clic.

```markdown
::: {.qcm}
Quel est le système légal ?

- [ ] NTF
    - Jusqu'en 2000 seulement.
- [x] RGF93
    - Oui.
:::
```

**Remise en ordre** — on écrit la liste dans le bon ordre, elle est mélangée à l'écran.

```markdown
::: {.ordre}
1. La Terre réelle
2. Le géoïde
3. L'ellipsoïde
:::
```

Une étape qui commence par `= ` prend le même rang que la précédente : l'étudiant peut les placer dans un ordre ou dans l'autre (`2. = Source : …` après `1. Nature : …`).

**Zones à cliquer sur une image** — chaque zone est donnée en pourcentage de l'image : gauche, haut, largeur, hauteur.

```markdown
::: {.zones image="images/carte.jpg" alt="Description de l'image"}
- [x] 30,0,16,22 : Bien vu, parce que…
- [ ] 45,33,17,30 : Non, ici…
:::
```

## Les expériences

Chaque brique s'écrit en quelques lignes. Le cours `cours/earth-to-map/De-la-Terre-a-la-carte.qmd` en contient un exemple de chacune, à copier.

**Pour aller plus loin** — un bouton en haut à droite ouvre un panneau de bonus : texte, image, lien.

```markdown
::: {.plus titre="La carte en T dans l'O"}
Le texte du bonus, avec un [lien](https://exemple.org) si besoin.
:::
```

**Pivoter une image** — l'étudiant la fait tourner ; le texte s'affiche quand il atteint l'angle `cible`.

```markdown
::: {.pivoter image="images/al-idrisi.jpg" alt="Description" cible="180" tolerance="20"}
Le sud était en haut.
:::
```

**Comparer des images** — un curseur fond les images l'une dans l'autre. Le texte entre crochets sert d'étiquette. Les images doivent couvrir la même emprise. Le curseur prend la largeur de l'image ; `style="--hauteur-comparer: 370px"` règle la hauteur maximale (390 px par défaut).

```markdown
::: {.comparer}
- ![Cassini](images/nancy-cassini.jpg)
- ![Aujourd'hui](images/nancy-top25.jpg)
:::
```

**Défiler des images** — une seule à la fois, en grand, avec deux flèches. Le texte entre crochets sert de légende. `auto="5"` fait tourner les images toutes les 5 secondes quand la diapo s'affiche ; un clic sur une flèche arrête la rotation.

```markdown
::: {.defiler}
- ![Bataille d'Austerlitz, 1805](images/austerlitz-1805.jpg)
- ![Frontière de l'Indochine](images/indochine.jpg)
:::
```

**Loupe** — un clic agrandit l'image dans son cadre, la souris (ou le doigt) déplace la zone agrandie, un second clic revient à la vue d'ensemble. `zoom` règle l'agrandissement, 3 par défaut. La loupe ne montre que ce que l'image contient : prévoir une image d'au moins 2 000 pixels de large.

```markdown
::: {.loupe zoom="3"}
![](images/peutinger.jpg){fig-alt="Description" height="310"}
:::
```

**Curseur** — une valeur `x` pilote des résultats calculés, écrits entre accents graves et accolades. Après la barre, le nombre de décimales.

```markdown
::: {.curseur min="2" max="30" pas="0.1" valeur="7.2" unite="°" etiquette="Angle"}
- Tour de la Terre : `{5000*360/x|0}` stades
:::
```

Avec `schema="images/schemas/mon-dessin.svg"`, le dessin suit le curseur s'il a été prévu pour.

**Classer** — un titre `###` par case, puis ce qui doit y aller. Laisser une ligne vide avant chaque titre. L'étudiant glisse une étiquette dans sa case (souris ou doigt), ou la clique puis clique la case. Quand tout est rangé, la réserve s'efface et les cases remontent.

```markdown
::: {.classer}
### Lever les yeux

- Tablette de Babylone

### Regarder l'horizon

- Portulan
:::
```

**Tenir un cap** — une flèche tourne sur la carte, par crans de 11,25°. `x` et `y` placent son origine, en pourcentage de l'image.

```markdown
::: {.cap image="images/portulan-1540.jpg" alt="Description" x="44" y="57" depart="90"}
Le texte d'accompagnement.
:::
```

**Tracer des visées** — l'étudiant relie des stations ; les triangles fermés se remplissent. Le texte placé après la liste s'affiche quand `objectif` triangles sont fermés.

```markdown
::: {.visees image="images/triangulation.jpg" alt="Description" objectif="2" solution="1-2 1-3 2-3"}
La consigne.

- Douvres : 59.5,52.1
- Cap Blanc-Nez : 70.7,70.3
- Montlambert : 69.4,90.0

Le commentaire de réussite.
:::
```

**Un schéma dessiné** — un fichier SVG aux couleurs de la charte. `hauteur` le limite, en pixels.

```markdown
::: {.schema fichier="images/schemas/trois-regards.svg" hauteur="170"}
:::
```

### Les briques de cartographie

Elles vivent dans `_briques/briques-carto.html` et `_briques/briques-carto.css`. Le cours `cours/cartography-basics` en contient un exemple de chacune.

**Carte vivante (atelier)** — une carte choroplèthe que l'étudiant reclasse lui-même : méthode de discrétisation (amplitudes égales, effectifs égaux, seuils naturels de Jenks), nombre de classes (3 à 7), palette. La légende donne l'effectif de chaque classe ; l'histogramme montre où tombent les seuils. Un texte écrit dans la brique se place sous la carte.

```markdown
::: {.atelier donnees="donnees/territoire.json" variable="taux" unite="%" methode="egales" classes="5" palette="sequentielle" style="--hauteur-atelier: 370px"}
[Source des données.]{.legende}
:::
```

| Réglage | Effet |
|---|---|
| `reglages="methode"` | ne montre que les boutons de méthode (par défaut `methode,classes,palette`) |
| `palettes="sequentielle,rouge-vert"` | les palettes proposées, parmi `sequentielle`, `arc-en-ciel`, `divergente`, `rouge-vert` |
| `histogramme="non"` | sans histogramme |
| `style="--hauteur-atelier: 290px"` | hauteur maximale de la carte |

Le fichier de données est un JSON : `largeur`, `hauteur`, un `contour` (chemin SVG) et une liste `communes`, chacune avec son `chemin` SVG et ses valeurs (`taux`, etc.). `outils/territoire-fictif.py` fabrique le territoire fictif du cours ; des données réelles exportées de QGIS (en coordonnées de page) prennent la même forme.

**Flash** — l'image n'apparaît que `duree` secondes, au clic sur un bouton ; on la revoit d'un second clic. Elle est toujours visible dans le PDF.

```markdown
::: {.flash duree="5"}
![](images/noel.png){height="250" fig-alt="Description"}
:::
```

**Solide des couleurs** — un solide teinte-saturation-valeur en 3D, coupé à la valeur choisie, avec trois curseurs crantés (24 teintes, 6 saturations, 8 valeurs). La case choisie se soulève et se cerne ; à côté, l'aplat et ses valeurs RVB, hexadécimale et CMJN. On le fait pivoter à la souris. Le texte écrit dans la brique (question, réponse) passe dans le panneau, sous les curseurs.

```markdown
::: {.couleur3d style="--hauteur-couleur: 370px"}
La teinte tourne autour de l'axe…

::: {.question}
…
:::
:::
```

**Synthèse des couleurs** — deux jeux de trois cercles : la synthèse additive (rouge, vert, bleu, sur du noir) et la soustractive (cyan, magenta, jaune, sur du blanc). Un curseur par couleur ; la couleur du centre est donnée.

```markdown
::: {.synthese}
:::
```

**Puzzle de légende** — l'étudiant construit, pièce à pièce et dans l'ordre de lecture, la légende d'une carte qui n'en a pas. La liste numérotée donne les pièces justes dans l'ordre ; « = » en tête d'une pièce lui donne le même rang que la précédente (ordre libre entre elles). La liste à puces donne les pièces fausses, chacune avec son commentaire après « : ». Le texte placé après les listes s'affiche quand la légende est complète. Le PDF corrigé porte la légende terminée.

```markdown
::: {.puzzle-legende carte="images/schemas/legende-carte.svg" alt="Description" style="--hauteur-puzzle: 330px"}
La consigne.

1. titre | Coupes rases
2. sous-titre | Part de la forêt coupée (%)
3. aplat #5c2c06 | 6,3 – 18,2
4. cercles #3E8FD0 16 10.2 5.1 | 245, 100, 25
5. titre | Filière bois
6. ligne #FFFFFF 2.5 #1B1B22 5.5 | Route forestière
7. = point #FFFFFF #1B1B22 9 | Scierie

- sous-titre | Part de la forêt coupée (ha) : Une part se dit en %, pas en hectares.

Légende complète : …
:::
```

Figurés : `titre`, `sous-titre`, `aplat COULEUR`, `ligne COULEUR ÉPAISSEUR [ENCADREMENT ÉPAISSEUR]`, `point COULEUR [CONTOUR] [TAILLE]`, `cercles [COULEUR] R1 R2 R3` (rayons dans les unités de la carte, ramenés à sa taille d'affichage).

Les schémas du cours (cartes en symboles, palettes, illusions) sont produits par `python3 cours/cartography-basics/outils/schemas.py`, en français et en anglais. Les valeurs données dans les réponses sont calculées par ce script, pas recopiées à la main.

**Déclaration de transparence IA** — le bloc de la Boussole IA de Géodata Paris, dans la langue du cours. Il se place sur la diapo « Comment lire ce support » de chaque cours. Un texte écrit dans la brique remplace la phrase type.

```markdown
::: {.transparence-ia profil="✒️ L'Auteur outillé" coordonnees="F2 · R0 · S0" outil="Claude 5"}
:::
```

En anglais : `profil="✒️ The equipped Author"`.

### Les briques d'enquête

Elles vivent dans `_briques/briques-enquete.html` et `_briques/briques-enquete.css`. Le cours `cours/image-intelligence` en contient un exemple de chacune. Ce que l'étudiant écrit ou choisit est gardé dans son navigateur seulement ; le PDF corrigé montre la réponse attendue.

**Coupe topographique** — un marcheur va de A à B sur une image, en partant du milieu des ordonnées ; à chaque pas, l'étudiant le fait monter ou descendre avec les flèches ↑ ↓ (→ ou espace pour avancer) et marque une **crête vive** avec la touche C. La courbe se dessine lissée, sauf aux crêtes vives, qui gardent leur angle : on distingue les crêtes qui cassent des fonds arrondis. À l'arrivée, son profil est comparé au profil de référence (écart moyen, et nombre de crêtes vives), et le bloc `.apres-jeu` s'affiche. `depart` et `arrivee` sont en % de l'image ; le profil est un JSON `{"points": [[t, z], …]}`, t et z entre 0 et 1 ; un troisième terme `"v"` marque une crête vive : `[0.17, 0.88, "v"]`. Avec `"alt": [800, 1150]` (le bas et le haut de l'échelle, en mètres), le graphique affiche les vraies altitudes sur ses lignes fortes.

```markdown
::: {.coupe image="images/fast-2016.jpg" alt="Description" depart="2,49" arrivee="98,49" pas="24" profil="donnees/fast-profil.json" style="--hauteur-coupe: 320px"}
::: {.apres-jeu}
Le commentaire, après le jeu.
:::
:::
```

**Arbre de déduction** — une question par étape ; chaque réponse mène à une autre étape ou à une conclusion. Le chemin suivi reste affiché, comme un faisceau d'indices. `### id | question` ouvre une étape, `### id ! titre` une conclusion ; chaque choix s'écrit `- texte → id`. La première étape est la première écrite.

```markdown
::: {.arbre image="images/rade-de-brest.jpg" alt="Description" style="--hauteur-arbre: 390px"}
### depart | Quelle taille ont les points blancs ?
- Quelques mètres → petits
- Plusieurs dizaines de mètres → grands

### petits ! Hypothèse : un mouillage
Le commentaire de la conclusion.
:::
```

**Observer** — une zone d'écriture, puis un bouton qui montre la lecture de l'expert (le texte écrit dans la brique). `cle` nomme ce qui est écrit ; `rappel="une-autre-cle"` réaffiche au-dessus ce que l'étudiant a écrit ailleurs dans le cours.

```markdown
::: {.observer cle="note-image" rappel="description-image" invite="J'observe…"}
La lecture de l'expert.
:::
```

**Indices** — une énigme : les indices viennent un à un, chacun peut encadrer une partie de l'image (`x,y,largeur,hauteur :` en %, devant l'indice). Avec `confiance="oui"`, l'étudiant dit sa certitude à chaque indice. Le texte placé après la liste est la solution : elle n'apparaît qu'au clic qui suit le dernier indice (et, avec `confiance="oui"`, une fois la certitude de ce dernier indice donnée).

```markdown
::: {.indices image="images/fast-2016.jpg" alt="Description" confiance="oui"}
- 30,28,29,42 : Le premier indice, encadré sur l'image.
- Un indice sans cadre.

La solution.
:::
```

**Barre de certitude** — autour d'un QCM : l'étudiant doit dire s'il est sûr avant de répondre. Ses réponses nourrissent la brique `calibration`.

```markdown
::: {.confiance}
::: {.qcm .serre}
…
:::
:::
```

**Vrai ou généré** — des images une à une ; l'étudiant dit sa certitude, puis « vraie » ou « générée par IA ». Chaque image porte `[vrai]` ou `[ia]` (en anglais, `[real]` ou `[ai]`), puis l'explication. Le score s'affiche à la fin.

```markdown
::: {.vrai-ia style="--hauteur-vraiia: 420px"}
- ![Une île, janvier 2022](images/ia-2022-ile.jpg) [ia] : Ce qui la trahit.
- ![Rade de Brest, orthophotographie](images/rade-de-brest.jpg) [vrai] : Ce qui la rend crédible.
:::
```

**Bilan** — les compétences du cours, à placer sur trois niveaux. `moment="debut"` au début, `moment="fin"` à la fin : la version de fin montre l'écart, et renvoie vers les diapos socle qui portent la compétence (`competences="C1 C3"` dans l'en-tête de la diapo).

```markdown
::: {.bilan moment="debut"}
- C1 | Décrire avant d'interpréter
- C2 | Identifier un objet avec les clés d'identification
:::
```

**Dossier** — une chemise cartonnée, tamponnée « TOP SECRET » ; un clic l'ouvre, et son contenu (une image, en général) s'affiche en plein écran. Échap ou un clic à côté la referme. Le PDF montre le contenu à plat. `tampon="…"` change le tampon.

```markdown
::: {.dossier titre="Le renseignement vu du ciel, 1858-2020"}
![](images/frise-intelligence.png){fig-alt="Description"}
:::
```

**Phrases à compléter** — chaque phrase porte un menu, entre accolades ; `=` marque le ou les choix justes. Après « : », le commentaire, affiché une fois le choix fait. Le PDF donne les mots attendus.

```markdown
::: {.phrases}
- Il est {presque certain|=probable|possible|peu probable} qu'il y ait des ouvriers sur le site : on ne voit personne, mais la base vie est là.
:::
```

**Combiner** — l'étudiant compose une réponse, un choix par ligne (`###` : une ligne de choix), puis découvre si elle existe. Chaque choix porte entre crochets les réponses qui l'admettent ; les réponses s'écrivent en `#### code | Titre`, suivies de leur texte ; `#### * | …` est le texte affiché quand aucune réponse ne réunit les choix. Le PDF donne toutes les réponses.

```markdown
::: {.combiner}
### Surface minimale

- 0,5 ha [fao, kyoto]
- 25 ha [clc]

### Hauteur des arbres

- 5 m [fao, kyoto, clc]

#### fao | La FAO

Plus de 0,5 ha, des arbres de plus de 5 m, un couvert de plus de 10 %.

#### * | Aucune définition connue

Le texte affiché sinon.
:::
```

**Calibration** — un tableau : quand l'étudiant se disait sûr, avait-il raison ? Il se remplit avec les barres de certitude du cours.

**Révision** — des cartes de rappel, mélangées et entrelacées (jamais deux cartes de la même compétence à la suite). Une carte sue revient dans un jour, puis une semaine, puis un mois ; une carte ratée revient dans la séance. En tête, les compétences : celle qui est interrogée s'allume, celle dont toutes les cartes sont sues se grise. L'adresse du support suivie de `?revision` ouvre directement cette diapo.

Les cartes s'écrivent dans la brique, pour le rappel (pas les questions du cours recopiées) : d'abord la liste des compétences, puis une carte par titre `###`, avec sa compétence et son type :

- `libre` : l'étudiant écrit de mémoire, puis voit la réponse et se juge ; la question, puis `---`, puis la réponse ;
- `image` : la même chose sur une image du cours, avec en option un cadre `x,y,largeur,hauteur` en % ;
- `qcm` : des choix `- [x]` (juste) ou `- [ ]`, chacun suivi de son retour après « : ».

```markdown
::: {.revision}
- C1 | Décrire avant d'interpréter
- C3 | Identifier avec les clés

### C1 libre

Réécrivez « Le site est une centrale nucléaire » en séparant ce que l'on voit de ce que l'on déduit.

---

La réponse attendue.

### C3 image | images/flamanville.jpg | 53,46,7,17

Quels sont ces objets encadrés ? Quelles clés vous l'ont dit ?

---

La réponse attendue.

### C3 qcm

La question.

- [x] Le bon choix : pourquoi.
- [ ] Un autre choix : pourquoi pas.
:::
```

Sans contenu (`::: {.revision}` puis `:::`), la brique reprend toutes les questions et tous les QCM du cours, comme avant.

**Relier** — deux colonnes ; l'étudiant relie chaque élément de gauche à son correspondant de droite (la colonne de droite est mélangée), puis vérifie : les lignes justes passent au vert, les fausses au rouge.

```markdown
::: {.relier}
- Ombre A -> Une éolienne
- Ombre B -> Un château d'eau
:::
```

Une énigme **Indices** sans texte après la liste n'a pas de conclusion : le bouton disparaît après le dernier indice. La colonne des indices ne dépasse jamais la hauteur de l'image : au-delà, elle défile.

```markdown
::: {.calibration}
:::
```

### Les briques d'application

Elles vivent dans `_briques/briques-application.html` et `_briques/briques-application.css`. Le cours `cours/image-application` en contient un exemple de chacune. Ce qui est fait est gardé dans le navigateur ; seul l'atelier peut l'envoyer, volontairement, vers une feuille de calcul.

**Vote** — des énoncés un à un ; l'étudiant répond oui, non ou pas sûr, puis lit l'explication. `[vrai]` ou `[faux]` en tête de l'énoncé ; `[?]` pour un simple sondage, sans bonne réponse. Le texte après « : » est l'explication. Un bilan termine la série.

```markdown
::: {.vote question="Peut-on le faire depuis le ciel ?"}
- [vrai] Voir une inondation à travers les nuages : Le radar traverse les nuages.
- [faux] Lire une plaque d'immatriculation : Il faudrait des pixels de quelques centimètres.
    - image : images/pleiades-neo.jpg
    - legende : © Airbus DS, Pléiades Neo, 2021.
    - lien : https://…
:::
```

Sous chaque énoncé, une sous-liste facultative montre, avec la réponse, une `image` (avec `zoom : 4`, un clic l'agrandit dans son cadre et la souris la parcourt, comme la loupe), un `fondu` (seconde image fondue dans la première par un curseur ; les deux de même emprise) ou une `video` (adresse YouTube), avec sa `legende` et son `lien`. Dans le PDF, seuls les énoncés et les explications sont imprimés.

**Compromis** — quatre curseurs centrés sur zéro (résolutions spatiale, temporelle, spectrale, radiométrique). Monter l'un en fait baisser un autre, et la brique dit pourquoi. Un titre `###` par objectif, suivi de sa condition après « | » (`temporelle >= 2`, plusieurs séparées par des virgules) ; un objectif impossible est reconnu comme tel. La liste donne les capteurs de référence : nom | quatre valeurs de -3 à 3 | une note. Le profil réglé est rapproché du capteur le plus proche.

```markdown
::: {.compromis}
### Suivre chaque jour un phénomène | temporelle >= 2
- Météosat | -3, 3, 0, 0 | une image toutes les 10 à 15 minutes
- Sentinel-2 | 0, 0, 0, 0 | 10 à 60 m, tous les cinq jours
:::
```

**Atelier des commandes** — le jeu sérieux : une commande, une réserve d'hexagones par famille, un plateau, quatre personnages à interroger (leurs réponses débloquent des hexagones « fins » et contiennent des pépites), la correction sur la proposition des étudiants, la fiche d'un cas réel, l'envoi. Tout le contenu est dans un fichier JSON du cours (`donnees/atelier.json`), qui se modifie sans toucher au moteur. `envoi="…"` donne l'adresse de la feuille Google qui reçoit les travaux (mise en place : `cours/image-application/outils/feuille-google.gs`) ; vide, l'envoi est remplacé par un téléchargement. La diapo prend la classe `{.atelier-plein}` pour gagner de la hauteur.

```markdown
## L'atelier {.atelier-plein}

::: {.atelier-commandes donnees="donnees/atelier.json" envoi=""}
:::
```

Les règles de l'atelier : chaque hexagone doit toucher un hexagone d'une étape antérieure, le verbe ouvre la chaîne, *Valider* n'est jamais facultatif. Dans le fichier, une entrée de correction `"ids": ["a", "b"]` se lit « a ou b ».

**Chaîne de référence**, **pépites**, **envoi** — trois briques qui relisent le même fichier : la chaîne de référence d'une commande, en hexagones ; la liste des pépites, celles que le groupe a entendues étant allumées ; le panneau d'envoi, pour une diapo de fin.

```markdown
::: {.chaine commande="lidar"}
:::

::: {.pepites}
:::

::: {.envoi}
:::
```

La **carte du cours** passe un niveau sur deux colonnes dès qu'il compte plus de 16 diapos, pour qu'il ne déborde pas de la diapo.

Deux classes de mise en page : `::: {.column .centre-v width="60%"}` centre une colonne sur la hauteur ; `::: {.cote-a-cote}` place des images côte à côte, sans colonnes imbriquées (une image par paragraphe). Les images ne sont jamais déformées : une hauteur imposée et une largeur bridée par la colonne gardent le rapport hauteur-largeur.

### Les briques du jeu de rôle

Elles vivent dans `_briques/briques-jeu.html` et `_briques/briques-jeu.css`, avec une identité propre (JRPG 8 bits aux couleurs de Géodata, police pixel *Press Start 2P*, sous licence OFL). Exemple complet : la partie 4 de `cours/image-application/IMAGE-Application.qmd` (l'atelier Saumos). Tout le contenu du jeu (préfet, experts, postures, enquêtes, indices, pistes, rapport, barème, sévérité, phrase) est dans un fichier JSON du cours, par défaut `donnees/saumos.json` ; les têtes en pixel art dans `donnees/pixels.json`, produit par `outils/pixels.py`. Une autre partie se joue en changeant de fichier : `donnees="…"`, `pixels="…"` sur la brique.

| Brique | Ce qu'elle fait |
|---|---|
| `{.jdr-commande}` | le préfet dit sa commande, sa tête parle, avec un son de lecture sans langue ; à côté, la carte 8 bits de la zone (`carte` dans le JSON : image, emprise, lieux), produite par `outils/carte-saumos.py` |
| `{.jdr-paris}` | les paris de départ (curseur ou choix) |
| `{.jdr-equipe}` | groupe, prénom, posture, tête de héros, mode solo, « Recommencer la partie » |
| `{.jdr-cadrage}` | Rose cadre le travail, réplique par réplique, selon la posture de celui qui lit ; une étape peut attendre une réponse libre de l'étudiant avant celle de Rose |
| `{.jdr-experts}` | les experts (nom, rôle, travail), Rose à part, et « C'est parti » qui lance le chrono |
| `{.jdr-enquete enquete="A"}` | le dialogue : « Avec qui veux-tu commencer ? », choix, réponses tapées, apartés, clefs des labos, carnet, journal, confiance du préfet, chrono |
| `{.jdr-labo labo="a"}` | les labos, versions JRPG des sites de référence (`a` Eumetsat, `b` Copernicus, `c` Deimos), fermés tant qu'un expert n'en a pas passé les clefs |
| `{.jdr-rapport envoi=""}` | le rapport au propre, relu par le préfet, téléchargé ou envoyé à la feuille Google |
| `{.jdr-phrase}` | la phrase à trous de la classe, pour la projection |
| `{.jdr-bulle qui="rose"}` | un expert dit le texte écrit dans la brique, ou une liste du fichier (`source="debrief" liste="oui"`) |
| `{.jdr-retour envoi=""}` | une case libre pour l'avis des étudiants sur le jeu, téléchargée ou envoyée à la feuille Google (onglet « Saumos — avis ») |

Les diapos de jeu prennent un identifiant, la classe `{.jdr-plein}` et `data-state="plein"` (le pied de page disparaît) : `{#enquete-a .jdr-plein data-state="plein"}`. En groupe, chacun n'a accès qu'à son enquête et à son labo ; en solo, aux trois. Le chrono (30 minutes d'enquête, 5 de rapport) part de « C'est parti ».

**La navigation du jeu.** Les flèches du clavier restent actives. Dans un cours dont le jeu n'est qu'une partie, l'intercalaire de cette partie prend la classe `.jdr-titre` (son titre passe en 8 bits) ; les boutons ◀ ▶ n'apparaissent alors que sur les diapos du jeu (`.jdr-titre`, `.jdr`, `.jdr-plein`). En plus, deux boutons, toujours en bas à droite (un peu au-dessus du bord), ◀ et ▶, prennent l'étiquette de la diapo : « Choisissez une posture » (grisé à l'équipe tant qu'aucune posture ni le mode solo n'est choisi), « Continuer ▶ » au cadrage, « C'est parti ▶ » aux experts (seul bouton de lancement), « ◀ experts » et « 🔑 Labo … ▶ » dans une enquête (grisé tant que la clef manque), « ◀ enquête X » dans un labo.

**Les termes techniques.** Dans n'importe quel texte du JSON, `[[mot affiché|terme]]` colore le mot ; `terme` renvoie à la rubrique `termes` (`mot`, `qui`, `texte`). Dans un dialogue, un clic ouvre un aparté de l'expert (« X · aparté : mot », puis « ↩ Reprendre la discussion ») ; ailleurs, une petite fenêtre. Le terme entre dans le lexique du carnet et s'y coche ✓. `[[mot]]` seul vaut `[[mot|mot]]`.

Dans le fichier, une enquête a des accueils (un par expert) et des nœuds. Un nœud a sa question `q`, sa réponse `r`, ses conditions `si` et `sauf` (nœuds entendus, essais, indices, clefs), un type (`choix`, `ouverte`, `aparte`) et ses effets (`indices`, `clefs`, `debloque`, `cout`, `note`, `image`) ; voir la clé `lisez-moi`. Pour relire les dialogues, `outils/dialogues.py` écrit un script lisible et un graphe façon Twine dans `source/Cas1-Saumos/`. Ce que fait le joueur reste dans son navigateur.

Deux supports dans un même dossier : `suffixe-plan: "-atelier-saumos"` dans l'en-tête du second lui donne son propre `plan-atelier-saumos.md` et son propre registre `figes-atelier-saumos.json`.

### Réglages utiles

| Écriture | Effet |
|---|---|
| `::: {.zones … hauteur="500"}` | fixe la hauteur de l'image cliquable, en pixels |
| `::: {.retour-ici}` suivi de `:::` | le commentaire des zones s'affiche à cet endroit plutôt que sous l'image, et figure dans le PDF corrigé |
| `::: {.qcm .serre}` | QCM plus compact, quand les commentaires sont nombreux |
| `::: {.apres-choix}` … `:::` | contenu masqué tant qu'aucune réponse du QCM n'est choisie |
| `:::: {.columns .resserre}` | colonnes au texte plus petit, pour laisser la place à une image |
| `::: {.centre}` … `:::` | centre une image |
| `::: {.defiler commande="haut"}` | les flèches et la légende passent au-dessus des images et ne bougent plus d'une image à l'autre |

Un schéma peut réagir au QCM de sa diapo : voir `images/schemas/aplatissement.svg` dans le cours.

Dans un schéma, les éléments marqués `class="s-apparait"` restent cachés jusqu'à l'ouverture de la réponse de la diapo, et figurent dans le PDF corrigé : voir `images/schemas/jointure.svg` dans le cours `gis-geoprocessing`.

## Les images d'un cours

- `images/` contient les versions légères, celles que le cours utilise : 1 600 pixels au plus, noms simples, sans espace ni accent.
- `images/originaux/` conserve les fichiers d'origine, tels qu'ils ont été déposés.
- `images/correspondance.csv` dit quel original a donné quelle version légère.
- `images/schemas/` contient les dessins vectoriels.

Pour ajouter une image : la déposer dans `images/` avec un nom simple. Si elle dépasse 1 600 pixels, la réduire d'abord, sinon le fichier HTML grossit vite.

## Adapter un cours sans le réécrire

Sans recompiler, en ajoutant à l'adresse de la page :

- `GIS-Basics.html?niveau=socle` — ne garde que le socle (fiche de révision) ;
- `GIS-Basics.html?niveau=socle,appui` — deux niveaux ;
- `GIS-Basics.html?optionnels=non` — retire les diapos `.optionnel`.

Pour graver ce tri dans le fichier produit, ajouter dans l'en-tête du cours (entre les `---`) puis recompiler :

```yaml
garder-niveaux: socle
masquer-optionnels: true
```

## Une version dans une autre langue

La version anglaise d'un cours est un second fichier à côté du premier, au même nom suivi de `-EN` (`GIS-Basics-EN.qmd`), avec `lang: en` dans son en-tête. Cette ligne suffit pour que tout ce que le gabarit écrit lui-même passe en anglais : noms des niveaux (Core, Support, Further), « Question », « Answer », « Going further », messages des exercices, format des nombres. La typographie française (espaces avant `:`, `;`, `?`) n'est appliquée qu'en français.

- Les fiches gardent les mêmes numéros ; leurs lignes s'écrivent `Intention :`, `Experience :`, `Request :`.
- Les schémas qui contiennent du texte sont doublés dans `images/schemas/en/`. Les images sont partagées.
- La compilation produit la version anglaise (`…-EN.html`, `…-EN.pdf`) et `plan-en.md` ; le script de gel tient un registre séparé, `figes-en.json`.
- Les deux fichiers sont indépendants : une correction faite dans l'un est à reporter dans l'autre.

Pour une autre langue, ajouter un jeu de textes en tête de `_briques/gabarit.lua` et de `_briques/briques.html`.

## Où est quoi

| Dossier | Contenu | On y touche ? |
|---------|---------|---------------|
| `cours/` | les cours, un dossier chacun, qui contient tout (voir « Créer un nouveau cours ») | oui, tout le temps |
| `bac-a-sable/` | brouillons jetables | oui |
| `_charte/` | couleurs, polices, logos Géodata, modèle PPT de l'école | seulement si la charte change |
| `_briques/` | le moteur : niveaux et exercices | rarement |
| `outils/` | les outils communs : `figer.py`, `sorties.py`, `pdf.py`, `controle.py` | rarement |
| `requirements.txt` | les modules Python à installer (voir « Ce qu'il faut installer ») | rarement |

Changer une couleur ou une police : tout est en tête de `_charte/geodata.css`.

## Limites connues

- Les exercices et les expériences ne sont interactifs qu'en HTML. Le PDF en montre l'énoncé et, par défaut, le corrigé.
- Les bonus « Pour aller plus loin » ne figurent pas dans le PDF.
- Les liens de la carte du cours ne fonctionnent pas dans le PDF.
- Les réponses des étudiants ne sont pas enregistrées, sauf l'envoi volontaire de l'atelier des commandes ou du rapport du jeu de rôle vers une feuille Google.
- Dans la version anglaise, les images qui contiennent du texte français (profil du géoïde, zones Lambert, schéma SPOT…) ne sont pas traduites.
- Les formules mathématiques s'affichent sans réseau, mais avec un rendu plus simple que LaTeX.
