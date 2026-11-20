# Atelier Saumos — script v2 : le graphe du jeu de rôle et le fil de réalisation

Document de travail. La v1 annotée par Marc (`atelier-saumos-script-v1.md`) reste la trace de ses
décisions ; cette v2 en tire les conséquences. Rien n'est codé avant validation du graphe (§ 4).

---

## 1. Décisions de Marc (relevées dans la v1 annotée)

- On reste sur la conception **v3bis** (pas de v4).
- **Pas de postes séparés** : chaque groupe de trois se répartit les tâches. Trois postures, chacune
  nommée : le **rapporteur** (prend les notes, compile, livre le résultat versé dans la feuille),
  l'**orbitographe** (perce le secret des couples vecteur / capteur), l'**analyste** (dégage les
  informations spatiales). Idéalement, chaque étudiant choisit sa tête de héros de JRPG dans une liste.
- **Cinq experts**, chacun avec une tête en pixel art 8 bits de JRPG, une spécialité, un trait de
  caractère : Elikia (le signal), Bastien (les données), Inès (les orbites), Youri (les traitements),
  Rose (la contradictrice).
- La **commande du préfet** : un outil qui donne précisément la surface brûlée à la fin du feu, et la
  date précise du départ.
- Deux **paris** au départ : combien de jours après la fin du feu pour la cartographie demandée ;
  combien d'ETP pour cette estimation. La réponse attendue : **cela dépend de la précision voulue et
  des moyens engagés**. Les groupes doivent finir en proposant au préfet **trois solutions datées** :
  avec de l'argent, une commande d'acquisition ; pour une précision relative, le radar ; sinon,
  attendre une Sentinel-2 sans nuages.
- L'**enquête** : une diapo par sujet, une seule question, « Avec qui veux-tu commencer ? ». On clique
  un expert, son portrait s'anime, sa réponse défile dessous. Le bon expert ouvre des pistes.
- Les experts **ne répondent pas la même chose selon le profil** qui les interroge. Ils aident aussi
  à manipuler les trois sites de référence.
- Un **secours intégré par poste**, Deimos compris (une animation simple : le Soleil, la Terre et les
  deux satellites).
- L'**échange** : Marc demande quels groupes ont plus de 6 points sur 8, puis revient sur les
  difficultés des autres.
- Le **verdict** pointe vers la méthode de UN-SPIDER (Normalized Burn Ratio).
- Les diapos actuelles du cours sont gardées, hors partie 4, qui est remplacée.

---

## 2. Les rôles dans le groupe

| Posture | Ce qu'il fait | Sujet qu'il porte | Ce que les experts lui disent |
|---|---|---|---|
| **Rapporteur** | prend les notes, compile, rédige le rapport, l'envoie | les paris, les trois solutions au préfet | ce qu'il faut écrire, la source, la limite |
| **Orbitographe** | trouve les satellites, leurs orbites, leurs passages | sujet C, et l'aide aux deux autres | quand passe quoi, et pourquoi |
| **Analyste** | lit les images, mesure, compare | sujets A et B | quelles bandes, quelle composition, quel pixel |

> **À trancher par Marc.** Le sujet A (la date de départ) revient-il à l'analyste, comme proposé
> ici, ou au rapporteur, pour qu'il ait lui aussi une enquête à mener ?

Chaque étudiant choisit sa posture et sa tête au début. La posture change les réponses des experts ;
la tête est seulement là pour le plaisir et l'engagement.

---

## 3. La mécanique du dialogue

- **Un nœud** : un expert, une question du joueur, une réponse. La réponse a un tronc commun (le fait)
  et un angle selon la posture qui pose la question. **Règle d'écriture : le même fait, trois angles.**
  Ainsi les trois membres du groupe entendent des choses complémentaires et doivent se parler.
- **Pas d'impasse.** Interroger le « mauvais » expert donne une réplique drôle, une miette utile, et
  une redirection (« Va voir Inès, elle compte en tours de Terre »).
- **Les indices** se débloquent par nœuds : un nœud ouvre de nouvelles questions, chez le même expert
  ou chez un autre. Trois paliers au plus par question : où regarder, quoi comparer, quelle question
  se poser. Jamais la réponse.
- **Les pistes** : certains nœuds ouvrent une piste sur un site de référence (« Dans EUMETView,
  laisse les paramètres par défaut et fais défiler »), avec le secours intégré en lien.
- **La confiance du préfet** : elle baisse un peu à chaque indice de palier 3, monte avec chaque
  réponse justifiée du rapport. Elle s'affiche, ne compte pas.

---

## 4. Le graphe, première piste (à valider, corriger)

Notation : `[expert] question du joueur` → réponse (tronc) ; angles par posture **R** (rapporteur),
**O** (orbitographe), **A** (analyste) ; `⇒` ce que le nœud débloque.

### Enquête A — « Quand le feu a-t-il démarré ? »  (bon premier expert : Elikia)

```
A0 [Elikia] (accueil)
   « Bonjour ! Il n'y a pas de fumée sans feu : si vous êtes là, c'est que vous cherchez à
     détecter quelque chose dans une image, je me trompe ? »
   Choix du joueur : « On cherche le départ du feu. » | « On cherche la fumée. » (réplique drôle)
   ⇒ A1

A1 [Elikia] « Qu'est-ce qui trahit un feu ? »
   Tronc : « Quels phénomènes trahissent un feu ? Pensez aux propriétés des photons qui vous
             intéressent : elles vous diront quelles bandes regarder. »
   A : « La fumée se voit dans le visible ; les flammes émettent dans l'infrarouge moyen.
         Quelles bandes allumeriez-vous ? »                      ⇒ indice « compositions colorées »
   O : « Un feu naît vite. Il vous faut un œil qui ne cligne jamais. Inès sait lequel. »
                                                                 ⇒ question C2 chez Inès
   R : « Notez bien : on ne voit pas le feu, on voit sa chaleur et sa fumée. Écrivez ce que vous
         observez, pas ce que vous croyez. »                     ⇒ champ « preuve » du rapport
   ⇒ A2

A2 [Elikia] « Où chercher le premier signe ? »
   Tronc : « Faites défiler les images une à une. Le premier point chaud, c'est quand ? »
   ⇒ piste EUMETView (paramètres par défaut) + secours : la série Meteosat intégrée
   ⇒ indice « date » : le rappel du jour du début de l'incendie

A3 [Elikia] « Peut-on tracer le contour du feu sur ces images ? »
   Tronc : « Comparez la taille d'un pixel à celle d'une commune. Vous pourriez tracer un contour,
             vous, avec des pixels pareils ? »
   ⇒ la limite du rapport A (« ce que je ne peux pas dire »)

Autres experts, s'ils sont interrogés pour l'enquête A :
   [Bastien]  « J'ai des images de cette forêt tous les cinq jours depuis des années. […] J'ai aussi
               des images toutes les 15 minutes, mais c'est plutôt utilisé pour la météo, pas le
               suivi de la végétation, cela vous intéresse ? »  ⇒ redirige vers Elikia et EUMETView
   [Inès]     « Un satellite qui regarde toujours la même face de la Terre ? Je connais. Revenez
               me voir avec son nom. »                          ⇒ C2
   [Youri]    « Trop tôt. Le feu n'a pas encore fini de brûler. Revenez avec des images d'après. »
   [Rose]     « "Il a démarré à 11 h." Selon quel capteur ? Avec quelle incertitude ? »
                                                                ⇒ exigence du rapport : source et marge
```

### Enquête B — « Quelle surface a brûlé ? »  (bon premier expert : Bastien)

```
B0 [Bastien] (accueil) — sa réplique d'accueil de la v1, blague sur les chocolatines comprise
B1 [Bastien] « Quelle image prendre ? »
   Tronc : « Une date avant, une date après. Commencez par l'avant : il n'y a rien à voir,
             et c'est justement pour ça qu'il compte. »
   A : les dates disponibles dans le Copernicus Browser, la couverture nuageuse à regarder
   O : « Pourquoi n'y a-t-il pas une image chaque jour ? Inès vous le dira. »   ⇒ C3
   R : « Notez la date exacte de chaque image : sans elle, votre surface ne veut rien dire. »
   ⇒ piste Copernicus Browser (Sentinel-2 L2A) + secours : l'outil de mesure intégré
B2 [Bastien] « La fumée gêne. » → « Essayez une composition qui ne regarde pas dans le visible. »
   ⇒ Elikia B2' : pourquoi l'infrarouge moyen traverse mieux la fumée
B3 [Bastien] « Ma surface change entre deux dates. » → « Le feu a grandi, ou c'est votre image
   qui voyait moins bien ? »                                    ⇒ la part non tracée (nuages)
B4 [Rose] « Le préfet veut UN chiffre demain matin. Lequel lui donnez-vous, et à quel prix ? »
   ⇒ les trois solutions datées (commande d'acquisition, radar, Sentinel-2 sans nuages)
```

### Enquête C — « Quels satellites, et quand passent-ils ? »  (bon premier expert : Inès)

```
C0 [Inès] (accueil) — ancienne de Géodata Paris, ne pense qu'en tours de Terre
C1 [Inès] « Par où commencer ? » → « Demandez à vos collègues le nom de leurs satellites. Sans eux,
   je calcule dans le vide. »                                   ⇒ échange obligatoire dans le groupe
C2 [Inès] « Un satellite qui ne quitte jamais l'Europe ? » → l'altitude du géostationnaire, ce qu'il
   gagne (la cadence) et ce qu'il perd (le pixel)               ⇒ piste Deimos + secours animé
C3 [Inès] « Pourquoi Sentinel-2 ne repasse-t-il que tous les cinq jours ? » → l'orbite héliosynchrone,
   la fauchée, et ce qui se passe si c'est nuageux ce jour-là   ⇒ lien avec les curseurs de la partie 2
C4 [Inès] « Qui a tracé le périmètre officiel si tôt ? » → un satellite que l'on pointe à la demande
   ⇒ la solution « commande d'acquisition » (et son coût : Rose)
```

### Sévérité et verdict (tous)

```
S0 [Youri] « Le plus noir à l'œil n'est presque jamais le plus brûlé. Vous voulez parier ? »
S1 [Youri] « La dune a le même indice qu'une zone brûlée. Alors, qu'est-ce qui la distingue ? »
   ⇒ la différence entre deux dates (dNBR) ; lien UN-SPIDER
V0 [Rose]  « "Presque en direct", c'est ce que dira le communiqué. Vous, vous signeriez quoi ? »
```

Volume à écrire, en suivant la règle « le même fait, trois angles » : une soixantaine de répliques
courtes, plus les accueils et les redirections.

---

## 5. Fil de réalisation proposé

| Étape | Contenu | Qui |
|---|---|---|
| R0 | Récupérer `saumos-seance.html` (voir § 7), en extraire les données et les images | Claude |
| R1 | Valider le graphe (§ 4), puis l'écrire en entier dans un fichier de données du cas (`donnees/saumos.json`), séparé du moteur | Claude, relecture Marc |
| R2 | Les têtes 8 bits : cinq experts, et une dizaine de têtes de héros au choix ; dessins originaux, aux couleurs de la charte | Claude, validation Marc |
| R3 | Le moteur de dialogue : choix de la posture et de la tête, portrait animé, réponse qui défile, indices, pistes, confiance du préfet | Claude |
| R4 | Les secours : la série Meteosat (déjà dans la séance), l'outil de mesure Sentinel-2 (déjà), l'animation Soleil-Terre-satellites pour Deimos (nouvelle) | Claude |
| R5 | Le rapport au propre, l'envoi à la feuille, la phrase collective et le barème sur 8 | Claude, barème Marc |
| R6 | La sévérité : trois points par groupe, les 60 points sur la projection | Claude (voir § 6, point 4) |
| R7 | Les diapos de la partie 4, dans l'ordre de la v1 annotée | Claude |
| R8 | Tests en navigateur, journal, puis relecture de Marc | Claude, puis Marc |

---

## 6. Commentaires de Claude

1. **Le radar dans les trois solutions.** La séance prépa ne contient aucune image radar. Soit on
   ajoute un couple Sentinel-1 avant / après sur Saumos (une donnée de plus à préparer), soit le radar
   reste une solution que Rose et Inès évoquent sans manipulation. Je pencherais pour la seconde en
   V1, et la première ensuite.
2. **Le pari des ETP.** Il faut une réponse de référence, même en ordre de grandeur, pour le verdict.
   Je n'en ai aucune source : c'est à toi de la fixer.
3. **Le barème sur 8** de l'échange n'est pas encore défini. Je propose huit items du rapport : la date
   de départ, la source de cette date, la surface, la date de l'image qui la donne, la résolution, les
   satellites et leurs orbites, les trois solutions au préfet, une limite juste.
4. **La sévérité à 60 points et l'affichage des paris** demandent un état partagé entre les écrans.
   C'est faisable avec la feuille Google, dans les deux sens : les groupes écrivent, la projection relit
   la feuille toutes les quelques secondes. Cela suppose que la feuille soit en place avant la séance.
5. **Deux cadences de Meteosat** coexistent dans les documents : « toutes les 15 minutes » (Bastien,
   ta réplique) et « toutes les 10 min » (fiche A). Les deux existent selon la génération de Meteosat ;
   il faut choisir celle des images de la séance (le suivi parle de Meteosat-12, de la nouvelle
   génération).
6. **Les têtes 8 bits** seront des dessins originaux : pas de personnages reconnaissables de jeux
   existants.
7. **Le temps.** 22 minutes d'enquête avec trois enquêtes en parallèle dans chaque groupe, c'est
   confortable. La sévérité en 5 minutes est serrée si chaque groupe pose ses trois points sur son écran
   et attend la révélation : à surveiller au premier test.

---

## 7. Données brutes nécessaires, telles qu'utilisées dans la séance

Le fichier `saumos-seance.html` n'est **pas** arrivé dans le dépôt : la règle `cours/**/*.html` du
`.gitignore` excluait tout HTML des cours, y compris dans `source/`. La règle est corrigée ; il suffit
de récupérer la mise à jour (`git pull`), puis de pousser le fichier à nouveau. En attendant, la liste
ci-dessous vient de la conception v3bis et du suivi ; je la confirmerai sur le HTML.

| Donnée | Rôle dans la séance | Caractéristiques connues |
|---|---|---|
| Sentinel-2 L2A, bande B8A, 21 juillet 2026 | avant le feu ; calcul du NBR | 20 m, même grille que le 4 septembre |
| Sentinel-2 L2A, bande B12, 21 juillet 2026 | avant le feu ; calcul du NBR | idem |
| Sentinel-2 L2A, bande B8A, 4 septembre 2026 | après le feu ; calcul du NBR | idem |
| Sentinel-2 L2A, bande B12, 4 septembre 2026 | après le feu ; calcul du NBR | idem |
| dNBR calculé sur ces bandes | sévérité ; les points de la classe | médian 0,654 dans le périmètre, 0,055 dehors |
| Composition « L2A SWIR » au 26 juillet | outil de mesure, référence d'environ 12 000 ha | à confirmer |
| Composition « L2A SWIR » au 4 septembre | outil de mesure, référence d'environ 25 000 ha | à confirmer |
| Périmètre officiel EMSR899 (délimitation du 29 juillet) | référence finale | 31 386 ha, tracé sur WorldView Legion à 1,2 m |
| Série Meteosat (secours de la station A) | défilement des images | 37 images, du 23 au 29 juillet, une toutes les 2 h ; ne couvre pas l'allumage du 22 |
| Série « Terra » (curseur du poste A dans la v3bis) | surface de détection au jour le jour | du 21 au 28 juillet ; chute de 177 à 21 km² le 27 (nuages) ; à confirmer |
| Visuel de l'EMSR899 (carte Copernicus EMS) | accroche et diapo 4.1 | à reprendre de la page EMSR899 |

**À ajouter pour le nouvel atelier**

- Les images « au propre » que tu as annoncées.
- Pour l'animation Deimos : rien, elle sera dessinée.
- Pour la solution radar, si on la manipule (commentaire 1) : un couple Sentinel-1 avant / après sur
  Saumos.
