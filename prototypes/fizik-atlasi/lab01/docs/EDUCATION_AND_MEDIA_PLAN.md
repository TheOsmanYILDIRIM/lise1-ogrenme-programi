# Fizik Atlası — Lab 01: bilimsel, pedagojik ve üretim planı

Durum: oynanabilir çevrimdışı prototip, 2026-10-16. Yapay zekâ modeliyle fotoğraf/video **üretilmedi**; şimdi çalışan dört simülasyon prosedürel Canvas çizimidir. Aşağıdaki istemler gelecekte üretim içindir.

## 1. Kaynak ve müfredat bağlantısı

- Müfredat deposu: `TheOsmanYILDIRIM/lise1-ogrenme-programi`, `main` doğrulanan ilk HEAD `1e9dc9d99e0db7230e0b020180ab6f055ce643de`.
- Kanonik kaynak: `curriculum/yillik_planlar/Fizik_Yillik_Plan_AL9.md`, 1–4. haftalar; ayrıca repo `AGENTS.md` ve `INDEX.md`.
- Uygulama konu envanteri: `TheOsmanYILDIRIM/study-tracker` / `main` `c4e254bac75fda1c7c8a4c62be530bee4d6035a5`, `content/v2/topic-blueprint.json` ve `content/v2/courses/course_fiz_9.json`.
- MEB 2026 zenginleştirilmiş etkinlik metni referansı: `lise1-ogrenme-programi/data/meb_kitaplari/fizik9.md`. Metindeki etkinlikleri kopyalamak yerine pedagojik hedeflerden yeni senaryolar üretilmiştir.

| Kod | Yıllık plandaki süreç bileşenleri | Bu sürümün kanıtı | Durum |
|---|---|---|---|
| FİZ.9.1.1 | Diğer disiplinlerle ilişkileri belirle, yararlanarak fizik bilimini tanımla | Dört gözleme dayalı fizik olayı + açıklama; *diğer disiplin* araştırması ve öğrenci tanımı henüz yok | Giriş / kısmi |
| FİZ.9.1.2 | Alt dalların özelliklerini belirle, ayrıştır, gruplandır, çalışma alanıyla eşleştir | Dört deneyden iki koşullu veri + açıklama, sekiz günlük/teknik olay sınıflandırması ve dört bağımsız transfer sorusu | Pilot değerlendirme |
| FİZ.9.1.3 | Bilim insanlarının yaklaşım ve çalışmasını incele, çıkarım üret, değerlendir | Henüz sahne ve mekanik yok | Gelecek bölüm |
| FİZ.9.1.4 | Kariyer sorusu belirle/sor, veri topla, güvenilirliğini değerlendir, çıkarım üret | Henüz kaynak değerlendirme ve araştırma günlükleri yok | Gelecek bölüm |

**Sınırlama:** Prototipteki puanlar resmî öğrenme belgesi değildir. FİZ.9.1.2 için süreç bileşenlerinin ön değerlendirmesidir; çevrimiçi öğretmen geri bildirimi, öğrenci kimliği ve psikometrik kalibrasyon içermez. 9.1.1, 9.1.3 ve 9.1.4 tamamlama iddiası yoktur.

## 2. Oyun döngüsü ve bilimsel doğruluk

1. Her istasyonda önce *beklenti* kaydedilir. Yanlış tahmin cezalandırılmaz; ön bilgi kanıtıdır.
2. Parametre gerçekten hesaplama/görselleştirmeyi değiştirir. İki **anlamlı farklı** koşul kaydetmek gerekir (mekanik en az 6° ya da sürtünme; optik renk ya da en az 8°; manyetik konum en az 12 puan ya da güç 25 puan; termal malzeme ya da kaynak sıcaklığı en az 20°C).
3. Ölçümün açıklaması doğru verilince istasyon tamamlanır. Sonuçları görmeden açıklama yoktur.
4. Sekiz alanın temel uzmanlığıyla sekiz yeni olay eşleştirilir. İlk yanıt / yardım takibi tutulur.
5. Dört aktarım görevinde yardım yoktur. 4/4 deney + sınıflandırmada ilk denemede en az 6/8 + aktarımda 3/4 + en fazla üç ipucu olduğunda **güçlü aday öğrenme göstergesi** gösterilir.

Bilimsel uyarılar: eğim düzeneği sabit sürtünme katsayısıyla (yaklaşık) hesaplanır; prizma modelinde fiziksel kırılma açıları hesaplanmaz, altı renk görünür spektrum örneklemesidir; manyetik çekim için gerçek alan denklemi çözülmez, görsel etki niteliktir; termal yayılım matematiksel bir ısı iletim PDE çözümü değil niteliksel animasyondur. Kesin veriymiş gibi sunulmamalıdır. Dört temel deney FİZ.9.1.2'nin **alan tanıma** hedefi için araçtır, kendi başlarına üst sınıf düzeyi nicel kazanım testleri değildir.

## 3. Görsel kimlik — GPT Image 2.5 üretim varlık planı

Tüm görseller aynı sanat anayasasına bağlı kalmalı:
- Stil: **premium 3D stylized interactive science museum**, oyun içi sağlam fiziksel hacimler, çağdaş ama sıcak mekânlar, okunabilir basit siluetler; karanlık petrol mavisi `#102c3b`, turkuaz `#9be9ce`, açık kehribar `#f8cd8f`, bakır `#da8676` ve düşük doygunluklu mineral yüzeyler.
- Kamera: göz hizasından hafif üstten 3/4, yaklaşık 35mm lens hissi, deney masasına odaklanan doğal perspektif; tüm odalarda sabit yatay bakış yönü ve benzer ışık şiddeti.
- Karakter: logo ve marka içermeyen, kapalı laboratuvar önlüğü ve minik omuz tableti taşıyan genç araştırmacı avatari, yaşça uygun ve abartısız.
- Sahne: aynı ana müze binasının dört kanadı, tekrar kullanılan kapı/zemin/modüler raf/kontrol konsolu, nesnelerin ölçekleri tutarlı.
- Yasak/kaçınılacak: okunamayan sahte harfler, deney kabının içine yüzen metin, hatalı kablo/fizik sahneleri, bulanık öğeler, aşırı parçacık kalabalığı, laboratuvarda korumasız tehlikeli deney canlandırmaları.

**Ortak istem gövdesi (değişmeden kullanılacak):**

> Consistent premium stylized 3D educational science-adventure game art. Recurring modular science museum architecture, deep navy-teal walls, mint holographic accents, restrained copper-amber rim lights, clean readable science instruments, 3/4 camera view, mild orthographic game-composition feel, 35mm lens, warm accessible wonder, high-quality physically plausible geometry, no logos, no text, no glyphs, no watermarks, same scene materials, same lighting orientation, no people unless reference character is given. Compose with safe empty UI margin in the upper corners.

Üretim listesi:

| ID | İçerik / varyasyon | Format | Devreye alma |
|---|---|---|---|
| `museum_hub_v1` | 4 kapılı giriş merkezi, ana kompozisyon | 16:9 WEBP, 1920×1080 hedef | Giriş / bölüm ekranı |
| `ramp_lab_v1` | Eğik düzlem ve iki yüzeyli deney masası; *hareket* gifi/asseti ayrıca katmanlı | 16:9 arka plan, saydam nesne PNG | Mekanik sahnesi |
| `optics_lab_v1` | Cam üçgen prizma, ayrı beyaz/kırmızı/mavi ışık kaynağı, ışın maskeleri | 16:9 arka plan + alpha PNG | Optik sahnesi |
| `magnet_lab_v1` | Kırmızı-mavi çubuk mıknatıs, demir bilye, ahşap blok, alan çizgisi overlay ayrı | alpha PNG nesneler | Manyetik sahne |
| `thermal_lab_v1` | Isıtıcı, metal ve ahşap çubuk, sıcaklık maskesi ayrı | alpha PNG nesneler | Isı sahnesi |
| `science_avatar_v1` | Tutarlı karakter, ön/yan/3-4 görünüm ve yüz ifadesi atlası | 1024px PNG atlas, alfa | Diyalog/UI |

Referans ve kompozisyon denetimi: `museum_hub_v1` onaylandıktan sonra diğer istasyonlar için renk, dolap, malzeme ve kamera referansı verilecek; her sonuç için 390px ve 360px mobil kesit, metin yerleşim boşluğu, nesne kontur okunurluğu ve neden-sonuç işaretlerinin açıklığı kontrol edilecek. Gerçek zamanlı simülasyon nesnelerini bütünleşik arka plana gömmek yerine ayrıştırılmış saydam katmanlar tutulacak. İnsan onayından geçmeden assetler otomatik yayınlanmayacak.

## 4. Veo 3.1 — sinematik kısa sahne/çekim listesi

**Veo yalnız hikâye, neden merakı ve duygusal bağ kurmak için kullanılacak; fiziksel hüküm ve oyuncu etkileşimi oyun motorunda kalır.** Üretim hedefi ilk 4 sahne için her biri yaklaşık 6–8 sn; yatay 16:9 ana master, mobil dikey kırpma ayrıca denetlenir. Sessiz/altyazı alternatifi bulunur; herhangi bir video yüklenemediğinde doğrudan canlı laboratuvara girilir.

| Klip | Görsel / ilk kare → son kare | Öğrenmedeki işlev | Oyun motoru geçişi |
|---|---|---|---|
| `intro_gate_v1` | Müze atriumundaki dört kapı karanlık → kontrollü ışıklar açılıyor; avatar işareti görüyor | Merak ve görev çağrısı | Oyuncu "Laboratuvara gir" seçer |
| `ramp_issue_v1` | İki farklı rampadan biri yavaş öteki hızlı, araştırmacı farkı sorguluyor | Tahmin tetikleme | Video durur; öğrenci eğim/sürtünme kontrollerini devralır |
| `light_issue_v1` | Işık demeti cam prizmaya yaklaşır → görüntü beyaz demet prizmada kesilir | Işık sorusu | Ayrılmayı birebir video canlandırmaz; motor beyaz/tek renk farkını gösterir |
| `magnet_issue_v1` | Deney masasında demir ve ahşap; mıknatıs uzakta → yaklaşma öncesi freeze | Ön görü oluşturma | Hareketi ve malzeme etkisini oyuncu deneyler |
| `thermal_issue_v1` | İki çubuk soğuk masada → ısı kaynağı açılmak üzere | Isı transferine merak | Malzeme seçimi ve nitel yayılma animasyonu motor tarafından hesaplanır |

**Tüm Veo klipleri için sahne kısıtı:** preserve museum visual bible, same surfaces and avatar, static/slow dolly camera, no spoken equations, no on-video instructional text or watermark, no implied guaranteed physical predictions, 1–2 second uncluttered holds at beginning and end, cinematic ambient sound with captioned alternative, no fast flashing. İlk ve son kareleri referans storyboard olarak sakla; üretim çıktılarından hiçbirini "bilimsel deneyin ölçüm sonucu" olarak değerlendirme.

## 5. Teknik yapı ve bütünlük

- Kaynak: `src/domain.mjs` (saf bilimsel hesap, görev verileri, kanıt), `src/app.mjs` (DOM, olaylar, Canvas sahneleri), `src/styles.css` (uyarlanabilir tema), `src/index.tpl.html` (erişilebilir başlangıç).
- Derleme: `node build.mjs`: bağımsız, deterministik iki ES Modülü için kapalı grafikli küçük bundler; CSS/JS tek `dist/index.html` içine gömülür. Dağıtım dosyası internet gerektirmez.
- Testler: `node --test tests/domain.test.mjs` (fizik/kanıt kuralları), `python tests/e2e.py` (gerçek Chromium DOM etkileşimi, 360/390/1280px, 4 istasyon+8 kart+4 transfer). Chromium yönetim politikası URL navigasyonunu engellediğinden test yerel HTML'yi `set_content` ile tarayıcıya yükler; kalıcı `localStorage` tarayıcı yeniden açma davranışı bu kısıtlı ortamda tam e2e doğrulanmış değildir.
- Gizlilik: yalnız `fizik-atlasi-lab01-v1` anahtarıyla aynı tarayıcıda yerel kayıt; kullanıcı onayı olmadan sunucu isteği/izleyici/öğrenci adı yok. `Reset` sadece bu anahtarı siler; StudyTracker KV/Room/Android veri akışıyla bağlantı **yok**.
- Görsel erişilebilirlik: düğmeler klavye erişimli, menüler mobil, slider ve alternatif metinler, `prefers-reduced-motion`, kontrastlı etiketler; grafiklerde renk dışındaki metinsel açıklamalar korunur.
- Sonraki üretim: Öğrenci aktarım başarısını daha büyük pilot grupta ve öğretmen rubriğiyle doğrula; GPT Image sahnelerini ayrı saydam katmanlarda, Veo videolarını da isteğe bağlı ön sahne olarak ekle. 9.1.3 için kaynaklı bilim insanı araştırmaları, 9.1.4 için güvenilir kurum/meslek kaynağı karşılaştırma görevleri gerekecek.
