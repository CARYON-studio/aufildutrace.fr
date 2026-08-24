# ⚠️ FICHIER GENERE par 04_SCRIPTS/build-et-sync.py — NE PAS EDITER.
# La source est 04_SCRIPTS/build/parse.py.
import re, pickle

with open('template.html', encoding='utf-8') as f:
    doc = f.read()

start = doc.index('<div data-screen-label="Site Au fil du tracé"')
end = doc.index('</div>\n</x-dc>')
body = doc[start:end]

TAGRE = re.compile(r'<(/?)(sc-if|sc-for)\b([^>]*)>')

def parse(text, pos=0):
    nodes = []
    while pos < len(text):
        m = TAGRE.search(text, pos)
        if not m:
            nodes.append(text[pos:])
            pos = len(text)
            break
        if m.start() > pos:
            nodes.append(text[pos:m.start()])
        closing, tag, attrs = m.group(1), m.group(2), m.group(3)
        if closing:
            return nodes, m.end()
        else:
            children, newpos = parse(text, m.end())
            nodes.append({'tag': tag, 'attrs': attrs, 'children': children})
            pos = newpos
    return nodes, pos

tree, _ = parse(body)
with open('tree.pkl', 'wb') as f:
    pickle.dump(tree, f)
print("top-level nodes:", len(tree))
