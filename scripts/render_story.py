#!/usr/bin/env python3
"""Rend une story annonce Woto en JPEG 1080x1920.

Usage : render_story.py --title "BMW X4" --price "24 999 €" \
    --spec "94 000 km  ·  2017  ·  Diesel  ·  Auto" \
    --photo photo.jpg --logo logo.png --out story.jpg [--focus 0.5] [--logo-box 355x170]
"""
import argparse
import asyncio
import html
import pathlib
import tempfile

from PIL import Image
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PHOTO_H = 870
CTA_HTML = """<div style="position:absolute;left:0;right:0;top:1495px;display:flex;justify-content:center"><div style="background:#D5F7AD;border-radius:20px;padding:30px 44px;font-weight:700;font-size:42px;letter-spacing:-.015em;display:flex;gap:18px;align-items:center;white-space:nowrap">Voir l’annonce sur woto.be<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#021D10" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></div></div>"""


def crop_photo(src, focus, dst, photo_h=PHOTO_H):
    a = Image.open(src).convert("RGB")
    r = photo_h / a.height
    a = a.resize((round(a.width * r), photo_h), Image.LANCZOS)
    if a.width < 1080:
        raise SystemExit("Photo trop étroite pour le gabarit")
    x = max(0, min(round(focus * a.width - 540), a.width - 1080))
    a.crop((x, 0, x + 1080, photo_h)).save(dst, quality=92)


def fit_logo(path, box):
    w, h = Image.open(path).size
    r = min(box[0] / w, box[1] / h)
    return round(w * r), round(h * r)


async def render(args):
    box = tuple(int(v) for v in args.logo_box.split("x"))
    with tempfile.TemporaryDirectory() as tmp:
        photo = pathlib.Path(tmp) / "photo.jpg"
        crop_photo(args.photo, args.focus, photo, args.photo_h)
        lw, lh = fit_logo(args.logo, box)
        cta = "" if args.no_cta else CTA_HTML
        page_html = f"""<!doctype html><meta charset=utf-8><style>*{{box-sizing:border-box}}body{{margin:0}}</style>
<div style="position:relative;width:1080px;height:1920px;overflow:hidden;font-family:'Inter Display','Inter';color:#021D10;background:#021D10">
<img src="file://{photo}" style="position:absolute;left:0;top:680px;width:1080px;height:{args.photo_h}px;object-fit:cover">
<svg style="position:absolute;left:0;top:0" width="1080" height="1100" viewBox="0 0 1080 1100"><path d="M0 0H1080V690Q540 870 0 690Z" fill="#D5F7AD"/></svg>
<img src="file://{ROOT}/assets/wordmark_forest.png" style="position:absolute;left:456px;top:250px;height:50px">
<div style="position:absolute;left:0;right:0;top:345px;text-align:center;font-weight:500;font-size:66px;letter-spacing:-.025em;line-height:1.1">{html.escape(args.title)}</div>
<div style="position:absolute;left:0;right:0;top:425px;text-align:center;font-weight:800;font-size:150px;letter-spacing:-.04em;line-height:1.05;white-space:nowrap">{html.escape(args.price)}</div>
<div style="position:absolute;left:0;right:0;top:600px;text-align:center;font-weight:500;font-size:36px;letter-spacing:-.01em;white-space:pre">{html.escape(args.spec)}</div>
{cta}
<img src="file://{pathlib.Path(args.logo).resolve()}" style="position:absolute;left:{(1080 - lw) // 2}px;top:1630px;width:{lw}px;height:{lh}px;border-radius:20px">
</div>"""
        page_file = pathlib.Path(tmp) / "story.html"
        page_file.write_text(page_html, encoding="utf-8")
        png = pathlib.Path(tmp) / "story.png"
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(viewport={"width": 1080, "height": 1920})
            await page.goto(f"file://{page_file}")
            await page.wait_for_timeout(300)
            await page.screenshot(path=str(png))
            await browser.close()
        Image.open(png).convert("RGB").save(args.out, quality=93)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for name in ("title", "price", "spec", "photo", "logo", "out"):
        ap.add_argument(f"--{name}", required=True)
    ap.add_argument("--focus", type=float, default=0.5)
    ap.add_argument("--logo-box", default="355x170")
    ap.add_argument("--photo-h", type=int, default=PHOTO_H, help="hauteur de photo, de 810 à 870 : réduire si la voiture touche les bords")
    ap.add_argument("--no-cta", action="store_true", help="sans bouton dessiné, pour poser un vrai sticker lien")
    asyncio.run(render(ap.parse_args()))
