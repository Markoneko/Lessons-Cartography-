# Supports de cours — Géodata Paris / FIRS

Un cours = un fichier texte (`index.qmd`) et un dossier d'images.
La mise en page, la charte et les exercices sont fournis par le gabarit : on ne s'occupe que du contenu.

Aucune IA n'est nécessaire pour écrire, modifier ou produire un support.

## Ce qu'il faut installer (une fois)

- [Quarto](https://quarto.org/docs/get-started/) — le programme qui transforme le texte en diapos.
- Un éditeur de texte. [VS Code](https://code.visualstudio.com/) avec l'extension Quarto donne un aperçu en direct, mais le Bloc-notes suffit.

## Produire un support

Dans un terminal, depuis ce dossier :

```
quarto render cours/mon-cours/index.qmd
```

Le résultat arrive dans `_sortie/cours/mon-cours/` :

`index.html` (ou le nom donné par `output-file:` dans l'en-tête du cours, par exemple `Cartography-Basics.html`) : un seul fichier, qui fonctionne sans réseau. Il sert à projeter et à faire manipuler les étudiants. Touche `F` : plein écran. Touche `S` : vue orateur avec les notes.

Pour le **PDF**, qui sert de support de cours : ouvrir `index.html` dans Chrome ou Edge, ajouter `?print-pdf` à la fin de l'adresse, puis Imprimer → Enregistrer au format PDF (marges : aucune, graphiques d'arrière-plan : cochés).

- `index.html?print-pdf` — le support avec le corrigé des exercices ;
- `index.html?print-pdf&reponses=non` — le même, sans les réponses.

Pour travailler avec un aperçu qui se met à jour à chaque enregistrement :

```
quarto preview cours/mon-cours/index.qmd
```

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
python3 outils/figer.py verifier cours/de-la-terre-a-la-carte/index.qmd
```

Les règles que doit suivre un assistant sont dans `CONSIGNES-IA.md`.

## Créer un nouveau cours

1. Copier le dossier `cours/de-la-terre-a-la-carte` et le renommer.
2. Remplacer le contenu de `index.qmd` et les images.

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

**Zones à cliquer sur une image** — chaque zone est donnée en pourcentage de l'image : gauche, haut, largeur, hauteur.

```markdown
::: {.zones image="images/carte.jpg" alt="Description de l'image"}
- [x] 30,0,16,22 : Bien vu, parce que…
- [ ] 45,33,17,30 : Non, ici…
:::
```

## Les expériences

Chaque brique s'écrit en quelques lignes. Le cours `cours/de-la-terre-a-la-carte/index.qmd` en contient un exemple de chacune, à copier.

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

**Comparer des images** — un curseur fond les images l'une dans l'autre. Le texte entre crochets sert d'étiquette. Les images doivent couvrir la même emprise.

```markdown
::: {.comparer}
- ![Cassini](images/nancy-cassini.jpg)
- ![Aujourd'hui](images/nancy-top25.jpg)
:::
```

**Défiler des images** — une seule à la fois, en grand, avec deux flèches. Le texte entre crochets sert de légende.

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

**Classer** — un titre `###` par case, puis ce qui doit y aller. Laisser une ligne vide avant chaque titre.

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

Les schémas du cours (cartes en symboles, palettes, illusions) sont produits par `python3 outils/schemas-cartography.py cours/cartography-basics`, en français et en anglais. Les valeurs données dans les réponses sont calculées par ce script, pas recopiées à la main.

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

Dans un schéma, les éléments marqués `class="s-apparait"` restent cachés jusqu'à l'ouverture de la réponse de la diapo, et figurent dans le PDF corrigé : voir `images/schemas/jointure.svg` dans le cours `geotraitements`.

## Les images d'un cours

- `images/` contient les versions légères, celles que le cours utilise : 1 600 pixels au plus, noms simples, sans espace ni accent.
- `images/originaux/` conserve les fichiers d'origine, tels qu'ils ont été déposés.
- `images/correspondance.csv` dit quel original a donné quelle version légère.
- `images/schemas/` contient les dessins vectoriels.

Pour ajouter une image : la déposer dans `images/` avec un nom simple. Si elle dépasse 1 600 pixels, la réduire d'abord, sinon le fichier HTML grossit vite.

## Adapter un cours sans le réécrire

Sans recompiler, en ajoutant à l'adresse de la page :

- `index.html?niveau=socle` — ne garde que le socle (fiche de révision) ;
- `index.html?niveau=socle,appui` — deux niveaux ;
- `index.html?optionnels=non` — retire les diapos `.optionnel`.

Pour graver ce tri dans le fichier produit, ajouter dans l'en-tête du cours (entre les `---`) puis recompiler :

```yaml
garder-niveaux: socle
masquer-optionnels: true
```

## Une version dans une autre langue

La version anglaise d'un cours est un second fichier à côté du premier : `index-en.qmd`, avec `lang: en` dans son en-tête. Cette ligne suffit pour que tout ce que le gabarit écrit lui-même passe en anglais : noms des niveaux (Core, Support, Further), « Question », « Answer », « Going further », messages des exercices, format des nombres. La typographie française (espaces avant `:`, `;`, `?`) n'est appliquée qu'en français.

- Les fiches gardent les mêmes numéros ; leurs lignes s'écrivent `Intention :`, `Experience :`, `Request :`.
- Les schémas qui contiennent du texte sont doublés dans `images/schemas/en/`. Les images sont partagées.
- La compilation produit `index-en.html` et `plan-en.md` ; le script de gel tient un registre séparé, `figes-en.json`.
- Les deux fichiers sont indépendants : une correction faite dans l'un est à reporter dans l'autre.

Pour une autre langue, ajouter un jeu de textes en tête de `_briques/gabarit.lua` et de `_briques/briques.html`.

## Où est quoi

| Dossier | Contenu | On y touche ? |
|---------|---------|---------------|
| `cours/` | les cours, un dossier chacun | oui, tout le temps |
| `bac-a-sable/` | brouillons jetables | oui |
| `sources/` | les supports d'origine (PPT) | jamais |
| `_charte/` | couleurs, polices, logos Géodata | seulement si la charte change |
| `_briques/` | le moteur : niveaux et exercices | rarement |
| `_sortie/` | les fichiers produits (non versionnés) | non |

Changer une couleur ou une police : tout est en tête de `_charte/geodata.css`.

## Limites connues

- Les exercices et les expériences ne sont interactifs qu'en HTML. Le PDF en montre l'énoncé et, par défaut, le corrigé.
- Les bonus « Pour aller plus loin » ne figurent pas dans le PDF.
- Les liens de la carte du cours ne fonctionnent pas dans le PDF.
- Les réponses des étudiants ne sont pas enregistrées.
- Dans la version anglaise, les images qui contiennent du texte français (profil du géoïde, zones Lambert, schéma SPOT…) ne sont pas traduites.
- Les formules mathématiques s'affichent sans réseau, mais avec un rendu plus simple que LaTeX.
