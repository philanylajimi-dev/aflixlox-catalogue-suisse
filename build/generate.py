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
        lignes = "".join(
            f'<div class="o-ligne"><dt>{lab}</dt><dd>{val}</dd></div>'
            for lab, val in o["lignes"])
        cartes.append(f"""<article class="o-carte{' o-carte--vedette' if o['vedette'] else ''}">
  <div class="o-carte__visuel">{img(o['image'], eager=o['vedette'])}</div>
  <div class="o-carte__corps">
    <p class="o-carte__rang"><span>{o['rang']}</span>{o['famille']}</p>
    <h3 class="o-carte__titre">{o['titre']}</h3>
    <dl class="o-detail">{lignes}</dl>
    <p class="o-carte__note">{o['note']}</p>
  </div>
</article>""")

    suivantes = []
    for f in C.OFFRES_SUIVANTES:
        formules = "".join(f"""<li class="r-formule">
      <p class="r-formule__qte"><span>{x['achat']}</span>{f'<em>{x["offert"]}</em>' if x['offert'] else ''}</p>
      <p class="r-formule__total">{x['total']}</p>
      <p class="r-formule__prix">{x['prix']}</p>
      <p class="r-formule__unite">{x['unite']}</p>
    </li>""" for x in f["formules"])
        suivantes.append(f"""<div class="r-bloc">
    <h3 class="r-bloc__titre">{f['famille']}</h3>
    <ul class="r-liste">{formules}</ul>
  </div>""")

    return f"""<section class="s-offres" id="offres" aria-labelledby="t-offres">
  <div class="l-wrap">
    <header class="s-tete s-tete--clair">
      <p class="s-tete__num">01</p>
      <h2 class="s-tete__titre" id="t-offres">Première commande</h2>
      <p class="s-tete__intro">Trois conditions d'ouverture de compte, valables ensemble
        sur une même première commande.</p>
    </header>
    <div class="o-grille">
{chr(10).join(cartes)}
    </div>
  </div>
</section>

<section class="s-reassort" aria-labelledby="t-reassort">
  <div class="l-wrap">
    <header class="s-tete s-tete--serree">
      <h2 class="s-tete__titre s-tete__titre--sm" id="t-reassort">Puis, à chaque réassort</h2>
      <p class="s-tete__intro">Les conditions permanentes, sans minimum de commande.</p>
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
    for label, h_litre, h_petit in a["lignes"]:
        lignes.append(f"""<tr>
      <th scope="row">{label}</th>
      <td>{chf(prix(h_litre, produits))}</td>
      <td>{chf(prix(h_petit, produits))}</td>
    </tr>""")

    decos = "".join(carte_produit(h, n, t, acc, produits)
                    for h, n, t, acc in C.DECOLORANTS["produits"]
                    if h in valides)

    return f"""<section class="s-section" id="colorations" aria-labelledby="t-colorations">
  <div class="l-wrap">
    <header class="s-tete">
      <p class="s-tete__num">02</p>
      <h2 class="s-tete__titre" id="t-colorations">Colorations 100 ml</h2>
      <p class="s-tete__intro">Deux gammes, un seul tarif. Les tons se choisissent
        au moment de la commande&nbsp;: indiquez-moi vos numéros, je prépare le colis.</p>
    </header>

    <div class="g-grille">
{chr(10).join(cartes)}
    </div>

    <div class="a-bloc">
      <div class="a-bloc__visuel">{img(a['image'])}</div>
      <div class="a-bloc__corps">
        <h3 class="c-groupe__nom">{a['titre']}</h3>
        <p class="a-bloc__note">{a['sous_titre']}</p>
        <table class="a-table">
          <caption class="u-vh">Tarifs des activateurs par volume et contenance, en CHF</caption>
          <thead>
            <tr><td></td><th scope="col">1 000 ml</th><th scope="col">150 ml</th></tr>
          </thead>
          <tbody>
{chr(10).join(lignes)}
          </tbody>
        </table>
        <p class="a-bloc__dev">Prix en CHF</p>
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
<meta name="description" content="Tarifs salon AF Lix Lox en Suisse : colorations 100 ml, bidons de shampoing 10 L, masques grand format, soins et technique. Prix professionnels en CHF.">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#0e0e0e">
<meta property="og:title" content="AF Lix Lox — Catalogue professionnel Suisse">
<meta property="og:description" content="Colorations, bidons 10 L, masques et soins. Tarifs professionnels en CHF.">
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
    <p class="u-kicker">Catalogue professionnel · Salons de coiffure</p>
    <h1 class="s-hero__titre">Vos tarifs salon,<br>en une seule page.</h1>
    <p class="s-hero__lede">Colorations, bidons de 10 litres, masques grand format
      et soins ProfesiaHair, aux prix professionnels. Vous notez les références
      et les tons qui vous intéressent, vous me répondez sur WhatsApp&nbsp;:
      je m'occupe du reste.</p>
    <ul class="s-hero__chiffres">
      <li><span class="n">10.40 CHF</span><span class="l">Le tube de coloration 100 ml</span></li>
      <li><span class="n">50.00 CHF</span><span class="l">Le bidon de shampoing 10 L</span></li>
      <li><span class="n">−50 %</span><span class="l">Sur toute la première commande</span></li>
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
        <p>Distribution de cosmétiques professionnels en Suisse.</p>
      </div>
      <div class="f-pied__col">
        <h2>Comment commander</h2>
        <p>Répondez-moi directement dans notre conversation WhatsApp&nbsp;: les
          références, les contenances et, pour les colorations, les numéros de ton
          et les quantités. Je confirme la disponibilité et le total avant l'envoi.</p>
      </div>
      <div class="f-pied__col">
        <h2>Tarifs</h2>
        <p>Prix professionnels en francs suisses, par unité. Les offres de première
          commande ne s'appliquent qu'à l'ouverture du compte&nbsp;; les conditions
          de réassort valent ensuite sans limite de durée.</p>
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
    for _, a, b in C.ACTIVATEURS["lignes"]:
        handles.update({a, b})
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
