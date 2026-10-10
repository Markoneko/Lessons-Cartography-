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

`index.html` : un seul fichier, qui fonctionne sans réseau. Il sert à projeter et à faire manipuler les étudiants. Touche `F` : plein écran. Touche `S` : vue orateur avec les notes.

Pour le **PDF**, qui sert de support de cours : ouvrir `index.html` dans Chrome ou Edge, ajouter `?print-pdf` à la fin de l'adresse, puis Imprimer → Enregistrer au format PDF (marges : aucune, graphiques d'arrière-plan : cochés).

- `index.html?print-pdf` — le support avec le corrigé des exercices ;
- `index.html?print-pdf&reponses=non` — le même, sans les réponses.

Pour travailler avec un aperçu qui se met à jour à chaque enregistrement :

```
quarto preview cours/mon-cours/index.qmd
```

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
- Les formules mathématiques s'affichent sans réseau, mais avec un rendu plus simple que LaTeX.
