# Web yayını, LÖVE2D ve önbellek sözleşmesi

## Teknoloji
- Mevcut kaynak: ES Modules + CSS, Node build ile tek dist/index.html. GitHub Pages ES6 modüllerine veya tek dosya build'e engel değildir.
- LÖVE2D: bir sonraki adımda 11.5 uyumlu love.js compatibility proof-of-concept; motor henüz dönüştürülmedi. Lua modülleri kaynak, JS/WASM runtime + hashli .love oyun paketi web dağıtımı.
- LÖVE seçilirse Android ve PC aynı Lua oyun kaynağından; web için WebGL, touch, audio unlock, tam ekran, IndexedDB ve shader kısıtları gerçek cihazda denenmeli.

## Cache güncelleme sözleşmesi
1. Her build'de commit SHA ve içerik hash'i üreten bir version.json manifesti yayınlanmalı.
2. Sabit index.html ve version.json yolları Cache-Control: no-store, max-age=0; içerik-hashli /assets/* yolları Cache-Control: public, max-age=31536000, immutable.
3. love.js IndexedDB paket cache kullanabilir. Geliştirmede player.js?g=game.love&n=1; yayında game.<sha>.love gibi hashli URL'ler. Kaynak gerçek dosya isimleriyle eşleşmeli.
4. Güncellemelerde kullanıcıya ait ilerleme kayıtları asla topluca silinmez. Yalnız uygulama varlık-cache alanları kontrollü temizlenir.
5. Service Worker prototipte bulunmaz; ileride eklenirse versioned ve scoped cache ile güvenli migration yapılır.
6. GitHub Pages kendi HTTP cache / COOP / COEP başlıkları üzerinde yeterli kontrol sağlamadığından, GitHub kaynaklı Cloudflare Pages preview + _headers daha iyi bir WASM/CDN adayıdır. GitHub Actions yalnız doğrulanmış artifact yayınlar.

## Cloudflare Pages _headers önerisi
    /index.html
      Cache-Control: no-store, max-age=0
    /version.json
      Cache-Control: no-store, max-age=0
    /assets/*
      Cache-Control: public, max-age=31536000, immutable
Bu immutable kural yalnız hashli varlıklarda geçerlidir. SharedArrayBuffer gerektiren love.js sürümlerinin COOP/COEP başlıkları ilk web PoC ölçümünden sonra eklenir.

## Gerçek test ve sınırlamalar
- Önceki rampa animasyonu 1.7 s zaman tavanıyla donuk kalıyordu. Yeni build ilk açılışta tekrar eden hareket önizlemesi sunuyor, 'Deneyi çalıştır' ile yeniden başlıyor. Şematik yol s=0.5*a*t^2, 4 metre çizim pisti.
- Node temel testleri 7/7 başarılı, 390px Chromium'da iki canvas karesi 900 ms arayla farklı bulundu. Gerçek Android cihaz henüz test edilmedi.
- Herhangi bir public preview, Pages deploy'u ve CDΝ cache header/doğru sürüm doğrulaması bu aşamada henüz yapılmadı.
