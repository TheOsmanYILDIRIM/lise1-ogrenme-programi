# Android YTDLnis → LiseDers Türkçe altyazı aktarımı

Bu yol, GitHub-hosted runner üzerinden YouTube'a erişim `LOGIN_REQUIRED` döndürdüğünde **kullanıcının kendi cihazından erişebildiği** normal altyazı dışa aktarımını kullanır. YouTube erişimi Android cihazda da garantili değildir. Platform kısıtlamalarını aşma veya otomatik çözme denemesi yoktur.

## 1. YTDLnis şablonu

[Hazır JSON şablonu](../configs/ytdlnis_playlist_subtitles.json) YTDLnis → **More → Command Templates → Import Templates** içinde pano üzerinden içe aktarılabilir. Şablon YTDLnis'in *Command* sekmesinde seçilir. **İçine playlist URL'si eklemeyin:** YTDLnis bağlantıyı kendisi ekler.

İlgili komut argümanları:

```bash
--skip-download --write-subs --write-auto-subs \
  --sub-langs "tr,tr-.*" --sub-format "vtt/best" \
  -P "/sdcard/Download/YTDLnis" \
  -o "%(playlist_title).80s/%(playlist_index)03d - %(id)s - %(title).100s.%(ext)s" \
  --sleep-interval 1
```

Playlist bağlantısı, uygulama arayüzünde **ayrıca** verilmelidir:

`https://youtube.com/playlist?list=PLSYiXUktJiZeqUJyNFUgFHwOUNydbC-II`

`%(id)s` eklenmesi önemlidir: her indirilen altyazı, başlığı ve indeksinin dili değişse bile playlistteki kalıcı video kimliğiyle birebir eşleşir. Komut video dosyası indirmez. `--sub-langs tr,tr-.*` Türkçe dil varyantlarını dener; mevcut olmayan altyazılar için içerik uydurmaz.

## 2. İndirmeyi doğrula ve klasörü ZIP yap

İndirme sonrasında hedef klasörde `.tr.vtt` veya `.tr-*.vtt` dosyaları bulunmalı (bazı altyazı kaynaklarında `.srt` de olabilir). Yalnız bu dosyaların olduğu playlist klasörünü ZIP'le.

**Şablonun eski hâlini kullandıysan:** video ID'si olmadan `01 - Başlık.tr.vtt` gibi dosyalar da kabul edilebilir. Ancak bu durumda eşleme, playlist sırası **ve başlığın doğrulanmış benzerliği** birlikte sağlanıyorsa yapılır. Yalnız sıraya bakılarak içerik atanmaz. Yanlış/eksik eşleşmeler `unmatched_files` listesinde belirtilir.

## 3. LiseDers'te offline (ağ bağlantısız) içe aktar

Proje kökünden:

```bash
python scripts/import_ytdlnis_subtitles.py \
  --catalog data/video_playlists/PLSYiXUktJiZeqUJyNFUgFHwOUNydbC-II/playlist-catalog.json \
  --input "/sdcard/Download/YTDLnis/PLAYLIST_KLASORU" \
  --output output/ytdlnis
```

`--input` parametresi klasör yerine **ZIP dosyası** da alır. Harici paket veya internet erişimi gerekmez.

Çıktılar:

- `output/ytdlnis/transcripts/manifest.json`: her video için `fetched/missing/duplicate`, parmak izi, kaynak dosya, başlık/ID eşleştirme yöntemi ve kontrol gerekçesi
- `output/ytdlnis/transcripts/<video-id>.tr.txt`: gerçek altyazıdan temizlenmiş metin
- `output/ytdlnis/transcripts/<video-id>.tr.cues.json`: zaman kodlarını koruyan konuşma parçaları
- `output/ytdlnis/transcripts/<video-id>.tr.vtt` veya `.srt`: orijinal dosya

Eşleşmeyen ve ayrıştırılamayan dosyalar açık şekilde raporlanır. Aynı video için birden çok altyazı varsa sessizce birleştirilmez. ZIP dosyası arşiv içinden okunur; path traversal ve aşırı dosya boyutu sınırları uygulanır.

## 4. Konu eşleştirmesini transcript ile yeniden denetleme

**Sadece okunabilir StudyTracker klonu varsa**:

```bash
python scripts/playlist_studytracker_bridge.py \
  --catalog data/video_playlists/PLSYiXUktJiZeqUJyNFUgFHwOUNydbC-II/playlist-catalog.json \
  --studytracker-dir /PATH/TO/study-tracker \
  --course course_mat_9 \
  --transcripts output/ytdlnis/transcripts \
  --output output/ytdlnis/topic-matches-with-transcripts.json
```

Bu sadece öneri/denetim raporudur; StudyTracker içerikleri, canlı KV, öğrenci ilerlemesi veya Matematik dersleri otomatik değiştirilmez. Kullanıcının durdurduğu Matematik 9 yeniden kurulum işi ancak yeni açık talimatla başlatılır.

## Güvenlik ve içerik sahipliği

Kullanıcının indirdiği altyazılar `output/` altında tutulur, Git commit'ine otomatik eklenmez. Bu dosyaları yalnız izinli olduğu kapsamda kullanın, paylaşım ve telif haklarına dikkat edin. Ana depo yalnız ID, sıralama, kaynak URL'si ve durum/metaveri gibi küçük açıklayıcı verileri sürümler.
