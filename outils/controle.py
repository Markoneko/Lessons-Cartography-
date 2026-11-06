#!/usr/bin/env python3
"""Contrôle d'un support produit : débordements, erreurs JavaScript, planches contact.

    python3 outils/controle.py cours/gis-basics/_sortie/GIS-Basics.html
    python3 outils/controle.py cours/gis-basics/_sortie/GIS-Basics.html --images /tmp/captures

Chaque diapo est affichée en 1280 × 720 avec toutes ses étapes déroulées (réponses ouvertes).
Une diapo dont le contenu sort du cadre est signalée « DÉBORDE ». Avec --images, chaque diapo est
capturée, et des planches de neuf diapos (planche-1.png, …) sont assemblées pour une relecture rapide.
Il faut Playwright (voir outils/pdf.py) ; les planches demandent aussi Pillow.
"""
import asyncio
import glob
import os
import sys

MESURE = """() => {
  const s = Reveal.getCurrentSlide(); let bas = 0, droite = 0;
  s.querySelectorAll('*').forEach(e => {
    const st = getComputedStyle(e);
    if (st.display == 'none' || st.visibility == 'hidden' || e.closest('.plus-panneau')) return;
    if (e.tagName.toLowerCase() != 'svg' && e.closest('svg')) return;   // un dessin se mesure en entier
    const q = e.getBoundingClientRect(); if (q.width == 0) return;
    bas = Math.max(bas, q.bottom); droite = Math.max(droite, q.right);
  });
  const h = s.querySelector('h2');
  return { titre: h ? h.textContent.trim() : '', bas: Math.round(bas), droite: Math.round(droite) };
}"""


async def controler(html, dossier_images=None):
    from playwright.async_api import async_playwright
    erreurs, rapport = [], []
    async with async_playwright() as p:
        navigateur = await p.chromium.launch()
        page = await navigateur.new_page(viewport={"width": 1280, "height": 720})
        page.on("pageerror", lambda e: erreurs.append(str(e)))
        await page.goto("file://" + os.path.abspath(html))
        await page.wait_for_function("window.Reveal && Reveal.isReady && Reveal.isReady()", timeout=60000)
        await page.wait_for_timeout(800)
        n = await page.evaluate("Reveal.getTotalSlides()")
        for i in range(n):
            await page.evaluate(f"Reveal.slide({i}, 0, 99)")
            await page.wait_for_timeout(250)
            info = await page.evaluate(MESURE)
            if dossier_images:
                await page.screenshot(path=os.path.join(dossier_images, f"d{i + 1:02d}.png"))
            rapport.append((i + 1, info))
        await navigateur.close()
    return rapport, erreurs


def planches(dossier):
    from PIL import Image, ImageDraw
    images = sorted(glob.glob(os.path.join(dossier, "d*.png")))
    L, H, col = 640, 360, 3
    for debut in range(0, len(images), 9):
        lot = images[debut:debut + 9]
        lignes = (len(lot) + col - 1) // col
        feuille = Image.new("RGB", (col * L, lignes * (H + 4)), "black")
        for k, f in enumerate(lot):
            x, y = (k % col) * L, (k // col) * (H + 4)
            feuille.paste(Image.open(f).resize((L, H)), (x, y))
            ImageDraw.Draw(feuille).text((x + 4, y + 2), str(debut + k + 1), fill="red")
        feuille.save(os.path.join(dossier, f"planche-{debut // 9 + 1}.png"))


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    dossier = None
    if "--images" in args:
        k = args.index("--images")
        dossier = args[k + 1]
        del args[k:k + 2]
        os.makedirs(dossier, exist_ok=True)
    rapport, erreurs = asyncio.run(controler(args[0], dossier))
    problemes = 0
    for n, info in rapport:
        deborde = info["bas"] > 715 or info["droite"] > 1282
        problemes += deborde
        print(f"{n:3d}  {info['titre'][:55]:55s} bas {info['bas']:4d}{'   <<< DÉBORDE' if deborde else ''}")
    print(f"\n{len(rapport)} diapos ; {problemes} débordement(s) ; erreurs JavaScript : {erreurs or 'aucune'}")
    if dossier:
        planches(dossier)
        print("Captures et planches dans", dossier)
    sys.exit(1 if problemes or erreurs else 0)


if __name__ == "__main__":
    main()
