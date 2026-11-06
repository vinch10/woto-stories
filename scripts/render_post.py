#!/usr/bin/env python3
"""Projet 2 : publication annonce Woto (gabarit B validé par Vincent le 6 novembre 2026).

--format fb : 1080x1080 (page Facebook)
--format ig : 1080x1350 (fil Instagram, 4:5)
"""
import argparse, asyncio, html, pathlib, tempfile
from PIL import Image
from playwright.async_api import async_playwright

REPO = pathlib.Path(__file__).resolve().parent.parent
GREEN, FOREST = "#D5F7AD", "#021D10"

# photo_h, courbe (haut du socle), y titre, taille prix, y prix, y spec, boîte logo
LAYOUT = {
    "fb": dict(H=1080, ph=760, curve=640, t=780, ts=46, p=832, ps=112, s=968, ss=27, logo=(230, 150), ly=800),
    "ig": dict(H=1350, ph=850, curve=730, t=940, ts=56, p=1006, ps=140, s=1178, ss=33, logo=(260, 170), ly=990),
}


def crop(src, w, h, focus, dst, vfocus=0.5):
    a = Image.open(src).convert("RGB")
    r = max(h / a.height, w / a.width)
    a = a.resize((round(a.width * r), round(a.height * r)), Image.LANCZOS)
    x = max(0, min(round(focus * a.width - w / 2), a.width - w))
    y = round((a.height - h) * vfocus)
    a.crop((x, y, x + w, y + h)).save(dst, quality=93)


def fit(path, bw, bh):
    w, h = Image.open(path).size
    r = min(bw / w, bh / h)
    return round(w * r), round(h * r)


def wordmark_light(tmp):
    im = Image.open(REPO / "assets/wordmark_forest.png").convert("RGBA")
    out = Image.new("RGBA", im.size, GREEN)
    out.putalpha(im.split()[3])
    p = pathlib.Path(tmp) / "wm_light.png"
    out.save(p)
    return p


async def render(a):
    L = LAYOUT[a.format]
    with tempfile.TemporaryDirectory() as tmp:
        ph = pathlib.Path(tmp) / "p.jpg"
        crop(a.photo, 1080, L["ph"], a.focus, ph, a.vfocus)
        bw, bh = L["logo"]
        w0, h0 = Image.open(a.logo).size
        if w0 / h0 > 4:  # bandeau très large : on l'élargit pour qu'il reste lisible
            bw = round(bw * 1.45)
        lw, lh = fit(a.logo, bw, bh)
        wm = wordmark_light(tmp)
        e = html.escape
        H = L["H"]
        page = f"""<!doctype html><meta charset=utf-8><style>*{{box-sizing:border-box}}body{{margin:0}}</style>
<div style="position:relative;width:1080px;height:{H}px;overflow:hidden;font-family:'Inter Display','Inter';background:{FOREST}">
<img src="file://{ph}" style="position:absolute;left:0;top:0;width:1080px;height:{L['ph']}px">
<svg style="position:absolute;left:0;top:{L['curve']}px" width="1080" height="{H - L['curve']}"><path d="M0 120Q540 0 1080 120V{H}H0Z" fill="{FOREST}"/></svg>
<div style="position:absolute;left:32px;top:30px;background:{FOREST};border-radius:14px;padding:12px 18px"><img src="file://{wm}" style="display:block;height:34px"></div>
<div style="position:absolute;left:56px;top:{L['t']}px;color:#fff;font-weight:500;font-size:{L['ts']}px;letter-spacing:-.02em">{e(a.title)}</div>
<div style="position:absolute;left:52px;top:{L['p']}px;color:{GREEN};font-weight:800;font-size:{L['ps']}px;letter-spacing:-.04em;line-height:1.05;white-space:nowrap">{e(a.price)}</div>
<div style="position:absolute;left:56px;top:{L['s']}px;color:#fff;opacity:.9;font-weight:500;font-size:{L['ss']}px;white-space:pre">{e(a.spec)}</div>
<div style="position:absolute;right:56px;top:{L['ly'] + (L['logo'][1] + 20 - lh - 20) // 2}px;background:#fff;border-radius:16px;padding:10px"><img src="file://{pathlib.Path(a.logo).resolve()}" style="display:block;width:{lw}px;height:{lh}px;border-radius:8px"></div>
</div>"""
        f = pathlib.Path(tmp) / "post.html"
        f.write_text(page, encoding="utf-8")
        png = pathlib.Path(tmp) / "post.png"
        async with async_playwright() as p:
            b = await p.chromium.launch()
            pg = await b.new_page(viewport={"width": 1080, "height": H})
            await pg.goto(f"file://{f}")
            await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(png))
            await b.close()
        Image.open(png).convert("RGB").save(a.out, quality=93)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for n in ("title", "price", "spec", "photo", "logo", "out"):
        ap.add_argument(f"--{n}", required=True)
    ap.add_argument("--format", choices=("fb", "ig"), default="fb")
    ap.add_argument("--focus", type=float, default=0.5)
    ap.add_argument("--vfocus", type=float, default=0.5, help="0 garde le haut de la photo, 1 garde le bas")
    asyncio.run(render(ap.parse_args()))
