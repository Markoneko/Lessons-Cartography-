/**
 * Feuille de réception de l'atelier des commandes (cours « Image Application »).
 *
 * Mise en place, une fois (dix minutes) :
 *   1. Créer une feuille Google Sheets vide, par exemple « Image Application — atelier ».
 *   2. Menu Extensions → Apps Script. Remplacer le contenu par ce fichier, enregistrer.
 *   3. Déployer → Nouveau déploiement → type « Application Web ».
 *        Exécuter en tant que : moi.  Qui a accès : tout le monde.
 *      Autoriser l'accès quand Google le demande.
 *   4. Copier l'adresse du déploiement (elle finit par /exec) et la coller dans le cours,
 *      diapo 4.3 :  ::: {.atelier-commandes donnees="donnees/atelier.json" envoi="https://script.google.com/…/exec"}
 *   5. Recompiler le cours. Tester avec un groupe fictif : une ligne doit apparaître dans la feuille.
 *
 * Atelier Saumos (jeu de rôle) : la même adresse reçoit aussi le rapport des groupes et leur avis sur le jeu.
 * Coller l'adresse dans IMAGE-AtelierSaumos.qmd :  ::: {.jdr-rapport envoi="…/exec"}  et  ::: {.jdr-retour envoi="…/exec"}
 * Les envois sont rangés dans deux onglets créés au premier envoi : « Saumos — rapports » et « Saumos — avis ».
 *
 * Chaque envoi ajoute une ligne. Un groupe qui renvoie son travail ajoute une nouvelle ligne :
 * la plus récente fait foi. Les données restent dans le Drive de l'enseignant.
 * Ne rien mettre de personnel dans le champ « Noms » si l'on ne veut pas que cela y figure.
 */

var COLONNES = [
  "reçu le", "groupe", "noms", "commande", "score", "chaîne", "ce qui manque", "pièges",
  "cas réel", "lien", "signal", "données", "résolutions", "traitements", "sensibilité",
  "moyens", "précision", "écarts", "pépites entendues", "votes", "projet un peu fou", "brut"
];

var SAUMOS = {
  "saumos-rapport": { onglet: "Saumos — rapports", colonnes: ["reçu le", "groupe", "nom", "posture", "solo", "confiance",
    "paris", "cadrage", "rapport", "contrôles du préfet", "indices", "termes", "clefs", "brut"] },
  "saumos-avis": { onglet: "Saumos — avis", colonnes: ["reçu le", "groupe", "nom", "posture", "avis", "cadrage", "confiance", "brut"] }
};

function onglet(nom, colonnes) {
  var classeur = SpreadsheetApp.getActiveSpreadsheet();
  var f = classeur.getSheetByName(nom) || classeur.insertSheet(nom);
  if (f.getLastRow() === 0) f.appendRow(colonnes);
  return f;
}

function doPost(e) {
  var p = {};
  try { p = JSON.parse(e.postData.contents); } catch (err) { p = { brut: e.postData ? e.postData.contents : "" }; }
  var S = SAUMOS[p.type];
  if (S) {
    var f = onglet(S.onglet, S.colonnes);
    if (p.type === "saumos-avis") {
      f.appendRow([new Date(), p.groupe || "", p.nom || "", p.posture || "", p.avis || "", p.cadrage || "", p.confiance, JSON.stringify(p)]);
    } else {
      f.appendRow([new Date(), p.groupe || "", p.nom || "", p.posture || "", p.solo ? "oui" : "", p.confiance,
        JSON.stringify(p.paris || {}), p.cadrage || "", JSON.stringify(p.rapport || {}), (p.controles || []).join(", "),
        (p.indices || []).join(", "), (p.termes || []).join(", "), (p.clefs || []).join(", "), JSON.stringify(p)]);
    }
    return ContentService.createTextOutput("ok");
  }
  var feuille = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  if (feuille.getLastRow() === 0) feuille.appendRow(COLONNES);
  var c = p.cas_reel || {};
  feuille.appendRow([
    new Date(), p.groupe || "", p.noms || "", p.commande_titre || p.commande || "", p.score || "",
    (p.chaine || []).join(", "), (p.manques || []).join(" | "), (p.pieges || []).join(", "),
    c.titre || "", c.lien || "", c.signal || "", c.donnee || "", (c.resol || []).join(" / "),
    c.traitements || "", c.sensibilite || "", c.moyens || "", c.precision || "", c.ecarts || "",
    (p.pepites || []).join(", "), JSON.stringify(p.votes || {}), p.projective || "",
    JSON.stringify(p)
  ]);
  return ContentService.createTextOutput("ok");
}
