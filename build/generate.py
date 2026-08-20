# -*- coding: utf-8 -*-
import sys, re, os, glob, html
sys.path.insert(0, os.path.dirname(__file__))
import render, context
from imgmap import IMG_MAP

try:
    import markdown as _markdown
except ImportError:
    _markdown = None

with open(os.path.join(os.path.dirname(__file__), 'base.css'), encoding='utf-8') as f:
    BASE_CSS = f.read()

GOOGLE_FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,500;1,8..60,400&display=swap">'

PAGE_META = {
    'accueil': {
        'route': '/', 'title': "Au fil du tracé — Béatrice Gouts Bourjac, graphothérapeute à Corme-Écluse (17)",
        'description': "Rééducation de l'écriture pour enfants, adolescents et adultes. Bilan graphomoteur et séances personnalisées à Corme-Écluse (17600), secteur Saintes, Gémozac, Pons.",
    },
    'presentation': {
        'route': '/qui-suis-je/', 'title': "Qui suis-je ? — Béatrice Gouts Bourjac, graphothérapeute certifiée CNPG",
        'description': "Graphothérapeute certifiée par le CNPG à Corme-Écluse (17600). Mon parcours, ma formation et mon approche de la rééducation de l'écriture.",
    },
    'prestations': {
        'route': '/prestations/', 'title': "Prestations et tarifs — Bilan graphomoteur et séances | Au fil du tracé",
        'description': "Bilan graphomoteur (110 €), séances enfant/adolescent (45 €) et adulte (50 €). Rééducation de l'écriture à Corme-Écluse, secteur Saintes, Gémozac, Pons.",
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
        'description': "Une question, une demande de bilan ? Contactez Béatrice Gouts Bourjac, graphothérapeute à Corme-Écluse (17600).",
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

# Copie "canonique CI" de ce pipeline : ce dossier build/ vit désormais DANS
# le repo publié (racine = dossier parent de build/), pour que GitHub Actions
# puisse le lancer après chaque publication d'article via Sveltia CMS.
# -> chemins relatifs à un seul niveau, plus besoin de remonter jusqu'au
# dossier de travail local "04_SCRIPTS" (qui n'est pas dans le repo).
BUILD_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_ROOT = os.path.dirname(BUILD_DIR)  # racine du repo = racine du site publié

# Dossier des articles "Coin des curieux" gérés par Béatrice via Sveltia CMS.
# Chaque fichier .md = un article (frontmatter titre/date/image + contenu).
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
    for a in articles:
        img_html = ''
        if a['image']:
            # Sveltia stocke déjà le chemin public complet (ex. /img/articles/x.jpg)
            # dans le frontmatter -- on ne fait que rebaser sur le préfixe relatif
            # de la page (./ pour l'accueil, ../ pour les pages en sous-dossier).
            img_src = a['image'] if a['image'].startswith('http') else prefix + a['image'].lstrip('/')
            img_html = (f'<img loading="lazy" decoding="async" src="{img_src}" alt="" '
                         'style="width:100%;height:auto;border-radius:12px;margin-bottom:16px">')
        date_html = ''
        if a['date_fr']:
            date_html = (f'<span style="display:block;font-size:12px;color:var(--second);'
                         f'font-weight:400;margin-top:4px;font-family:\'Plus Jakarta Sans\',sans-serif">'
                         f'{html.escape(a["date_fr"])}</span>')
        cards.append(f'''
          <div style="background:#fff;border:1px solid var(--bordure);border-radius:16px;overflow:hidden;transition:border-color .2s ease" data-article-item data-open="false">
            <button data-article-toggle aria-expanded="false" style="width:100%;display:flex;justify-content:space-between;align-items:center;gap:16px;background:none;border:none;cursor:pointer;text-align:left;padding:18px 22px;font-family:'Source Serif 4',serif;font-size:17.5px;color:var(--olive);min-height:44px">
              <span>
                <span style="display:block">{html.escape(a['title'])}</span>
                {date_html}
              </span>
              <span data-article-chevron style="font-size:20px;color:var(--brun);flex-shrink:0;transform:rotate(0deg);transition:transform .25s ease">+</span>
            </button>
            <div data-article-panel hidden style="padding:0 22px 24px;font-size:15px;color:var(--corps);line-height:1.75">
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

CARD_RE = re.compile(r'<div style="background:#fff;border:1px solid #f0e7da;border-radius:16px;overflow:hidden;transition:border-color \.2s ease">')
BUTTON_RE = re.compile(r'<button sc-camel-on-click="" aria-expanded="true"')
PANEL_RE = re.compile(r'<div (?:data-pave="" )?style="padding:0 22px 20px;font-size:15px;color:var\(--corps\);line-height:1\.75">')

def patch_faq(html):
    html2, n1 = CARD_RE.subn(
        lambda m: m.group(0)[:-1] + ' data-faq-item data-open="false">',
        html)
    html2, n2 = BUTTON_RE.subn('<button data-faq-toggle aria-expanded="false"', html2)
    html2, n3 = PANEL_RE.subn(
        '<div data-faq-panel hidden style="padding:0 22px 20px;font-size:15px;color:var(--corps);line-height:1.75">',
        html2)
    return html2, min(n1, n2, n3)

def build_doc(page_id, body_html, hover_rules, prefix):
    meta = PAGE_META[page_id]
    hover_css = '\n'.join(hover_rules)
    canonical = 'https://aufildutrace.fr' + meta['route']
    head = f'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{GOOGLE_FONTS}
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
<style>
{BASE_CSS}
{hover_css}
</style>
</head>
<body data-anim="on" data-sprigs="on" data-contraste="off">
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
    if page_id == 'faq':
        body_html, n = patch_faq(body_html)
        print('faq items patched:', n)
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
