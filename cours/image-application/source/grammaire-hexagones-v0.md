# Image Application — grammaire des hexagones

> Document de travail, v0 du 17 novembre 2026. À déposer dans `cours/image-application/source/`.
> On est au stade du plan : rien n'est encore figé, rien n'est produit.
> Les mentions **[à vérifier]** signalent un fait non encore confirmé par une source.

---

## 0. Décisions actées

| Sujet | Décision |
|---|---|
| Débat « qui a le droit de regarder ? » | Supprimé comme bloc. Il devient un **quatrième personnage**, le contradicteur, dans l'atelier. Les 10 min libérées vont à l'atelier. |
| Les verbes | Rangés par **niveau d'inférence**. *Cartographier* n'est plus un verbe : c'est la forme de sortie, transversale. |
| Partie 2 « Qu'est-ce que voir ? » | Un objectif (ex. « suivre l'évolution quotidienne d'un phénomène ») et **4 curseurs centrés sur 0** (spatiale, temporelle, spectrale, radiométrique). Monter un curseur en fait baisser un autre : on découvre le pourquoi du compromis. |
| Vote sur les cas d'usage | Liste des cas proposés par Marc, plus des vrais inattendus (vent à la surface de Mars) et des faux. Vote oui / non / pas sûr. *Place dans le cours à confirmer : en remplacement de la liste de l'accroche ?* |
| Jeu sérieux | **7 commandes**, une par type de donnée. Les 7 corrigés servent de support de cours. |
| Personnages | Dialogues scénarisés à choix (esprit Ink), pas de LLM. |
| Trace écrite | Envoi vers une **Google Sheet** (script Apps Script) depuis la page GitHub. |

---

## 1. Inventaire des hexagones (tout ce qui est pertinent, avant tri)

Cinq familles. Chaque hexagone porte un nom court, une phrase « ce que c'est », une phrase « ce que ça permet », **sans exemple**.

### Famille A — Les verbes (ce que veut le client)

Du plus direct au plus inféré :

| Verbe | Ce que le client demande |
|---|---|
| **Mesurer** | une grandeur physique (température, hauteur, déplacement) |
| **Détecter** | la présence ou l'absence d'un objet ou d'un événement |
| **Classer** | ranger chaque lieu dans une catégorie |
| **Suivre** | ce qui change entre deux dates ou plus |
| **Estimer** | une grandeur qu'on ne voit pas, déduite d'une autre (volume, biomasse, débit) |
| **Modéliser / prévoir** | ce qui va se passer, ou ce qui se passe hors de la vue |

*Cartographier* : la forme de sortie, le cadre du plateau (pas un hexagone).

### Famille B — Les signaux (ce que le monde renvoie au capteur)

| Signal | Axe | Ce qu'il révèle |
|---|---|---|
| Réflectance visible | spectral | couleur, ce que l'œil voit |
| Proche infrarouge | spectral | végétation vivante |
| Infrarouge moyen (SWIR) | spectral | eau des feuilles et des sols, brûlis, minéraux |
| Émission thermique | spectral | température de surface |
| Absorption atmosphérique | spectral | gaz (méthane, NO₂, ozone) |
| Lumière nocturne émise | spectral | activité humaine, éclairage |
| Rétrodiffusion radar (amplitude) | spatial | rugosité, structure, eau libre, métal ; de jour comme de nuit, à travers les nuages |
| Phase radar | 3D | déplacement du sol au millimètre |
| Temps de retour laser (LiDAR) | 3D | hauteur, sol sous la végétation |
| Temps de retour radar (altimétrie) | 3D | hauteur de la mer, des glaces |

### Famille C — Les données (les capteurs), avec leurs 4 résolutions

Ordres de grandeur ; carte au dos avec spatiale / temporelle / spectrale / radiométrique.

| Donnée | Spatiale | Temporelle | Spectrale | Remarque |
|---|---|---|---|---|
| Optique multispectrale « libre » (Sentinel-2, Landsat) | 10 à 30 m | 5 à 16 jours | 10 à 13 bandes | gratuite ; nuages |
| Optique très haute résolution (Pléiades, Pléiades Neo) | 0,3 à 0,5 m | sur commande | 4 à 6 bandes | payante ; programmable |
| Orthophoto aérienne (IGN) | 0,2 m | tous les 3 ans environ **[à vérifier]** | 3 à 4 bandes | |
| Thermique (Landsat TIRS, ECOSTRESS) | 70 à 100 m | jours | 1 à 2 bandes | heure de passage imposée |
| Radar SAR (Sentinel-1, RadarSat) | 5 à 50 m | 6 à 12 jours | 1 fréquence, polarisations | jour/nuit, nuages |
| Interférométrie (séries Sentinel-1, service EGMS) | ~10 m | 6 jours | phase | précision millimétrique |
| LiDAR aérien (LiDAR HD IGN) | 10 points/m² environ **[à vérifier]** | une campagne | — | nuage de points classé |
| Altimètre (Sentinel-3) | km | jours | — | fait pour la mer |
| Spectromètre atmosphérique (Sentinel-5P) | quelques km | quotidien | centaines de bandes | gaz |
| Nocturne (VIIRS) | 375 à 750 m | quotidien | 1 bande | |
| Drone | cm | à la demande | variable | petite zone |
| **Hors image** : terrain, données exogènes (cadastre, déclarations, cartes d'aléa), modèles (météo, dérive) | | | | indispensables, souvent oubliées |

### Famille D — Les opérations (par étape de la chaîne)

**B** = carte de base, visible dès le départ. **F** = carte fine, débloquée par un personnage.

**D1. Acquérir**

| Opération | Niveau |
|---|---|
| Choisir la donnée existante (catalogue, archive) | B |
| Programmer une acquisition | F |
| Choisir les dates (saison, nuages, heure de passage) | F |
| Constituer une série temporelle | B |
| Relever le terrain (vérité terrain, placettes) | B |

**D2. Préparer (prétraitements)**

| Opération | Niveau |
|---|---|
| Étalonner, calibrer le signal | B |
| Corriger l'atmosphère | F |
| Orthorectifier | F |
| Recaler deux images entre elles | F |
| Masquer nuages et ombres | F |
| Filtrer le chatoiement radar | F |
| Mosaïquer, rééchantillonner | F |

*En base, D2 peut se réduire à une seule carte « Préparer », que le spécialiste des données décompose.*

**D3. Dériver (créer une primitive)**

| Opération | Axe | Niveau |
|---|---|---|
| Composition colorée | spectral | B |
| Indice spectral (combiner des bandes) | spectral | B |
| Différence ou rapport entre dates | temporel | B |
| Texture | spatial | F |
| Analyse en composantes principales | spectral | F |
| Interférogramme | 3D | F |
| Modèle de hauteur (MNS − MNT) | 3D | B |
| Température de surface (émissivité) | spectral | F |

**D4. Analyser, extraire**

| Opération | Niveau |
|---|---|
| Photo-interprétation | B |
| Seuillage | B |
| Segmentation (découper en objets) | F |
| Classification supervisée | B |
| Classification non supervisée | F |
| Créer des données d'apprentissage | B (lien avec le cours Image Intelligence) |
| Apprentissage profond (détection d'objets) | B |
| Détection de changement | B |
| Analyse de série temporelle (tendance, rupture) | F |
| Statistiques zonales, comptage | F |
| Modèle empirique (régression) | F |
| Modèle physique (inversion) | F |
| Croiser avec des données exogènes (SIG) | B |

**D5. Valider**

| Opération | Niveau |
|---|---|
| Comparer au terrain ou à une référence | B |
| Matrice de confusion, taux d'erreur | F |
| Estimer l'incertitude | F |
| Contrôle humain des détections | B |

**D6. Restituer**

| Opération | Niveau |
|---|---|
| Carte (sémiologie) | B |
| Alerte, notification | F |
| Indicateur, tableau de bord | F |

### Famille E — Les résultats

Un hexagone de sortie par commande : le livrable attendu par le client (une carte, une alerte, un chiffre, une zone d'exclusion…).

---

## 2. Grammaire (règles d'assemblage)

1. **La chaîne type** : Commande → Verbe → Signal → Donnée → Préparer → Dériver → Analyser → Valider → Résultat.
2. **Adjacence** : un hexagone doit toucher au moins un hexagone de l'étape précédente. La géométrie hexagonale permet les **branches** (deux données qui fusionnent) et les **raccourcis** (photo-interprétation directe, sans primitive).
3. **Étapes facultatives** : D3 (Dériver) peut être sautée ; D5 (Valider) ne l'est jamais. Une chaîne sans validation est refusée par le contradicteur.
4. **Granularité à deux niveaux** : environ 20 cartes de base au départ. Un personnage peut « ouvrir » une carte de base en cartes fines. *L'exemple type : le spécialiste des données dit « Préparer, oui, mais quoi ? » et la carte se scinde en 3.* Les étudiants découvrent ainsi la profondeur sans être noyés au départ.
5. **Les axes** : chaque primitive porte une couleur d'axe (spectral, temporel, spatial, 3D), en écho aux 4 curseurs de la partie 2.
6. **Correction** : pour chaque commande, trois listes.
   - **Indispensables** : sans eux la chaîne ne marche pas.
   - **Acceptables** : alternatives valides.
   - **Pièges** : cartes plausibles mais fausses, signalées par un personnage.

### Les personnages

| Personnage | Rôle | Pépite type |
|---|---|---|
| Le spécialiste du signal | ce que la physique permet ou interdit | « Ce capteur ne mesure pas ce que tu crois mesurer. » |
| Le spécialiste des données | catalogue, résolutions, coûts, dates | « La meilleure donnée est celle qui existe déjà. » |
| Le spécialiste des traitements | prétraitements, méthodes, validation | « Sans terrain, ton modèle ne vaut rien. » |
| Le contradicteur (juriste / journaliste) | recevabilité, preuve, droit de savoir | « Ton résultat tiendrait-il devant un juge ? » |

---

## 3. Les 7 commandes

Couverture visée : chaque type de donnée une fois, chaque verbe au moins une fois.

| # | Donnée | Client | Verbe principal |
|---|---|---|---|
| 1 | LiDAR | Gestionnaire forestier | Estimer |
| 2 | Optique THR (aérien) | Administration fiscale | Détecter |
| 3 | Multispectral SWIR | Préfet ou assureur | Classer |
| 4 | Thermique | Maire d'une grande ville | Mesurer (et le piège de la mesure) |
| 5 | Radar SAR | Direction de course au large | Détecter, suivre, prévoir |
| 6 | Interférométrie | Assureur | Mesurer, suivre |
| 7 | Atmosphère | ONG ou journaliste | Détecter, estimer |

### 1 — LiDAR : « Quel volume de bois sur pied dans ce massif ? »

- **Client** : gestionnaire forestier (ONF, forêt publique).
- **Chaîne attendue** : temps de retour laser → LiDAR HD IGN (nuage classé) → MNT et MNS → modèle de hauteur (MNH) → placettes de calibration sur le terrain → modèle empirique hauteur → volume → carte.
- **Pièges** : croire que le LiDAR mesure le volume. Il mesure une hauteur ; le volume vient du terrain et du modèle.
- **Pépite** : la valeur du LiDAR forestier est maximale avec des placettes terrain synchrones avec le vol.
- **Cas réel** : chaîne LiDAR de l'ONF avec placettes de calibration (journée CRIG Occitanie, nov. 2023) ; produit MNH LiDAR HD de l'IGN (différence MNS − MNT).

### 2 — Optique THR : « Quelles piscines ne sont pas déclarées ? »

- **Client** : administration fiscale.
- **Chaîne attendue** : réflectance visible → orthophotos IGN → données d'apprentissage → apprentissage profond (détection d'objets) → croisement avec le cadastre et les déclarations → contrôle humain → alerte au service local.
- **Pièges** : piscines hors-sol ou bâchées, faux positifs, date de prise de vue ancienne.
- **Pépite** : l'IA ne décide pas, elle pré-alerte ; un humain contrôle. C'est le pont direct avec le cours Image Intelligence (données d'apprentissage, contrôle par l'interprète).
- **Contradicteur** : surveillance généralisée des jardins ? Droit à l'erreur du contribuable ?
- **Cas réel** : « Foncier innovant » (DGFiP, avec Capgemini et Google). Expérimentation sur 9 départements, 20 000 piscines en 2022, généralisation en 2023, 140 000 piscines détectées au total. Extension en cours aux vérandas et abris de jardin.

### 3 — SWIR : « Quelle surface a brûlé, et avec quelle sévérité ? »

- **Client** : préfet (après un grand feu) ou assureur.
- **Chaîne attendue** : SWIR et proche infrarouge → Sentinel-2 avant et après → masque nuages et fumée → indice de brûlis (NBR) avant et après → différence (dNBR) → classes de sévérité → validation (terrain ou THR) → carte.
- **Pièges** : la fumée, les ombres de relief, la repousse si l'image « après » est trop tardive.
- **Pépite** : c'est la différence entre deux dates qui parle, pas une image seule.
- **Cas réel** : cartographie rapide Copernicus EMS ou EFFIS **[à vérifier, choisir un feu précis]**.
- **Alternative** : crise phytosanitaire (scolytes), détection précoce par Sentinel-2.

### 4 — Thermique : « Où sont les îlots de chaleur, rue par rue ? »

- **Client** : maire d'une grande ville, en vue d'un plan canicule.
- **Chaîne naïve** : émission thermique → Landsat → température de surface → carte.
- **Pièges, c'est le cœur de cette commande** :
  - la résolution thermique satellite (90 à 100 m) ne descend pas à la rue ;
  - la **température de surface n'est pas la température de l'air** ;
  - l'heure de passage est en journée, alors que l'îlot de chaleur nocturne est celui qui pèse sur la santé.
- **Chaîne corrigée** : satellite pour le repérage à l'échelle du quartier, plus capteurs au sol, thermographie aérienne nocturne ou modélisation.
- **Pépite** : savoir dire au client « pas comme ça ». C'est la commande où la bonne réponse contient un refus partiel, et elle relie directement aux curseurs de la partie 2.
- **Cas réels** :
  - la carte de l'APUR (nuit du 25 au 26 juillet 2019, températures de l'air) ;
  - le projet Santé publique France sur la canicule de 2003 (images thermiques NOAA-AVHRR) ;
  - le LNE juge la thermographie satellite insuffisante pour identifier les îlots de chaleur.

### 5 — Radar SAR : « Où sont les icebergs sur la route des skippers ? »

- **Client** : direction de course du Vendée Globe.
- **Chaîne attendue** :
  - altimétrie pour les gros icebergs ;
  - images radar Sentinel-1 programmées sur les zones critiques (mode large fauchée, ~50 m) pour les plus petits ;
  - modèle de dérive ;
  - zone d'exclusion Antarctique (ZEA).
- **Pièges** : la mer formée et les bateaux donnent de faux échos ; les petits blocs passent sous la résolution. C'est le compromis fauchée / résolution de la partie 2.
- **Pépite** : la détection d'icebergs est une application d'opportunité de l'altimétrie, une donnée faite pour autre chose. La réutilisation est un réflexe de métier.
- **Cas réel** : CLS, filiale du CNES, fournisseur officiel des données de glace du Vendée Globe depuis 2008.
  - En 2020, une vingtaine d'icebergs douteux vers Crozet et Kerguelen ont fait remonter la ZEA de 5° vers le nord.
  - En janvier 2025, des icebergs ont été confirmés hors de la ZEA.

### 6 — Interférométrie : « Ces maisons fissurées bougent-elles à cause des argiles ? »

- **Client** : assureur, face aux sinistres sécheresse (retrait-gonflement des argiles).
- **Chaîne attendue** : phase radar → séries Sentinel-1 → interférométrie (points persistants) → séries de déplacement → croisement avec la carte d'aléa argiles, le bâti et les épisodes de sécheresse → évaluation.
- **Pièges** :
  - le déplacement est mesuré selon la ligne de visée du satellite ;
  - les mesures n'ont de sens que relativement à un point de référence ;
  - on n'obtient des points que sur des structures stables ;
  - il ne faut pas confondre le cycle saisonnier et la tendance.
- **Pépite** : un service gratuit existe déjà à l'échelle de l'Europe. Commencer par chercher le produit avant de le fabriquer.
- **Cas réel** : le service européen EGMS (Copernicus), qui mesure les mouvements du sol au millimètre à partir de Sentinel-1, avec une série temporelle par point. Des projets InSAR + IA sur les argiles existent **[à vérifier, en choisir un]**.
- **Alternative** : chantiers du Grand Paris Express **[à vérifier]**.

### 7 — Atmosphère : « Qui relâche ces panaches de méthane ? »

- **Client** : ONG ou journaliste d'investigation.
- **Chaîne attendue** :
  - absorption atmosphérique → Sentinel-5P (couverture quotidienne, grossière) pour **détecter** les très gros panaches ;
  - satellites à plus haute résolution (Sentinel-2, PRISMA…) pour **attribuer** la source ;
  - estimation du débit ;
  - notification.
- **Pièges** : le vent déplace le panache ; les nuages ; un satellite à maille de plusieurs km ne désigne pas une installation.
- **Pépite** : un capteur grossier pour chercher, un capteur fin pour désigner. C'est un enchaînement de données, pas une seule.
- **Contradicteur** : le système de l'ONU notifie d'abord gouvernements et entreprises, et ne rend les données publiques que 45 à 75 jours après la détection. Qui a le droit de savoir, et quand ?
- **Cas réel** : MARS (Methane Alert and Response System), PNUE / IMEO.
- **Alternative** : le NO₂ et l'arrêt des usines chinoises pendant le Covid.

### En réserve — une 8ᵉ commande de fusion

- **Contrôle PAC par suivi** : optique et radar en séries temporelles. **[à vérifier]**

---

## 4. Points à trancher

1. Granularité à deux niveaux (base / fine, débloquée par les personnages) : on garde ?
2. Le vote vrai / faux des cas d'usage : il remplace la liste de l'accroche, ou il vient en partie 3 ?
3. Correction : score automatique (indispensables / pièges) ou seulement le corrigé visuel ?
4. Nombre de groupes en séance : une commande par groupe, ou deux groupes sur la même commande pour comparer les chaînes ?
5. Cas déjà utilisés dans Image Intelligence (bases russes, Angkor, radar de Baltimore, FLAIR) : exclus des 7 commandes pour éviter les redites ; ils peuvent rester dans le vote.

---

## Sources consultées

- CNES, « Vendée Globe : des icebergs sous étroite surveillance grâce aux satellites », 20 janvier 2025.
- ESA, « Copernicus satellites keep eyes on icebergs for Vendée Globe », 2020.
- Figaro Nautisme, « Zone d'Exclusion Antarctique », 2020.
- impots.gouv.fr, « Généralisation du Foncier innovant », 2 juin 2023 ; bilans relayés par la presse (140 000 piscines).
- ONF, « Le LiDAR HD au service de la forêt », journée CRIG Occitanie, 16 novembre 2023.
- data.gouv.fr, « MNH LiDAR HD IGN ».
- Copernicus Land Monitoring Service, « European Ground Motion Service ».
- PNUE, « About the Methane Alert and Response System (MARS) » et entretien avec M. Caltagirone, août 2023.
- LNE, fiche « Îlots de chaleur urbains ».
- Paris.fr, « Canicule : visualisez les écarts de température » (carte APUR, 2019).
- Santé publique France, « Évolution climatique et canicule en milieu urbain ».
