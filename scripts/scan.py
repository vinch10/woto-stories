#!/usr/bin/env python3
"""Scanne tout le stock Woto via le sitemap et écrit inventory.json.

Usage : scan.py [--out inventory.json]
"""
import argparse
import concurrent.futures as cf
import json
import re
import urllib.request

SITEMAP_LISTINGS = "https://app.woto.be/sitemap-listings-fr.xml"
SITEMAP_DEALERS = "https://app.woto.be/sitemap-dealers-fr.xml"
UA = {"User-Agent": "woto-stories/1.0"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=40) as r:
        return r.read().decode("utf-8", "replace")


def locs(xml):
    return re.findall(r"<loc>([^<]+)</loc>", xml)


def ld_blocks(html):
    out = []
    for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            out.append(json.loads(raw))
        except ValueError:
            pass
    return out


def num(v):
    if isinstance(v, dict):
        v = v.get("value")
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


def parse_listing(url):
    html = get(url)
    car = next((b for b in ld_blocks(html) if "Car" in (b.get("@type") or [])), None)
    if not car:
        return {"url": url, "error": "pas de données structurées"}
    offers = car.get("offers") or {}
    if isinstance(offers, list):
        offers = offers[0] if offers else {}
    seller = offers.get("seller") or car.get("seller") or {}
    desc = car.get("description") or ""
    km_text = None
    m = re.search(r"(?:km\s*:\s*|affiche\s+)(\d{1,3}(?:[ . ]\d{3})+|\d+)", desc, re.I)
    if m:
        km_text = int(re.sub(r"\D", "", m.group(1)))
    logos = re.findall(r"https://[a-z0-9.]+/storage/v1/object/public/organization-logos/[^\"'\\\s<>]+", html)
    images = car.get("image") or []
    if isinstance(images, str):
        images = [images]
    images = [i if isinstance(i, str) else i.get("url") for i in images]
    gallery = re.findall(r"https://[a-z0-9.]+/storage/v1/object/public/listing-images/[^\"'\\\s<>]+", html)
    images = list(dict.fromkeys(images + gallery))
    dealer = re.findall(r'href="(?:https://[a-z.]+)?(/professional/[^"?#]+)"', html)
    avail = str(offers.get("availability") or "")
    return {
        "url": url,
        "id": url.rstrip("/").split("/")[-1],
        "name": car.get("name"),
        "brand": (car.get("brand") or {}).get("name") if isinstance(car.get("brand"), dict) else car.get("brand"),
        "model": car.get("model"),
        "price": num(offers.get("price")),
        "km_field": num(car.get("mileageFromOdometer")),
        "km_description": km_text,
        "car_pass_in_description": bool(re.search(r"car-?pass", desc, re.I)),
        "year": car.get("vehicleModelDate") or car.get("productionDate") or car.get("dateVehicleFirstRegistered"),
        "fuel": car.get("fuelType") if not isinstance(car.get("vehicleEngine"), dict) else (car.get("fuelType") or car["vehicleEngine"].get("fuelType")),
        "gearbox": car.get("vehicleTransmission"),
        "seller": seller.get("name") if isinstance(seller, dict) else seller,
        "seller_page": dealer[0] if dealer else None,
        "logo": logos[0] if logos else None,
        "availability": avail.rsplit("/", 1)[-1],
        "images": images,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="inventory.json")
    args = ap.parse_args()
    urls = locs(get(SITEMAP_LISTINGS))
    dealers = locs(get(SITEMAP_DEALERS))
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(lambda u: _safe(u), urls))
    data = {"listings_in_sitemap": len(urls), "dealer_pages_in_sitemap": dealers, "listings": results}
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    errors = [r for r in results if r.get("error")]
    print(f"{len(results)} fiches lues, {len(errors)} en erreur, {len(dealers)} pages garage dans le sitemap")


def _safe(url):
    try:
        return parse_listing(url)
    except Exception as exc:  # une fiche en panne ne bloque pas le scan
        return {"url": url, "error": str(exc)}


if __name__ == "__main__":
    main()
