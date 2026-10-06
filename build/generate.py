#!/usr/bin/env python3
"""
Génère index.html à partir de build/catalogue.py et de l'export de la boutique.

    python3 build/generate.py            # régénère le HTML
    python3 build/generate.py --images   # télécharge aussi les visuels manquants

Les visuels sont récupérés une fois sur le CDN Shopify puis versionnés dans
assets/img/ : le catalogue reste autonome, même si la boutique évolue.
"""

import html
import json
import re
import os
import sys
import urllib.request
from datetime import date

import catalogue as C

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "build", "source")
IMG_DIR = os.path.join(ROOT, "assets", "img", "p")
IMG_W = 640

MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
        "août", "septembre", "octobre", "novembre", "décembre"]


# --------------------------------------------------------------------------- #
# Données
# --------------------------------------------------------------------------- #

def charger():
    with open(os.path.join(SOURCE, "shopify-products.json"), encoding="utf-8") as f:
        produits = {p["handle"]: p for p in json.load(f)}
    with open(os.path.join(SOURCE, "product-descriptions.json"), encoding="utf-8") as f:
        descriptions = json.load(f)
    return produits, descriptions


def prix(handle, produits):
    """Tarif confirmé s'il existe, sinon celui de la boutique."""
    if handle in C.PRIX_VALIDES:
        return C.PRIX_VALIDES[handle]
    return produits[handle]["price"]


def verifier(handle, produits, descriptions, incidents):
    """Une référence n'est publiée qu'avec une image et une description."""
    p = produits.get(handle)
    if p is None:
        incidents.append(f"{handle} : absent de la boutique")
        return False
    if handle in C.EXCLUS:
        return False
    if p["status"] != "ACTIVE":
        incidents.append(f"{handle} : statut {p['status']}")
        return False
    if not p["image"]:
        incidents.append(f"{handle} : pas d'image")
        return False
    if handle not in descriptions:
        incidents.append(f"{handle} : pas de description")
        return False
    return True


def telecharger_images(handles, produits):
    os.makedirs(IMG_DIR, exist_ok=True)
    for h in sorted(handles):
        cible = os.path.join(IMG_DIR, h + ".webp")
        if os.path.exists(cible):
            continue
        url = produits[h]["image"].split("?")[0] + f"?width={IMG_W}&format=webp"
        print("↓", h)
        urllib.request.urlretrieve(url, cible)


# --------------------------------------------------------------------------- #
# Rendu
# --------------------------------------------------------------------------- #

def e(s):
    return html.escape(str(s), quote=False)

def typo(doc):
    """Typographie française appliquée aux seuls nœuds de texte.

    Espace insécable avant les ponctuations doubles, apostrophe courbe. On ne
    touche jamais à ce qui est entre chevrons : attributs, URL et classes
    doivent rester intacts.
    """
    morceaux = re.split(r"(<[^>]*>)", doc)
    for i, m in enumerate(morceaux):
        if m.startswith("<"):
            continue
        m = re.sub(r" +([:;!?»])", "\u00a0" + r"\1", m)
        m = re.sub(r"« +", "«\u00a0", m)
        m = re.sub(r"(\d) (?=\d)", r"\1" + "\u00a0", m)
        m = m.replace("'", "\u2019")
        morceaux[i] = m
    return "".join(morceaux)



def chf(valeur):
    """10.40 → 10.<span>40</span> : les centimes en plus petit."""
    entier, _, cents = str(valeur).partition(".")
    return f'{entier}.<span class="c-prix__cts">{cents or "00"}</span>'


def img(handle, eager=False):
    """Packshot. L'alt reste vide : le nom du produit est toujours juste à côté,
    le répéter ne ferait qu'alourdir la lecture au lecteur d'écran."""
    loading = "eager" if eager else "lazy"
    fetch = ' fetchpriority="high"' if eager else ""
    return (f'<img src="assets/img/p/{handle}.webp" alt="" '
            f'width="{IMG_W}" height="{IMG_W}" loading="{loading}" '
            f'decoding="async"{fetch}>')


def carte_produit(handle, nom, taille, accroche, produits, eager=False):
    return f"""<article class="c-carte">
  <div class="c-carte__visuel">{img(handle, eager=eager)}</div>
  <div class="c-carte__corps">
    <p class="c-carte__taille">{e(taille)}</p>
    <h4 class="c-carte__nom">{nom}</h4>
    <p class="c-carte__note">{accroche}</p>
    <p class="c-prix"><span class="c-prix__val">{chf(prix(handle, produits))}</span><span class="c-prix__dev">CHF</span></p>
  </div>
</article>"""


def groupe(g, produits, valides, eager=False):
    cartes = []
    for handle, nom, taille, accroche in g["produits"]:
        if handle not in valides:
            continue
        cartes.append(carte_produit(handle, nom, taille, accroche, produits,
                                    eager=eager and not cartes))
    note = f'<p class="c-groupe__note">{g["note"]}</p>' if g.get("note") else ""
    marque = (f'<p class="c-groupe__marque">{g["marque"]}</p>'
              if g.get("marque") else "")
    return f"""<div class="c-groupe">
  <header class="c-groupe__tete">
    <div>{marque}<h3 class="c-groupe__nom">{g['nom']}</h3></div>
    {note}
  </header>
  <div class="c-grille">
{chr(10).join(cartes)}
  </div>
</div>"""


def section(s, produits, valides, alt=False, eager=False):
    groupes = [groupe(g, produits, valides, eager=eager and not i)
               for i, g in enumerate(s["groupes"])]
    vedette = " s-section--alt" if alt else ""
    return f"""<section class="s-section{vedette}" id="{s['id']}" aria-labelledby="t-{s['id']}">
  <div class="l-wrap">
    <header class="s-tete">
      <p class="s-tete__num">{s['numero']}</p>
      <h2 class="s-tete__titre" id="t-{s['id']}">{s['titre']}</h2>
      <p class="s-tete__intro">{s['intro']}</p>
    </header>
{chr(10).join(groupes)}
  </div>
</section>"""


def bloc_offres(produits):
    cartes = []
    for o in C.OFFRES_PREMIERE:
        lignes = []
        for g in o["lignes"]:
            sous = f'<span class="o-ligne__sous">{g["s"]}</span>' if g.get("s") else ""
            accent = " o-ligne--accent" if g.get("a") else ""
            lignes.append(
                f'<div class="o-ligne{accent}"><dt>{g["l"]}</dt>'
                f'<dd>{g["v"]}{sous}</dd></div>')
        cartes.append(f"""<article class="o-carte{' o-carte--vedette' if o['vedette'] else ''}">
  <div class="o-carte__visuel">{img(o['image'], eager=o['vedette'])}</div>
  <div class="o-carte__corps">
    <p class="o-carte__rang"><span>{o['rang']}</span>{o['famille']}</p>
    <h3 class="o-carte__titre">{o['titre']}</h3>
    <dl class="o-detail">{''.join(lignes)}</dl>
    <p class="o-carte__note">{o['note']}</p>
  </div>
</article>""")

    suivantes = []
    for f in C.OFFRES_SUIVANTES:
        note = f'<p class="r-bloc__note">{f["note"]}</p>' if f.get("note") else ""
        sous = f'<p class="r-bloc__sous">{f["sous"]}</p>' if f.get("sous") else ""
        formules = "".join(f"""<li class="r-formule">
      <p class="r-formule__qte"><span>{x['achat']}</span>{f'<em>{x["offert"]}</em>' if x['offert'] else ''}</p>
      <p class="r-formule__total">{x['total']}</p>
      <p class="r-formule__prix">{x['prix']}</p>
      <p class="r-formule__unite">{x['unite']}</p>
    </li>""" for x in f["formules"])
        suivantes.append(f"""<div class="r-bloc">
    <h3 class="r-bloc__titre">{f['famille']}</h3>
    {sous}
    <ul class="r-liste">{formules}</ul>
    {note}
  </div>""")

    return f"""<section class="s-offres" id="offres" aria-labelledby="t-offres">
  <div class="l-wrap">
    <header class="s-tete s-tete--clair">
      <p class="s-tete__num">01</p>
      <h2 class="s-tete__titre" id="t-offres">Offres professionnelles&nbsp;: première commande</h2>
      <p class="s-tete__intro">Trois offres distinctes, une par catégorie, à l'ouverture
        du compte.</p>
    </header>
    <div class="o-grille">
{chr(10).join(cartes)}
    </div>
    <p class="o-clarif">{C.OFFRES_CLARIFICATION}</p>
  </div>
</section>

<section class="s-reassort" aria-labelledby="t-reassort">
  <div class="l-wrap">
    <header class="s-tete s-tete--serree">
      <h2 class="s-tete__titre s-tete__titre--sm" id="t-reassort">Puis, à chaque réassort</h2>
      <p class="s-tete__intro">Les conditions permanentes, sans minimum de commande.
        Sur les colorations, l'avantage progresse avec le volume.</p>
    </header>
    <div class="r-grille">
{chr(10).join(suivantes)}
    </div>
  </div>
</section>"""


def bloc_colorations(produits, valides):
    cartes = []
    for g in C.GAMMES_COLORATION:
        familles = "".join(f'<li>{f}</li>' for f in g["familles"])
        cartes.append(f"""<article class="g-carte">
  <div class="g-carte__visuel">{img(g['image'])}</div>
  <div class="g-carte__corps">
    <p class="g-carte__marque">ProfesiaHair</p>
    <h3 class="g-carte__nom">{g['nom']} <span>{g['sous_titre']}</span></h3>
    <p class="g-carte__accroche">{g['accroche']}</p>
    <p class="g-carte__nuances"><strong>{g['nuances']}</strong>, toutes disponibles —
      {g['echelle'].lower()}.</p>
    <ul class="g-familles">{familles}</ul>
    <div class="g-carte__pied">
      <p class="g-carte__taille">{g['contenance']}</p>
      <p class="c-prix c-prix--lg"><span class="c-prix__val">{chf(g['prix'])}</span><span class="c-prix__dev">CHF</span></p>
    </div>
  </div>
</article>""")

    a = C.ACTIVATEURS
    lignes = []
    for label, handle in a["lignes"]:
        lignes.append(f"""<div class="a-ligne">
            <dt>{label}</dt>
            <dd><span class="c-prix__val">{chf(prix(handle, produits))}</span><span class="c-prix__dev">CHF</span></dd>
          </div>""")

    decos = "".join(carte_produit(h, n, t, acc, produits)
                    for h, n, t, acc in C.DECOLORANTS["produits"]
                    if h in valides)

    return f"""<section class="s-section" id="colorations" aria-labelledby="t-colorations">
  <div class="l-wrap">
    <header class="s-tete">
      <p class="s-tete__num">02</p>
      <h2 class="s-tete__titre" id="t-colorations">Colorations 100 ml</h2>
      <p class="s-tete__intro">Deux gammes, avec ou sans ammoniaque. Toutes les
        nuances sont disponibles&nbsp;: indiquez-nous les numéros de ton souhaités
        au moment de la commande.</p>
    </header>

    <div class="g-grille">
{chr(10).join(cartes)}
    </div>

    <div class="a-bloc">
      <div class="a-bloc__visuel">{img(a['image'])}</div>
      <div class="a-bloc__corps">
        <h3 class="c-groupe__nom">{a['titre']}</h3>
        <p class="a-bloc__note">{a['sous_titre']}</p>
        <p class="a-bloc__fmt">{a['contenance']}</p>
        <dl class="a-liste">
{chr(10).join(lignes)}
        </dl>
      </div>
    </div>

    <div class="c-groupe">
      <header class="c-groupe__tete">
        <div><p class="c-groupe__marque">ProfesiaHair</p>
        <h3 class="c-groupe__nom">{C.DECOLORANTS['titre']}</h3></div>
      </header>
      <div class="c-grille">{decos}</div>
    </div>
  </div>
</section>"""


def nav(sections):
    liens = [("offres", "Offres"), ("colorations", "Colorations")]
    liens += [(s["id"], s.get("nav", s["titre"])) for s in sections]
    return "".join(f'<a href="#{i}">{t}</a>' for i, t in liens)


def rendre(produits, valides):
    sections = C.SECTIONS
    # Colorations en blanc, puis une bande sur deux en neutre chaud : le rythme
    # tient tout seul sans avoir à décider section par section.
    corps = [bloc_offres(produits), bloc_colorations(produits, valides)]
    corps += [section(s, produits, valides, alt=(i % 2 == 0))
              for i, s in enumerate(sections)]

    aujourdhui = date.today()
    maj = f"{aujourdhui.day} {MOIS[aujourdhui.month - 1]} {aujourdhui.year}"

    return typo(f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AF Lix Lox — Catalogue professionnel Suisse</title>
<meta name="description" content="Catalogue professionnel AF Lix Lox Suisse : colorations, formats 10 L, masques, soins et produits techniques aux tarifs professionnels, en CHF.">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#0e0e0e">
<meta property="og:title" content="AF Lix Lox — Catalogue professionnel Suisse">
<meta property="og:description" content="Colorations, formats professionnels 10 L, masques, soins et produits techniques aux tarifs professionnels AF Lix Lox Suisse.">
<meta property="og:type" content="website">
<meta property="og:image" content="assets/img/aflixlox-logo.png">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600&amp;family=Inter:wght@400;500;600&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap">
<link rel="stylesheet" href="assets/catalogue.css">
</head>
<body>
<a class="u-skip" href="#offres">Aller au catalogue</a>

<header class="h-bar">
  <div class="l-wrap h-bar__haut">
    <a class="h-logo" href="#top" aria-label="AF Lix Lox — haut de page">
      <img src="assets/img/aflixlox-logo.png" alt="AF Lix Lox, Professional Cosmetics" width="1200" height="259">
    </a>
    <p class="h-meta"><span>Suisse</span><span class="h-meta__sep" aria-hidden="true"></span><span>Tarifs CHF</span></p>
  </div>
  <nav class="h-nav" aria-label="Sections du catalogue">
    <div class="l-wrap h-nav__piste">{nav(C.SECTIONS)}</div>
  </nav>
</header>

<main id="top">

<section class="s-hero">
  <div class="l-wrap">
    <p class="u-kicker">AF Lix Lox · Distributeur professionnel · Suisse</p>
    <h1 class="s-hero__titre">Tarifs professionnels<br>pour salons de coiffure.</h1>
    <p class="s-hero__lede">Colorations, formats professionnels 10 L, masques, soins
      et produits techniques aux tarifs professionnels AF Lix Lox Suisse.
      Sélectionnez vos références, contenances et nuances, puis transmettez-nous
      votre commande sur WhatsApp&nbsp;: nous confirmons ensuite la disponibilité
      et le montant.</p>
    <p class="s-hero__label">Offres professionnelles&nbsp;: première commande</p>
    <ul class="s-hero__chiffres">
      <li><span class="n">24 + 24</span><span class="l">Colorations 100 ml&nbsp;: 24 tubes achetés, 24 offerts</span></li>
      <li><span class="n">50 + 25 CHF</span><span class="l">Bidons 10 L&nbsp;: le second bidon à −50 %</span></li>
      <li><span class="n">−50 %</span><span class="l">Masques, soins, technique, Homme et consommables</span></li>
    </ul>
  </div>
</section>

{chr(10).join(corps)}

</main>

<footer class="f-pied">
  <div class="l-wrap">
    <div class="f-pied__grille">
      <div class="f-pied__marque">
        <img src="assets/img/aflixlox-logo-blanc.png" alt="AF Lix Lox" width="1200" height="259">
        <p>Distributeur de produits capillaires et cosmétiques professionnels
          en Suisse.</p>
      </div>
      <div class="f-pied__col">
        <h2>Comment commander</h2>
        <p>Sélectionnez vos références, contenances et nuances, puis envoyez-nous
          votre sélection directement sur WhatsApp. Nous confirmons la disponibilité
          et le montant de la commande avant expédition.</p>
      </div>
      <div class="f-pied__col">
        <h2>Tarifs et offres</h2>
        <p>Prix professionnels en francs suisses, par unité. Les offres de première
          commande s'appliquent à l'ouverture du compte&nbsp;; les conditions de
          réassort valent ensuite sans limite de durée. Chaque offre concerne sa
          propre catégorie et ne se cumule pas avec une autre sur un même produit.</p>
        <p class="f-pied__maj">Catalogue à jour au {maj}</p>
      </div>
    </div>
  </div>
</footer>

<script src="assets/catalogue.js" defer></script>
</body>
</html>
""")


def main():
    produits, descriptions = charger()
    incidents = []

    # Toutes les références citées par le catalogue.
    handles = set()
    for s in C.SECTIONS:
        for g in s["groupes"]:
            handles.update(p[0] for p in g["produits"])
    handles.update(p[0] for p in C.DECOLORANTS["produits"])
    handles.update(h for _, h in C.ACTIVATEURS["lignes"])
    handles.add(C.ACTIVATEURS["image"])
    handles.update(g["image"] for g in C.GAMMES_COLORATION)
    handles.update(o["image"] for o in C.OFFRES_PREMIERE)

    valides = {h for h in handles if verifier(h, produits, descriptions, incidents)}
    manquants = sorted(handles - valides)
    if manquants:
        print("Références écartées :", ", ".join(manquants), file=sys.stderr)
    for i in incidents:
        print("  ·", i, file=sys.stderr)

    if "--images" in sys.argv:
        telecharger_images(valides, produits)

    sortie = os.path.join(ROOT, "index.html")
    with open(sortie, "w", encoding="utf-8") as f:
        f.write(rendre(produits, valides))
    print(f"index.html généré · {len(valides)} références publiées")


if __name__ == "__main__":
    main()
