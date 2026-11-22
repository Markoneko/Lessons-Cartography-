# Atelier Saumos — les dialogues, tels que le jeu les joue

Fichier produit par `outils/dialogues.py` à partir de `donnees/saumos.json` : ne pas le modifier à la main,
modifier le JSON puis relancer. ▶ question, ✦ aparté, ✎ réponse tapée, ◆ choix ; *effets* en italique, `conditions` en code.

## Enquête A — Quand le feu a-t-il démarré ?

Jouée par **le rapporteur** ; labo : Labo Eumetsat.

### Elikia (Le signal)

**Accueil.** Bonjour ! Rose m'a prévenue : si vous êtes là, c'est que vous cherchez à détecter quelque chose dans une image, je me trompe ? Quel phénomène vous intéresse donc ?
- ◆ *« La fumée. »* → Bon instinct. Au tout début, la chaleur tient dans quelques mètres carrés : vue de très loin, elle se noie dans un pixel de plusieurs kilomètres, sauf pour des canaux faits exprès. La fumée, elle, monte vite et s'étale : sur des images en couleurs naturelles, on la voit avant les flammes. — *carnet : Le signal du départ*
- ◆ *« La chaleur. »* → Ah, la chaleur… Au départ, il n'y en a pas beaucoup, et elle tient dans quelques mètres carrés : vue de très loin, elle se noie dans un pixel de plusieurs kilomètres. Je privilégierais la fumée : elle monte vite et s'étale ; sur des images en couleurs naturelles, on la voit avant les flammes. — *carnet : Le signal du départ*
- ◆ *« Autre chose : l'odeur ? »* → Les satellites n'ont pas de nez. Pas encore. Je vous propose la fumée : au départ, peu de chaleur visible de loin, mais la fumée monte vite et s'étale. — *carnet : Le signal du départ*

**A-E1** ▶ *« Et pour voir cette fumée, quel signal regarder ? »*  
Quel signal serait pertinent, à votre avis ? Oui, là, on parle de photons.
- ◆ *« La lumière du Soleil renvoyée par la fumée, dans le visible. »* ✓ → Oui ! La fumée diffuse la lumière du Soleil : elle se voit dans le visible. Retenez la conséquence : de jour seulement. — *carnet : Voir la fumée*
- ◆ *« Le rayonnement thermique émis par la fumée. »* ✗ → La fumée émet peu dans l'infrarouge thermique ; à ces longueurs d'onde, elle est même presque transparente. Elle, elle diffuse ce qu'elle reçoit. De qui ?
- ◆ *« Les ondes radio. »* ✗ → Ça, c'est le domaine du radar, et il voit à travers la fumée : l'inverse de ce que vous cherchez !

**A-E2** ▶ *« Alors, quel satellite ? »* `si entendu A-E1 ; sauf si carnet La bonne résolution ou clef a`  
Un signal, c'est la moitié du chemin. L'autre moitié, c'est la donnée : à quelle cadence faut-il une image pour saisir un départ ? Bastien adore cette question.

**A-E3** ▶ *« Un signal visible, une image très souvent : quel satellite ? »* `si entendu A-E1 et carnet La bonne résolution ; sauf si clef a`  
Un satellite de la famille des Meteosat, ou Terra, peut répondre à vos besoins. Voyez avec votre orbitographe comment connaître leurs caractéristiques. Tenez : je vous passe les clefs du labo Eumetsat. — *carnet : Deux familles ; 🔑 les clefs du labo Eumetsat*

**A-E4** ▶ *« Comment trouver le premier signe ? »* `si clef a`  
Faites défiler les images une à une, en commençant la veille. La première fumée qui part de la forêt, c'est quand ? Notez l'heure inscrite sur l'image : elle est en UTC. — *carnet : L'heure*

**A-E5** ▶ *« Et la nuit, on voit encore le sol ? »* `si entendu A-E4`  
La nuit, plus de Soleil à renvoyer : la fumée disparaît avec lui. Faites défiler jusqu'à 22 h : que reste-t-il ? Des lumières de villes… et pas notre fumée. Les canaux infrarouges, eux, continuent de voir ce qui émet. — *carnet : La nuit*

**A-E6** ▶ *« Peut-on tracer le contour du feu avec ces images ? »* `si entendu A-E4`  
Comparez la taille d'un pixel à celle d'une commune. Vous traceriez un contour, vous, avec des pixels pareils ? — *carnet : Ce que Meteosat ne sait pas faire ; −1 confiance*

**A-E7** ▶ *« Il n'y a qu'un satellite qui voit les feux ? »* `si clef a`  
Oh non. Il y a un second œil, en orbite basse cette fois : Terra. Il passe une à deux fois par jour, et marque en rouge les pixels anormalement chauds. Je vous l'ajoute dans le labo : comparez le 21 et le 22 juillet. Deux capteurs qui disent la même date, c'est une preuve plus solide qu'un seul. — *🔑 un second œil dans le labo Eumetsat : Terra*

**A-E8** ✦ *« Une anecdote ? »*  
Chaque jour, la NASA publie les feux actifs détectés sur toute la planète par les capteurs MODIS et VIIRS, quelques heures après le passage des satellites : c'est le service FIRMS. Des pompiers du monde entier le consultent le matin, comme on lit la météo.

### Bastien (Les données et les traitements)

**Accueil.** Salut ! Bastien, données et traitements. Un départ de feu, hein ? Alors, question d'archiviste : pour attraper un départ, quelle résolution faut-il privilégier dans la donnée ?
- ◆ *« La résolution spatiale : voir fin. »* ✗ → Voir fin, c'est beau. Mais un satellite qui voit fin passe rarement : le feu aura démarré, brûlé et fait la une avant qu'il revienne. Une autre idée ?
- ◆ *« La résolution temporelle : voir souvent. »* ✓ → Voilà ! Un départ, c'est un instant : il faut une image très souvent, quitte à voir flou. J'ai des images toutes les 15 minutes, mais c'est plutôt utilisé pour la météo, pas le suivi de la végétation. — *carnet : La bonne résolution*
- ◆ *« La résolution spectrale : beaucoup de bandes. »* ✗ → Beaucoup de bandes, c'est précieux pour savoir ce qui brûle. Pour savoir quand ça démarre, il faut autre chose. Encore un essai ?

**A-B1** ▶ *« On sait quoi chercher : la fumée, dans le visible. Et maintenant ? »* `si carnet Voir la fumée ; sauf si clef a`  
Une image très souvent, un signal visible : un satellite comme Meteosat ou Terra peut répondre à vos besoins. Voyez avec votre orbitographe comment connaître leurs caractéristiques. Allez, je vous ouvre le labo Eumetsat. Et ne regardez pas que les dates, regardez les heures. — *carnet : Deux familles ; 🔑 les clefs du labo Eumetsat*

**A-B2** ▶ *« Quel satellite nous faut-il ? »* `sauf si carnet Voir la fumée ou clef a`  
Doucement. Une cadence, je vous l'ai donnée ; mais une cadence pour voir quoi, et dans quel signal ? Ça, c'est le rayon d'Elikia. Revenez avec la réponse.

**A-B3** ✦ *« Vous avez des images de cette forêt depuis quand ? »*  
Landsat photographie la Terre depuis 1972. Cette forêt des Landes, je l'ai vue pousser, brûler, repousser. Une archive, c'est une machine à remonter le temps : sans elle, pas d'« avant », donc pas d'« après ».

### Inès (Les orbites)

**Accueil.** On va voir avec votre spécialiste orbito quelles sont les caractéristiques de vos couples capteur / vecteur, ceux qui vont mesurer votre signal. Pour cela, il a besoin d'infos sur les types de signaux et les résolutions auxquelles vous voulez les acquérir : trouvez-lui ces infos. Au fait, un couple capteur / vecteur, cela vous parle ? Parmi ces trois propositions, laquelle en est un ?
- ◆ *« Une image Sentinel-2 en fausses couleurs. »* ✗ → Ça, c'est une donnée : ce qui sort du couple. Cherchez ce qui la fabrique.
- ◆ *« Un avion avec une caméra RVB + PIR. »* ✓ → Exactement : le vecteur porte, le capteur mesure. Un satellite et son instrument, un drone et sa caméra… Notez bien les deux noms : tout le monde les confond. — *carnet : Capteur et vecteur*
- ◆ *« Une station au sol qui reçoit les images. »* ✗ → Ça, c'est le segment sol : il écoute le couple, il n'en fait pas partie. Un autre essai ?

**A-I1** ▶ *« Pourquoi Meteosat voit-il tout le temps ? »* `si carnet Deux familles`  
Parce qu'il tourne aussi vite que la Terre : très haut au-dessus de l'équateur, il reste au-dessus du même point. Le prix ? Il est si loin que ses pixels font des kilomètres. Donnez son nom à votre orbitographe : il en fera la fiche. — *carnet : Loin, donc flou*

**A-I2** ✦ *« C'est vrai que tu calcules l'heure du déjeuner en orbites ? »*  
Évidemment. Sentinel-2 boucle un tour de Terre en une centaine de minutes. Le déjeuner, c'est un tour. Le café, un quart de tour. Les réunions… on ne compte plus.

### Rose (La contradictrice)

**Accueil.** Moi, je ne vous donnerai aucun fait : je vous poserai les questions du préfet. Première : « il a démarré à 11 h ». Selon quel capteur ? Avec quelle incertitude ? — *carnet : La marge*

**A-R1** ▶ *« Le feu a démarré le 22. C'est sûr ? »* `si clef a`  
Sûr selon quel capteur ? À quelle heure, et à combien de minutes près ? Si le satellite prend une image toutes les dix ou quinze minutes, votre heure a au moins cette marge-là. Et si la fumée a mis du temps à devenir visible ? Écrivez tout cela dans le rapport. — *carnet : La marge*

**A-R2** ▶ *« Et la surface ? »* `si clef a`  
La surface, c'est le travail de votre analyste. Mais le préfet vous la demandera à vous : vous compilez. Alors demandez-lui trois choses : son chiffre, la date de l'image, et ce qu'il ne peut pas dire.

**A-R3** ✦ *« Rose, on peut faire une pause ? »*  
Non. Mais dites-moi : vous passez un bon moment ?
- ◆ *« Oui, carrément. »* → Tant mieux. Le préfet, lui, ne s'amuse pas : il attend votre heure de départ.
- ◆ *« Bof. »* → Noté. Je le dirai à Marc : c'est lui qui écrit nos répliques. En attendant, il vous reste du temps : servez-vous-en.
- ◆ *« On est perdus. »* → Alors on revient au début : qu'est-ce qu'on cherche à voir ? Qui, ici, parle de signal ? Et qui, de cadence ? Les réponses sont chez deux experts différents.

## Enquête B — Quelle surface a brûlé ?

Jouée par **l'analyste** ; labo : Labo Copernicus.

### Elikia (Le signal)

**Accueil.** Rose m'a prévenue que vous vouliez mesurer l'étendue d'un feu de forêt. Cela va sans doute demander des traitements : Bastien vous en parlera. Pour cela, il faut croiser des signaux qui mesurent l'état de la végétation et son humidité : le proche infrarouge et le moyen infrarouge, le SWIR. Regardez : en vert la forêt vivante, en brun la forêt brûlée. Dans Sentinel-2, ce sont les bandes B8 et B12. — *carnet : Les deux signaux de la brûlure ; montre : reflectance*

**B-E1** ✎ *« Un satellite avec ces bandes ? Il y en a beaucoup ! »* `sauf si clef b`  
Un satellite avec ces caractéristiques, il y en a beaucoup ! Vous pensez à un en particulier ?
- ✎ si la réponse contient `senti?nel+e?\s*-?\s*(2|ii|deux)\b|\bs\s*-?\s*2\b` **(bonne réponse)** → Oui, c'est un très bon candidat, gratuit en plus ! Ses bandes B8 et B12 sont faites pour ça. Tenez : les clefs du labo Copernicus. — *🔑 les clefs du labo Copernicus*
- ✎ si la réponse contient `landsat` → Landsat ferait l'affaire, il a les bonnes bandes. Mais il en existe un plus récent, plus fin, qui repasse plus souvent sur la Gironde. Votre orbitographe connaît son nom.
- ✎ si la réponse contient `met[eo]*\s*-?\s*sat|\bmsg\b|\bmtg\b|seviri|\bfci\b` → Celui-là voit le feu naître, pas son contour : ses pixels sont bien trop gros pour mesurer des hectares. Il vous faut un œil plus fin. Demandez à votre orbitographe.
- ✎ si la réponse contient `terra|modis|\baqua\b` → Terra a de bonnes bandes, mais des pixels de 250 m à 1 km : pour des hectares, c'est grossier. Il vous faut plus fin. Votre orbitographe a sûrement un nom.
- ✎ sinon → Hum, je ne le connais pas, celui-là. Voyez avec votre orbitographe : Inès lui a sûrement soufflé un nom.
- ⇄ relais : Sentinel-2 : Inès l'a soufflé à l'orbitographe.

**B-E2** ▶ *« On ne trouve pas de nom de satellite… »* `si déjà tenté B-E1 ; sauf si clef b`  
Un indice, alors : il fait partie d'une famille européenne qui porte le nom d'un guetteur. Le deuxième de la famille, c'est le vôtre. Votre orbitographe le sait déjà, je parie. — *−1 confiance*

**B-E3** ▶ *« Qu'est-ce qui traverse la fumée ? »* `si clef b ; caché tant qu'on ne l'a pas débloqué`  
Les grandes longueurs d'onde. La fumée arrête le bleu bien plus que l'infrarouge moyen : une composition SWIR voit à travers, et le front de flammes y brille. Comparez couleurs naturelles et SWIR sur le 26 juillet : ce qui change, c'est la fumée, pas le feu. — *carnet : À travers la fumée*

**B-E4** ✦ *« Pourquoi une forêt vivante brille-t-elle autant dans le proche infrarouge ? »*  
Parce que l'intérieur d'une feuille est un labyrinthe de cellules et d'air : le proche infrarouge y rebondit et ressort. Brûlée, plus de feuilles, plus de labyrinthe : le miroir s'éteint. Et le SWIR remonte quand l'eau s'en va.

### Bastien (Les données et les traitements)

**Accueil.** Bastien, données et traitements. Et chocolatines, mais ça, c'est hors service. Pour mesurer l'étendue d'un feu, une bonne solution est de créer un indice qui mette en valeur la disparition de la végétation et l'assèchement du milieu. Vous avez une idée du satellite et des bandes nécessaires ?

**B-B1** ✎ *« Le satellite et les bandes ? On propose. »*  
Je vous écoute : quel satellite, et quelles bandes ?
- ✎ si la réponse contient `senti?nel+e?\s*-?\s*(2|ii|deux)\b|\bs\s*-?\s*2\b + \bb\s*-?\s*0?8\s*a?\b|proche\s*infra|\bpir\b|\bnir\b + \bb\s*-?\s*12\b|swir|infra\s*-?\s*rouge\s*moyen|moyen\s*infra` **(bonne réponse)** → Parfait ! Grâce à ça, on peut créer le NBR, l'indice de brûlure normalisé. Mais avant cela, on peut visualiser le phénomène en composition colorée. Je vous ouvre le labo Copernicus. — *carnet : Les compositions colorées ; 🔑 les clefs du labo Copernicus ; débloque B-E3*
- ✎ si la réponse contient `senti?nel+e?\s*-?\s*(2|ii|deux)\b|\bs\s*-?\s*2\b` → Le satellite, oui. Et les bandes ? Une pour la végétation vivante, une pour la sécheresse : il vous les faut toutes les deux.
- ✎ si la réponse contient `\bb\s*-?\s*0?8\s*a?\b|proche\s*infra|\bpir\b|\bnir\b + \bb\s*-?\s*12\b|swir|infra\s*-?\s*rouge\s*moyen|moyen\s*infra` → Les bandes, bravo. Et le satellite qui les porte ? Votre orbitographe doit avoir un nom.
- ✎ si la réponse contient `\bb\s*-?\s*0?8\s*a?\b|proche\s*infra|\bpir\b|\bnir\b` → Le proche infrarouge, oui : la végétation vivante. Il en manque une : celle qui voit la sécheresse.
- ✎ si la réponse contient `\bb\s*-?\s*12\b|swir|infra\s*-?\s*rouge\s*moyen|moyen\s*infra` → Le SWIR, oui : la sécheresse. Il en manque une : celle qui voit la végétation vivante.
- ✎ si la réponse contient `met[eo]*\s*-?\s*sat|\bmsg\b|\bmtg\b|seviri|\bfci\b|terra|modis|\baqua\b` → Trop grossier pour des hectares. Il vous faut un œil fin, qui passe régulièrement. Votre orbitographe le connaît.
- ✎ sinon → Allez en discuter avec Elikia : les interactions avec les objets, c'est une de ses spécialités.
- ⇄ relais : Le satellite vient de l'orbitographe, les bandes d'Elikia.

**B-B2** ▶ *« Quelle image prendre ? »* `si clef b`  
Une date avant, une date après. Commencez par l'avant : il n'y a rien à voir, et c'est justement pour ça qu'il compte. Notez la date exacte de chaque image : sans elle, votre surface ne veut rien dire. — *carnet : Avant, après*

**B-B3** ▶ *« La fumée nous gêne. »* `si entendu B-B2`  
Si la fumée vous gêne, essayez une composition qui ne regarde pas dans le visible. Et demandez à Elikia ce qui traverse la fumée : elle a une réponse en longueurs d'onde. — *débloque B-E3*

**B-B4** ▶ *« Et après le 26 juillet ? »* `si entendu B-B2`  
Cherchez la première image claire après le 26 juillet, et dites-moi combien de semaines il a fallu attendre. Je vous attends. Avec une chocolatine. — *carnet : Attendre ou payer*

**B-B5** ▶ *« Et ce NBR, on le calcule ? »* `si entendu B-B2`  
Le NBR, c'est (PIR − SWIR) / (PIR + SWIR) : il s'effondre là où la forêt a brûlé. La différence entre avant et après, le dNBR, dit à quel point ça a brûlé. Je vous l'ai ajouté dans le labo. Et pas de seuil choisi au feeling, hein : les classes viennent de UN-SPIDER. — *carnet : Le NBR ; 🔑 le calcul du dNBR dans le labo Copernicus*

**B-B6** ▶ *« Notre surface change entre deux dates. »* `si entendu B-B3`  
Votre surface change entre deux dates ? Le feu a grandi, ou c'est votre image qui voyait moins bien ? — *carnet : Ce que Sentinel-2 ne sait pas faire ; débloque B-R1 ; −1 confiance*

**B-B7** ✦ *« Vous avez des images de cette forêt depuis quand ? »*  
Landsat photographie la Terre depuis 1972, Sentinel-2 depuis 2015. Cette forêt des Landes, je l'ai vue pousser, brûler, repousser. Une archive, c'est une machine à remonter le temps : sans elle, pas d'« avant », donc pas d'« après ».

### Inès (Les orbites)

**Accueil.** On va voir avec votre spécialiste orbito quelles sont les caractéristiques de vos couples capteur / vecteur, ceux qui vont mesurer votre signal. Pour cela, il a besoin d'infos sur les types de signaux et les résolutions auxquelles vous voulez les acquérir : trouvez-lui ces infos. Au fait, un couple capteur / vecteur, cela vous parle ? Parmi ces trois propositions, laquelle en est un ?
- ◆ *« Une image Sentinel-2 en fausses couleurs. »* ✗ → Ça, c'est une donnée : ce qui sort du couple. Cherchez ce qui la fabrique.
- ◆ *« Un avion avec une caméra RVB + PIR. »* ✓ → Exactement : le vecteur porte, le capteur mesure. Un satellite et son instrument, un drone et sa caméra… Notez bien les deux noms : tout le monde les confond. — *carnet : Capteur et vecteur*
- ◆ *« Une station au sol qui reçoit les images. »* ✗ → Ça, c'est le segment sol : il écoute le couple, il n'en fait pas partie. Un autre essai ?

**B-I1** ▶ *« Pourquoi pas d'image entre le 21 et le 26 ? »* `si clef b`  
Parce que Sentinel-2 ne survole Saumos que tous les quelques jours : il vole bas, sa trace au sol défile, et sa fauchée n'est pas infinie. Votre orbitographe est en train de le calculer : allez lui demander. — *carnet : La revisite*

**B-I2** ✦ *« C'est vrai que tu calcules l'heure du déjeuner en orbites ? »*  
Évidemment. Sentinel-2 boucle un tour de Terre en une centaine de minutes. Le déjeuner, c'est un tour. Le café, un quart de tour.

### Rose (La contradictrice)

**Accueil.** Le préfet veut UN chiffre demain matin. Lequel lui donnez-vous, et à quel prix ? Réfléchissez-y en mesurant : une surface sans date ni méthode, ce n'est pas un chiffre, c'est une rumeur.

**B-R1** ▶ *« Alors, quel chiffre pour le préfet ? »* `caché tant qu'on ne l'a pas débloqué`  
Le préfet a trois options, pas une. Ce qui les sépare : l'argent, la précision, la patience. Pour chacune, trouvez une date. Et pour chacune, dites ce qu'elle ne permet pas. — *carnet : Les options du préfet*

**B-R2** ▶ *« Notre chiffre est bon ? »* `si clef b`  
Bon par rapport à quoi ? Le 26 juillet, le feu brûle encore. Une surface, c'est une date, une image, une méthode. Donnez les trois, et le préfet vous croira.

**B-R3** ✦ *« Rose, on peut faire une pause ? »*  
Non. Mais dites-moi : vous passez un bon moment ?
- ◆ *« Oui, carrément. »* → Tant mieux. Le préfet, lui, attend son chiffre.
- ◆ *« Bof. »* → Noté. Je le dirai à Marc : c'est lui qui écrit nos répliques. En attendant, mesurez.
- ◆ *« On est perdus. »* → Alors on revient au début : quels signaux voient une forêt brûlée ? Qui parle de photons ici ? Et quel satellite les capte ? Votre orbitographe a peut-être la réponse.

## Enquête C — Quels satellites, et quand passent-ils ?

Jouée par **l'orbitographe** ; labo : Labo Deimos.

### Elikia (Le signal)

**Accueil.** Les orbites ? Moi, je m'arrête là où le photon touche le capteur. Avant, il a voyagé ; après, c'est de l'électronique ; autour, c'est de la mécanique céleste. Et la mécanique céleste, c'est Inès : elle a déjà calculé dans combien de minutes vous allez la voir.

**C-E1** ▶ *« Pourquoi celui qui voit tout le temps voit-il si flou ? »* `caché tant qu'on ne l'a pas débloqué`  
Parce qu'il est loin. De si haut, chaque pixel de son capteur couvre des kilomètres au sol. Plus près, plus fin. Plus fin, moins souvent : c'est le même compromis partout. — *carnet : Loin, donc flou*

### Bastien (Les données et les traitements)

**Accueil.** Des noms de satellites ? J'ai tout le catalogue. Il y en a deux que vos collègues vont chercher, et un troisième que personne ne cite : celui qui a servi au périmètre officiel. Il est dans la page de l'activation EMSR899. Mais commencez par Inès : moi, je range ; elle, elle calcule.

**C-B1** ▶ *« Le satellite et le capteur, c'est pareil ? »* `si clef c`  
Jamais de la vie. Meteosat-10, c'est le satellite ; SEVIRI, l'appareil qu'il transporte. Sentinel-2 porte MSI, Terra porte MODIS. Dans mon catalogue, une ligne par couple. Vos collègues confondent tout le temps : corrigez-les.

**C-B2** ✦ *« Vous avez des images de cette forêt depuis quand ? »*  
Landsat photographie la Terre depuis 1972. Une archive, c'est une machine à remonter le temps : sans elle, pas d'« avant », donc pas d'« après ».

### Inès (Les orbites)

**Accueil.** Alors, il y a près de 500 satellites d'observation de la Terre en orbite. Pour t'aider à trouver ceux qui t'intéressent, j'ai besoin de connaître leur famille. Par contre, je suis prête à parier que vous aurez besoin de Sentinel-2 : c'est la star du moment, le satellite à tout faire, en particulier pour le suivi de la végétation. Dis-le à ton analyste. — *carnet : La star du moment*

**C-I1** ✎ *« La famille du satellite de notre rapporteur ? On propose. »* `sauf si clef c`  
Alors, quelle famille cherche ton rapporteur ?
- ✎ si la réponse contient `met[eo]*\s*-?\s*sat|\bmsg\b|\bmtg\b|seviri|\bfci\b` **(bonne réponse)** → Oui ! Il y a un satellite en position au-dessus de l'Europe, un Meteosat. Les images de ton rapporteur portent la mention MSG 0° : Meteosat Seconde Génération, posé à 0° de longitude. Cet été, c'est Meteosat-10 qui assurait ce service, avec son capteur SEVIRI. Tu peux le visualiser sur Deimos : je te passe les clefs. Essaie de comprendre le lien entre son orbite et ses résolutions… — *🔑 les clefs du labo Deimos ; débloque C-E1*
- ✎ si la réponse contient `terra|modis|\baqua\b` → Terra, c'est une piste : il voit les feux une à deux fois par jour. Mais ton rapporteur cherche l'heure du départ : il lui faut un œil qui ne cligne jamais. Quelle autre famille lui a-t-on soufflée ?
- ✎ si la réponse contient `senti?nel+e?\s*-?\s*(2|ii|deux)\b|\bs\s*-?\s*2\b` → Sentinel-2, c'est la star, je te l'ai dit, et c'est pour ton analyste. Ton rapporteur, lui, a besoin d'un autre œil. Va lui demander quelle famille ses experts lui ont soufflée.
- ✎ sinon → Je ne la connais pas, celle-là. Demande à ton rapporteur : il cherche un satellite qui ne quitte jamais l'Europe des yeux.
- ⇄ relais : Meteosat : le rapporteur l'a appris d'Elikia ou de Bastien.

**C-I0** ▶ *« Notre rapporteur n'a pas encore de nom… »* `si déjà tenté C-I1 ; sauf si clef c`  
Un indice, alors : cette famille porte le nom du temps qu'il fait. Ça vous coûte un peu de la confiance du préfet, mais pas trop. — *−1 confiance*

**C-I2** ▶ *« Un satellite qui ne quitte jamais l'Europe, c'est possible ? »* `si clef c`  
Un satellite qui ne bouge pas par rapport à la Terre : à quelle altitude doit-il être ? Regarde dans le labo si sa trace défile ou reste fixe, et note son altitude. — *carnet : Géostationnaire*

**C-I3** ▶ *« Et Sentinel-2, pourquoi ne repasse-t-il pas chaque jour ? »* `si clef c`  
Il vole bas, il voit fin, mais sa trace défile : chaque jour, il survole une autre bande de Terre. Combien de jours avant de revenir sur Saumos ? Compte-les dans le labo. — *carnet : La revisite*

**C-I4** ▶ *« Et s'il fait nuageux le jour du passage ? »* `si entendu C-I3`  
S'il repasse tous les cinq jours et qu'il fait nuageux ce jour-là, combien de temps attends-tu ? — *carnet : Les nuages ; −1 confiance*

**C-I5** ▶ *« Qui a tracé le périmètre officiel si tôt ? »* `si entendu C-I2, C-I3`  
Un satellite qu'on ne laisse pas défiler : on le pointe, à la demande, sur la zone. Très fin, très cher. Je t'ajoute sa fiche dans le labo ; son nom est aussi dans la page de l'activation EMSR899. — *carnet : La commande ; 🔑 la fiche du satellite commandé dans le labo Deimos ; débloque C-R1*

**C-I6** ▶ *« Et le radar, il ne pourrait pas nous aider ? »* `si entendu C-I5`  
Si ! Le radar voit à travers les nuages et la fumée, de jour comme de nuit. Sa précision sur les zones brûlées est plus relative, mais il ne vous fait pas attendre le soleil. On ne le manipule pas aujourd'hui : note-le comme une solution. — *carnet : Le radar*

**C-I7** ▶ *« Et Terra, dans tout ça ? »* `si clef c`  
Terra vole à 705 km, sur une orbite héliosynchrone comme Sentinel-2, mais son capteur MODIS a une fauchée immense : plus de 2 000 km. Il voit donc presque tout, tous les jours, avec des pixels de 250 m à 1 km. Le compromis, encore. Je t'ajoute sa fiche. — *🔑 la fiche de Terra dans le labo Deimos*

**C-I8** ✦ *« C'est vrai que tu calcules l'heure du déjeuner en orbites ? »*  
Évidemment. Sentinel-2 boucle un tour de Terre en une centaine de minutes. Le déjeuner, c'est un tour. Le café, un quart de tour. Les réunions… on ne compte plus.

### Rose (La contradictrice)

**Accueil.** Un satellite que l'on pointe à la demande, ça coûte combien, et qui paie ? Gardez la question : vous la reposerez au préfet. — *carnet : La commande*

**C-R1** ▶ *« Une image commandée, c'est la solution ? »* `caché tant qu'on ne l'a pas débloqué`  
C'est une solution. Rapide, précise, et chère. Le préfet en a deux autres. Faites-lui la liste, avec une date et un prix pour chacune. — *carnet : Les options du préfet*

**C-R2** ▶ *« Et nos coéquipiers, on leur dit quoi ? »* `si clef c`  
Ce que leurs capteurs savent faire, et ce qu'ils ne savent pas. Au rapporteur : pourquoi son heure est fiable mais pas son contour. À l'analyste : pourquoi ses images sautent du 21 au 26. C'est votre livrable, à vous.

**C-R3** ✦ *« Rose, on peut faire une pause ? »*  
Non. Mais dites-moi : vous passez un bon moment ?
- ◆ *« Oui, carrément. »* → Tant mieux. Vos coéquipiers, eux, attendent vos fiches.
- ◆ *« Bof. »* → Noté. Je le dirai à Marc : c'est lui qui écrit nos répliques. En attendant, allez voir vos coéquipiers : ils ont des noms pour vous.
- ◆ *« On est perdus. »* → Alors on revient au début : Inès a besoin d'une famille de satellites. Qui, dans votre groupe, cherche le départ du feu ? Allez lui demander ce que ses experts lui ont dit.

## Le carnet

- **Le signal du départ** : Au départ, peu de chaleur visible de loin : on cherche la fumée, qui monte vite et s'étale.
- **Voir la fumée** : La fumée renvoie la lumière du Soleil : elle se voit dans le visible… donc de jour.
- **La bonne résolution** : Pour saisir un départ, il faut voir souvent, quitte à voir flou : la résolution temporelle prime.
- **Deux familles** : Meteosat ou Terra peuvent répondre. Leurs caractéristiques : voir avec l'orbitographe.
- **L'heure** : L'heure de l'image est en UTC ; l'heure française d'été est en avance de deux heures.
- **La nuit** : La nuit, plus de lumière solaire renvoyée : la fumée disparaît du visible ; restent les lumières des villes et ce qui émet.
- **La marge** : Une heure de départ n'a de sens qu'avec le capteur qui la donne et sa cadence : écrivez les deux.
- **Ce que Meteosat ne sait pas faire** : Il voit le feu naître, mais pas son contour : ses pixels font des kilomètres.
- **Capteur et vecteur** : Le vecteur porte (satellite, avion, drone), le capteur mesure (l'instrument). Deux noms distincts.
- **Les deux signaux de la brûlure** : Proche infrarouge (B8) : la végétation vivante. Infrarouge moyen, SWIR (B12) : la sécheresse. Brûlée, la forêt perd l'un et gagne l'autre.
- **La star du moment** : Inès parie sur Sentinel-2, le satellite à tout faire, en particulier pour la végétation. À transmettre à l'analyste.
- **Les compositions colorées** : Avant de calculer, on regarde : couleurs naturelles pour la fumée, SWIR pour voir à travers.
- **Le NBR** : NBR = (PIR − SWIR) / (PIR + SWIR) : il s'effondre là où la forêt a brûlé. Avant moins après : le dNBR.
- **Avant, après** : Une date avant le feu, une date après : c'est la différence qui parle.
- **À travers la fumée** : Les grandes longueurs d'onde traversent mieux la fumée : la composition SWIR montre le front de flammes.
- **Ce que Sentinel-2 ne sait pas faire** : Il voit fin, mais seulement les jours où il passe, et seulement sans nuages : la surface d'un jour n'est pas la surface finale.
- **Attendre ou payer** : Après le feu, le ciel reste couvert : soit on attend une image claire, soit on en commande une.
- **Géostationnaire** : Au-dessus de l'équateur, à 36 000 km, il tourne avec la Terre : il regarde toujours le même point, en permanence, mais de très loin.
- **Loin, donc flou** : Plus haut, plus souvent, plus flou ; plus bas, plus fin, moins souvent. C'est le même compromis partout.
- **La revisite** : Sentinel-2 vole bas et sa trace au sol défile : il ne revient sur Saumos qu'au bout de quelques jours.
- **Les nuages** : Un passage nuageux ne compte pas : il faut attendre le suivant, et le suivant encore.
- **La commande** : Un satellite très haute résolution se pointe à la demande sur la zone : il ne fait pas attendre, mais il coûte.
- **Le radar** : Le radar voit à travers les nuages et la fumée, de jour comme de nuit ; sa précision sur les zones brûlées est plus relative. Pas manipulé ici : une solution à proposer.
- **Les options du préfet** : Trois options, pas une : ce qui les sépare, c'est l'argent, la précision et la patience. Pour chacune, une date.
