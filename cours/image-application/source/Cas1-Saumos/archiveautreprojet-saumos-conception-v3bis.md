# Séance Saumos — document de conception v2

Document de travail. Rien n'est codé tant que tu n'as pas donné le feu vert.
Annote directement, contredis, raye.

---

## 1. Constat Simple :
Le buyt est de faire découvrir le potentiel des images satellites à un groupe de 18 étudiants qui viennent découvrir Géodata Paris.
Ils doivent avant tout comprendre les principes très généraux (ce n'est pas un cours de Télédec)
Ils doivent degager de la finesse et de la complémentarité dans les données.
Découvrir aussi que l'image est souvent la matière brute, à partir desquelles on créée des cartes (souvent par de la vectorisation, interprétaiton, automatisme, etc..?)

Si possible on doit trouver une petite tensio ludique.
S'appuyer sur les sites existants ou ils vont pouvoir trouver les infos, tout simplement.

---

## 2. La question de la séance, et sa réponse

**Question affichée au départ :** comment fait-on pour cartographier presque en direct un feu de forêt ?

Je présente à ce moment là l'EMSR899

https://mapping.emergency.copernicus.eu/activations/EMSR899/reporting/

En présentant les cartes, je pose la question suivante :

**Question affichée au départ :** comment fait-on pour cartographier presque en direct un feu de forêt ?

On va voir que c'est lié à différents capteurs. ChAQUE groupe de 2 va choisir un capteur, pour que nous puissons à la fin croiser vos infos :

**Réponse que la classe doit produire**, en trois morceaux, un par poste. C'est le livrable
unique de la séance, il s'affiche sur ta projection et se remplit sous leurs yeux :

> Le feu de Saumos a été repéré le **[A1]**, par des capteurs qui repassent **[A2]** mais ne
> voient qu'à **[A3]**. Sa surface totale — **[B1] hectares** — n'a pu être mesurée qu'à partir du> **[B2]**, avec une image à **[B3]** de résolution spatiale.
> La sévérité des dégâts a demandé **[T1]** de plus, parce
> qu'il fallait **[T2]**, et le périmètre officiel a finalement été tracé sur **[T3]**.

Neuf trous. Trois par poste. Chaque poste ne peut remplir que les siens.

On parallélise donc les 3 groupes.

À la fin, on relit la phrase entière : « presque en direct » est vrai pour la première partie,
faux pour la deuxième, et la troisième explique pourquoi.

=> Les réponses attendues
A1 : le 22 juillet à 11 heure,
A2 :  en permanence
A3 mais ne voient qu'à faible résolution spatiale.

Sa surface totale 
B1 : XXX
B2 : 31 juillet
B3 : avec une image à haute résolution, c'est à dire 20m

T1 : Six semaines de plus
22 : une image vierge de nuage
T3 : plus tôt le 29 juillet grâce à une commande de WorldViewLegion

## 3. Les trois postes

Plus de secteurs. Trois postes, trois binômes chacun, un objectif d'une ligne.

Pour le Poste A, on va commencer par EUMETSAT, On leur fait répondre :

>Rendez- vous sur le site suivant : 
>https://view.eumetsat.int/productviewer?v=default
>En laissant les paramètres par défaut, observer le feu,
>Quand est-il possible de le voir démarrer? S'éteindre?
>Est-il facilement possible de délimiter l'emprise du feu?
>Ce satellite MeteoSat voit-il le sol la nuit?
>Pour connaitre son orbite demande au groupe C


Pour le Poste B, on va s'appuyer sur Sentinel2-MSI

>Rendez-vous sur le site suivant :
>https://browser.dataspace.copernicus.eu/
>Choisissez le donnée satellite de Sentinel2-L2A
>Quelle date permet de voir toute la zone intacte avant le feu?
>Après le feu?
>Il y en a t-il pendant le feu?
>Si oui quelle composition colorée permet de voir au mieux les dégats?
>Quelle est sa surface au 26 Juillet?
>ET au 4 Septembre juillet?
> Voir avec le groupe C si cela est lié aux orbites des Satellites Sentinel2.

On intègre là un outil de mesure sur ces 2 images, on coche la date, la compostion est celle de L2ASWIR, tu as déjà les données.


Pour le poste C, ils ne vont que s'occuper des orbites en supports des A et B.

Enfin quelle est son orbite ?
>Pour comprendre les caractéristiques des satellites, il faut connaitre leurs orbites.
>Pour répondre à cette question, se rendre sur : https://deimos.ign.fr/
>Demandez au groupe A et B le nom de leur satellite. Trouver leur trajectoire pour les aider à comprendre les caractéristiques d'acquisition.


Pour Tous ?

>On se propose de faire maintenant un analyse des dégats opérés par le feu, avec une résolution terrain inférieure à 50m. Quelles dates et quels capteurs sont pertinents (réponse attendues du groupe B)

>Quelles seraient selon vous les dégats visible sur cette image (on reprend ton vote)

>En appliquant la méthodologie de Spider, jointe ici : https://un-spider.org/advisory-support/recommended-practices/recommended-practice-burn-severity/in-detail/normalized-burn-ratio

Voilà ce qu'on obient :

Carte PIR (B8A), puis SWIR (B12), puis Dnbr. On clique sur les différentes images. On applique strictement la légende de spider que l'on met dans l'image du DNBR


---

## 4. La fiche de transmission

C'est le remplacement de la case de texte libre, et c'est le point le plus important du document.

On reprend les qeustions soulevées et ils cochent tous ensemble en s'aidant. 

### Fiche A — Thermique

- Première détection du feu : le `____`
- Ces capteurs repassent : ☐ toutes les 10 min ☐ plusieurs fois par jour ☐ tous les 5 jours
- Ils voient à : ☐ 20 m ☐ 375 m à 1 km ☐ 3 km
- Le 27 juillet les détections chutent de 177 à 21 km². Cause :
  ☐ le feu est éteint ☐ les nuages bloquent la mesure
- **Ce que je ne peux pas dire :** combien d'hectares ont brûlé.

### Fiche B — Optique

- Surface que j'ai mesurée : `____` hectares
- Date de l'image utilisée : `____`
- Résolution de cette image : `____`
- Part du périmètre que je n'ai pas pu tracer, à cause des nuages : `____` %
- **Ce que je ne peux pas dire :** à quelle heure le feu a démarré, ni où il en est aujourd'hui.

### Fiche C — Orbites

- Premier Sentinel-2 vraiment exploitable : le `____`, soit `____` jours après le départ
- Image propre nécessaire au calcul de sévérité : le `____`
- Capteur qui a réellement servi à tracer le périmètre officiel : `____`
- Pourquoi lui : ☐ il voit à travers les nuages ☐ il peut être pointé à la demande
- **Ce que je ne peux pas dire :** ce que ces images montreront.

Chaque champ rempli alimente automatiquement un trou de la phrase collective. Sur ta projection,
la phrase se complète mot par mot pendant qu'ils lisent leur fiche à voix haute.

---

## 5. Traitement des images

Trois règles, à tenir partout.

**Une image par écran, pleine largeur.** Minimum 900 px. Jamais deux vignettes côte à côte pour
faire une comparaison.

**Les comparaisons se font par superposition, pas par juxtaposition.** Un curseur avant/après,
ou une bascule à un clic entre deux dates. On voit le changement au même endroit de l'écran,
c'est ça qui fait comprendre.

**La série Terra se parcourt.** Un curseur de date, du 21 au 28 juillet, que le poste A fait
glisser. La date et la surface de détection s'affichent en dessous. C'est l'action principale du
poste A, et elle est physique.

---

## 6. Déroulé et minutage

| Temps | Séquence | Qui | Ce qui se passe |
|---|---|---|---|
| 0–3′ | **La question** | tous | Photo, dépêche, la question de la séance. Le pari : « dans combien de jours saura-t-on précisément ce qui a brûlé ? » |
| 3–4′ | **Affectation** | tous | Numéro de binôme → poste. Une phrase d'objectif, rien d'autre. |
| 4–12′ | **Les trois postes** | séparés | 3 écrans par poste : question / manipulation / fiche. |
| 12–16′ | **L'échange** | plénière | Chaque poste lit sa fiche. La phrase collective se remplit sur ta projection. |
| 16–22′ | **La sévérité** | tous | dNBR. Tout le monde, sur la même image. |
| 22–26′ | **Le verdict** | plénière | Les trois délais, retour sur le pari, empreinte réelle du pixel. |

26 minutes. Si tu débordes, c'est l'échange qui se raccourcit : deux fiches lues au lieu de trois,
la troisième s'affiche seule.

---

## 7. La sévérité, sans secteurs

Tout le monde travaille sur la même image, la zone brûlée entière.

Chaque binôme désigne **trois points** : un qu'il juge sévèrement brûlé, un moyen, un épargné.
Il annonce son pronostic, puis l'appli révèle les réflectances B8A et B12 et calcule.

Sur ta projection, les **27 points de la classe** s'accumulent, colorés par leur classe de
sévérité. Le motif de la cicatrice apparaît sans qu'on ait eu besoin de découper quoi que ce soit.

L'enseignement reste le même : la zone la plus noire à l'œil n'est presque jamais la plus sévère,
et le sable de la dune a le même NBR qu'une zone brûlée — c'est la différence entre deux dates
qui l'élimine.


## 8. Dépendances ouvertes

1. ~~**Bandes brutes B8A et B12 du 21 juillet.**~~ **Reçues et intégrées.** Même grille, même
   origine, même pas de pixel que le 4 septembre : aucun rééchantillonnage nécessaire. Le dNBR
   porte désormais sur de vraies réflectances aux deux dates. Le bandeau d'avertissement saute.
2. **Ton adresse mail** pour le bouton d'envoi du rapport.

