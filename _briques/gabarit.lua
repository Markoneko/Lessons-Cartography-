--[[
  gabarit.lua — le « moteur » des supports de cours.

  Il lit le Markdown et fabrique :
    1. le pictogramme de niveau (socle / appui / veille) devant le titre de chaque diapo ;
    2. la diapo « carte du cours », générée toute seule ;
    3. les briques d'exercice (question, qcm, ordre, zones) et d'expérience
       (pivoter, comparer, défiler, curseur, classer, cap, visées, pour aller plus loin, schéma) ;
    4. le tri des diapos (ne garder qu'un niveau, masquer les optionnelles) ;
    5. le plan du cours, à partir des fiches posées sous chaque titre.

  On n'a normalement pas besoin de modifier ce fichier pour écrire un cours.
]]

local NIVEAUX = { "socle", "appui", "veille" }
local LIBELLE = { socle = "Socle", appui = "Appui", veille = "Veille" }

-- Langue du cours : « lang: en » dans l'en-tête d'un cours bascule les textes du gabarit en anglais.
local LANGUE = "fr"
local TEXTES = {
  fr = {
    question = "Question", reponse = "Réponse", plus = "Pour aller plus loin", fermer = "Fermer",
    cliquez_image = "Cliquez sur l’image.", recommencer = "Recommencer",
    diapo = "diapo", diapos = "diapos", retour_carte = "Retour à la carte du cours",
    tourner_gauche = "Tourner vers la gauche", tourner_droite = "Tourner vers la droite",
    comparer = "Passer d’une image à l’autre", precedente = "Image précédente", suivante = "Image suivante",
    venir_gauche = "Venir sur la gauche", venir_droite = "Venir sur la droite",
    loupe = "Cliquez pour zoomer, déplacez pour explorer", effacer = "Effacer",
    reponse_notes = "Réponse : ", ordre_notes = "Ordre attendu : ",
    flash_voir = "Voir la carte", flash_revoir = "Revoir", pieces = "Les pièces",
    ia_titre = "DÉCLARATION DE TRANSPARENCE IA", ia_boussole = "Boussole IA · Géodata Paris",
    ia_profil = "Profil :", ia_coordonnees = "coordonnées",
    ia_texte = "Certaines illustrations et certains passages ont été réalisés par %s. La conception, les sources et le texte dans son ensemble sont de l’auteur.",
  },
  en = {
    question = "Question", reponse = "Answer", plus = "Going further", fermer = "Close",
    cliquez_image = "Click on the image.", recommencer = "Start again",
    diapo = "slide", diapos = "slides", retour_carte = "Back to the course map",
    tourner_gauche = "Rotate left", tourner_droite = "Rotate right",
    comparer = "Fade from one image to the next", precedente = "Previous image", suivante = "Next image",
    venir_gauche = "Come to port", venir_droite = "Come to starboard",
    loupe = "Click to zoom, move to explore", effacer = "Clear",
    reponse_notes = "Answer: ", ordre_notes = "Expected order: ",
    flash_voir = "Show the map", flash_revoir = "Show again", pieces = "The pieces",
    ia_titre = "AI TRANSPARENCY STATEMENT", ia_boussole = "AI Compass · Géodata Paris",
    ia_profil = "Profile:", ia_coordonnees = "coordinates",
    ia_texte = "Some illustrations and passages were created by %s. The design, sources, and text as a whole were created by the author.",
  },
}
local LIBELLES = {
  fr = { socle = "Socle", appui = "Appui", veille = "Veille" },
  en = { socle = "Core", appui = "Support", veille = "Further" },
}
local function t(cle) return (TEXTES[LANGUE] or TEXTES.fr)[cle] end

local EN_HTML = FORMAT:match("revealjs") ~= nil

-- Réglages lus dans l'en-tête du cours (ou donnés en ligne de commande avec -M)
local garder = nil            -- nil = tous les niveaux
local masquer_optionnels = false

----------------------------------------------------------------------------
-- Outils
----------------------------------------------------------------------------

local function echappe(s)
  return (s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"):gsub('"', "&quot;"))
end

-- Espaces insécables de la typographie française : pas de « ? » ou de « : » seul en début de ligne.
local INSECABLE = "\u{00A0}"
local function typo(texte)
  if LANGUE ~= "fr" then return texte end
  return (texte:gsub(" ([%?!:;»])", INSECABLE .. "%1"):gsub("« ", "«" .. INSECABLE))
end
local function typo_inlines(inlines)
  if LANGUE ~= "fr" then return inlines end
  for i = 1, #inlines - 1 do
    local a, b = inlines[i], inlines[i + 1]
    if a.t == "Space" and b.t == "Str" and b.text:match("^[%?!:;»]") then
      inlines[i] = pandoc.Str(INSECABLE)
    elseif a.t == "Str" and a.text:match("«$") and b.t == "Space" then
      inlines[i + 1] = pandoc.Str(INSECABLE)
    end
  end
  return inlines
end

-- Retire les espaces, insécables compris, et les deux-points en tête d'un texte.
local function sans_tete(texte)
  local avant
  repeat
    avant = texte
    texte = texte:gsub("^[%s:]+", "")
    if texte:sub(1, 2) == INSECABLE then texte = texte:sub(3) end
  until texte == avant
  return texte
end
local function sans_queue(texte)
  local avant
  repeat
    avant = texte
    texte = texte:gsub("%s+$", "")
    if texte:sub(-2) == INSECABLE then texte = texte:sub(1, -3) end
  until texte == avant
  return texte
end

local function niveau_de(classes)
  for _, n in ipairs(NIVEAUX) do
    if classes:includes(n) then return n end
  end
  return nil
end

--[[ Les pictogrammes de niveau. Trois formes tirées des strates du logo Géodata :
       socle  : trois strates à décrochement, trait gras, bleu    → évoque un S
       appui  : deux strates en crête, trait moyen, orange        → évoque un A
       veille : une strate en creux, trait fin, violet            → évoque un V
     Forme, nombre de traits, épaisseur et couleur disent quatre fois la même chose :
     le code reste lisible en noir et blanc. La couleur est donnée par la charte (CSS). ]]
local TRACES = {
  socle = { epaisseur = 5.5, "M2 34 H15 L24 29 H46", "M2 23 H15 L24 18 H46", "M2 12 H15 L24 7 H46" },
  appui = { epaisseur = 3.8, "M2 24 H11 L24 6 L37 24 H46", "M2 36 H11 L24 18 L37 36 H46" },
  veille = { epaisseur = 2.6, "M2 7 H11 L24 33 L37 7 H46" },
  -- variantes proposées à la comparaison
  ["appui-barre"] = { epaisseur = 3.8, "M2 35 H9 L24 6 L39 35 H46", "M2 24 H46" },
  ["veille-double"] = { epaisseur = 2.2, "M2 5 H10 L24 25 L38 5 H46", "M2 14 H10 L24 34 L38 14 H46" },
}

local function glyphe(nom, largeur)
  local t = TRACES[nom]
  largeur = largeur or 48
  local traits = ""
  for _, d in ipairs(t) do traits = traits .. '<path d="' .. d .. '"/>' end
  return string.format(
    '<svg class="strates" viewBox="0 0 48 40" width="%d" height="%d" fill="none" stroke="currentColor" '
    .. 'stroke-width="%s" stroke-linejoin="round" aria-hidden="true">%s</svg>',
    largeur, math.floor(largeur * 40 / 48 + 0.5), t.epaisseur, traits)
end

-- Une case à cocher Markdown ([x] ou [ ]) en tête d'un élément de liste ?
local function lire_case(item)
  local premier = item[1]
  if not premier or not premier.content then return nil end
  local tete = premier.content[1]
  if tete and tete.t == "Str" and (tete.text == "☒" or tete.text == "☐") then
    local juste = tete.text == "☒"
    local reste = pandoc.List()
    for i = 3, #premier.content do reste:insert(premier.content[i]) end
    return juste, reste
  end
  return nil
end

----------------------------------------------------------------------------
-- Briques d'exercice
----------------------------------------------------------------------------

-- ::: {.question}  … texte … :::   (étiquette modifiable : etiquette="Prédiction")
local function brique_question(div)
  local etiquette = div.attributes["etiquette"] or t("question")
  div.attributes["etiquette"] = nil
  table.insert(div.content, 1, pandoc.Div(pandoc.Plain(pandoc.Str(etiquette)), pandoc.Attr("", { "etiquette" })))
  return div
end

-- ::: {.reponse}  … :::   → n'apparaît qu'au clic suivant
local function brique_reponse(div)
  local etiquette = div.attributes["etiquette"] or t("reponse")
  div.attributes["etiquette"] = nil
  table.insert(div.content, 1, pandoc.Div(pandoc.Plain(pandoc.Str(etiquette)), pandoc.Attr("", { "etiquette" })))
  if EN_HTML then div.classes:insert("fragment") end
  return div
end

-- ::: {.qcm}  liste de cases à cocher, [x] = bonne réponse,
--             un sous-point = le commentaire affiché après le clic
local function brique_qcm(div)
  local sortie, bonnes = pandoc.List(), pandoc.List()
  for _, bloc in ipairs(div.content) do
    if bloc.t == "BulletList" then
      local choix = pandoc.List()
      for _, item in ipairs(bloc.content) do
        local juste, texte = lire_case(item)
        if juste == nil then juste, texte = false, item[1].content end
        local retour = pandoc.List()
        if item[2] and item[2].t == "BulletList" then
          for _, sous in ipairs(item[2].content) do retour:extend(sous) end
        end
        if juste then bonnes:insert(pandoc.utils.stringify(texte)) end
        if EN_HTML then
          local contenu = pandoc.List({ pandoc.Div(pandoc.Plain(texte), pandoc.Attr("", { "choix-texte" })) })
          if #retour > 0 then
            contenu:insert(pandoc.Div(retour, pandoc.Attr("", { "choix-retour" })))
          end
          choix:insert(pandoc.Div(contenu, pandoc.Attr("", { "choix" },
            { ["data-juste"] = juste and "oui" or "non", role = "button", tabindex = "0" })))
        else
          local t = pandoc.List({ pandoc.Str("☐"), pandoc.Space() }); t:extend(texte)
          choix:insert({ pandoc.Plain(t) })
        end
      end
      if EN_HTML then sortie:extend(choix) else sortie:insert(pandoc.BulletList(choix)) end
    else
      sortie:insert(bloc)
    end
  end
  if not EN_HTML and #bonnes > 0 then
    sortie:insert(pandoc.Div(pandoc.Para(pandoc.Str(t("reponse_notes") .. table.concat(bonnes, " ; "))),
      pandoc.Attr("", { "notes" })))
  end
  div.content = sortie
  return div
end

-- ::: {.ordre}  liste numérotée écrite DANS LE BON ORDRE ; elle est mélangée à l'écran
local function brique_ordre(div)
  local sortie = pandoc.List()
  for _, bloc in ipairs(div.content) do
    if bloc.t == "OrderedList" then
      if EN_HTML then
        local etapes = pandoc.List()
        for rang, item in ipairs(bloc.content) do
          etapes:insert(pandoc.Div(item, pandoc.Attr("", { "etape" },
            { ["data-rang"] = tostring(rang), role = "button", tabindex = "0" })))
        end
        sortie:insert(pandoc.Div(etapes, pandoc.Attr("", { "etapes" })))
        sortie:insert(pandoc.RawBlock("html",
          '<div class="ordre-pied"><span class="ordre-etat" aria-live="polite"></span>'
          .. '<button type="button" class="ordre-recommencer">' .. t("recommencer") .. '</button></div>'))
      else
        -- hors écran : on mélange de façon fixe, la solution va dans les notes
        local n, melange, solution = #bloc.content, pandoc.List(), pandoc.List()
        for i = n, 1, -1 do if i % 2 == 0 then melange:insert(bloc.content[i]) end end
        for i = 1, n do if i % 2 == 1 then melange:insert(bloc.content[i]) end end
        for i, item in ipairs(bloc.content) do
          solution:insert(i .. ". " .. pandoc.utils.stringify(item))
        end
        sortie:insert(pandoc.BulletList(melange))
        sortie:insert(pandoc.Div(pandoc.Para(pandoc.Str(t("ordre_notes") .. table.concat(solution, " — "))),
          pandoc.Attr("", { "notes" })))
      end
    else
      sortie:insert(bloc)
    end
  end
  div.content = sortie
  return div
end

-- ::: {.zones image="images/carte.jpg" alt="…"}
--   - [x] gauche,haut,largeur,hauteur : commentaire     (en % de l'image)
local function brique_zones(div)
  local image = div.attributes["image"]
  local alt = div.attributes["alt"] or ""
  local hauteur_image = div.attributes["hauteur"]
  div.attributes["image"], div.attributes["alt"], div.attributes["hauteur"] = nil, nil, nil
  local avant, boutons = pandoc.List(), {}
  for _, bloc in ipairs(div.content) do
    if bloc.t == "BulletList" then
      for _, item in ipairs(bloc.content) do
        local juste, texte = lire_case(item)
        local brut = pandoc.utils.stringify(texte or item[1].content)
        local x, y, l, h, retour = brut:match("^%s*([%d%.]+)%s*,%s*([%d%.]+)%s*,%s*([%d%.]+)%s*,%s*([%d%.]+)%s*:?%s*(.*)$")
        if x then
          retour = sans_tete(retour)
          table.insert(boutons, string.format(
            '<button type="button" class="zone" data-juste="%s" data-retour="%s" aria-label="zone %d" '
            .. 'style="left:%s%%;top:%s%%;width:%s%%;height:%s%%"></button>',
            juste and "oui" or "non", echappe(retour), #boutons + 1, x, y, l, h))
        end
      end
    else
      avant:insert(bloc)
    end
  end
  local img = pandoc.Image({ pandoc.Str(alt) }, image)
  if not EN_HTML then
    return pandoc.Para({ img })
  end
  local cadre = pandoc.Div({
    pandoc.Plain({ img }),
    pandoc.RawBlock("html", table.concat(boutons, "\n")),
  }, pandoc.Attr("", { "zones-cadre" },
    hauteur_image and { style = "--hauteur-image:" .. hauteur_image .. "px" } or {}))
  avant:insert(cadre)
  avant:insert(pandoc.RawBlock("html", '<p class="zones-retour" aria-live="polite">' .. t("cliquez_image") .. '</p>'))
  div.content = avant
  return div
end

-- ::: {.codes-niveau}  → planche de présentation du code des niveaux (diapo de travail)
local function brique_codes()
  if not EN_HTML then return {} end
  local sens = {
    socle = "Trois strates à décrochement, trait gras. À maîtriser.",
    appui = "Deux strates en crête, trait moyen. Pour consolider.",
    veille = "Une strate en creux, trait fin. Pour aller plus loin.",
  }
  local h = '<div class="codes-niveau"><div class="code code-retenu">'
  for _, n in ipairs(NIVEAUX) do
    h = h .. '<div class="code-ligne niveau-' .. n .. '">' .. glyphe(n, 96)
        .. '<div><div class="niveau-mot">' .. LIBELLE[n] .. '</div><p>' .. sens[n] .. '</p></div></div>'
  end
  h = h .. '</div><div class="code code-variantes"><h3>Deux variantes</h3>'
      .. '<div class="code-ligne niveau-appui">' .. glyphe("appui-barre", 72)
      .. '<p>Appui : une seule crête, barrée d’une strate. Plus proche de la lettre A.</p></div>'
      .. '<div class="code-ligne niveau-veille">' .. glyphe("veille-double", 72)
      .. '<p>Veille : deux creux. Plus visible de loin, mais on perd le compte 3 – 2 – 1.</p></div>'
      .. '</div></div>'
  return pandoc.RawBlock("html", h)
end

----------------------------------------------------------------------------
-- Briques d'expérience
----------------------------------------------------------------------------

local function attribut(div, nom, defaut)
  local v = div.attributes[nom]
  div.attributes[nom] = nil
  if v == nil or v == "" then return defaut end
  return v
end

-- Lit un fichier voisin du cours (un schéma SVG, par exemple).
local function lire_fichier(chemin)
  local f = io.open(chemin, "r")
  if not f and PANDOC_STATE and PANDOC_STATE.input_files[1] then
    f = io.open(pandoc.path.join({ pandoc.path.directory(PANDOC_STATE.input_files[1]), chemin }), "r")
  end
  if not f and quarto and quarto.project and quarto.project.directory then
    f = io.open(pandoc.path.join({ quarto.project.directory, chemin }), "r")
  end
  if not f then return nil end
  local contenu = f:read("a")
  f:close()
  return contenu
end

local function schema_html(chemin, hauteur)
  local svg = lire_fichier(chemin)
  if not svg then
    return '<p class="legende">Schéma introuvable : ' .. echappe(chemin) .. '</p>'
  end
  svg = svg:gsub("<%?xml.-%?>", ""):gsub("<!%-%-.-%-%->", "")
  local style = hauteur and (' style="--hauteur:' .. hauteur .. 'px"') or ''
  return '<div class="schema"' .. style .. '>' .. svg .. '</div>'
end

-- ::: {.schema fichier="images/schemas/escalier.svg"}  → dessin vectoriel aux couleurs de la charte
local function brique_schema(div)
  local chemin = attribut(div, "fichier", "")
  local hauteur = attribut(div, "hauteur", nil)
  if not EN_HTML then return {} end
  local sortie = pandoc.List({ pandoc.RawBlock("html", schema_html(chemin, hauteur)) })
  sortie:extend(div.content)
  div.content = sortie
  div.classes = pandoc.List({ "schema-bloc" })
  return div
end

-- ::: {.plus titre="…"}  → « Pour aller plus loin » : un bonus qui s'ouvre au clic
local function brique_plus(div)
  local titre = attribut(div, "titre", t("plus"))
  if not EN_HTML then
    table.insert(div.content, 1, pandoc.Para(pandoc.Strong(pandoc.Str(titre))))
    return div
  end
  local corps = pandoc.Div(div.content, pandoc.Attr("", { "plus-corps" }))
  div.content = pandoc.List({
    pandoc.RawBlock("html", '<button type="button" class="plus-bouton" aria-expanded="false">'
      .. '<span class="plus-signe" aria-hidden="true">+</span>' .. t("plus") .. '</button>'
      .. '<div class="plus-panneau" role="dialog" aria-label="' .. echappe(titre) .. '">'
      .. '<button type="button" class="plus-fermer" aria-label="' .. t("fermer") .. '">×</button>'
      .. '<div class="plus-titre"><span class="plus-signe" aria-hidden="true">+</span>' .. echappe(titre) .. '</div>'),
    corps,
    pandoc.RawBlock("html", '</div>'),
  })
  return div
end

-- ::: {.pivoter image="…" alt="…" cible="180" tolerance="20"}  le texte = commentaire affiché à la réussite
local function brique_pivoter(div)
  local image = attribut(div, "image", "")
  local alt = attribut(div, "alt", "")
  local cible = attribut(div, "cible", "0")
  local tolerance = attribut(div, "tolerance", "20")
  local img = pandoc.Image({ pandoc.Str(alt) }, image)
  if not EN_HTML then
    table.insert(div.content, 1, pandoc.Para({ img }))
    return div
  end
  div.attributes["data-cible"] = cible
  div.attributes["data-tolerance"] = tolerance
  local retour = pandoc.Div(div.content, pandoc.Attr("", { "pivot-retour" }))
  div.content = pandoc.List({
    pandoc.Div({ pandoc.Plain({ img }) }, pandoc.Attr("", { "pivot-cadre" })),
    pandoc.RawBlock("html", '<div class="pivot-commandes">'
      .. '<button type="button" class="pivot-tourner" data-pas="-15" aria-label="' .. t("tourner_gauche") .. '">↺</button>'
      .. '<span class="pivot-angle" aria-live="polite">0°</span>'
      .. '<button type="button" class="pivot-tourner" data-pas="15" aria-label="' .. t("tourner_droite") .. '">↻</button>'
      .. '</div>'),
    retour,
  })
  return div
end

-- ::: {.comparer}  liste d'images ; le texte alternatif de chacune sert d'étiquette
local function brique_comparer(div)
  local images, avant = pandoc.List(), pandoc.List()
  for _, bloc in ipairs(div.content) do
    if bloc.t == "BulletList" then
      for _, item in ipairs(bloc.content) do
        pandoc.walk_block(pandoc.Div(item), { Image = function(i) images:insert(i) end })
      end
    else
      avant:insert(bloc)
    end
  end
  if not EN_HTML then
    for _, i in ipairs(images) do avant:insert(pandoc.Para({ i })) end
    div.content = avant
    return div
  end
  local couches, etiquettes = pandoc.List(), ""
  for n, i in ipairs(images) do
    local nom = pandoc.utils.stringify(i.caption)
    couches:insert(pandoc.Div({ pandoc.Plain({ i }) }, pandoc.Attr("", { "comparer-couche" }, { ["data-nom"] = nom })))
    etiquettes = etiquettes .. '<button type="button" class="comparer-etiquette" data-rang="' .. (n - 1) .. '">'
        .. echappe(nom) .. '</button>'
  end
  avant:insert(pandoc.Div(couches, pandoc.Attr("", { "comparer-pile" })))
  avant:insert(pandoc.RawBlock("html", '<div class="comparer-commande"><input type="range" class="comparer-curseur" min="0" max="'
    .. (#images - 1) .. '" step="0.01" value="0" aria-label="' .. t("comparer") .. '">'
    .. '<div class="comparer-etiquettes">' .. etiquettes .. '</div></div>'))
  div.content = avant
  return div
end

-- ::: {.loupe zoom="3"}  une image que l'on agrandit d'un clic, puis que l'on explore en déplaçant le pointeur
local function brique_loupe(div)
  local zoom = attribut(div, "zoom", "3")
  if not EN_HTML then return div end
  div.attributes["data-zoom"] = zoom
  div.attributes["role"] = "button"
  div.attributes["tabindex"] = "0"
  div.attributes["title"] = t("loupe")
  div.content:insert(pandoc.RawBlock("html", '<span class="loupe-aide" aria-hidden="true">' .. t("loupe") .. '</span>'))
  return div
end

-- ::: {.defiler}  liste d'images montrées une à une, en grand ; le texte alternatif sert de légende
local function brique_defiler(div)
  local images, avant = pandoc.List(), pandoc.List()
  for _, bloc in ipairs(div.content) do
    if bloc.t == "BulletList" then
      for _, item in ipairs(bloc.content) do
        pandoc.walk_block(pandoc.Div(item), { Image = function(i) images:insert(i) end })
      end
    else
      avant:insert(bloc)
    end
  end
  if not EN_HTML then
    for _, i in ipairs(images) do avant:insert(pandoc.Para({ i })) end
    div.content = avant
    return div
  end
  local vues = pandoc.List()
  for _, i in ipairs(images) do
    local nom = pandoc.utils.stringify(i.caption)
    vues:insert(pandoc.Div({ pandoc.Plain({ i }) }, pandoc.Attr("", { "defiler-vue" }, { ["data-nom"] = nom })))
  end
  local commande = pandoc.RawBlock("html", '<div class="defiler-commande">'
    .. '<button type="button" class="defiler-bouton" data-pas="-1" aria-label="' .. t("precedente") .. '">◀</button>'
    .. '<span class="defiler-legende" aria-live="polite"></span>'
    .. '<button type="button" class="defiler-bouton" data-pas="1" aria-label="' .. t("suivante") .. '">▶</button></div>')
  -- commande="haut" : boutons et légende au-dessus des images, à position fixe
  if div.attributes["commande"] == "haut" then
    div.classes:insert("commande-haut")
    avant:insert(commande)
    avant:insert(pandoc.Div(vues, pandoc.Attr("", { "defiler-vues" })))
  else
    avant:insert(pandoc.Div(vues, pandoc.Attr("", { "defiler-vues" })))
    avant:insert(commande)
  end
  div.content = avant
  return div
end

-- ::: {.curseur min="1" max="20" pas="0.1" valeur="7.2" unite="°" etiquette="Angle" schema="…svg"}
--   - Tour de la Terre : {5000*360/x} stades        ← les accolades sont recalculées, x = la valeur
local function brique_curseur(div)
  local mini, maxi = attribut(div, "min", "0"), attribut(div, "max", "100")
  local pas, valeur = attribut(div, "pas", "1"), attribut(div, "valeur", "0")
  local unite, etiquette = attribut(div, "unite", ""), attribut(div, "etiquette", "Valeur")
  local chemin = attribut(div, "schema", nil)
  local hauteur = attribut(div, "hauteur", nil)
  if not EN_HTML then return div end
  local avant, lignes = pandoc.List(), ""
  for _, bloc in ipairs(div.content) do
    if bloc.t == "BulletList" then
      for _, item in ipairs(bloc.content) do
        lignes = lignes .. '<li data-modele="' .. echappe(pandoc.utils.stringify(item)) .. '"></li>'
      end
    else
      avant:insert(bloc)
    end
  end
  local h = ""
  if chemin then h = h .. schema_html(chemin, hauteur) end
  h = h .. '<div class="curseur-commande"><label><span class="curseur-etiquette">' .. echappe(etiquette)
      .. (LANGUE == "fr" and ' : ' or ': ') .. '<output class="curseur-valeur"></output></span>'
      .. '<input type="range" class="curseur-entree" min="' .. mini .. '" max="' .. maxi .. '" step="' .. pas
      .. '" value="' .. valeur .. '" data-unite="' .. echappe(unite) .. '"></label></div>'
  if lignes ~= "" then h = h .. '<ul class="curseur-resultats" aria-live="polite">' .. lignes .. '</ul>' end
  avant:insert(pandoc.RawBlock("html", h))
  div.content = avant
  return div
end

-- ::: {.classer}  un titre ### par case, puis la liste de ce qui doit y aller
local function brique_classer(div)
  local avant, cases, etiquettes, rang = pandoc.List(), "", "", 0
  local sans_html = pandoc.List()
  for _, bloc in ipairs(div.content) do
    if bloc.t == "Header" then
      rang = rang + 1
      cases = cases .. '<div class="classer-case" data-case="' .. rang .. '" role="button" tabindex="0">'
          .. '<div class="classer-nom">' .. echappe(typo(pandoc.utils.stringify(bloc.content))) .. '</div>'
          .. '<div class="classer-contenu"></div></div>'
      sans_html:insert(pandoc.Para(pandoc.Strong(bloc.content)))
    elseif bloc.t == "BulletList" and rang > 0 then
      for _, item in ipairs(bloc.content) do
        etiquettes = etiquettes .. '<button type="button" class="classer-etiquette" data-case="' .. rang .. '">'
            .. echappe(typo(pandoc.utils.stringify(item))) .. '</button>'
      end
      sans_html:insert(bloc)
    else
      avant:insert(bloc)
      sans_html:insert(bloc)
    end
  end
  if not EN_HTML then
    div.content = sans_html
    return div
  end
  avant:insert(pandoc.RawBlock("html", '<div class="classer-reserve">' .. etiquettes .. '</div>'
    .. '<div class="classer-cases">' .. cases .. '</div>'
    .. '<p class="classer-etat" aria-live="polite"></p>'))
  div.content = avant
  return div
end

-- ::: {.cap image="…" alt="…" x="50" y="50" depart="90"}  un cap à faire tourner sur une carte marine
local function brique_cap(div)
  local image, alt = attribut(div, "image", ""), attribut(div, "alt", "")
  local x, y = attribut(div, "x", "50"), attribut(div, "y", "50")
  local depart = attribut(div, "depart", "0")
  local img = pandoc.Image({ pandoc.Str(alt) }, image)
  if not EN_HTML then
    table.insert(div.content, 1, pandoc.Para({ img }))
    return div
  end
  div.attributes["data-depart"] = depart
  local texte = pandoc.Div(div.content, pandoc.Attr("", { "cap-texte" }))
  local rose = '<svg class="cap-rose" viewBox="-60 -60 120 120" width="150" height="150" aria-hidden="true">'
      .. '<circle r="52" class="cap-cercle"/>'
  for i = 0, 31 do
    local long = (i % 8 == 0) and 12 or ((i % 4 == 0) and 9 or ((i % 2 == 0) and 6 or 3))
    rose = rose .. string.format('<line class="cap-graduation" x1="0" y1="-52" x2="0" y2="%d" transform="rotate(%s)"/>',
      -52 + long, i * 11.25)
  end
  rose = rose .. '<text class="cap-nord" x="0" y="-30" text-anchor="middle">N</text>'
      .. '<g class="cap-aiguille"><path d="M0 -44 L7 0 L0 8 L-7 0 Z"/></g></svg>'
  div.content = pandoc.List({
    pandoc.Div({
      pandoc.Plain({ img }),
      pandoc.RawBlock("html", '<div class="cap-fleche" style="left:' .. x .. '%;top:' .. y .. '%"><span></span></div>'),
    }, pandoc.Attr("", { "cap-cadre" })),
    pandoc.Div({
      pandoc.RawBlock("html", '<div class="cap-compas">'
        .. '<button type="button" class="cap-bouton" data-pas="-1" aria-label="' .. t("venir_gauche") .. '">◀</button>'
        .. rose
        .. '<button type="button" class="cap-bouton" data-pas="1" aria-label="' .. t("venir_droite") .. '">▶</button></div>'
        .. '<p class="cap-lecture" aria-live="polite"></p>'),
      texte,
    }, pandoc.Attr("", { "cap-cote" })),
  })
  return div
end

-- ::: {.visees image="…" alt="…" objectif="2" solution="1-2 1-3 2-3"}
--   - Nom de la station : gauche,haut      (en % de l'image)
local function brique_visees(div)
  local image, alt = attribut(div, "image", ""), attribut(div, "alt", "")
  local objectif = attribut(div, "objectif", "1")
  local solution = attribut(div, "solution", "")
  local img = pandoc.Image({ pandoc.Str(alt) }, image)
  -- ce qui précède la liste est la consigne ; ce qui la suit est le commentaire de réussite
  local avant, apres, points = pandoc.List(), pandoc.List(), ""
  local n, liste_vue = 0, false
  for _, bloc in ipairs(div.content) do
    if bloc.t == "BulletList" then
      liste_vue = true
      for _, item in ipairs(bloc.content) do
        local brut = pandoc.utils.stringify(item)
        local nom, x, y = brut:match("^(.-)%s*:%s*([%d%.]+)%s*,%s*([%d%.]+)%s*$")
        if nom then
          n = n + 1
          nom = sans_queue(nom)
          points = points .. string.format(
            '<button type="button" class="visee-point" data-rang="%d" data-x="%s" data-y="%s" '
            .. 'style="left:%s%%;top:%s%%" aria-label="%s"><span>%s</span></button>',
            n, x, y, x, y, echappe(nom), echappe(nom))
        end
      end
    elseif liste_vue then
      apres:insert(bloc)
    else
      avant:insert(bloc)
    end
  end
  if not EN_HTML then
    table.insert(avant, 1, pandoc.Para({ img }))
    avant:extend(apres)
    div.content = avant
    return div
  end
  div.attributes["data-objectif"] = objectif
  div.attributes["data-solution"] = solution
  div.content = pandoc.List({
    pandoc.Div({
      pandoc.Plain({ img }),
      pandoc.RawBlock("html", '<svg class="visee-traits" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"></svg>'
        .. points),
    }, pandoc.Attr("", { "visee-cadre" })),
    pandoc.Div({
      pandoc.Div(avant, pandoc.Attr("", { "visee-consigne" })),
      pandoc.RawBlock("html", '<p class="visee-etat" aria-live="polite"></p>'),
      pandoc.Div(apres, pandoc.Attr("", { "visee-retour" })),
      pandoc.RawBlock("html", '<button type="button" class="visee-effacer">' .. t("effacer") .. '</button>'),
    }, pandoc.Attr("", { "visee-cote" })),
  })
  return div
end

----------------------------------------------------------------------------
-- Briques de cartographie : atelier, flash, couleur 3D
-- (leur comportement est dans _briques/briques-carto.html)
----------------------------------------------------------------------------

-- ::: {.atelier donnees="donnees/territoire.json" variable="taux" unite="%"
--      methode="egales" classes="5" palette="sequentielle" reglages="methode,classes,palette"}
-- Une carte vivante : la discrétisation, le nombre de classes et la palette se règlent à l'écran.
local function brique_atelier(div)
  local chemin = attribut(div, "donnees", "")
  local json = lire_fichier(chemin)
  if not EN_HTML then return div end
  if not json then
    return pandoc.Para(pandoc.Str("Données introuvables : " .. chemin))
  end
  local a = function(n, d) return echappe(attribut(div, n, d)) end
  local h = '<div class="atelier-zone" data-variable="' .. a("variable", "taux")
      .. '" data-unite="' .. a("unite", "") .. '" data-methode="' .. a("methode", "egales")
      .. '" data-classes="' .. a("classes", "5") .. '" data-palette="' .. a("palette", "sequentielle")
      .. '" data-reglages="' .. a("reglages", "methode,classes,palette")
      .. '" data-palettes="' .. a("palettes", "sequentielle,arc-en-ciel,divergente")
      .. '" data-histogramme="' .. a("histogramme", "oui") .. '">'
      .. '<script type="application/json" class="atelier-donnees">' .. json:gsub("</", "<\\/") .. '</script>'
      .. '<div class="atelier-carte"></div><div class="atelier-panneau"></div></div>'
  local sortie = pandoc.List({ pandoc.RawBlock("html", h) })
  sortie:extend(div.content)
  div.content = sortie
  return div
end

-- ::: {.flash duree="5"}  ![](images/carte.png) :::
-- L'image n'apparaît qu'au clic, pendant quelques secondes. Dans le PDF, elle est visible.
local function brique_flash(div)
  if not EN_HTML then return div end
  local duree = attribut(div, "duree", "5")
  div.attributes["duree"] = nil
  div.attributes["data-duree"] = duree
  div.content:insert(pandoc.RawBlock("html", '<button type="button" class="flash-bouton" data-voir="'
      .. echappe(t("flash_voir")) .. '" data-revoir="' .. echappe(t("flash_revoir")) .. '">'
      .. echappe(t("flash_voir")) .. ' · ' .. duree .. ' s</button><div class="flash-barre"></div>'))
  return div
end

-- ::: {.couleur3d} :::  le solide des couleurs (teinte, saturation, valeur), qui tourne, et trois curseurs
----------------------------------------------------------------------------
-- Briques d'enquête (cours « Image Intelligence ») : leur comportement est dans
-- _briques/briques-enquete.html
----------------------------------------------------------------------------

local function json_texte(x) return '"' .. tostring(x):gsub('\\', '\\\\'):gsub('"', '\\"'):gsub('\n', ' ') .. '"' end
local function html_de(blocs) return pandoc.write(pandoc.Pandoc(blocs), "html") end
local function sans_insecables(s) return (s:gsub("\u{a0}", " "):gsub("\u{202f}", " ")) end

-- ::: {.coupe image="…" alt="…" depart="8,52" arrivee="92,48" pas="24" profil="donnees/profil.json"}
--   Consigne.
--   ::: {.apres-jeu} Commentaire affiché quand la coupe est terminée. :::
-- Un mini-jeu : le marcheur va de A à B ; ↑ ↓ règlent son altitude, → le fait avancer.
local function brique_coupe(div)
  local image, alt = attribut(div, "image", ""), attribut(div, "alt", "")
  local profil = lire_fichier(attribut(div, "profil", "")) or "[]"
  if not EN_HTML then
    local sortie = pandoc.List({ pandoc.Para({ pandoc.Image({ pandoc.Str(alt) }, image) }) })
    sortie:extend(div.content); div.content = sortie; return div
  end
  local h = '<div class="coupe-zone" tabindex="0" data-depart="' .. echappe(attribut(div, "depart", "5,50"))
      .. '" data-arrivee="' .. echappe(attribut(div, "arrivee", "95,50")) .. '" data-pas="' .. echappe(attribut(div, "pas", "20"))
      .. '" data-hauteur="' .. echappe(attribut(div, "hauteur", "300")) .. '">'
      .. '<script type="application/json" class="coupe-profil">' .. profil:gsub("</", "<\\/") .. '</script>'
      .. '<div class="coupe-image"><img src="' .. echappe(image) .. '" alt="' .. echappe(alt) .. '"></div>'
      .. '<div class="coupe-jeu"></div></div>'
  local sortie = pandoc.List({ pandoc.RawBlock("html", h) }); sortie:extend(div.content)
  div.content = sortie
  return div
end

-- ::: {.arbre image="…" alt="…"}
--   Consigne.
--   ### depart | La question posée à ce nœud ?
--   - Une réponse → autre-noeud
--   ### autre-noeud ! Conclusion
--   Paragraphe d'explication de la conclusion.
-- Un arbre de déduction : chaque choix est un indice ; le chemin parcouru reste affiché.
local function brique_arbre(div)
  local image, alt = attribut(div, "image", ""), attribut(div, "alt", "")
  local consigne, noeuds, courant = pandoc.List(), {}, nil
  for _, bloc in ipairs(div.content) do
    if bloc.t == "Header" then
      local texte = sans_insecables(pandoc.utils.stringify(bloc.content))
      local id, sep, reste = texte:match("^%s*(%S+)%s*([|!])%s*(.*)$")
      courant = { id = id or texte, fin = (sep == "!"), texte = reste or "", choix = {}, corps = pandoc.List() }
      table.insert(noeuds, courant)
    elseif courant and bloc.t == "BulletList" and not courant.fin then
      for _, item in ipairs(bloc.content) do
        local t = sans_insecables(pandoc.utils.stringify(item))
        local libelle, cible = t:match("^(.-)%s*→%s*(%S+)%s*$")
        if not libelle then libelle, cible = t:match("^(.-)%s*%->%s*(%S+)%s*$") end
        table.insert(courant.choix, { libelle = libelle or t, cible = cible or "" })
      end
    elseif courant then courant.corps:insert(bloc)
    else consigne:insert(bloc) end
  end
  local morceaux = {}
  for _, n in ipairs(noeuds) do
    local ch = {}
    for _, c in ipairs(n.choix) do table.insert(ch, '{"t":' .. json_texte(c.libelle) .. ',"v":' .. json_texte(c.cible) .. '}') end
    table.insert(morceaux, '{"id":' .. json_texte(n.id) .. ',"fin":' .. tostring(n.fin) .. ',"q":' .. json_texte(n.texte)
      .. ',"corps":' .. json_texte(html_de(n.corps)) .. ',"choix":[' .. table.concat(ch, ",") .. ']}')
  end
  local sortie = pandoc.List()
  sortie:extend(consigne)
  if not EN_HTML then
    if image ~= "" then sortie:insert(pandoc.Para({ pandoc.Image({ pandoc.Str(alt) }, image) })) end
    for _, n in ipairs(noeuds) do sortie:insert(pandoc.Para({ pandoc.Strong(pandoc.Str(n.texte)) })); sortie:extend(n.corps) end
    div.content = sortie; return div
  end
  local h = '<div class="arbre-zone"><script type="application/json" class="arbre-donnees">[' .. table.concat(morceaux, ","):gsub("</", "<\\/") .. ']</script>'
      .. (image ~= "" and ('<div class="arbre-image"><img src="' .. echappe(image) .. '" alt="' .. echappe(alt) .. '"></div>') or '')
      .. '<div class="arbre-cote"><div class="arbre-chemin"></div><div class="arbre-noeud"></div></div></div>'
  sortie:insert(pandoc.RawBlock("html", h))
  div.content = sortie
  return div
end

-- ::: {.observer cle="description-image"}   la lecture experte, cachée jusqu'à la comparaison :::
-- ::: {.observer cle="note-image" rappel="description-image"}   rappelle ce que l'étudiant avait écrit
local function brique_observer(div)
  local cle, rappel = attribut(div, "cle", ""), attribut(div, "rappel", "")
  local invite = attribut(div, "invite", "")
  if not EN_HTML then return div end
  local h = '<div class="observer-zone" data-cle="' .. echappe(cle) .. '" data-rappel="' .. echappe(rappel)
      .. '" data-invite="' .. echappe(invite) .. '"></div>'
  local expert = pandoc.Div(div.content, pandoc.Attr("", { "observer-expert" }))
  div.content = pandoc.List({ pandoc.RawBlock("html", h), expert })
  return div
end

-- ::: {.indices image="…" alt="…" confiance="oui"}
--   - 20,30,15,10 : Premier indice (la zone, en % de l'image, s'encadre sur l'image)
--   - Deuxième indice, sans zone
--   Paragraphes après la liste : la conclusion.
local function brique_indices(div)
  local image, alt = attribut(div, "image", ""), attribut(div, "alt", "")
  local confiance = attribut(div, "confiance", "non")
  local avant, apres, liste, vu = pandoc.List(), pandoc.List(), {}, false
  for _, bloc in ipairs(div.content) do
    if bloc.t == "BulletList" and not vu then
      vu = true
      for _, item in ipairs(bloc.content) do
        local t = sans_insecables(pandoc.utils.stringify(item))
        local x, y, l, hh, texte = t:match("^%s*([%d%.]+)%s*,%s*([%d%.]+)%s*,%s*([%d%.]+)%s*,%s*([%d%.]+)%s*:%s*(.*)$")
        local zone = x and ('[' .. x .. ',' .. y .. ',' .. l .. ',' .. hh .. ']') or 'null'
        table.insert(liste, '{"z":' .. zone .. ',"t":' .. json_texte(texte or t) .. '}')
      end
    elseif vu then apres:insert(bloc) else avant:insert(bloc) end
  end
  if not EN_HTML then
    local s = pandoc.List(); s:extend(avant)
    s:insert(pandoc.Para({ pandoc.Image({ pandoc.Str(alt) }, image) }))
    s:extend(apres); div.content = s; return div
  end
  local h = '<div class="indices-zone" data-confiance="' .. echappe(confiance) .. '">'
      .. '<script type="application/json" class="indices-donnees">[' .. table.concat(liste, ","):gsub("</", "<\\/") .. ']</script>'
      .. '<div class="indices-image"><img src="' .. echappe(image) .. '" alt="' .. echappe(alt) .. '"></div>'
      .. '<div class="indices-cote"><ol class="indices-liste"></ol><div class="indices-commandes"></div></div></div>'
  local s = pandoc.List(); s:extend(avant); s:insert(pandoc.RawBlock("html", h))
  s:insert(pandoc.Div(apres, pandoc.Attr("", { "indices-conclusion" })))
  div.content = s
  return div
end

-- ::: {.confiance}  un QCM ou une question dans la brique : on dit d'abord sa certitude :::
local function brique_confiance(div)
  if not EN_HTML then return div end
  div.content:insert(1, pandoc.RawBlock("html", '<div class="confiance-barre"></div>'))
  return div
end

-- ::: {.vrai-ia}
--   - ![Légende, année](images/a.jpg) [ia] : Ce qui la trahit.
--   - ![Légende](images/b.jpg) [vrai] : Pourquoi elle est réelle.
local function brique_vrai_ia(div)
  local cartes = {}
  for _, bloc in ipairs(div.content) do
    if bloc.t == "BulletList" then
      for _, item in ipairs(bloc.content) do
        local src, legende, reste = "", "", {}
        pandoc.walk_block(pandoc.Div(item), { Image = function(im)
          src = im.src; legende = pandoc.utils.stringify(im.caption); return {} end })
        local t = sans_insecables(pandoc.utils.stringify(item))
        local verdict = t:match("%[(%a+)%]") or ""
        verdict = verdict:lower()
        local nature = (verdict == "ia" or verdict == "ai") and "ia" or "vrai"
        local explication = t:match("%]%s*:%s*(.*)$") or ""
        table.insert(cartes, '{"src":' .. json_texte(src) .. ',"legende":' .. json_texte(legende)
          .. ',"nature":"' .. nature .. '","e":' .. json_texte(explication) .. '}')
      end
    end
  end
  if not EN_HTML then return div end
  local imgs = ""
  for k, c in ipairs(cartes) do
    local src = c:match('^{"src":"(.-)","legende"') or ""
    imgs = imgs .. '<img class="vraiia-source" data-i="' .. (k - 1) .. '" src="' .. src .. '" alt="" hidden>'
  end
  local h = '<div class="vraiia-zone"><script type="application/json" class="vraiia-donnees">['
      .. table.concat(cartes, ","):gsub("</", "<\\/") .. ']</script>' .. imgs .. '</div>'
  local garde = pandoc.List()
  for _, bloc in ipairs(div.content) do if bloc.t ~= "BulletList" then garde:insert(bloc) end end
  garde:insert(pandoc.RawBlock("html", h))
  div.content = garde
  return div
end

-- ::: {.bilan moment="debut"}  - C1 | Décrire avant d'interpréter  … :::   (moment="fin" : la comparaison)
local function brique_bilan(div)
  local moment = attribut(div, "moment", "debut")
  local comps = {}
  for _, bloc in ipairs(div.content) do
    if bloc.t == "BulletList" then
      for _, item in ipairs(bloc.content) do
        local t = sans_insecables(pandoc.utils.stringify(item))
        local code, texte = t:match("^%s*(%S+)%s*|%s*(.*)$")
        table.insert(comps, '{"c":' .. json_texte(code or t) .. ',"t":' .. json_texte(texte or t) .. '}')
      end
    end
  end
  if not EN_HTML then return div end
  div.content = pandoc.List({ pandoc.RawBlock("html", '<div class="bilan-zone" data-moment="' .. echappe(moment)
    .. '"><script type="application/json" class="bilan-donnees">[' .. table.concat(comps, ",") .. ']</script></div>') })
  return div
end

-- ::: {.revision} :::   le mode révision : toutes les questions du cours, en cartes à répéter
-- ::: {.calibration} :::   la certitude déclarée, comparée à la réussite
local function brique_simple(div, classe)
  if not EN_HTML then return div end
  div.content = pandoc.List({ pandoc.RawBlock("html", '<div class="' .. classe .. '"></div>') })
  return div
end

-- ::: {.transparence-ia profil="✒️ L'Auteur outillé" coordonnees="F2 · R0 · S0" outil="Claude 5"} :::
-- La déclaration de transparence IA (Boussole IA de Géodata Paris), dans la langue du cours.
-- Un texte écrit dans la brique remplace la phrase type.
local function brique_transparence_ia(div)
  local profil = attribut(div, "profil", "")
  local coord = attribut(div, "coordonnees", "")
  local outil = attribut(div, "outil", "Claude")
  local h = '<div class="transparence-titre">─── ' .. echappe(t("ia_titre")) .. ' ─── ' .. echappe(t("ia_boussole")) .. ' ───</div>'
      .. '<p class="transparence-profil"><strong>' .. echappe(t("ia_profil")) .. '</strong> ' .. echappe(profil)
      .. (coord ~= "" and (' — ' .. echappe(t("ia_coordonnees")) .. ' ' .. echappe(coord)) or '') .. '</p>'
  local sortie = pandoc.List({ pandoc.RawBlock("html", h) })
  if #div.content > 0 then
    sortie:extend(div.content)
  else
    sortie:insert(pandoc.RawBlock("html", '<p class="transparence-texte">' .. echappe(string.format(t("ia_texte"), outil)) .. '</p>'))
  end
  div.content = sortie
  for _, k in ipairs({ "profil", "coordonnees", "outil" }) do div.attributes[k] = nil end
  return div
end

-- ::: {.puzzle-legende carte="images/schemas/legende-carte.svg" alt="…"}
--   Consigne (paragraphes avant les listes).
--   1. titre | Coupes rases             liste numérotée : les pièces justes, dans l'ordre de lecture
--   2. = point #000 | Scierie           « = » : même rang que la pièce précédente (ordre libre entre elles)
--   - sous-titre | Surface (%) : Une surface se mesure en hectares.   liste à puces : pièces fausses et leur commentaire
--   Texte final (paragraphes après les listes) : affiché quand la légende est complète.
-- Figurés : titre, sous-titre, aplat COULEUR, ligne COULEUR, point COULEUR, cercles R1,R2,R3 (rayons en unités de la carte).
local function json_chaine(s)
  s = s:gsub('\\', '\\\\'):gsub('"', '\\"'):gsub('\n', ' ')
  return '"' .. s .. '"'
end
local function piece_lue(texte, juste)
  local rang_egal = false
  texte = texte:gsub("\u{a0}", " "):gsub("\u{202f}", " "):gsub("^%s+", "")
  if texte:sub(1, 2) == "= " then rang_egal = true; texte = texte:sub(3) end
  local figure, reste = texte:match("^(.-)%s*|%s*(.*)$")
  if not figure then figure, reste = "", texte end
  local libelle, commentaire = reste, ""
  if not juste then
    local a, b = reste:find(" : ", 1, true)
    if a then libelle, commentaire = reste:sub(1, a - 1), reste:sub(b + 1) end
  end
  local sorte, param = figure:match("^(%S+)%s*(.*)$")
  return { sorte = sorte or "", param = param or "", libelle = libelle, commentaire = commentaire, egal = rang_egal }
end
local function brique_puzzle_legende(div)
  local carte = attribut(div, "carte", "")
  local alt = attribut(div, "alt", "")
  local avant, apres, justes, fausses = pandoc.List(), pandoc.List(), {}, {}
  local vu_liste = false
  for _, bloc in ipairs(div.content) do
    if bloc.t == "OrderedList" then
      vu_liste = true
      for _, item in ipairs(bloc.content) do table.insert(justes, piece_lue(pandoc.utils.stringify(item), true)) end
    elseif bloc.t == "BulletList" then
      vu_liste = true
      for _, item in ipairs(bloc.content) do table.insert(fausses, piece_lue(pandoc.utils.stringify(item), false)) end
    elseif vu_liste then apres:insert(bloc) else avant:insert(bloc) end
  end
  local morceaux, rang = {}, 0
  for _, p in ipairs(justes) do
    if not p.egal or rang == 0 then rang = rang + 1 end
    table.insert(morceaux, '{"s":' .. json_chaine(p.sorte) .. ',"p":' .. json_chaine(p.param) .. ',"t":' .. json_chaine(p.libelle)
      .. ',"r":' .. rang .. '}')
  end
  for _, p in ipairs(fausses) do
    table.insert(morceaux, '{"s":' .. json_chaine(p.sorte) .. ',"p":' .. json_chaine(p.param) .. ',"t":' .. json_chaine(p.libelle)
      .. ',"r":0,"e":' .. json_chaine(p.commentaire) .. '}')
  end
  if not EN_HTML then
    -- hors écran : la légende attendue, en liste
    local l = pandoc.List()
    for _, p in ipairs(justes) do l:insert({ pandoc.Plain(pandoc.Str(p.libelle)) }) end
    local sortie = pandoc.List()
    sortie:extend(avant)
    sortie:insert(pandoc.Para({ pandoc.Image({ pandoc.Str(alt) }, carte) }))
    sortie:insert(pandoc.OrderedList(l))
    sortie:extend(apres)
    div.content = sortie
    return div
  end
  local h = '<div class="puzzle-zone"><script type="application/json" class="puzzle-donnees">['
      .. table.concat(morceaux, ",") .. ']</script>'
      .. '<div class="puzzle-gauche"><img class="puzzle-carte" src="' .. echappe(carte) .. '" alt="' .. echappe(alt) .. '">'
      .. '<div class="puzzle-reserve" aria-label="' .. echappe(t("pieces")) .. '"></div></div>'
      .. '<div class="puzzle-droite"><div class="puzzle-consigne"></div><div class="puzzle-cadre"></div>'
      .. '<div class="puzzle-message" aria-live="polite"></div><div class="puzzle-fin"></div>'
      .. '<button type="button" class="ordre-recommencer puzzle-recommencer">' .. t("recommencer") .. '</button></div></div>'
  local sortie = pandoc.List({ pandoc.RawBlock("html", h) })
  sortie:insert(pandoc.Div(avant, pandoc.Attr("", { "puzzle-texte-consigne" })))
  sortie:insert(pandoc.Div(apres, pandoc.Attr("", { "puzzle-texte-fin" })))
  div.content = sortie
  div.attributes["carte"], div.attributes["alt"] = nil, nil
  return div
end

-- ::: {.synthese} :::  synthèse additive (RVB, sur du noir) et soustractive (CMJ, sur du blanc),
-- trois cercles et trois curseurs par mode ; la couleur du centre est donnée
local function brique_synthese(div)
  if not EN_HTML then return div end
  div.content:insert(1, pandoc.RawBlock("html", '<div class="synthese-zone"></div>'))
  return div
end

local function brique_couleur3d(div)
  if not EN_HTML then return div end
  div.content:insert(1, pandoc.RawBlock("html", '<canvas class="couleur3d-toile" width="760" height="500"></canvas>'
      .. '<div class="couleur3d-panneau"></div>'))
  return div
end

local function briques(div)
  if div.classes:includes("question") then return brique_question(div) end
  if div.classes:includes("reponse") then return brique_reponse(div) end
  if div.classes:includes("qcm") then return brique_qcm(div) end
  if div.classes:includes("ordre") then return brique_ordre(div) end
  if div.classes:includes("zones") then return brique_zones(div) end
  if div.classes:includes("codes-niveau") then return brique_codes() end
  if div.classes:includes("schema") then return brique_schema(div) end
  if div.classes:includes("plus") then return brique_plus(div) end
  if div.classes:includes("pivoter") then return brique_pivoter(div) end
  if div.classes:includes("comparer") then return brique_comparer(div) end
  if div.classes:includes("curseur") then return brique_curseur(div) end
  if div.classes:includes("loupe") then return brique_loupe(div) end
  if div.classes:includes("defiler") then return brique_defiler(div) end
  if div.classes:includes("classer") then return brique_classer(div) end
  if div.classes:includes("cap") then return brique_cap(div) end
  if div.classes:includes("visees") then return brique_visees(div) end
  if div.classes:includes("atelier") then return brique_atelier(div) end
  if div.classes:includes("flash") then return brique_flash(div) end
  if div.classes:includes("couleur3d") then return brique_couleur3d(div) end
  if div.classes:includes("synthese") then return brique_synthese(div) end
  if div.classes:includes("puzzle-legende") then return brique_puzzle_legende(div) end
  if div.classes:includes("transparence-ia") then return brique_transparence_ia(div) end
  if div.classes:includes("coupe") then return brique_coupe(div) end
  if div.classes:includes("arbre") then return brique_arbre(div) end
  if div.classes:includes("observer") then return brique_observer(div) end
  if div.classes:includes("indices") then return brique_indices(div) end
  if div.classes:includes("confiance") then return brique_confiance(div) end
  if div.classes:includes("vrai-ia") then return brique_vrai_ia(div) end
  if div.classes:includes("bilan") then return brique_bilan(div) end
  if div.classes:includes("revision") then return brique_simple(div, "revision-zone") end
  if div.classes:includes("calibration") then return brique_simple(div, "calibration-zone") end
  return nil
end

----------------------------------------------------------------------------
-- Carte du cours : la liste des diapos, rangées par niveau
----------------------------------------------------------------------------

local function carte_du_cours(inventaire, parties, seulement)
  if not EN_HTML then
    local groupes = pandoc.List()
    for _, n in ipairs(NIVEAUX) do
      local sous = pandoc.List()
      for _, d in ipairs(inventaire[n]) do sous:insert({ pandoc.Plain(pandoc.Str(d.titre)) }) end
      groupes:insert({ pandoc.Plain(pandoc.Strong(pandoc.Str(LIBELLE[n]))), pandoc.BulletList(sous) })
    end
    return pandoc.BulletList(groupes)
  end
  local liste = NIVEAUX
  if seulement and seulement ~= "" then
    liste = {}
    for mot in seulement:gmatch("%a+") do table.insert(liste, mot) end
  end
  local plus_longue = 0
  for _, n in ipairs(liste) do plus_longue = math.max(plus_longue, #inventaire[n]) end
  local h = ''
  if #parties > 0 and #liste > 1 then
    h = h .. '<p class="carte-parties">'
    for i, pt in ipairs(parties) do
      h = h .. '<a href="#/' .. pt.id .. '"><span class="puce-partie partie-' .. i .. '">' .. i .. '</span>'
          .. echappe(pt.titre) .. '</a>'
    end
    h = h .. '</p>'
  end
  h = h .. '<div class="carte-du-cours' .. (plus_longue > 8 and ' dense' or '')
      .. (#liste == 1 and ' un-niveau' or '') .. '">'
  for _, n in ipairs(liste) do
    local nb = #inventaire[n]
    h = h .. '<div class="carte-colonne niveau-' .. n .. '"><div class="carte-tete">' .. glyphe(n, 54)
        .. '<div><div class="niveau-mot">' .. LIBELLE[n] .. '</div><div class="carte-compte">'
        .. nb .. ' ' .. (nb > 1 and t("diapos") or t("diapo")) .. '</div></div></div><ul>'
    for _, d in ipairs(inventaire[n]) do
      h = h .. '<li><a href="#/' .. d.id .. '"><span class="puce-partie partie-' .. d.partie .. '">'
          .. (d.partie > 0 and d.partie or '') .. '</span>' .. echappe(d.titre) .. '</a></li>'
    end
    h = h .. '</ul></div>'
  end
  h = h .. '</div>'
  return pandoc.RawBlock("html", h)
end

----------------------------------------------------------------------------
-- Fiches : le plan du cours, porté par chaque diapo
----------------------------------------------------------------------------

local ETATS = { fige = "figé", ["a-revoir"] = "à revoir", ["a-realiser"] = "à réaliser" }

-- Le texte d'un bloc, en gardant les retours à la ligne tels qu'ils sont écrits.
local function texte_avec_lignes(blocs)
  local morceaux = {}
  for _, bloc in ipairs(blocs) do
    if bloc.content then
      local ligne = pandoc.List()
      for _, el in ipairs(bloc.content) do
        if el.t == "SoftBreak" or el.t == "LineBreak" then
          table.insert(morceaux, pandoc.utils.stringify(pandoc.Plain(ligne)))
          ligne = pandoc.List()
        else
          ligne:insert(el)
        end
      end
      table.insert(morceaux, pandoc.utils.stringify(pandoc.Plain(ligne)))
    end
  end
  return morceaux
end

-- ::: {.fiche n="1.9" etat="fige"}  Intention : … / Expérience : … / Demande : …
local function lire_fiche(div)
  local fiche = { n = div.attributes["n"] or "", etat = div.attributes["etat"] or "a-revoir",
                  intention = "", experience = "", demande = "" }
  local champ = nil
  for _, ligne in ipairs(texte_avec_lignes(div.content)) do
    local cle, reste = ligne:match("^%s*([^:]-)%s*:%s*(.*)$")
    local c = cle and cle:lower() or ""
    if c:match("^int") then champ = "intention"
    elseif c:match("^exp") then champ = "experience"
    elseif c:match("^dem") or c:match("^req") then champ = "demande"
    else reste = ligne end
    if champ then
      fiche[champ] = (fiche[champ] ~= "" and (fiche[champ] .. " ") or "") .. (reste or "")
    end
  end
  return fiche
end

local function cellule(texte)
  return ((texte or ""):gsub("|", "/"):gsub("%s+", " "):gsub("^%s+", ""):gsub("%s+$", ""))
end

-- Écrit plan.md à côté du cours : une vue d'ensemble, régénérée à chaque compilation.
local function ecrire_plan(fiches, titre_cours)
  if #fiches == 0 then return end
  local entree = (quarto and quarto.doc and quarto.doc.input_file)
      or (PANDOC_STATE and PANDOC_STATE.input_files[1]) or ""
  -- le fichier du cours donne plan.md ; sa version anglaise (nom en « -en.qmd ») donne plan-en.md
  local nom_source = pandoc.path.filename(entree)
  local suffixe = nom_source:lower():match("%-en%.qmd$") and "-en" or ""
  local chemin = pandoc.path.join({ pandoc.path.directory(entree), "plan" .. suffixe .. ".md" })
  local comptes, demandes = {}, {}
  local l = {
    "# Plan — " .. titre_cours, "",
    "> Fichier généré à chaque compilation à partir des fiches de `" .. nom_source .. "`.",
    "> Ne pas le modifier : pour changer le plan, modifier les fiches.", "",
    "| N° | Diapo | Niveau | État | Intention | Expérience | Demande |",
    "|----|-------|--------|------|-----------|------------|---------|",
  }
  for _, f in ipairs(fiches) do
    comptes[f.etat] = (comptes[f.etat] or 0) + 1
    if f.demande ~= "" then table.insert(demandes, f) end
    table.insert(l, string.format("| %s | %s | %s | %s | %s | %s | %s |", cellule(f.n), cellule(f.titre),
      cellule(f.niveau), ETATS[f.etat] or f.etat, cellule(f.intention), cellule(f.experience), cellule(f.demande)))
  end
  table.insert(l, "")
  table.insert(l, "## Où en est-on")
  table.insert(l, "")
  table.insert(l, string.format("- %d diapos, dont %d figées, %d à revoir, %d à réaliser.", #fiches,
    comptes["fige"] or 0, comptes["a-revoir"] or 0, comptes["a-realiser"] or 0))
  if #demandes > 0 then
    table.insert(l, "- Demandes en attente :")
    for _, f in ipairs(demandes) do
      table.insert(l, "    - " .. f.n .. " " .. cellule(f.titre) .. " — " .. cellule(f.demande))
    end
  else
    table.insert(l, "- Aucune demande en attente.")
  end
  local f = io.open(chemin, "w")
  if f then f:write(table.concat(l, "\n") .. "\n"); f:close() end
end

----------------------------------------------------------------------------
-- Passage principal
----------------------------------------------------------------------------

local function lire_reglages(meta)
  local langue = meta["lang"] and pandoc.utils.stringify(meta["lang"]):sub(1, 2):lower() or "fr"
  LANGUE = TEXTES[langue] and langue or "fr"
  LIBELLE = LIBELLES[LANGUE]
  local g = meta["garder-niveaux"]
  if g then
    garder = {}
    local texte = pandoc.utils.stringify(g)
    for mot in texte:gmatch("[%a]+") do garder[mot:lower()] = true end
  end
  local m = meta["masquer-optionnels"]
  if m then
    local v = pandoc.utils.stringify(m):lower()
    masquer_optionnels = (v == "true" or v == "oui")
  end
end

function Pandoc(doc)
  lire_reglages(doc.meta)

  -- 1er passage : trier les diapos, dresser l'inventaire par niveau et la liste des parties
  local inventaire = { socle = {}, appui = {}, veille = {} }
  local parties, id_carte, dernier_id = {}, nil, nil
  local gardes, saute = pandoc.List(), false
  local fiches, diapo = {}, { titre = "Couverture", niveau = "" }
  for _, bloc in ipairs(doc.blocks) do
    if bloc.t == "Header" and bloc.level == 2 then
      local niv = niveau_de(bloc.classes)
      local mention = niv and LIBELLE[niv] or ""
      if bloc.classes:includes("intercalaire") then mention = "partie" end
      if bloc.classes:includes("optionnel") then mention = mention .. (mention ~= "" and ", " or "") .. "option" end
      diapo = { titre = pandoc.utils.stringify(bloc.content), niveau = mention }
    end
    if bloc.t == "Div" and bloc.classes:includes("fiche") then
      local f = lire_fiche(bloc)
      f.titre, f.niveau = diapo.titre, diapo.niveau
      table.insert(fiches, f)
      goto suivant
    end
    if bloc.t == "Header" and bloc.level <= 2 then
      saute = false
      if bloc.level == 2 then
        local n = niveau_de(bloc.classes)
        if masquer_optionnels and bloc.classes:includes("optionnel") then saute = true end
        if garder and n and not garder[n] then saute = true end
        if not saute then
          dernier_id = bloc.identifier
          local titre = typo(pandoc.utils.stringify(bloc.content))
          if bloc.classes:includes("intercalaire") then
            table.insert(parties, { titre = titre, id = bloc.identifier })
          elseif n then
            table.insert(inventaire[n], { titre = titre, id = bloc.identifier, partie = #parties })
          end
        end
      end
    elseif bloc.t == "Div" and bloc.classes:includes("carte-du-cours") and not saute then
      id_carte = dernier_id
    end
    if not saute then gardes:insert(bloc) end
    ::suivant::
  end
  if EN_HTML then ecrire_plan(fiches, pandoc.utils.stringify(doc.meta.title or "")) end

  -- 2e passage : habiller chaque diapo
  local sortie, partie = pandoc.List(), 0
  for _, bloc in ipairs(gardes) do
    if bloc.t == "Header" and bloc.level == 2 and bloc.classes:includes("intercalaire") then
      partie = partie + 1
      bloc.classes:insert("partie-" .. (((partie - 1) % 5) + 1))
      bloc.attributes["data-state"] = "plein"
      sortie:insert(bloc)
      if EN_HTML then
        sortie:insert(pandoc.RawBlock("html", '<div class="numero-partie" aria-hidden="true">' .. partie .. '</div>'))
      end
    elseif bloc.t == "Header" and bloc.level == 2 and bloc.classes:includes("fin") then
      bloc.attributes["data-state"] = "plein"
      sortie:insert(bloc)
    elseif bloc.t == "Header" and bloc.level == 2 then
      local n = niveau_de(bloc.classes)
      local perle = bloc.attributes["perle"]
      if bloc.classes:includes("image-pleine") then bloc.attributes["data-state"] = "plein" end
      if n and EN_HTML then
        -- Le pictogramme passe devant le titre ; il ramène à la carte du cours quand elle existe.
        local picto = glyphe(n, 58)
        if id_carte then
          picto = '<a class="niveau-picto" href="#/' .. id_carte .. '" title="' .. t("retour_carte") .. '" '
              .. 'aria-label="' .. LIBELLE[n] .. ' — ' .. t("retour_carte") .. '">' .. picto .. '</a>'
        else
          picto = '<span class="niveau-picto">' .. picto .. '</span>'
        end
        local mot = '<span class="niveau-mot">' .. LIBELLE[n]
        if perle and perle ~= "" then mot = mot .. '<span class="niveau-perle">' .. echappe(perle) .. '</span>' end
        mot = mot .. '</span>'
        bloc.content = pandoc.List({
          pandoc.RawInline("html", picto),
          pandoc.RawInline("html", mot),
          pandoc.Span(bloc.content, pandoc.Attr("", { "titre-texte" })),
        })
      elseif n then
        local titre = pandoc.List({ pandoc.Str(LIBELLE[n] .. " ·"), pandoc.Space() })
        titre:extend(bloc.content)
        bloc.content = titre
      end
      sortie:insert(bloc)
    elseif bloc.t == "Div" and bloc.classes:includes("carte-du-cours") then
      sortie:insert(carte_du_cours(inventaire, parties, bloc.attributes["niveaux"]))
    else
      sortie:insert(bloc)
    end
  end
  doc.blocks = sortie

  -- 3e passage : les briques d'exercice, où qu'elles soient
  return doc:walk({ Div = briques, Inlines = typo_inlines })
end
