"""Render saved .dc.html artboards to reference PNGs (local, read-only use of originals).

Usage: python3 -I render.py ../design/originals ../references/renders ./node_modules
(each subfolder holds canvas.json + *.dc.html, either directly or under project/)
Originals are only read; transformed copies are written to a temp folder.
"""
import json, os, re, sys, tempfile
from playwright.sync_api import sync_playwright

SRC, OUT, FONTS = sys.argv[1], sys.argv[2], sys.argv[3]
POSTS_BY_ID = {
    "4bd27fb4-5065-46cf-8394-f77f770c18c4": "000-start-here",
    "4ded5c8c-8720-48c4-a942-79aec30446ca": "001-dont-miss-twice",
    "a1e4fcb7-e41a-4359-b3e5-fc713e371105": "002-planning-fallacy",
    "7055f013-8d2f-4d0a-8bf2-04f1ed1f7c43": "003-average-lies",
    "b96a96fd-c1c5-44b5-8e39-eefd2d1b413a": "004-spotlight-effect",
    "b1f6ecbd-82ea-4b8e-ac7e-da27bdb386be": "005-follow-your-passion",
    "a9356e5c-28ef-4e71-bab3-f4afc9562476": "006-invented-sources",
}
POSTS = {d: d for d in sorted(os.listdir(SRC)) if os.path.isdir(os.path.join(SRC, d))}
POSTS = {k: POSTS_BY_ID.get(k, k) for k in POSTS}
font_css = []
for pkg, weights in [("ibm-plex-sans-arabic", [400, 500, 700]), ("ibm-plex-mono", [400, 500, 600]), ("aref-ruqaa", [400, 700])]:
    for w in weights:
        p = os.path.join(FONTS, "@fontsource", pkg, f"{w}.css")
        if os.path.exists(p):
            css = open(p, encoding="utf-8").read()
            base = "file://" + os.path.join(FONTS, "@fontsource", pkg)
            css = css.replace("url(./", f"url({base}/")
            font_css.append(css)
FONT_CSS = "\n".join(font_css)

def to_plain(html):
    html = re.sub(r'<script src="\./support\.js"></script>', "", html)
    html = re.sub(r'<script type="text/x-dc".*?</script>', "", html, flags=re.S)
    html = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis[^>]*>', "", html)
    html = html.replace("<helmet>", "").replace("</helmet>", "")
    html = html.replace("<x-dc>", "<div>").replace("</x-dc>", "</div>")
    return html.replace("<head>", f"<head><style>{FONT_CSS}</style>", 1)

tmp = tempfile.mkdtemp()
report = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for aid, name in POSTS.items():
        proj = os.path.join(SRC, aid, "project")
        if not os.path.isdir(proj):
            proj = os.path.join(SRC, aid)
        canvas = json.load(open(os.path.join(proj, "canvas.json"), encoding="utf-8"))
        os.makedirs(os.path.join(OUT, name), exist_ok=True)
        for i, board in enumerate(canvas["order"], 1):
            meta = canvas["boards"][board]
            w, h = meta["w"], meta["h"]
            plain = to_plain(open(os.path.join(proj, board), encoding="utf-8").read())
            tp = os.path.join(tmp, f"{name}-{board}")
            open(tp, "w", encoding="utf-8").write(plain)
            pg = b.new_page(viewport={"width": w, "height": h})
            pg.goto("file://" + tp)
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(250)
            stem = f"{i:02d}-" + board.replace(".dc.html", "")
            out = os.path.join(OUT, name, stem + ".png")
            pg.screenshot(path=out, clip={"x": 0, "y": 0, "width": w, "height": h})
            # overflow check: any text element whose box leaves the artboard
            over = pg.evaluate("""([w,h]) => { const r=[]; document.querySelectorAll('body *').forEach(e=>{
                if(e.closest('svg')) return; if(!e.childNodes.length) return;
                const t=[...e.childNodes].filter(n=>n.nodeType===3&&n.textContent.trim()); if(!t.length) return;
                const b=e.getBoundingClientRect(); if(b.left<-1||b.right>w+1||b.bottom>h+1) r.push(e.textContent.trim().slice(0,30)+' ['+Math.round(b.left)+','+Math.round(b.right)+']');});
                return r; }""", [w, h])
            report.append(f"{name}/{stem}.png {w}x{h}" + (f"  OVERFLOW: {over}" if over else ""))
            pg.close()
    b.close()
print("\n".join(report))
