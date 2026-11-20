# Séance Saumos — fichier de suivi

Dernière mise à jour après livraison de la version anglaise.

---

## 1. Fichiers de référence

| Fichier | Rôle |
|---|---|
| `saumos-seance.html` | **Version française de référence.** Intègre tes reprises de texte. C'est la base de toute modification ultérieure. |
| `saumos-session-EN.html` | Version anglaise, traduite depuis la référence française. Même code, mêmes données, mêmes images. |
| `saumos-conception-v4.md` | Document de conception. Décrit le déroulé, les postes, les réponses attendues. |
| `saumos-suivi.md` | Ce fichier. |

Les deux applications sont autonomes : un seul fichier HTML, aucune dépendance réseau pour fonctionner, images incluses. 4,4 Mo chacune.

---

## 2. État de la séance

Trois groupes, trois stations, 25 minutes.

| Station | Satellite | Site externe | Produit |
|---|---|---|---|
| A | Meteosat-12 / FCI | EUMETView | date et heure de départ, cadence, résolution |
| B | Sentinel-2 / MSI | Copernicus Browser | surface mesurée, date, résolution |
| C | — | Deimos (IGN) | altitude, type d'orbite, période de revisite |

La séance produit une phrase collective à douze trous : neuf remplis par les groupes, trois révélés par l'enseignant en clôture.

**Ordre verrouillé.** L'analyse de sévérité (dNBR) n'est atteignable qu'après transmission de la fiche. Elle est annoncée comme bonus, et un bouton permet de produire le rapport sans elle.

---

## 3. Données intégrées

- **Sentinel-2 L2A**, bandes brutes B8A et B12 aux deux dates : 21 juillet 2026 (pré-feu) et 4 septembre 2026 (post-feu), 20 m, même grille, aucun rééchantillonnage.
- **dNBR réel** calculé sur ces bandes : médian 0,654 dans le périmètre officiel, 0,055 à l'extérieur. Répartition : 48,5 % sévérité élevée, 40,5 % modérée-haute, 8,6 % modérée-basse.
- **Périmètre officiel EMSR899**, délimitation du 29 juillet : 31 386 ha, tracé sur imagerie WorldView Legion à 1,2 m.
- **Références de surface** pour l'outil de mesure : environ 12 000 ha au 26 juillet, 25 000 ha au 4 septembre.
- **Secours Meteosat** : 37 images, 23 au 29 juillet, une toutes les deux heures. Ne couvre pas l'allumage du 22.

---

## 4. Modes et raccourcis

- Ouverture normale : parcours étudiant.
- `#proj` à la fin de l'URL : écran de projection enseignant. Neuf blancs saisissables, trois boutons de révélation, bouton d'effacement.

---

## 5. Reste à faire

1. **Adresse mail.** Remplacer `prenom.nom@etablissement.fr` dans les deux fichiers. C'est la seule chaîne à modifier.
2. **URL EUMETView préparée.** Le lien pointe aujourd'hui sur le viewer par défaut. Avec une URL portant la date et l'emprise, la station A gagne une à deux minutes.
3. **Test réseau en salle.** Les trois stations dépendent de sites externes. Seule la station B fonctionne entièrement hors ligne, grâce à l'outil de mesure intégré.
4. **Vérifier que Deimos référence Meteosat-12.** Les images de juillet 2026 viennent de MTG-I1, exploité sous ce nom. Si seul un Meteosat plus ancien est listé, la réponse sur l'orbite reste valable : tout Meteosat est géostationnaire à 36 000 km.
5. **Compte Copernicus Browser.** À tester en navigation privée : la recherche par date peut en demander un.

---

## 6. Journal

- **v1** — application autonome hébergeant tout le contenu. Abandonnée : trop d'exposition, pas assez d'investigation, transmission non outillée.
- **v2 à v4** — refonte autour des sites externes et de la phrase collective. Passage de neuf secteurs à trois groupes.
- **Correctifs** — validation de la fiche B (champ pré-rempli non enregistré), export PDF (isolation du rapport à l'impression), références en liens cliquables dont la page EMSR899.
- **Reprises de texte** par toi : accroche sans le chiffre de 42 000 ha pour garder le suspens, introduction sur les vecteurs d'acquisition et l'orbite, consigne d'échange entre stations A et C.
- **Version anglaise** — traduction intégrale de l'interface, des questions, des fiches, de la phrase collective et du rapport. Formats de nombre et de date en `en-GB`. Les noms de capteurs, dates de données, URLs et valeurs numériques sont inchangés.
