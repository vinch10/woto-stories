#!/usr/bin/env python3
"""Rend une annonce feed Woto en JPEG 1080x1350 (couverture ou photo de carrousel).

Couverture : render_feed.py --title "BMW X4" --price "24 999 €" --spec "..." --photo p.jpg --logo l.png --out o.jpg [--focus 0.5]
Carrousel  : render_feed.py --slide --photo p.jpg --out o.jpg
"""
import argparse
import asyncio
import html
import pathlib
import tempfile

from PIL import Image
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PHOTO_TOP, PHOTO_H = 355, 790


def crop_cover(src, focus, dst):
    a = Image.open(src).convert("RGB")
    r = max(PHOTO_H / a.height, 1080 / a.width)
    a = a.resize((round(a.width * r), round(a.height * r)), Image.LANCZOS)
    x = max(0, min(round(focus * a.width - 540), a.width - 1080))
    y = (a.height - PHOTO_H) // 2
    a.crop((x, y, x + 1080, y + PHOTO_H)).save(dst, quality=93)


def fit_logo(path, box=(300, 110)):
    w, h = Image.open(path).size
    r = min(box[0] / w, box[1] / h)
    return round(w * r), round(h * r)


def cover_html(args, photo):
    lw, lh = fit_logo(args.logo)
    return f"""<div style="position:relative;width:1080px;height:1350px;overflow:hidden;font-family:'Inter Display','Inter';color:#021D10;background:#021D10">
<img src="file://{photo}" style="position:absolute;left:0;top:{PHOTO_TOP}px;width:1080px;height:{PHOTO_H}px">
<svg style="position:absolute;left:0;top:0" width="1080" height="500" viewBox="0 0 1080 500"><path d="M0 0H1080V362Q540 472 0 362Z" fill="#D5F7AD"/></svg>
<img src="file://{ROOT}/assets/wordmark_forest.png" style="position:absolute;left:468px;top:38px;height:42px">
<div style="position:absolute;left:0;right:0;top:96px;text-align:center;font-weight:500;font-size:54px;letter-spacing:-.025em;line-height:1.1">{html.escape(args.title)}</div>
<div style="position:absolute;left:0;right:0;top:156px;text-align:center;font-weight:800;font-size:126px;letter-spacing:-.04em;line-height:1.05;white-space:nowrap">{html.escape(args.price)}</div>
<div style="position:absolute;left:0;right:0;top:302px;text-align:center;font-weight:500;font-size:31px;letter-spacing:-.01em;white-space:pre">{html.escape(args.spec)}</div>
<img src="file://{pathlib.Path(args.logo).resolve()}" style="position:absolute;left:{(1080 - lw) // 2}px;top:{PHOTO_TOP + PHOTO_H + (1350 - PHOTO_TOP - PHOTO_H - lh) // 2}px;width:{lw}px;height:{lh}px;border-radius:14px">
</div>"""


def slide_html(photo):
    return f"""<div style="position:relative;width:1080px;height:1350px;overflow:hidden;background:#021D10;display:flex;align-items:center">
<img src="file://{pathlib.Path(photo).resolve()}" style="width:1080px;display:block">
</div>"""


async def render(args):
    with tempfile.TemporaryDirectory() as tmp:
        if args.slide:
            body = slide_html(args.photo)
        else:
            photo = pathlib.Path(tmp) / "photo.jpg"
            crop_cover(args.photo, args.focus, photo)
            body = cover_html(args, photo)
        page_file = pathlib.Path(tmp) / "feed.html"
        page_file.write_text(f"<!doctype html><meta charset=utf-8><style>*{{box-sizing:border-box}}body{{margin:0}}</style>{body}", encoding="utf-8")
        png = pathlib.Path(tmp) / "feed.png"
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(viewport={"width": 1080, "height": 1350})
            await page.goto(f"file://{page_file}")
            await page.wait_for_timeout(300)
            await page.screenshot(path=str(png))
            await browser.close()
        Image.open(png).convert("RGB").save(args.out, quality=93)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    for name in ("title", "price", "spec", "logo"):
        ap.add_argument(f"--{name}")
    ap.add_argument("--photo", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--focus", type=float, default=0.5)
    ap.add_argument("--slide", action="store_true")
    asyncio.run(render(ap.parse_args()))
