# YouTube playlist → mevcut StudyTracker Matematik 9 videoları

Kaynak: `PLSYiXUktJiZeqUJyNFUgFHwOUNydbC-II` (İlyas Güneş 9. sınıf Matematik playlisti; geometri bölümünde Nurtaç Kozak videoları da var). Amaç **yeni ders/kart eklemek değil**; mevcut StudyTracker matematik VIDEO kartlarının oynatma kaynağını güvenilir, elle incelenmiş bir karşılıkla değiştirmek.

## 1. LiseDers: kaynak ve aday hazırlama

[GitHub Actions: YouTube → StudyTracker lesson bridge](../.github/workflows/youtube-playlist.yml) çalışması:
1. `yt-dlp` ile playlistin sıralı video kimliklerini, başlıklarını, öğretmen/kanal bilgilerini çıkarır.
2. Erişilebildiğinde Türkçe VTT altyazı ve zaman kodlarını ayrı işler. YouTube GitHub runner'ına bot doğrulaması istediğinden son çalışmada **0 transkript** alındı; başarısız denemelerden sonra kontrollü biçimde durdurulur. Transkript uydurulmaz.
3. Gerçek StudyTracker V2 matematik dersleriyle başlık/tema eşleştirmesi yapar. Alt konu kanıtı olmayan videoları **needs_review** olarak bırakır.
4. StudyTracker'ın **replacement-only** betiğiyle manuel karşılaştırma CSV'si ve onaysız dry-run raporu üretir.
5. Sürümlediği kaynaklar: `data/video_playlists/PLSYiXUktJiZeqUJyNFUgFHwOUNydbC-II/{playlist-catalog.json,topic-matches.json,transcript-status.json}`.

Tam çalıştırma manuel `workflow_dispatch` veya commit mesajında `[playlist-run]` ile tetiklenir. Normal kaynak kodu push'ları yalnız test yapar.

Artifact: `playlist-catalog.json`, `raw-playlist.json`, `transcripts/manifest.json`, varsa altyazı dosyaları, `studytracker-mapping.json`, `math9-video-replacement-candidates.csv`, `math9-video-replacement-dry-run.json`.

## 2. StudyTracker: yalnız mevcut video kartlarını değiştir

[StudyTracker Action: Review and replace existing Math 9 videos](https://github.com/TheOsmanYILDIRIM/study-tracker/actions/workflows/import-liseders-playlist.yml) gerçek ders ve kart kimliklerini korur. İnceleme CSV'sindeki her satır adaydır, otomatik atama değildir.

Onay sözleşmesi: `study-tracker/content/v2/playlist-imports/ilyas-gunes-mat9.replacements.json`
- `mode: "replace_existing_only"`
- `target_item_id`: **mevcut** video kartı
- `expected_old_url`: eldeki videonun doğrulanmış eski URL'si
- `video_id`: playlistteki yeni video
- `reviewed: true`, `reviewed_contents: true`, `reason`: gerçekten izlenip kontrol edilen konu kapsama kanıtı
- Quiz varsa `quiz_reviewed: true`, `quiz_review_note`: dersle uyum inceleme notu
- İlyas Güneş dışındaki bir öğretmene geçişte açık `allow_other_teacher: true`; konu dışı override'da `cross_topic_override: true` ve ayrıntılı kanıt gerekir.

Varsayılan eylem dry-run. `apply_replacements=true` yalnız elle onaylanan **mevcut** VIDEO dosyalarını değiştirir, V2 kataloğu derleyip CLI testlerinden geçirdikten sonra commit oluşturur. Yeni ders/kart, quiz, ilerleme kaydı **eklemez veya silmez**.

Quizler mevcut eski transkript kaynaklarına dayanıyor olabilir; dosyaları otomatik değiştirilmez, geçmiş kaynak kanıtları korunur ve çakışma inceleme uyarısı olarak kaydedilir. GitHub'da katalog commit'i **canlı Cloudflare KV kataloğunu otomatik güncellemez**; bunun için ayrı V2 seed/diff/apply akışı gerekir.

Ayrıntılı kullanım: [StudyTracker LiseDers video değiştirme rehberi](https://github.com/TheOsmanYILDIRIM/study-tracker/blob/main/docs/LISEDERS_PLAYLIST_IMPORT.md).
