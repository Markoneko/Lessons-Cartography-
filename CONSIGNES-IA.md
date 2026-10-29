# Consignes pour une IA qui travaille sur ce dépôt

Ces règles valent pour tout assistant, en ligne ou local, à qui l'on confie un cours.

## La référence

Un cours a une seule source : son fichier `.qmd`, qui porte le nom du cours (`GIS-Basics.qmd`, version anglaise `GIS-Basics-EN.qmd`). Le fichier `plan.md` est généré à partir de lui ; on ne le modifie jamais.

Sous chaque titre de diapo, une fiche dit ce que la diapo doit faire et dans quel état elle est :

```markdown
::: {.fiche n="1.9" etat="fige"}
Intention : ce que la diapo doit faire comprendre.
Expérience : ce que l'étudiant fait.
Demande : ce que l'enseignant veut changer.
:::
```

Quand un cours existe en deux langues, le fichier français reste la référence et le fichier en `-EN.qmd` sa traduction (fiches `Intention :`, `Experience :`, `Request :`, registre `figes-en.json`). Une correction demandée dans l'un est reportée dans l'autre, et le compte rendu le dit.

## Ce que l'on a le droit de toucher

| État | Règle |
|---|---|
| `fige` | Ne rien modifier, pas même une virgule ou une espace. |
| `a-revoir` | Appliquer la demande, sur cette diapo seulement. |
| `a-realiser` | Construire la diapo à partir de la fiche. |

- Ne jamais réécrire le fichier en entier. On travaille diapo par diapo.
- Une diapo figée dont la ligne « Demande » est remplie : ne pas y toucher, le signaler à l'enseignant.
- Ce que l'enseignant écrit entre guillemets « » est recopié mot pour mot.
- Ne pas inventer de brique : n'utiliser que celles du `README.md`.
- Ne pas affirmer un fait non vérifié. En cas de doute, le dire dans le compte rendu.

## Le déroulé d'un passage

1. Récupérer la dernière version du dépôt.
2. Lancer `python3 outils/figer.py verifier cours/<cours>/<Nom-du-cours>.qmd` : il montre ce que l'enseignant a dégelé ou modifié depuis le dernier passage.
3. Lancer `python3 outils/figer.py enregistrer cours/<cours>/<Nom-du-cours>.qmd` : l'état reçu devient la référence.
4. Traiter les diapos `a-revoir` et `a-realiser`. Une fois la demande appliquée, vider la ligne « Demande » et laisser l'état tel quel : c'est l'enseignant qui fige.
5. Compiler avec `quarto render cours/<cours>/<Nom-du-cours>.qmd` (et sa version `-EN.qmd`), puis vérifier le rendu : `python3 outils/controle.py cours/<cours>/_sortie/<Titre>.html` doit répondre « 0 débordement(s) », sans erreur JavaScript.
6. Relancer `verifier` : il doit répondre « Aucune diapo figée n'a été modifiée ».
7. Noter le passage dans `JOURNAL.md`, puis envoyer.

## Le compte rendu

Dire, par numéro de diapo, ce qui a été changé, ce qui n'a pas pu l'être, et ce qui reste à vérifier.
