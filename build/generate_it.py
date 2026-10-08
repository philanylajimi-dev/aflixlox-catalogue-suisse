#!/usr/bin/env python3
"""
Génère it/index.html à partir de build/catalogue_it.py.

    python3 build/generate_it.py

Le catalogue italien vit dans un sous-dossier et réutilise tels quels les
visuels, le logo, la feuille de style et le script du catalogue français. Il
n'écrit que deux fichiers : `it/index.html` et, séparément, sa propre couche de
style `assets/catalogue-it.css` — de sorte que rien de ce que charge la page
française ne soit modifié.
"""

import html
import json
import os
import re
import sys
from datetime import date

import catalogue_it as C

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "build", "source")
SORTIE = os.path.join(ROOT, "it", "index.html")
# Depuis it/, tout ce qui est partagé se trouve un cran au-dessus.
BASE = ".."
IMG_W = 640

MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio",
        "agosto", "settembre", "ottobre", "novembre", "dicembre"]


# --------------------------------------------------------------------------- #
# Contrôles
# --------------------------------------------------------------------------- #

def charger():
    with open(os.path.join(SOURCE, "shopify-products.json"), encoding="utf-8") as f:
        produits = {p["handle"]: p for p in json.load(f)}
    with open(os.path.join(SOURCE, "product-descriptions.json"), encoding="utf-8") as f:
        descriptions = json.load(f)
    return produits, descriptions


def verifier(handles, produits, descriptions):
    """Même règle que le catalogue français : ni image ni description, pas de fiche."""
    problemes = []
    for h in sorted(handles):
        p = produits.get(h)
        if p is None:
            problemes.append(f"{h} : absent de la boutique")
            continue
        if p["status"] != "ACTIVE":
            problemes.append(f"{h} : statut {p['status']}")
        if not p["image"] or h not in descriptions:
            problemes.append(f"{h} : image ou description manquante")
        if not os.path.exists(os.path.join(ROOT, "assets", "img", "p", h + ".webp")):
            problemes.append(f"{h} : visuel absent du dépôt")
    return problemes


# --------------------------------------------------------------------------- #
# Rendu
# --------------------------------------------------------------------------- #

def e(s):
    return html.escape(str(s), quote=False)


def typo(doc):
    """Typographie italienne.

    L'italien ne met pas d'espace avant les ponctuations doubles — contrairement
    au français. Seule l'apostrophe est redressée. On ne touche jamais à ce qui
    est entre chevrons.
    """
    morceaux = re.split(r"(<[^>]*>)", doc)
    for i, m in enumerate(morceaux):
        if not m.startswith("<"):
            morceaux[i] = m.replace("'", "’")
    return "".join(morceaux)


def prezzo(valeur, grande=False):
    """CHF 10,20 — franc suisse en tête, virgule décimale, centimes en retrait."""
    intero, _, cent = str(valeur).partition(",")
    cls = " p-prezzo--lg" if grande else ""
    return (f'<span class="p-prezzo{cls}"><span class="p-prezzo__cur">CHF</span>'
            f'<span class="p-prezzo__val">{intero},'
            f'<span class="p-prezzo__cts">{cent}</span></span></span>')


def img(handle, eager=False):
    loading = "eager" if eager else "lazy"
    fetch = ' fetchpriority="high"' if eager else ""
    return (f'<img src="{BASE}/assets/img/p/{handle}.webp" alt="" '
            f'width="{IMG_W}" height="{IMG_W}" loading="{loading}" '
            f'decoding="async"{fetch}>')


def grande_offerta(parties):
    """La ligne qui doit se lire d'un bout de la pièce à l'autre."""
    out = []
    for genre, texte in parties:
        if genre == "n":
            out.append(f'<span class="i-big__n">{texte}</span>')
        elif genre == "op":
            out.append(f'<span class="i-big__op">{texte}</span>')
        else:
            out.append(f'<em class="i-big__free">{texte}</em>')
    return "".join(out)


def bandeau(o, eager=False):
    return f"""<div class="i-banda">
      <p class="i-banda__tag">Offerta di lancio</p>
      <p class="i-big">{grande_offerta(o['grande'])}</p>
      <p class="i-banda__nota">{o['nota']}</p>
    </div>"""


def carta(immagine, linea, sotto, righe, eager=False):
    prix = "".join(
        f'<div class="i-riga"><dt>{fmt}</dt><dd>{prezzo(p)}</dd></div>'
        for fmt, p in righe)
    return f"""<article class="i-carta">
  <div class="i-carta__img">{img(immagine, eager=eager)}</div>
  <div class="i-carta__corpo">
    <h3 class="i-carta__linea">{linea}</h3>
    <p class="i-carta__sotto">{sotto}</p>
    <dl class="i-prezzi">{prix}</dl>
  </div>
</article>"""


def sezione_shampoo():
    cartes = [carta(h1000, linea, sotto,
                    [("300 ml", p300), ("1000 ml", p1000)], eager=(i == 0))
              for i, (linea, sotto, h300, h1000, p300, p1000)
              in enumerate(C.SHAMPOO)]
    o = C.OFFERTE[0]
    return f"""<section class="i-sez" id="shampoo" aria-labelledby="t-shampoo">
  <div class="l-wrap">
    <header class="i-testa">
      <p class="i-testa__num">{o['rango']}</p>
      <h2 class="i-testa__titolo" id="t-shampoo">Shampoo</h2>
      <p class="i-testa__intro">Otto linee, due formati.</p>
    </header>
    {bandeau(o, eager=True)}
    <div class="i-griglia">
{chr(10).join(cartes)}
    </div>
  </div>
</section>"""


def sezione_maschere():
    cartes = [carta(hg, linea, sotto, [(fp, pp), (fg, pg)])
              for linea, sotto, hp, hg, fp, fg, pp, pg in C.MASCHERE]
    o = C.OFFERTE[1]
    return f"""<section class="i-sez i-sez--alt" id="maschere" aria-labelledby="t-maschere">
  <div class="l-wrap">
    <header class="i-testa">
      <p class="i-testa__num">{o['rango']}</p>
      <h2 class="i-testa__titolo" id="t-maschere">Maschere</h2>
      <p class="i-testa__intro">Quattro linee, due formati.</p>
    </header>
    {bandeau(o)}
    <div class="i-griglia i-griglia--4">
{chr(10).join(cartes)}
    </div>
  </div>
</section>"""


def sezione_colorazioni():
    cartes = []
    for g in C.COLORAZIONI:
        cartes.append(f"""<article class="i-gamma">
  <div class="i-gamma__img">{img(g['immagine'])}</div>
  <div class="i-gamma__corpo">
    <h3 class="i-gamma__nome">{g['nome']} <span>{g['sotto']}</span></h3>
    <div class="i-gamma__piede">
      <p class="i-gamma__formato">{g['formato']}</p>
      {prezzo(g['prezzo'], grande=True)}
    </div>
  </div>
</article>""")
    o = C.OFFERTE[2]
    return f"""<section class="i-sez" id="colorazioni" aria-labelledby="t-colorazioni">
  <div class="l-wrap">
    <header class="i-testa">
      <p class="i-testa__num">{o['rango']}</p>
      <h2 class="i-testa__titolo" id="t-colorazioni">Colorazioni</h2>
      <p class="i-testa__intro">Due gamme, 100 ml.</p>
    </header>
    {bandeau(o)}
    <p class="i-claim">{C.COLORAZIONI_CLAIM}</p>
    <div class="i-gamme">
{chr(10).join(cartes)}
    </div>
    <p class="i-nota">{C.COLORAZIONI_NOTA}</p>
  </div>
</section>"""


def sintesi():
    """Les trois offres, ensemble, avant tout le reste."""
    tuiles = []
    for o in C.OFFERTE:
        tuiles.append(f"""<a class="i-tessera" href="#{o['id']}">
      <span class="i-tessera__sez"><span>{o['rango']}</span>{o['sezione']}</span>
      <span class="i-tessera__big">{o['sintesi']}<em>gratis</em></span>
      <span class="i-tessera__freccia" aria-hidden="true">↓</span>
    </a>""")
    return f"""<section class="i-offerte" aria-labelledby="t-offerte">
  <div class="l-wrap">
    <p class="i-offerte__tag">Offerte di lancio</p>
    <h2 class="i-offerte__titolo" id="t-offerte">Tre offerte,<br>una per categoria.</h2>
    <div class="i-tessere">
{chr(10).join(tuiles)}
    </div>
  </div>
</section>"""


def rendre():
    oggi = date.today()
    agg = f"{oggi.day} {MESI[oggi.month - 1]} {oggi.year}"

    return typo(f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AF Lix Lox — Listino professionale Svizzera Italiana</title>
<meta name="description" content="Listino professionale AF Lix Lox: shampoo, maschere e colorazioni ai prezzi di lancio, in CHF, per i saloni della Svizzera italiana.">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#0e0e0e">
<meta property="og:title" content="AF Lix Lox — Listino professionale Svizzera Italiana">
<meta property="og:description" content="Shampoo, maschere e colorazioni ai prezzi professionali AF Lix Lox. Tre offerte di lancio.">
<meta property="og:type" content="website">
<meta property="og:image" content="{BASE}/assets/img/aflixlox-logo.png">
<link rel="icon" href="{BASE}/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600&amp;family=Inter:wght@400;500;600&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap">
<link rel="stylesheet" href="{BASE}/assets/catalogue.css">
<link rel="stylesheet" href="{BASE}/assets/catalogue-it.css">
</head>
<body>
<a class="u-skip" href="#shampoo">Vai al listino</a>

<header class="h-bar">
  <div class="l-wrap h-bar__haut">
    <a class="h-logo" href="#top" aria-label="AF Lix Lox — inizio pagina">
      <img src="{BASE}/assets/img/aflixlox-logo.png" alt="AF Lix Lox, Professional Cosmetics" width="1200" height="259">
    </a>
    <p class="h-meta"><span>Svizzera</span><span class="h-meta__sep" aria-hidden="true"></span><span>Prezzi CHF</span></p>
  </div>
  <nav class="h-nav" aria-label="Sezioni del listino">
    <div class="l-wrap h-nav__piste"><a href="#shampoo">Shampoo</a><a href="#maschere">Maschere</a><a href="#colorazioni">Colorazioni</a></div>
  </nav>
</header>

<main id="top">

<section class="i-hero">
  <div class="l-wrap">
    <p class="u-kicker">AF Lix Lox · Distributore professionale · Svizzera</p>
    <h1 class="i-hero__titolo">Listino professionale<br>per saloni di parrucchieri.</h1>
    <p class="i-hero__lede">Shampoo, maschere e colorazioni ai prezzi professionali
      AF Lix Lox. Selezionate referenze, formati e tonalità, poi inviateci
      l'ordine su WhatsApp: confermiamo disponibilità e importo.</p>
  </div>
</section>

{sintesi()}

{sezione_shampoo()}

{sezione_maschere()}

{sezione_colorazioni()}

</main>

<footer class="f-pied">
  <div class="l-wrap">
    <div class="f-pied__grille">
      <div class="f-pied__marque">
        <img src="{BASE}/assets/img/aflixlox-logo-blanc.png" alt="AF Lix Lox" width="1200" height="259">
        <p>Distributore di prodotti per capelli e cosmetici professionali
          in Svizzera.</p>
      </div>
      <div class="f-pied__col">
        <h2>Come ordinare</h2>
        <p>Selezionate referenze, formati e tonalità, poi inviateci la vostra
          selezione direttamente su WhatsApp. Confermiamo disponibilità e importo
          dell'ordine prima della spedizione.</p>
      </div>
      <div class="f-pied__col">
        <h2>Prezzi e offerte</h2>
        <p>Prezzi professionali in franchi svizzeri, per unità. Le tre offerte di
          lancio si applicano ciascuna alla propria categoria.</p>
        <p class="f-pied__maj">Listino aggiornato al {agg}</p>
      </div>
    </div>
  </div>
</footer>

<script src="{BASE}/assets/catalogue.js" defer></script>
<script src="{BASE}/assets/catalogue-it.js" defer></script>
</body>
</html>
""")


def main():
    produits, descriptions = charger()

    handles = set()
    for _, _, h300, h1000, _, _ in C.SHAMPOO:
        handles.update({h300, h1000})
    for _, _, hp, hg, _, _, _, _ in C.MASCHERE:
        handles.update({hp, hg})
    handles.update(g["immagine"] for g in C.COLORAZIONI)

    problemes = verifier(handles, produits, descriptions)
    if problemes:
        for p in problemes:
            print("  ·", p, file=sys.stderr)
        sys.exit("Références incomplètes : génération interrompue.")

    os.makedirs(os.path.dirname(SORTIE), exist_ok=True)
    with open(SORTIE, "w", encoding="utf-8") as f:
        f.write(rendre())
    print(f"it/index.html généré · {len(handles)} références, "
          f"{len(C.SHAMPOO)} linee shampoo, {len(C.MASCHERE)} maschere, "
          f"{len(C.COLORAZIONI)} colorazioni")


if __name__ == "__main__":
    main()
