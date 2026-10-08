#!/usr/bin/env node
/**
 * study-forge: Ultra-Lightweight Node.js FLUX.2 Klein Image Generator
 * - Model: @cf/black-forest-labs/flux-2-klein-4b (Cloudflare Workers AI)
 * - Stil: 3D Isometric Educational Clay / Pixar-style Digital Art (Textless, No Words)
 * - Optimizasyon: Native ImageMagick (convert) 512x512 JPEG 75Q
 */

const fs = require('fs');
const path = require('path');
const { execFile } = require('child_process');

const CF_TOKEN = process.env.CLOUDFLARE_API_TOKEN || "";
const CF_ACCOUNT_ID = process.env.CLOUDFLARE_ACCOUNT_ID || "";
const MODEL = "@cf/black-forest-labs/flux-2-klein-4b";

const MEDIA_DIR = path.resolve(__dirname, '../data/anki_decks/media');

const PROMPTS = [
  {
    filename: "flux_v3_cog_muhtesem_dortlu.jpg",
    title: "Muhteşem Dörtlü (4 Temel Ortam)",
    prompt: "A stunning 3D isometric cross-section cube of planet Earth floating in space, divided into four interconnected magical elemental quadrants: glowing volcanic rock and mountain strata (Lithosphere), sparkling crystal blue oceans and waterfalls (Hydrosphere), swirling translucent atmospheric clouds (Atmosphere), and a lush vibrant miniature rainforest teeming with wildlife (Biosphere). Vibrant Pixar-style 3D render, soft ambient lighting, clean solid background, textless, no words, no letters."
  },
  {
    filename: "flux_v3_cog_litosfer.jpg",
    title: "Litosfer (Taş Küre)",
    prompt: "A beautiful 3D isometric geological cross-section block of Earth crust, displaying rugged mountain peaks, sedimentary rock strata layers, glowing magma layer underneath, tectonic plates shifting, miniature volcano. Stylized 3D clay aesthetic, warm studio lighting, clean solid background, textless, no text, no labels."
  },
  {
    filename: "flux_v3_cog_atmosfer.jpg",
    title: "Atmosfer (Hava Küre)",
    prompt: "A glowing stylized 3D planet Earth surrounded by concentric glowing translucent rings of atmosphere, floating fluffy white storm clouds, aurora borealis light trails, and sparkling satellites in outer orbit. Soft neon glow, Pixar aesthetic 3D render, solid background, textless, no words."
  },
  {
    filename: "flux_v3_cog_hidrosfer.jpg",
    title: "Hidrosfer (Su Küre)",
    prompt: "A magnificent 3D isometric water wonderland floating sphere: deep sapphire ocean with swimming whales, cascading crystal clear waterfall into a calm lake, dynamic rain clouds showering droplets. Vibrant 3D digital art, sparkling reflections, clean background, textless, no text, no letters."
  },
  {
    filename: "flux_v3_cog_biyosfer.jpg",
    title: "Biyosfer (Canlı Küre)",
    prompt: "A vibrant 3D miniature floating island of rich biodiversity: lush emerald canopy trees, colorful tropical birds flying, deer walking through blooming flowers, coral reef visible underwater. Warm golden sunlight, charming stylized 3D render, clean background, textless, no labels."
  },
  {
    filename: "flux_v3_cog_dagilis_ilkesi.jpg",
    title: "Dağılış İlkesi",
    prompt: "A stylized 3D tabletop antique cartographer desk with a glowing holographic world globe projecting colorful shimmering pinpoint light beacons and migration flow lines across continents, golden compass, brass magnifying glass. Cinematic warm lighting, clean studio background, textless, no words, no text."
  },
  {
    filename: "flux_v3_cog_geoit.jpg",
    title: "Geoit Şekil ve Sonuçları",
    prompt: "A humorous and clear 3D stylized globe showing exaggerated oblate spheroid shape: flattened top and bottom polar ice caps, bulging glowing equatorial belt, miniature gravity pull arrows pulling stronger at poles. Vibrant 3D clay model, studio lighting, textless, no text."
  },
  {
    filename: "flux_v3_cog_cizgisel_hiz.jpg",
    title: "Çizgisel Hız",
    prompt: "A dynamic 3D spinning planet Earth with bright glowing neon speed motion streaks rushing rapidly around the wide equator, while the polar axes remain calm and still, showing high-speed rotation. Futuristic clean 3D render, solid background, textless, no words."
  },
  {
    filename: "flux_v3_cog_gunluk_hareket.jpg",
    title: "Günlük (Eksen) Hareketi",
    prompt: "A striking 3D isometric globe split down the middle into contrasting halves: golden bright sunny morning with glowing sun on the right half, and deep starry night with glowing moon and city lights on the left half, smooth spinning axis tilt. High-end 3D art, textless, no text."
  },
  {
    filename: "flux_v3_cog_meltem.jpg",
    title: "Meltem Rüzgarları",
    prompt: "A charming 3D isometric coastal beach scene split between day and night: daytime side showing cool breeze blowing from glistening sea toward warm sandy hills, nighttime side showing cool breeze flowing from dark hills back to sea. Colorful 3D clay render, textless, no text."
  },
  {
    filename: "flux_v3_cog_koriolis.jpg",
    title: "Koriolis (Sapma) Kuvveti",
    prompt: "A 3D spinning globe viewed from space with colorful glowing wind ribbons curving gracefully to the right in northern hemisphere and curving to the left in southern hemisphere due to planetary spin. Clean scientific visual metaphor, textless, no text, no letters."
  },
  {
    filename: "flux_v3_cog_eksen_egikligi.jpg",
    title: "Eksen Eğikliği (23° 27')",
    prompt: "A whimsical 3D astronomical diorama showing planet Earth tilted at a distinct angle on its orbital golden ring circling a radiant glowing smiling sun, casting changing seasonal light patterns. Pixar-style lighting, solid background, textless, no text."
  },
  {
    filename: "flux_v3_cog_ekinoks.jpg",
    title: "21 Mart ve 23 Eylül (Ekinokslar)",
    prompt: "A 3D celestial diorama of planet Earth perfectly balanced in space, golden solar beams hitting directly onto the central equator line, illuminating exactly half the globe from North pole to South pole equally. Harmonious warm lighting, textless, no text."
  },
  {
    filename: "flux_v3_cog_21_haziran.jpg",
    title: "21 Haziran (Yaz Solstisi)",
    prompt: "A 3D cosmic diorama showing planet Earth with its northern polar region completely bathed in perpetual 24-hour golden sunlight, lush blooming summer nature on the top half, dark winter ice on the bottom half. Vibrant 3D art, textless, no text."
  },
  {
    filename: "flux_v3_cog_21_aralik.jpg",
    title: "21 Aralık (Kış Solstisi)",
    prompt: "A 3D cosmic diorama showing planet Earth with its northern hemisphere shrouded in cozy dark snowy winter night with aurora, while the southern hemisphere is fully sunlit and golden. Contrasting seasonal diorama, textless, no text."
  },
  {
    filename: "flux_v3_cog_aydinlanma_cemberi.jpg",
    title: "Aydınlanma Çemberi",
    prompt: "A smooth minimalist 3D Earth floating in dark space with a razor-sharp glowing golden twilight ring dividing radiant daylight from deep cosmic shadow, city lights twinkling on night side. Cinematic 3D render, textless, no text."
  },
  {
    filename: "flux_v3_cog_paraleller.jpg",
    title: "Paraleller ve Enlem",
    prompt: "A gorgeous translucent crystalline 3D globe encircled by evenly spaced glowing golden horizontal rings from bottom to top, gleaming like latitude bands with equal spacing. Elegant minimalist 3D design, clean solid background, textless, no text."
  },
  {
    filename: "flux_v3_cog_meridyenler.jpg",
    title: "Meridyenler ve Yerel Saat",
    prompt: "A glowing glass 3D globe with vertical golden meridian rib arches converging at the poles, illuminated miniature pocket watches glowing softly along the longitudinal arcs showing changing solar hours. Beautiful 3D visualization, textless, no numbers, no text."
  },
  {
    filename: "flux_v3_cog_turkiye_konum.jpg",
    title: "Türkiye'nin Mutlak Konumu",
    prompt: "A vibrant 3D relief map tile of the Anatolian peninsula of Turkey glowing in emerald and golden hills, situated between deep blue Black Sea and Mediterranean Sea, framed by glowing coordinates lattice. High-end 3D miniature map, clean background, textless, no text."
  },
  {
    filename: "flux_v3_cog_projeksiyonlar.jpg",
    title: "Harita Projeksiyonları",
    prompt: "A creative 3D isometric laboratory showing a glowing transparent Earth globe being wrapped by three origami paper geometric shapes: a cylinder around equator, a cone on top, and a flat disc on the pole. Cute 3D clay aesthetic, clean background, textless, no text."
  },
  {
    filename: "flux_v3_cog_izohips_egim.jpg",
    title: "İzohipslerde Eğim ve Sıklaşma",
    prompt: "A 3D isometric terrain model featuring a dramatic mountain: one side is a sheer vertical cliff with tightly packed glowing contour tiers, the other side is a gentle rolling meadow with widely spaced terraces and meandering brook. Stylized 3D render, textless, no text."
  },
  {
    filename: "flux_v3_cog_vadi_sirt.jpg",
    title: "İzohips: Vadi ve Sırt Ayrımı",
    prompt: "A 3D isometric comparative landscape: on left a deep carved mountain valley with a sparkling blue river running down the V-crease, on right a prominent mountain ridge crest sloping outward like an elevated spine. Beautiful 3D terrain diorama, textless, no text."
  },
  {
    filename: "flux_v3_cog_boyun_falez.jpg",
    title: "İzohips: Boyun, Çukur ve Falez",
    prompt: "A 3D isometric mountain diorama showing three distinct landforms: a saddle pass between two twin peaks, a circular volcanic crater depression, and a sheer coastal sea cliff dropping into ocean waves. Charming 3D nature model, textless, no text."
  },
  {
    filename: "flux_v3_cog_delta.jpg",
    title: "İzohips: Delta Ovası",
    prompt: "A breathtaking 3D isometric coastal landscape showing a major meandering river branching out into a lush green triangular fan-shaped delta entering a turquoise calm sea, rich alluvial deposits. Vibrant 3D diorama, clean background, textless, no text."
  }
];

function curlGenerate(prompt) {
  const url = `https://api.cloudflare.com/client/v4/accounts/${CF_ACCOUNT_ID}/ai/run/${MODEL}`;
  const args = [
    '-s', '-S',
    '--resolve', 'api.cloudflare.com:443:104.19.192.29',
    '-X', 'POST', url,
    '-H', `Authorization: Bearer ${CF_TOKEN}`,
    '-F', `prompt=${prompt}`,
    '--max-time', '180'
  ];

  return new Promise((resolve, reject) => {
    execFile('curl', args, { maxBuffer: 10 * 1024 * 1024 }, (err, stdout, stderr) => {
      if (err) return reject(new Error(`Curl error: ${stderr || err.message}`));
      try {
        const data = JSON.parse(stdout);
        if (!data.success) {
          const msg = data.errors?.[0]?.message || 'API error';
          return reject(new Error(`API Error: ${msg}`));
        }
        const imgB64 = data.result?.image;
        if (!imgB64) return reject(new Error("No 'image' field in JSON response"));
        resolve(Buffer.from(imgB64, 'base64'));
      } catch (e) {
        reject(new Error(`JSON Parse Error: ${e.message} - raw: ${stdout.slice(0, 100)}`));
      }
    });
  });
}

function optimizeWithConvert(inputBuffer, outPath) {
  const tmpPath = outPath + '.tmp.jpg';
  fs.writeFileSync(tmpPath, inputBuffer);

  return new Promise((resolve, reject) => {
    execFile('convert', [tmpPath, '-resize', '512x512', '-quality', '75', outPath], (err) => {
      try { fs.unlinkSync(tmpPath); } catch {}
      if (err) return reject(err);
      const stats = fs.statSync(outPath);
      resolve(`${Math.round(stats.size / 1024)} KB`);
    });
  });
}

async function run() {
  fs.mkdirSync(MEDIA_DIR, { recursive: true });
  console.log(`🚀 [Node.js] FLUX.2 Klein 4B 3D-Isometric Yazısız Görsel Üretimi Başlatılıyor...`);
  console.log(`📂 Medya Dizini: ${MEDIA_DIR}`);
  console.log(`⚡ Model: ${MODEL} (Sıfır CPU Yükü, Hafif Node.js + C-ImageMagick)\n`);

  let successCount = 0;
  const total = PROMPTS.length;

  for (let i = 0; i < total; i++) {
    const item = PROMPTS[i];
    const outPath = path.join(MEDIA_DIR, item.filename);
    const num = String(i + 1).padStart(2, '0');

    console.log(`[${num}/${total}] 🎨 ${item.title} (${item.filename})...`);
    const t0 = Date.now();

    try {
      const imgBuffer = await curlGenerate(item.prompt);
      const sizeStr = await optimizeWithConvert(imgBuffer, outPath);
      const elapsed = ((Date.now() - t0) / 1000).toFixed(1);
      console.log(`       ✅ Başarılı (${elapsed}s) - 512x512 3D JPEG (${sizeStr})`);
      successCount++;
    } catch (err) {
      const elapsed = ((Date.now() - t0) / 1000).toFixed(1);
      console.log(`       ❌ Hata (${elapsed}s): ${err.message}`);
    }

    // Kısa bekleme
    await new Promise(r => setTimeout(r, 1000));
  }

  console.log(`\n✨ Node.js FLUX.2 Üretimi Tamamlandı: ${successCount}/${total} görsel oluşturuldu.`);
}

run().catch(console.error);
