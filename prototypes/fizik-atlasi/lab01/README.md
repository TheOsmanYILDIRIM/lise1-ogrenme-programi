# Fizik Atlası — Laboratuvar 01

9. sınıf Fizik Bilimi ve Kariyer Keşfi için **özerk, çevrimdışı, mobil uyumlu** deney temelli web prototipi. FİZ.9.1.2 alt dalları deneylerle tanıma ana hedefidir; FİZ.9.1.1–9.1.4 kapsam notları `docs/EDUCATION_AND_MEDIA_PLAN.md` içindedir.

## Hemen çalıştır

`dist/index.html` dosyasını modern tarayıcıda aç. Tek dosyada stil, veri, mantık ve Canvas çizimleri gömülüdür. Sunucu, paket kurulum veya API anahtarı yoktur.

## Geliştirme

```sh
node build.mjs
node --test tests/domain.test.mjs
python tests/e2e.py
```

Node 22+, Playwright Python ve Chromium yalnız uçtan uca testte gerekir. Üretim yapısı `src/domain.mjs` + `src/app.mjs` + `src/styles.css` + HTML şablonudur. `build.mjs` modül grafiğini kontrol edip kapalı grafikten tek HTML çıkarır. `dist/index.html` yayımlanabilir final dosyadır.

## Oynanış

Eğim, prizma, mıknatıs ve ısı istasyonlarında tahmin → iki anlamlı farklı parametreyle deney → açıklama; ardından sekiz alan sınıflandırması ve dört bağımsız transfer görevi. İpucu sayısı, ilk deneme doğruluğu ve istasyon kaydı raporlanır. Demo skoru akademik sertifika değildir. Çizimler bilimsel hesap yerine geçmez; sadeleştirmeler ve model sınırları tasarım belgesindedir.

## Gizlilik / koruma

Bu dal bağımsız prototiptir; StudyTracker uygulama kaynakları, yayınlanmış katalog, öğrenci hesapları/ilerlemesi, KV, Room ve kanonik müfredat dosyaları değiştirilmedi. Tarayıcıdaki yalnız oyunla ilgili `fizik-atlasi-lab01-v1` anahtarı kullanılır; kullanıcı sıfırladığında bu anahtar silinir. Dışarıya otomatik rapor gönderilmez.

## Görsel / video

Şimdilik tüm sahneler kodla Canvas üzerinden çizilir ve çalışır. GPT Image 2.5 varlık paketi ile Veo 3.1 beş kliplik sinematik planı hazırlanmıştır; üretim yapılmış gibi gösterilmez. Video oyun mantığını veya öğrenme kanıtlarını belirlemez.
