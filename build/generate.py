# ⚠️ FICHIER GENERE par 04_SCRIPTS/build-et-sync.py — NE PAS EDITER.
# La source est 04_SCRIPTS/build/generate.py.
# -*- coding: utf-8 -*-
import sys, re, os, glob, html
import urllib.parse
sys.path.insert(0, os.path.dirname(__file__))
import render, context
from imgmap import IMG_MAP

try:
    import markdown as _markdown
except ImportError:
    _markdown = None

with open(os.path.join(os.path.dirname(__file__), 'base.css'), encoding='utf-8') as f:
    BASE_CSS = f.read()

# Polices auto-hébergées dans /fonts/ (19/10/2026, conformité RGPD) :
# plus aucune requête vers les serveurs de polices de Google.
# Fichiers .woff2 issus de Fontsource (sous-ensembles latin + latin-ext),
# licences OFL dans /fonts/. Les @font-face sont injectés en tête du <style>
# de chaque page avec le bon préfixe relatif ('./' ou '../').
_LATIN = 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD'
_LATIN_EXT = 'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF'
_FONTS = [
    ('Plus Jakarta Sans', 'plus-jakarta-sans', [('normal', 400), ('normal', 500), ('normal', 600), ('normal', 700), ('italic', 400)]),
    ('Source Serif 4', 'source-serif-4', [('normal', 400), ('normal', 500), ('italic', 400)]),
]

def font_faces(prefix):
    rules = []
    for family, slug, styles in _FONTS:
        for style, weight in styles:
            for subset, urange in (('latin-ext', _LATIN_EXT), ('latin', _LATIN)):
                rules.append(
                    f"@font-face{{font-family:'{family}';font-style:{style};font-weight:{weight};font-display:swap;"
                    f"src:url('{prefix}fonts/{slug}-{subset}-{weight}-{style}.woff2') format('woff2');unicode-range:{urange}}}"
                )
    return '\n'.join(rules)

def font_preloads(prefix):
    return (f'<link rel="preload" href="{prefix}fonts/plus-jakarta-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>'
            f'<link rel="preload" href="{prefix}fonts/source-serif-4-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>')

# JSON-LD Person + LocalBusiness (ajout du 25/08/2026).
# NOTE : adresse volontairement limitée a ville/CP/pays -- Beatrice a choisi
# (06/07/2026, cf memoire projet) de ne PAS publier son adresse complete
# hors page /mentions-legales/. Ne pas ajouter 'streetAddress' ici sans son
# accord explicite : ce JSON-LD est inclus sur TOUTES les pages.
JSONLD_ORG = '{\n  "@context": "https://schema.org",\n  "@graph": [\n    {\n      "@type": "LocalBusiness",\n      "@id": "https://aufildutrace.fr/#business",\n      "name": "Au fil du tracé",\n      "url": "https://aufildutrace.fr",\n      "image": "https://aufildutrace.fr/img/logo-trans.png",\n      "email": "aufildutrace@gmail.com",\n      "telephone": "+33782110029",\n      "address": {\n        "@type": "PostalAddress",\n        "addressLocality": "Corme-Écluse",\n        "postalCode": "17600",\n        "addressCountry": "FR"\n      },\n      "areaServed": [{"@type": "City", "name": "Corme-Écluse"}, {"@type": "City", "name": "Saujon"}, {"@type": "City", "name": "Cozes"}, {"@type": "City", "name": "Saintes"}, {"@type": "City", "name": "Gémozac"}, {"@type": "City", "name": "Pons"}, {"@type": "City", "name": "Meursac"}, {"@type": "City", "name": "Royan"}, {"@type": "City", "name": "Le Gua"}, {"@type": "City", "name": "Semussac"}, {"@type": "City", "name": "Meschers-sur-Gironde"}, {"@type": "City", "name": "Saint-Romain-de-Benet"}, {"@type": "City", "name": "Saint-Georges-de-Didonne"}],\n      "founder": {\n        "@type": "Person",\n        "@id": "https://aufildutrace.fr/#beatrice",\n        "name": "Béatrice Gouts Bourjac",\n        "jobTitle": "Graphothérapeute",\n        "hasCredential": {\n          "@type": "EducationalOccupationalCredential",\n          "recognizedBy": {\n            "@type": "Organization",\n            "name": "CNPG"\n          }\n        }\n      }\n    }\n  ]\n}'

PAGE_META = {
    'accueil': {
        'route': '/', 'title': "Au fil du tracé — Béatrice Gouts Bourjac, graphothérapeute à Corme-Écluse (17)",
        'description': "Rééducation de l'écriture pour enfants, adolescents et adultes. Bilan graphomoteur et séances à Corme-Écluse (17600) et alentours (Royan, Saintes...).",
    },
    'presentation': {
        'route': '/qui-suis-je/', 'title': "Qui suis-je ? — Béatrice Gouts Bourjac, graphothérapeute certifiée CNPG",
        'description': "Graphothérapeute certifiée par le CNPG à Corme-Écluse (17600). Mon parcours, ma formation et mon approche de la rééducation de l'écriture.",
    },
    'prestations': {
        'route': '/prestations/', 'title': "Prestations et tarifs — Bilan graphomoteur et séances | Au fil du tracé",
        'description': "Bilan graphomoteur (110 €), séances enfant/adolescent (45 €) et adulte (50 €). Rééducation à Corme-Écluse et alentours (Royan, Saintes...).",
    },
    'exercices': {
        'route': '/exercices/', 'title': "Exercices d'écriture à faire à la maison | Au fil du tracé",
        'description': "Quatre exercices simples pour progresser en écriture entre les séances : posture, contrôle de la main, lettres liées, rapidité.",
    },
    'coin': {
        'route': '/le-coin-des-curieux/', 'title': "Le coin des curieux — Pourquoi l'écriture compte | Au fil du tracé",
        'description': "Attention, mémoire, fonctions exécutives, créativité : ce que l'écriture manuscrite apporte, expliqué simplement.",
    },
    'faq': {
        'route': '/faq/', 'title': "Questions fréquentes sur la graphothérapie | Au fil du tracé",
        'description': "Âge de démarrage, déroulé des séances, tarifs, remboursement : les réponses aux questions les plus posées sur la rééducation de l'écriture.",
    },
    'contact': {
        'route': '/contact/', 'title': "Contact — Prendre rendez-vous | Au fil du tracé, Corme-Écluse",
        'description': "Une question, une demande de bilan ? Contactez Béatrice Gouts Bourjac, graphothérapeute à Corme-Écluse (17600) et alentours (Royan, Saintes...).",
    },
    'mentions': {
        'route': '/mentions-legales/', 'title': "Mentions légales | Au fil du tracé",
        'description': "Mentions légales du site aufildutrace.fr.",
    },
    'confidentialite': {
        'route': '/politique-de-confidentialite/', 'title': "Politique de confidentialité | Au fil du tracé",
        'description': "Politique de confidentialité et protection des données personnelles du site aufildutrace.fr.",
    },
}

# Copie "canonique CI" de ce pipeline : ce dossier build/ vit DANS le repo
# publie (racine = dossier parent de build/), pour que GitHub Actions puisse le
# lancer apres chaque publication d'article via Sveltia CMS.
#
# ⚠️ CE FICHIER EST GENERE PAR 04_SCRIPTS/build-et-sync.py — NE PAS L'EDITER.
# La source est 04_SCRIPTS/build/generate.py.
BUILD_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_ROOT = os.path.dirname(BUILD_DIR)  # racine du repo = racine du site publie

# Dossier des articles "Coin des curieux" gérés par Béatrice via Sveltia CMS.
# Chaque fichier .md = un article (frontmatter titre/date/image + contenu).
# Vit DANS le repo publié (OUT_ROOT), pas dans 04_SCRIPTS -- c'est ce dossier
# que Sveltia CMS modifie directement via l'API GitHub.
ARTICLES_DIR = os.path.join(OUT_ROOT, "content", "coin-des-curieux")

FRONTMATTER_RE = re.compile(r'^---\s*\n(.*?)\n---\s*\n?(.*)$', re.DOTALL)
MONTHS_FR = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet',
             'août', 'septembre', 'octobre', 'novembre', 'décembre']

def _parse_frontmatter(text):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    raw, body = m.group(1), m.group(2)
    meta = {}
    for line in raw.splitlines():
        if ':' not in line:
            continue
        k, v = line.split(':', 1)
        meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, body

def _format_date_fr(iso_date):
    try:
        y, m, d = iso_date.split('-')
        return f"{int(d)} {MONTHS_FR[int(m) - 1]} {y}"
    except Exception:
        return iso_date

def _md_to_html(body):
    body = body.strip()
    if not body:
        return ''
    if _markdown is not None:
        return _markdown.markdown(body, extensions=['nl2br'])
    # Repli très simple si le paquet "markdown" n'est pas installé :
    # un paragraphe par bloc séparé par une ligne vide.
    paras = [p.strip() for p in re.split(r'\n\s*\n', body) if p.strip()]
    return ''.join(f'<p>{html.escape(p)}</p>' for p in paras)

def load_articles():
    """Lit tous les .md de ARTICLES_DIR (frontmatter titre/date/image + contenu),
    triés du plus récent au plus ancien. Retourne [] si le dossier n'existe pas
    encore ou est vide (page affiche alors un message d'attente, pas d'erreur)."""
    articles = []
    if not os.path.isdir(ARTICLES_DIR):
        return articles
    for path in sorted(glob.glob(os.path.join(ARTICLES_DIR, '*.md'))):
        with open(path, encoding='utf-8') as f:
            raw = f.read()
        meta, body = _parse_frontmatter(raw)
        date_iso = meta.get('date', '')
        articles.append({
            'title': meta.get('title', '(Sans titre)'),
            'date_iso': date_iso,
            'date_fr': _format_date_fr(date_iso) if date_iso else '',
            'image': (meta.get('image') or '').strip(),
            'html': _md_to_html(body),
        })
    articles.sort(key=lambda a: a['date_iso'], reverse=True)
    return articles

def render_articles_section(articles, prefix):
    if not articles:
        return ('<section style="max-width:860px;margin:clamp(28px,4vw,44px) auto 0;'
                'padding:0 clamp(16px,5vw,56px);text-align:center">'
                '<p style="font-size:15px;color:var(--second)">'
                'De nouveaux articles arrivent bientôt.</p></section>')
    cards = []
    for idx, a in enumerate(articles, 1):
        img_html = ''
        if a['image']:
            # Sveltia stocke déjà le chemin public complet (ex. /img/articles/x.jpg)
            # dans le frontmatter -- on ne fait que rebaser sur le préfixe relatif
            # de la page (./ pour l'accueil, ../ pour les pages en sous-dossier).
            img_src = a['image'] if a['image'].startswith('http') else prefix + a['image'].lstrip('/')
            img_html = (f'<img loading="lazy" decoding="async" src="{img_src}" alt="" '
                         'style="width:100%;height:auto;border-radius:12px;margin-bottom:16px">')
        # Vignette à côté du titre (demande Béatrice, oct. 2026) : on réutilise
        # le champ "image" du CMS. alt="" car purement illustrative : le titre
        # juste à côté donne déjà le nom du bouton aux lecteurs d'écran.
        # Pas d'image -> pas de vignette (le titre occupe toute la largeur).
        thumb_html = ''
        if a['image']:
            thumb_src = a['image'] if a['image'].startswith('http') else prefix + urllib.parse.quote(a['image'].lstrip('/'))
            thumb_html = ('<span aria-hidden="true" style="display:block;flex:0 0 72px;width:72px;min-width:72px;height:72px;'
                          'border-radius:10px;overflow:hidden;background:var(--peche)">'
                          f'<img loading="lazy" decoding="async" src="{thumb_src}" alt="" width="72" height="72" '
                          'style="display:block;width:100%;height:100%;max-width:none;object-fit:cover"></span>')
        date_html = ''
        if a['date_fr']:
            date_html = (f'<span style="display:block;font-size:12px;color:var(--second);'
                         f'font-weight:400;margin-top:4px;font-family:\'Plus Jakarta Sans\',sans-serif">'
                         f'{html.escape(a["date_fr"])}</span>')
        cards.append(f'''
          <div style="background:#fff;border:1px solid var(--bordure);border-radius:16px;overflow:hidden;transition:border-color .2s ease" data-article-item data-open="false">
            <button data-article-toggle aria-expanded="false" aria-controls="article-panel-{idx}" style="width:100%;display:flex;justify-content:space-between;align-items:center;gap:16px;background:none;border:none;cursor:pointer;text-align:left;padding:18px 22px;font-family:'Source Serif 4',serif;font-size:17.5px;color:var(--olive);min-height:44px">
              <span style="display:flex;align-items:center;gap:16px;min-width:0">
                {thumb_html}
                <span style="flex:1 1 auto;min-width:0">
                  <span style="display:block">{html.escape(a['title'])}</span>
                  {date_html}
                </span>
              </span>
              <span data-article-chevron style="font-size:20px;color:var(--brun);flex-shrink:0;transform:rotate(0deg);transition:transform .25s ease">+</span>
            </button>
            <div data-article-panel id="article-panel-{idx}" hidden style="padding:0 22px 24px;font-size:15px;color:var(--corps);line-height:1.75">
              {img_html}{a['html']}
            </div>
          </div>''')
    return f'''<section style="max-width:860px;margin:clamp(28px,4vw,44px) auto 0;padding:0 clamp(16px,5vw,56px)">
      <div data-reveal="" style="text-align:center;margin-bottom:clamp(26px,4vw,40px)">
        <span style="display:inline-flex;align-items:center;gap:12px;font-size:12px;letter-spacing:2.5px;text-transform:uppercase;color:var(--second);font-weight:600;margin-bottom:14px"><span data-trait="" style="width:34px;height:1.5px;background:var(--rose);transform-origin:left"></span>Les derniers articles<span data-trait="" style="width:34px;height:1.5px;background:var(--rose);transform-origin:left"></span></span>
        <h2 style="font-family:'Source Serif 4',serif;font-weight:400;color:var(--olive);font-size:clamp(24px,3.4vw,32px);line-height:1.25">Le coin des curieux, au fil des découvertes</h2>
      </div>
      <div style="display:flex;flex-direction:column;gap:12px">{''.join(cards)}
      </div>
    </section>'''

def apply_images(html, prefix):
    for uuid, path in IMG_MAP.items():
        relpath = prefix + path.lstrip('/')
        html = html.replace('"' + uuid + '"', '"' + relpath + '"')
        html = html.replace("('" + uuid + "')", "('" + relpath + "')")
    return html

# NOTE 24/08/2026 : patch_faq() a été supprimé. Le balisage accessible de la FAQ
# (data-faq-item / aria-expanded / aria-controls / titres) est désormais produit
# directement par template.html + context.py. Les expressions régulières qui le
# reconstruisaient après coup dépendaient du HTML brut du prototype et avaient
# déjà cessé de fonctionner sans que rien ne le signale.

def build_doc(page_id, body_html, hover_rules, prefix):
    meta = PAGE_META[page_id]
    hover_css = '\n'.join(hover_rules)
    canonical = 'https://aufildutrace.fr' + meta['route']
    head = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{font_preloads(prefix)}
<link rel="icon" href="{prefix}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{prefix}img/favicon-32.png">
<link rel="apple-touch-icon" sizes="180x180" href="{prefix}img/apple-touch-icon.png">
<title>{meta['title']}</title>
<meta name="description" content="{meta['description']}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Au fil du tracé">
<meta property="og:title" content="{meta['title']}">
<meta property="og:description" content="{meta['description']}">
<meta property="og:url" content="{canonical}">
<meta name="color-scheme" content="light">
<script type="application/ld+json">{JSONLD_ORG}</script>
<style>
{font_faces(prefix)}
{BASE_CSS}
{hover_css}
</style>
</head>
<body data-anim="on" data-sprigs="on" data-contraste="off">
<a class="skip" href="#contenu">Aller au contenu</a>
{body_html}
<script src="{prefix}site.js" defer></script>
</body>
</html>
'''
    return head

def generate(page_id):
    route = PAGE_META[page_id]['route']
    prefix = './' if route == '/' else '../'
    ctx = context.build_context(page_id)
    body_html, hover_rules = render.render_page(ctx)
    body_html = apply_images(body_html, prefix)
    if page_id == 'coin':
        articles = load_articles()
        articles_html = render_articles_section(articles, prefix)
        body_html = body_html.replace('<!-- ARTICLES_PLACEHOLDER -->', articles_html, 1)
        print('coin articles injected:', len(articles))
    doc = build_doc(page_id, body_html, hover_rules, prefix)
    if route == '/':
        out_path = os.path.join(OUT_ROOT, 'index.html')
    else:
        out_path = os.path.join(OUT_ROOT, route.strip('/'), 'index.html')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(doc)
    print('wrote', out_path, len(doc), 'bytes')

if __name__ == '__main__':
    os.makedirs(OUT_ROOT, exist_ok=True)
    for pid in PAGE_META:
        generate(pid)
