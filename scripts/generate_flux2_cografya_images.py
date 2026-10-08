#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
study-forge: FLUX.2 [klein] 4B Coğrafya Görsel Sözlük Üretici
- Model: @cf/black-forest-labs/flux-2-klein-4b (Cloudflare Workers AI)
- Multipart/form-data schema desteği
- Otomatik base64 decode & Pillow 512px optimizasyonu
"""

import os
import sys
import json
import time
import subprocess
import base64
import io
from PIL import Image

CF_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
CF_ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
MODEL = "@cf/black-forest-labs/flux-2-klein-4b"

COGRAFYA_PROMPTS = [
    {
        "filename": "cf_cog_muhtesem_dortlu.jpg",
        "title": "Muhteşem Dörtlü (4 Temel Ortam)",
        "prompt": "Educational scientific infographic showing Earth four natural spheres: Lithosphere (rocky crust, mountains), Hydrosphere (oceans, blue water), Atmosphere (clouds, sky air layers), and Biosphere (forests, animals, living ecosystem). Crisp vector textbook illustration, vibrant clean colors, white background."
    },
    {
        "filename": "cf_cog_litosfer.jpg",
        "title": "Litosfer (Taş Küre)",
        "prompt": "Educational geological cross-section diagram of Earth Lithosphere showing continental crust, oceanic crust, mountain ranges, rock strata, tectonic plate layer. Clean scientific textbook vector, crisp details, white background."
    },
    {
        "filename": "cf_cog_atmosfer.jpg",
        "title": "Atmosfer (Hava Küre)",
        "prompt": "Educational scientific diagram of Earth atmosphere layers: Troposphere with weather clouds, Stratosphere, Mesosphere, Thermosphere, Exosphere. Labeled concentric atmospheric shells around globe, clean modern vector style, white background."
    },
    {
        "filename": "cf_cog_hidrosfer.jpg",
        "title": "Hidrosfer (Su Küre)",
        "prompt": "Educational scientific illustration of Earth Hydrosphere featuring global water bodies: deep ocean, cascading river, fresh lake, underground groundwater aquifer, and water cycle clouds. Clean textbook vector diagram, white background."
    },
    {
        "filename": "cf_cog_biyosfer.jpg",
        "title": "Biyosfer (Canlı Küre)",
        "prompt": "Educational scientific infographic of Earth Biosphere showing intersection of land, water, and air filled with rich biodiversity: forest wildlife, birds in sky, marine fishes in ocean. Clean harmonious nature illustration, white background."
    },
    {
        "filename": "cf_cog_dagilis_ilkesi.jpg",
        "title": "Dağılış İlkesi",
        "prompt": "Educational geographic cartography concept showing spatial distribution map of the world with thematic color gradients, geographic pins, spatial data points, compass rose, map legend. Crisp textbook graphic, white background."
    },
    {
        "filename": "cf_cog_geoit.jpg",
        "title": "Geoit Şekil ve Sonuçları",
        "prompt": "Educational physics and geography diagram of Earth Geoid shape: slightly flattened at the poles, bulging at the Equator, showing gravity force vectors larger at the poles than equator. Clean scientific textbook diagram, white background."
    },
    {
        "filename": "cf_cog_cizgisel_hiz.jpg",
        "title": "Çizgisel Hız",
        "prompt": "Educational physics diagram of spinning planet Earth showing rotational linear velocity: maximum speed vectors at the Equator, decreasing speed at mid latitudes, zero at poles. Dynamic scientific vector graphic, white background."
    },
    {
        "filename": "cf_cog_gunluk_hareket.jpg",
        "title": "Günlük (Eksen) Hareketi",
        "prompt": "Educational astronomy diagram showing Earth daily rotation around its axis from West to East in 24 hours, day and night division line, sunrise and sunset progression, timezone markers. Clean vector illustration, white background."
    },
    {
        "filename": "cf_cog_meltem.jpg",
        "title": "Meltem Rüzgarları",
        "prompt": "Educational 2-panel weather diagram showing diurnal coastal breeze: Daytime Sea Breeze blowing from cool sea to warm land, and Nighttime Land Breeze blowing from cool land to warm sea with thermal convection arrows. Clean textbook vector."
    },
    {
        "filename": "cf_cog_koriolis.jpg",
        "title": "Koriolis (Sapma) Kuvveti",
        "prompt": "Educational atmospheric physics diagram showing Coriolis effect on rotating globe: wind and ocean currents deflecting to the right in Northern Hemisphere and deflecting to the left in Southern Hemisphere. Crisp scientific graphic, white background."
    },
    {
        "filename": "cf_cog_eksen_egikligi.jpg",
        "title": "Eksen Eğikliği (23° 27')",
        "prompt": "Educational astronomy diagram showing Earth axial tilt of 23.5 degrees relative to its orbital plane around the Sun, Tropic of Cancer, Tropic of Capricorn, Polar Circles. Clean scientific vector illustration, white background."
    },
    {
        "filename": "cf_cog_ekinoks.jpg",
        "title": "21 Mart ve 23 Eylül (Ekinokslar)",
        "prompt": "Educational astronomy diagram of Earth during Equinox (March 21 and September 23): direct vertical solar rays hitting the Equator, terminator line passing exactly through both North and South poles, equal 12-hour day and 12-hour night. Clean vector."
    },
    {
        "filename": "cf_cog_21_haziran.jpg",
        "title": "21 Haziran (Yaz Solstisi)",
        "prompt": "Educational astronomy diagram of Earth during Summer Solstice (June 21): Northern hemisphere tilted toward Sun, solar rays perpendicular on Tropic of Cancer, Arctic circle in 24-hour midnight sun daylight, longest day. Clean textbook graphic."
    },
    {
        "filename": "cf_cog_21_aralik.jpg",
        "title": "21 Aralık (Kış Solstisi)",
        "prompt": "Educational astronomy diagram of Earth during Winter Solstice (December 21): Southern hemisphere tilted toward Sun, solar rays perpendicular on Tropic of Capricorn, Northern hemisphere in long winter night and shortest day. Clean textbook graphic."
    },
    {
        "filename": "cf_cog_aydinlanma_cemberi.jpg",
        "title": "Aydınlanma Çemberi",
        "prompt": "Educational astronomy diagram of Earth showing the solar terminator line (circle of illumination) clearly dividing the illuminated sunny daytime hemisphere from the shadowed nighttime hemisphere. Crisp scientific graphic, white background."
    },
    {
        "filename": "cf_cog_paraleller.jpg",
        "title": "Paraleller ve Enlem",
        "prompt": "Educational cartography diagram showing globe with horizontal parallel latitude lines from Equator 0 degrees to Poles 90 degrees North and South, showing equal 111 km spacing between degrees. Crisp vector map graphic, white background."
    },
    {
        "filename": "cf_cog_meridyenler.jpg",
        "title": "Meridyenler ve Yerel Saat",
        "prompt": "Educational cartography diagram showing globe with vertical meridian longitude lines converging at poles, Prime Meridian Greenwich 0 degrees, showing 4-minute local solar time intervals. Crisp vector map graphic, white background."
    },
    {
        "filename": "cf_cog_turkiye_konum.jpg",
        "title": "Türkiye'nin Mutlak Konumu",
        "prompt": "Educational geographic map showing country of Turkey precisely enclosed in coordinate grid: 36-42 North Latitudes and 26-45 East Longitudes, positioned in the Northern Temperate Zone. Crisp vector cartography, labeled grid, clean white background."
    },
    {
        "filename": "cf_cog_projeksiyonlar.jpg",
        "title": "Harita Projeksiyonları",
        "prompt": "Educational 3-panel comparative cartography diagram showing 3 main map projections: Cylindrical projection wrapping Equator, Conical projection over mid-latitudes, and Planar azimuthal projection over the North Pole. Clean textbook illustration."
    },
    {
        "filename": "cf_cog_izohips_egim.jpg",
        "title": "İzohipslerde Eğim ve Sıklaşma",
        "prompt": "Educational topography diagram pairing a 2D contour line map (isohypses) with a side 3D relief profile: showing dense contour lines on steep cliff mountain slope and widely spaced contour lines on gentle valley slope. Clean textbook vector."
    },
    {
        "filename": "cf_cog_vadi_sirt.jpg",
        "title": "İzohips: Vadi ve Sırt Ayrımı",
        "prompt": "Educational 2-panel topographic contour map comparing Valley vs Ridge: Valley where V-shaped contour lines point toward higher elevation with blue stream flow, and Ridge where V-shaped lines point toward lower elevation. Clean vector diagram."
    },
    {
        "filename": "cf_cog_boyun_falez.jpg",
        "title": "İzohips: Boyun, Çukur ve Falez",
        "prompt": "Educational topographic contour map showing mountain landforms: Col (saddle pass between two peaks), closed depression crater with inward hachures, and coastal cliff (falez) where contours stack at shoreline. Clean labeled diagram."
    },
    {
        "filename": "cf_cog_delta.jpg",
        "title": "İzohips: Delta Ovası",
        "prompt": "Educational topography and geography diagram of a river Delta plain: river dividing into distributary branches and depositing rich alluvial fan into sea creating triangular coastal landform, shallow continental shelf. Clean textbook vector."
    }
]

def generate_flux2_image(prompt, out_path):
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/{MODEL}"
    
    cmd = [
        "curl", "-s", "-S",
        "--resolve", "api.cloudflare.com:443:104.19.192.29",
        "-X", "POST", url,
        "-H", f"Authorization: Bearer {CF_TOKEN}",
        "-F", f"prompt={prompt}",
        "--max-time", "180"
    ]
    
    try:
        res = subprocess.run(cmd, capture_output=True, timeout=190)
        if res.returncode != 0:
            return False, f"Curl hatası: {res.stderr.decode('utf-8')[:80]}"
        
        data = json.loads(res.stdout.decode('utf-8'))
        if not data.get("success"):
            err = data.get("errors", [{}])[0].get("message", "Bilinmeyen API hatası")
            return False, f"API Hatası: {err}"
        
        img_b64 = data.get("result", {}).get("image")
        if not img_b64:
            return False, "JSON içinde 'image' anahtarı bulunamadı"
        
        img_bytes = base64.b64decode(img_b64)
        im = Image.open(io.BytesIO(img_bytes))
        im = im.convert('RGB')
        im.thumbnail((512, 512), Image.Resampling.LANCZOS)
        im.save(out_path, format='JPEG', quality=75, optimize=True)
        
        fsize = os.path.getsize(out_path)
        return True, f"512x512 JPEG ({fsize // 1024} KB)"
    except Exception as e:
        return False, str(e)

def main():
    media_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "anki_decks", "media"))
    os.makedirs(media_dir, exist_ok=True)
    
    print(f"🚀 FLUX.2 [klein] 4B ile 24 Coğrafya Görseli Üretimi Başlatılıyor...")
    print(f"📂 Hedef Dizin: {media_dir}")
    print(f"⚡ Model: {MODEL}\n")
    
    total = len(COGRAFYA_PROMPTS)
    success_count = 0
    
    for idx, item in enumerate(COGRAFYA_PROMPTS):
        fname = item["filename"]
        out_path = os.path.join(media_dir, fname)
        title = item["title"]
        prompt = item["prompt"]
        
        print(f"[{idx+1:02d}/{total:02d}] 🎨 {title} ({fname})...")
        t0 = time.time()
        ok, msg = generate_flux2_image(prompt, out_path)
        elapsed = time.time() - t0
        
        if ok:
            success_count += 1
            print(f"       ✅ Başarılı ({elapsed:.1f}s) - {msg}")
        else:
            print(f"       ❌ Hata ({elapsed:.1f}s): {msg}")
        
        time.sleep(1.0)
        
    print(f"\n✨ FLUX.2 Üretim Tamamlandı: {success_count}/{total} görsel başarıyla oluşturuldu ve optimize edildi.")

if __name__ == "__main__":
    main()
