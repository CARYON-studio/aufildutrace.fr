import re, pickle

with open('tree.pkl','rb') as f:
    tree = pickle.load(f)

MUSTACHE = re.compile(r'\{\{\s*([^}]+?)\s*\}\}')
GO_TO_ROUTE = {}  # unused fallback; routes resolved via ctx directly now

hover_rules = []
hover_counter = [0]

NAVCLICK = re.compile(r'href="#"\s+sc-camel-on-click="\{\{\s*([\w.]+)\s*\}\}"')
STYLEHOVER = re.compile(r'\s+style-hover="([^"]*)"')
# Le bundler Claude Design émet des attributs JSX camelCase préfixés
# "sc-camel-*" (viewBox -> sc-camel-view-box, pathLength -> sc-camel-path-length)
# qui n'existent pas en HTML/SVG standard et sont normalement réécrits par le
# runtime JS du bundle. En extraction statique ce runtime ne tourne pas : sans
# cette conversion, les <svg> perdent leur système de coordonnées (viewBox) et
# les animations de tracé (pathLength) ne fonctionnent plus. On les remappe ici
# vers les vrais attributs SVG.
SC_CAMEL_ATTR = re.compile(r'sc-camel-([a-z-]+)=')
def _sc_camel_repl(m):
    # kebab-case -> camelCase (view-box -> viewBox, path-length -> pathLength)
    parts = m.group(1).split('-')
    name = parts[0] + ''.join(p.capitalize() for p in parts[1:])
    return f'{name}='


def resolve_expr(expr, ctx):
    expr = expr.strip()
    cur = ctx
    for part in expr.split('.'):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur

def subst_text(text, ctx):
    def navrepl(m):
        expr = m.group(1)
        route = resolve_expr(expr, ctx)
        if not isinstance(route, str) or not route:
            route = GO_TO_ROUTE.get(expr, '#')
        return f'href="{route}"'
    text = NAVCLICK.sub(navrepl, text)

    def hoverrepl(m):
        hover_counter[0] += 1
        cls = f'hv{hover_counter[0]}'
        # Chaque élément porte déjà ses styles de base en attribut `style="..."`
        # inline (background, box-shadow, color, border-bottom...). Une règle
        # de feuille de style, même sur :hover, ne peut jamais l'emporter sur
        # un style inline pour la même propriété (spécificité CSS) — sans
        # !important, le survol ne changeait donc visuellement que les
        # propriétés absentes du style inline (ex. transform), et laissait
        # fond/ombre/couleur inchangés. D'où le !important sur chaque
        # déclaration générée ici.
        decls = ';'.join(
            f'{d.strip()} !important' for d in m.group(1).split(';') if d.strip()
        )
        hover_rules.append(f'[data-hv="{cls}"]:hover{{{decls}}}')
        return f' data-hv="{cls}"'
    text = STYLEHOVER.sub(hoverrepl, text)
    text = SC_CAMEL_ATTR.sub(_sc_camel_repl, text)

    def mrepl(m):
        val = resolve_expr(m.group(1), ctx)
        if val is None:
            return ''
        if isinstance(val, bool):
            return 'true' if val else 'false'
        return str(val)
    text = MUSTACHE.sub(mrepl, text)
    return text

def render_nodes(nodes, ctx):
    out = []
    for node in nodes:
        if isinstance(node, str):
            out.append(subst_text(node, ctx))
        else:
            tag, attrs, children = node['tag'], node['attrs'], node['children']
            if tag == 'sc-if':
                m = re.search(r'value="\{\{\s*([^}]+?)\s*\}\}"', attrs)
                expr = m.group(1) if m else None
                val = resolve_expr(expr, ctx)
                if val:
                    out.append(render_nodes(children, ctx))
            elif tag == 'sc-for':
                mlist = re.search(r'list="\{\{\s*([^}]+?)\s*\}\}"', attrs)
                mas = re.search(r'as="(\w+)"', attrs)
                listname = mlist.group(1).strip()
                asname = mas.group(1)
                items = resolve_expr(listname, ctx) or []
                for item in items:
                    subctx = dict(ctx)
                    subctx[asname] = item
                    out.append(render_nodes(children, subctx))
    return ''.join(out)

def render_page(ctx):
    hover_rules.clear()
    hover_counter[0] = 0
    html_out = render_nodes(tree, ctx)
    return html_out, list(hover_rules)
