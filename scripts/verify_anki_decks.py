import sys
import os

def check_anki_deck(file_path):
    if not os.path.exists(file_path):
        print(f"HATA: {file_path} bulunamadi.")
        return False
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    card_count = 0
    errors = []
    for idx, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            errors.append(f"Satir {idx}: TAB ayraci eksik veya satir hatali: {line[:30]}...")
        else:
            card_count += 1
            front, back = parts[0], parts[1]
            if len(front) == 0 or len(back) == 0:
                errors.append(f"Satir {idx}: On veya arka yuz bos.")
    
    deck_name = os.path.basename(file_path)
    if errors:
        print(f"❌ {deck_name}: {len(errors)} hata bulundu:")
        for err in errors:
            print(f"   - {err}")
        return False
    else:
        print(f"✅ {deck_name}: {card_count} kart basariyla dogrulandi (Anki TSV formatina tam uyumlu).")
        return True

if __name__ == "__main__":
    decks_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "anki_decks"))
    all_ok = True
    for fname in sorted(os.listdir(decks_dir)):
        if fname.endswith(".txt") or fname.endswith(".tsv"):
            fpath = os.path.join(decks_dir, fname)
            ok = check_anki_deck(fpath)
            if not ok:
                all_ok = False
    
    if all_ok:
        print("\n🎉 Tum Anki desteleri dogrulandi ve import edilmeye hazir!")
    else:
        sys.exit(1)
