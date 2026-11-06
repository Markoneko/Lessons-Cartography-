#!/usr/bin/env python3
"""Imprime un support HTML en PDF, une diapo par page, comme Chrome avec ?print-pdf.

    python3 outils/pdf.py cours/gis-basics/_sortie/GIS-Basics.html            # PDF corrigé
    python3 outils/pdf.py cours/gis-basics/_sortie/GIS-Basics.html --vierge    # sans les réponses

Le PDF est écrit à côté du HTML, sous le même nom (« -vierge » ajouté pour la version sans réponses).
Il faut Playwright et son Chromium :  pip install playwright  puis  playwright install chromium
"""
import asyncio
import os
import sys


def disponible():
    try:
        import playwright.async_api  # noqa: F401
        return True
    except ImportError:
        return False


async def _imprimer(paires):
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        navigateur = await p.chromium.launch()
        for html, pdf, vierge in paires:
            page = await navigateur.new_page(viewport={"width": 1280, "height": 720})
            adresse = "file://" + os.path.abspath(html) + "?print-pdf" + ("&reponses=non" if vierge else "")
            await page.goto(adresse)
            await page.wait_for_function("window.Reveal && Reveal.isReady && Reveal.isReady()", timeout=60000)
            await page.evaluate("document.fonts.ready")
            await page.wait_for_timeout(1500)          # le temps aux briques de se dessiner
            await page.pdf(path=pdf, width="1280px", height="720px", print_background=True)
            await page.close()
        await navigateur.close()


def imprimer(fichiers, vierge=False):
    """fichiers : chemins HTML. Renvoie la liste des PDF écrits."""
    paires = []
    for html in fichiers:
        pdf = os.path.splitext(html)[0] + ("-vierge" if vierge else "") + ".pdf"
        paires.append((html, pdf, vierge))
    asyncio.run(_imprimer(paires))
    return [p[1] for p in paires]


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    if not disponible():
        sys.exit("Playwright n'est pas installé : pip install playwright, puis playwright install chromium")
    for pdf in imprimer(args, vierge="--vierge" in sys.argv):
        print("PDF :", pdf)
