"""Export one post at 2x (e.g. 2160x2880). Usage from tools/: PW_CHROMIUM=/opt/pw-browsers/chromium python3 -I render_2x.py ../design/work/<post> ../exports/<post>-2x ./node_modules"""
import sys, os, json, tempfile
sys.argv = [sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3]]
src = open(os.path.join(os.path.dirname(os.path.abspath(sys.argv[3])), "render.py")).read().split("tmp = tempfile.mkdtemp()")[0]
exec(src)
from playwright.sync_api import sync_playwright
post = sys.argv[1]; out = sys.argv[2]; os.makedirs(out, exist_ok=True)
canvas = json.load(open(os.path.join(post, "canvas.json"), encoding="utf-8"))
tmp = tempfile.mkdtemp()
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get("PW_CHROMIUM") or None)
    for i, board in enumerate(canvas["order"], 1):
        m = canvas["boards"][board]
        tp = os.path.join(tmp, board); open(tp, "w", encoding="utf-8").write(to_plain(open(os.path.join(post, board), encoding="utf-8").read()))
        pg = b.new_page(viewport={"width": m["w"], "height": m["h"]}, device_scale_factor=2)
        pg.goto("file://" + tp); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
        f = os.path.join(out, f"daftar-007-{i:02d}.png"); pg.screenshot(path=f, clip={"x":0,"y":0,"width":m["w"],"height":m["h"]}); print(f)
        pg.close()
    b.close()
