--[[
  gabarit.lua — le « moteur » des supports de cours.

  Il lit le Markdown et fabrique :
    1. le repère de niveau (socle / appui / veille) sur chaque diapo ;
    2. la diapo « carte du cours », générée toute seule ;
    3. les briques d'exercice (question, qcm, ordre, zones) ;
    4. le tri des diapos (ne garder qu'un niveau, masquer les optionnelles).

  On n'a normalement pas besoin de modifier ce fichier pour écrire un cours.
]]

local NIVEAUX = { "socle", "appui", "veille" }
local LIBELLE = { socle = "Socle", appui = "Appui", veille = "Veille" }
local TEXTE_PPT = { socle = "▰▰▰ Socle", appui = "▰▰ Appui", veille = "▱ Veille" }

local EN_HTML = FORMAT:match("revealjs") ~= nil

-- Réglages lus dans l'en-tête du cours (ou donnés en ligne de commande avec -M)
local garder = nil            -- nil = tous les niveaux
local masquer_optionnels = false
local code_niveau = "quantite" -- quantite | position | pastille

----------------------------------------------------------------------------
-- Outils
----------------------------------------------------------------------------

local function echappe(s)
  return (s:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"):gsub('"', "&quot;"))
end

local function niveau_de(classes)
  for _, n in ipairs(NIVEAUX) do
    if classes:includes(n) then return n end
  end
  return nil
end

-- Une strate : un trait épais avec un décrochement, comme dans le logo Géodata.
local function strate(y, mode)
  local d = string.format("M2 %d H15 L24 %d H46", y, y - 5)
  if mode == "plein" then
    return '<path d="' .. d .. '" stroke="currentColor" stroke-width="5.5" fill="none" stroke-linejoin="round"/>'
  elseif mode == "contour" then
    return '<path d="' .. d .. '" stroke="currentColor" stroke-width="6" fill="none" stroke-linejoin="round"/>'
        .. '<path d="' .. d .. '" stroke="#fff" stroke-width="2.4" fill="none" stroke-linejoin="round"/>'
  else -- fantôme : strate présente mais éteinte
    return '<path d="' .. d .. '" stroke="currentColor" stroke-opacity="0.18" stroke-width="5.5" fill="none" stroke-linejoin="round"/>'
  end
end

-- Dessin du repère de niveau. Trois codes possibles, pour comparer.
local function glyphe(niveau, code)
  code = code or code_niveau
  if code == "pastille" then
    local lettre = niveau:sub(1, 1):upper()
    return '<span class="pastille pastille-' .. niveau .. '" aria-hidden="true">' .. lettre .. '</span>'
  end
  local traits
  if code == "position" then
    -- la strate concernée est allumée, les deux autres sont éteintes
    traits = strate(30, niveau == "socle" and "plein" or "fantome")
          .. strate(20, niveau == "appui" and "plein" or "fantome")
          .. strate(10, niveau == "veille" and "plein" or "fantome")
  else
    -- quantité : trois strates pleines, deux, puis une seule en contour
    if niveau == "socle" then
      traits = strate(30, "plein") .. strate(20, "plein") .. strate(10, "plein")
    elseif niveau == "appui" then
      traits = strate(30, "plein") .. strate(20, "plein")
    else
      traits = strate(30, "contour")
    end
  end
  return '<svg class="strates" viewBox="0 0 48 36" width="48" height="36" aria-hidden="true">' .. traits .. '</svg>'
end

local function repere_html(niveau, perle, code)
  local h = '<div class="niveau niveau-' .. niveau .. '">' .. glyphe(niveau, code)
      .. '<span class="niveau-texte"><span class="niveau-mot">' .. LIBELLE[niveau] .. '</span>'
  if perle and perle ~= "" then
    h = h .. '<span class="niveau-perle">' .. echappe(perle) .. '</span>'
  end
  return h .. '</span></div>'
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

-- ::: {.codes-niveau}  → planche de comparaison des trois codes visuels (diapo de test)
local function brique_codes()
  if not EN_HTML then
    return pandoc.Para(pandoc.Str("Comparaison des codes de niveau : à voir dans la version HTML."))
  end
  local noms = {
    { "quantite", "A · Quantité", "Trois strates, deux, puis une en contour." },
    { "position", "B · Position", "La strate concernée s’allume : en bas, au milieu, en haut." },
    { "pastille", "C · Pastille", "Une lettre et une couleur de la charte." },
  }
  local h = '<div class="codes-niveau">'
  for _, c in ipairs(noms) do
    h = h .. '<div class="code"><h3>' .. c[2] .. '</h3><p class="legende">' .. c[3] .. '</p>'
    for _, n in ipairs(NIVEAUX) do
      h = h .. '<div class="niveau niveau-' .. n .. ' en-ligne">' .. glyphe(n, c[1])
          .. '<span class="niveau-texte"><span class="niveau-mot">' .. LIBELLE[n] .. '</span></span></div>'
    end
    h = h .. '</div>'
  end
  return pandoc.RawBlock("html", h .. '</div>')
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

local function carte_du_cours(inventaire)
  if EN_HTML then
    local h = '<div class="carte-du-cours">'
    for _, n in ipairs(NIVEAUX) do
      h = h .. '<div class="carte-colonne"><div class="niveau niveau-' .. n .. ' en-ligne">' .. glyphe(n)
          .. '<span class="niveau-texte"><span class="niveau-mot">' .. LIBELLE[n] .. '</span>'
          .. '<span class="niveau-perle">' .. #inventaire[n] .. ' diapo' .. (#inventaire[n] > 1 and 's' or '')
          .. '</span></span></div><ul>'
      for _, titre in ipairs(inventaire[n]) do h = h .. '<li>' .. echappe(titre) .. '</li>' end
      h = h .. '</ul></div>'
    end
    return pandoc.RawBlock("html", h .. '</div>')
  end
  local groupes = pandoc.List()
  for _, n in ipairs(NIVEAUX) do
    local sous = pandoc.List()
    for _, titre in ipairs(inventaire[n]) do sous:insert({ pandoc.Plain(pandoc.Str(titre)) }) end
    groupes:insert({ pandoc.Plain(pandoc.Strong(pandoc.Str(TEXTE_PPT[n]))), pandoc.BulletList(sous) })
  end
  return pandoc.BulletList(groupes)
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
  local c = meta["code-niveau"]
  if c then code_niveau = pandoc.utils.stringify(c) end
end

function Pandoc(doc)
  lire_reglages(doc.meta)

  -- 1er passage : trier les diapos et dresser l'inventaire par niveau
  local inventaire = { socle = {}, appui = {}, veille = {} }
  local gardes, saute, partie = pandoc.List(), false, 0
  for _, bloc in ipairs(doc.blocks) do
    if bloc.t == "Header" and bloc.level <= 2 then
      saute = false
      if bloc.level == 2 then
        local n = niveau_de(bloc.classes)
        if masquer_optionnels and bloc.classes:includes("optionnel") then saute = true end
        if garder and n and not garder[n] then saute = true end
        if n and not saute then
          table.insert(inventaire[n], pandoc.utils.stringify(bloc.content))
        end
      end
    end
    if not saute then gardes:insert(bloc) end
  end

  -- 2e passage : habiller chaque diapo
  local sortie = pandoc.List()
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
      if n and not EN_HTML then
        local titre = pandoc.List({ pandoc.Str(TEXTE_PPT[n] .. " ·"), pandoc.Space() })
        titre:extend(bloc.content)
        bloc.content = titre
      end
      sortie:insert(bloc)
      if n and EN_HTML then
        sortie:insert(pandoc.RawBlock("html", repere_html(n, perle)))
      end
    elseif bloc.t == "Div" and bloc.classes:includes("carte-du-cours") then
      sortie:insert(carte_du_cours(inventaire))
    else
      sortie:insert(bloc)
    end
  end
  doc.blocks = sortie

  -- 3e passage : les briques d'exercice, où qu'elles soient
  return doc:walk({ Div = briques })
end
