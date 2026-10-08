--[[
  gabarit.lua — le « moteur » des supports de cours.

  Il lit le Markdown et fabrique :
    1. le pictogramme de niveau (socle / appui / veille) devant le titre de chaque diapo ;
    2. la diapo « carte du cours », générée toute seule ;
    3. les briques d'exercice (question, qcm, ordre, zones) ;
    4. le tri des diapos (ne garder qu'un niveau, masquer les optionnelles).

  On n'a normalement pas besoin de modifier ce fichier pour écrire un cours.
]]

local NIVEAUX = { "socle", "appui", "veille" }
local LIBELLE = { socle = "Socle", appui = "Appui", veille = "Veille" }

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
  return (texte:gsub(" ([%?!:;»])", INSECABLE .. "%1"):gsub("« ", "«" .. INSECABLE))
end
local function typo_inlines(inlines)
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
  local etiquette = div.attributes["etiquette"] or "Question"
  div.attributes["etiquette"] = nil
  table.insert(div.content, 1, pandoc.Div(pandoc.Plain(pandoc.Str(etiquette)), pandoc.Attr("", { "etiquette" })))
  return div
end

-- ::: {.reponse}  … :::   → n'apparaît qu'au clic suivant
local function brique_reponse(div)
  local etiquette = div.attributes["etiquette"] or "Réponse"
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
    sortie:insert(pandoc.Div(pandoc.Para(pandoc.Str("Réponse : " .. table.concat(bonnes, " ; "))),
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
          .. '<button type="button" class="ordre-recommencer">Recommencer</button></div>'))
      else
        -- hors écran : on mélange de façon fixe, la solution va dans les notes
        local n, melange, solution = #bloc.content, pandoc.List(), pandoc.List()
        for i = n, 1, -1 do if i % 2 == 0 then melange:insert(bloc.content[i]) end end
        for i = 1, n do if i % 2 == 1 then melange:insert(bloc.content[i]) end end
        for i, item in ipairs(bloc.content) do
          solution:insert(i .. ". " .. pandoc.utils.stringify(item))
        end
        sortie:insert(pandoc.BulletList(melange))
        sortie:insert(pandoc.Div(pandoc.Para(pandoc.Str("Ordre attendu : " .. table.concat(solution, " — "))),
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
  div.attributes["image"], div.attributes["alt"] = nil, nil
  local avant, boutons = pandoc.List(), {}
  for _, bloc in ipairs(div.content) do
    if bloc.t == "BulletList" then
      for _, item in ipairs(bloc.content) do
        local juste, texte = lire_case(item)
        local brut = pandoc.utils.stringify(texte or item[1].content)
        local x, y, l, h, retour = brut:match("^%s*([%d%.]+)%s*,%s*([%d%.]+)%s*,%s*([%d%.]+)%s*,%s*([%d%.]+)%s*:?%s*(.*)$")
        if x then
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
  }, pandoc.Attr("", { "zones-cadre" }))
  avant:insert(cadre)
  avant:insert(pandoc.RawBlock("html", '<p class="zones-retour" aria-live="polite">Cliquez sur l’image.</p>'))
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

local function briques(div)
  if div.classes:includes("question") then return brique_question(div) end
  if div.classes:includes("reponse") then return brique_reponse(div) end
  if div.classes:includes("qcm") then return brique_qcm(div) end
  if div.classes:includes("ordre") then return brique_ordre(div) end
  if div.classes:includes("zones") then return brique_zones(div) end
  if div.classes:includes("codes-niveau") then return brique_codes() end
  return nil
end

----------------------------------------------------------------------------
-- Carte du cours : la liste des diapos, rangées par niveau
----------------------------------------------------------------------------

local function carte_du_cours(inventaire, parties)
  if not EN_HTML then
    local groupes = pandoc.List()
    for _, n in ipairs(NIVEAUX) do
      local sous = pandoc.List()
      for _, d in ipairs(inventaire[n]) do sous:insert({ pandoc.Plain(pandoc.Str(d.titre)) }) end
      groupes:insert({ pandoc.Plain(pandoc.Strong(pandoc.Str(LIBELLE[n]))), pandoc.BulletList(sous) })
    end
    return pandoc.BulletList(groupes)
  end
  local h = ''
  if #parties > 0 then
    h = h .. '<p class="carte-parties">'
    for i, pt in ipairs(parties) do
      h = h .. '<a href="#/' .. pt.id .. '"><span class="puce-partie partie-' .. i .. '">' .. i .. '</span>'
          .. echappe(pt.titre) .. '</a>'
    end
    h = h .. '</p>'
  end
  h = h .. '<div class="carte-du-cours">'
  for _, n in ipairs(NIVEAUX) do
    local nb = #inventaire[n]
    h = h .. '<div class="carte-colonne niveau-' .. n .. '"><div class="carte-tete">' .. glyphe(n, 54)
        .. '<div><div class="niveau-mot">' .. LIBELLE[n] .. '</div><div class="carte-compte">'
        .. nb .. ' diapo' .. (nb > 1 and 's' or '') .. '</div></div></div><ul>'
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
-- Passage principal
----------------------------------------------------------------------------

local function lire_reglages(meta)
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
  for _, bloc in ipairs(doc.blocks) do
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
  end

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
          picto = '<a class="niveau-picto" href="#/' .. id_carte .. '" title="Retour à la carte du cours" '
              .. 'aria-label="' .. LIBELLE[n] .. ' — retour à la carte du cours">' .. picto .. '</a>'
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
      sortie:insert(carte_du_cours(inventaire, parties))
    else
      sortie:insert(bloc)
    end
  end
  doc.blocks = sortie

  -- 3e passage : les briques d'exercice, où qu'elles soient
  return doc:walk({ Div = briques, Inlines = typo_inlines })
end
