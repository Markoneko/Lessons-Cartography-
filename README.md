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

1. Copier le dossier `bac-a-sable/terre-a-la-carte` dans `cours/` et le renommer.
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

Pour relier une diapo à une perle de la Canopée : `{.socle perle="CODE-01"}`.

### La carte du cours

```markdown
## Carte du cours

::: {.carte-du-cours}
:::
```

Elle liste les diapos par niveau. Chaque ligne est un lien vers sa diapo, et le pictogramme de chaque diapo ramène à la carte.

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
| `bac-a-sable/` | essais jetables | oui |
| `sources/` | les supports d'origine (PPT) | jamais |
| `_charte/` | couleurs, polices, logos Géodata | seulement si la charte change |
| `_briques/` | le moteur : niveaux et exercices | rarement |
| `_sortie/` | les fichiers produits (non versionnés) | non |

Changer une couleur ou une police : tout est en tête de `_charte/geodata.css`.

## Limites connues

- Les exercices ne sont interactifs qu'en HTML. Le PDF en montre l'énoncé et, par défaut, le corrigé.
- Les liens de la carte du cours ne fonctionnent pas dans le PDF.
- Les réponses des étudiants ne sont pas enregistrées.
- Les formules mathématiques s'affichent sans réseau, mais avec un rendu plus simple que LaTeX.
