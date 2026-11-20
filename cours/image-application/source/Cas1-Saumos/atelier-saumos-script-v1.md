# Atelier Saumos — script v1

Document de travail pour le cours « Image & Application ». Rien n'est codé tant que Marc n'a pas
donné son feu vert. Annoter, contredire, rayer directement dans ce fichier.

Point de départ : la séance Saumos (conception v3bis, suivi après version anglaise), qui tient en
45 minutes avec trois postes complémentaires. On ne la refait pas : on l'améliore sur deux points
demandés par Marc.

1. **Sortir de la démonstration** : chaque poste est accompagné par un expert, un personnage un peu
   drôle, qui aiguille sans jamais donner la réponse.
2. **Faire noter les résultats au propre** : la fiche de transmission devient un rapport de station,
   où chaque réponse porte sa preuve.

---

## 1. Ce qui change par rapport à la séance prépa

| | Séance prépa (v3bis) | Atelier Ing1 |
|---|---|---|
| Public | 18 étudiants de prépa, en visite | 60 Ing1, après photo-interprétation et la partie 2 du cours |
| Groupes | binômes, 3 postes | 20 groupes de 3 : 7 groupes par poste environ |
| Guidage | questions écrites | questions écrites + un expert par poste, indices à trois paliers |
| Trace | fiche à cocher | rapport de station : réponse + preuve + limite, envoyé à la feuille du cours |
| Sévérité | 3 points par binôme, 27 points | 3 points par groupe, 60 points sur la projection |
| Clôture | la phrase collective | la phrase collective, le verdict de Rose, la chaîne d'hexagones reconstituée |

Ce qui ne change pas : la question de départ, l'EMSR899, les trois postes, la phrase collective à
trous, la sévérité dNBR sur données réelles, le mode projection `#proj`.

---

## 2. Déroulé (45 minutes)

| Temps | Séquence | Qui | Ce qui se passe |
|---|---|---|---|
| 0–4′ | **La question** | tous | EMSR899, la dépêche, la question : « comment cartographie-t-on presque en direct un feu de forêt ? » Le pari : « dans combien de jours saura-t-on précisément ce qui a brûlé ? » Chaque groupe inscrit son pari. |
| 4–6′ | **Affectation** | tous | Numéro de groupe → poste (1, 4, 7… → A ; 2, 5, 8… → B ; 3, 6, 9… → C). L'expert du poste se présente en deux lignes. |
| 6–21′ | **L'enquête** | par poste | Questions du poste, sites externes (EUMETView, Copernicus Browser, Deimos), outil de mesure intégré pour B. L'expert répond aux questions du groupe ; les indices coûtent de la confiance (§ 4). |
| 21–27′ | **Le rapport au propre** | par poste | Chaque groupe remplit son rapport de station (§ 5), puis l'envoie. |
| 27–32′ | **L'échange** | plénière | Un groupe par poste lit son rapport ; la phrase collective se remplit sur la projection. Les autres groupes du même poste confirment ou contestent. |
| 32–40′ | **La sévérité** | tous | dNBR, la même image pour tous. Chaque groupe pose trois points (sévère, moyen, épargné), annonce son pronostic, puis l'appli révèle. Les 60 points s'accumulent sur la projection. |
| 40–45′ | **Le verdict** | plénière | Rose relit la phrase : « presque en direct », vrai pour quoi, faux pour quoi ? Retour sur les paris. La chaîne d'hexagones du feu se reconstitue à l'écran : c'est la chaîne qu'ils viennent de suivre. Clin d'œil au DM biosphère de l'an prochain. |

Si l'on déborde : l'échange se raccourcit (un rapport lu par poste, les autres s'affichent seuls),
comme dans la séance prépa.

---

## 3. Les experts

Un expert par poste, et Rose pour tout le monde à la fin. Ils ont un caractère, une manie, un
registre un peu drôle. Ils ne donnent **jamais** la réponse : ils disent où regarder, quoi comparer,
quelle question se poser.

| Poste | Expert | Caractère (à valider par Marc) |
|---|---|---|
| A, thermique | **Héloïse**, le signal | Physicienne. Parle des photons comme de témoins capricieux. |
| B, optique | **Bastien**, les données | Archiviste compulsif. Vexé quand on cherche une image sans regarder les dates. |
| C, orbites | **Youri**, l'orbitographe (nouveau ; nom à valider) | Ne pense qu'en tours de Terre. Calcule tout en orbites, même l'heure du déjeuner. |
| Sévérité | **Inès**, les traitements | Pince-sans-rire. Allergique aux seuils choisis « au feeling ». |
| Verdict | **Rose**, la contradictrice | Juriste, ancienne journaliste. Toujours la question qui gêne. |

### Exemples de répliques, pour fixer le ton (à reprendre ou rayer)

**Héloïse, poste A**
- Accueil : « Un satellite qui voit la Terre entière toutes les dix minutes, ça vous paraît trop beau ?
  Vous avez raison. Cherchez ce qu'il sacrifie. »
- Indice 1 : « Le feu, c'est chaud. Qu'est-ce qu'un capteur sensible à la chaleur peut voir que l'œil
  ne voit pas ? »
- Indice 2 : « Faites défiler les images une à une. Le premier point chaud, c'est quand ? »
- Indice 3 : « Comparez la taille d'un pixel à celle d'une commune. Vous pourriez tracer un contour,
  vous, avec des pixels pareils ? »

**Bastien, poste B**
- Accueil : « J'ai des images de cette forêt tous les cinq jours depuis des années. Enfin, quand il ne
  fait pas trop nuageux. Enfin, quand il ne fume pas. Bref, cherchez bien. »
- Indice 1 : « Une date avant, une date après. Commencez par l'avant : il n'y a rien à voir, et c'est
  justement pour ça qu'il compte. »
- Indice 2 : « Si la fumée vous gêne, essayez une composition qui ne regarde pas dans le visible. »
- Indice 3 : « Votre surface change entre deux dates ? Le feu a grandi, ou c'est votre image qui
  voyait moins bien ? »

**Youri, poste C**
- Accueil : « Rien ne passe au-dessus de Saumos par hasard. Tout est écrit dans l'orbite. Vous me
  donnez un nom de satellite, je vous dis quand il revient. Enfin, Deimos vous le dira. »
- Indice 1 : « Demandez aux groupes A et B le nom de leur satellite. Sans eux, vous calculez dans
  le vide. »
- Indice 2 : « Un satellite qui ne bouge pas par rapport à la Terre : à quelle altitude doit-il être ? »
- Indice 3 : « S'il repasse tous les cinq jours et qu'il fait nuageux ce jour-là, combien de temps
  attendez-vous ? »

**Inès, sévérité**
- « Le plus noir à l'œil n'est presque jamais le plus brûlé. Vous voulez parier ? Posez vos points. »
- « La dune a le même indice qu'une zone brûlée. Alors, qu'est-ce qui la distingue ? »

**Rose, verdict**
- « "Presque en direct", c'est ce que dira le communiqué. Vous, vous signeriez quoi ? »
- « Le préfet vous demande la surface demain matin. Vous lui donnez quel chiffre, et avec quelle marge ? »

---

## 4. Les indices et la confiance du préfet

- Chaque expert a, pour chaque question du poste, **trois paliers d'indice** : où regarder, quoi
  comparer, quelle question se poser. Jamais la réponse.
- Une **jauge de confiance du préfet** par groupe : elle monte avec chaque réponse justifiée du
  rapport, elle baisse légèrement à chaque indice demandé. Elle ne compte pas dans une note ; elle
  s'affiche dans le rapport envoyé, et sur la projection en fin de séance.
- Pour l'échange : le groupe le plus « fiable » de chaque poste lit son rapport. (Ou au hasard : à
  trancher par Marc.)

---

## 5. Le rapport de station (la trace au propre)

La fiche à cocher devient un rapport. Pour chaque réponse, trois champs :

- **la réponse** (date, valeur, choix) ;
- **la preuve** : ce que l'on a vu, et où (site, date de l'image, composition colorée) ;
- **la limite** : ce que cette réponse ne permet pas de dire.

Les questions sont celles de la séance prépa (fiches A, B et C), reprises telles quelles. Chaque
rapport se termine par la ligne déjà prévue « Ce que je ne peux pas dire », qui devient obligatoire.

Le rapport est envoyé à la feuille du cours (le même mécanisme que l'atelier actuel) et alimente
la phrase collective sur la projection.

---

## 6. Intégration au support de cours

Proposition : l'atelier Saumos **remplace** l'atelier des commandes dans la partie 4.

- 4.0 Intercalaire : « Le feu de Saumos ».
- 4.1 La question et le pari (EMSR899).
- 4.2 Les trois postes et leurs experts.
- 4.3 L'enquête : l'application Saumos, intégrée à la diapo, un onglet par poste.
- 4.4 Le rapport de station et l'envoi.
- 4.5 La phrase collective (mode projection).
- 4.6 La sévérité (dNBR, les points de la classe).
- 4.7 Le verdict : Rose, les paris, la chaîne d'hexagones du feu.

Les huit solutions de la partie 5 restent en support de cours. Les autres cas (deux faciles, deux
difficiles) viendront ensuite, sur le même modèle.

---

## 7. Questions ouvertes pour Marc

1. **Le HTML de la séance** (`saumos-seance.html`) n'est pas dans le dépôt : seuls la conception
   v3bis et le suivi y sont. Il contient les données (bandes B8A et B12, périmètre, série Meteosat).
   Il faut le pousser, avec les images « au propre » dont tu parles.
2. **Deux chronologies à réconcilier** dans les documents :
   - la conception v3bis donne la surface mesurée au **31 juillet** (B2) et le périmètre officiel
     tracé **le 29 juillet** sur WorldView Legion (T3) ;
   - le suivi donne les références de mesure au **26 juillet** (environ 12 000 ha) et au
     **4 septembre** (environ 25 000 ha), et 31 386 ha pour le périmètre du 29 juillet ;
   - l'accroche parlait de 42 000 ha (retirée pour garder le suspense).
   Quelle version fait foi ? Le suivi étant le plus récent, je partirais de lui.
3. **La conception v4** citée dans le suivi n'est pas dans le dépôt (seule la v3bis y est). Si elle
   existe, c'est elle qu'il faut reprendre.
4. **Sites externes avec 20 groupes** : le suivi signale le test réseau et le compte Copernicus
   comme risques. On garde les sites externes (c'est l'esprit de la séance), avec un secours intégré
   par poste ?
5. **Youri** : un cinquième personnage pour les orbites, ou Bastien prend aussi le poste C ?
