# -*- coding: utf-8 -*-
import os, json, time, urllib.request

BASE_URLS = [
    'https://cdn.jsdelivr.net/gh/spa5k/tafsir_api@main/tafsir',
    'https://cdn.statically.io/gh/spa5k/tafsir_api/main/tafsir',
    'https://raw.githubusercontent.com/spa5k/tafsir_api/main/tafsir',
    'https://rawcdn.githack.com/spa5k/tafsir_api/main/tafsir',
]

MAPPING = {
    'urdu/as_saadi': 'ur-tafsir-as-saadi-urdu',
}

def fetch(spa5k_slug, surah):
    for base in BASE_URLS:
        try:
            url = f'{base}/{spa5k_slug}/{surah}.json'
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=20) as r:
                data = json.loads(r.read().decode('utf-8'))
                # ✅ Dono formats handle karo
                if isinstance(data, list) and len(data) > 0:
                    return data
                if isinstance(data, dict) and data.get('ayahs'):
                    return data
        except Exception:
            continue
    return None

def main():
    downloaded, skipped, failed = 0, 0, 0
    for app_path, spa5k_slug in MAPPING.items():
        out_dir = app_path.replace('/', os.sep)
        os.makedirs(out_dir, exist_ok=True)
        print(f'\n[*] {app_path}/')
        for surah in range(1, 115):
            out_file = os.path.join(out_dir, f'{surah}.json')
            if os.path.exists(out_file) and os.path.getsize(out_file) > 200:
                skipped += 1
                continue
            data = fetch(spa5k_slug, surah)
            if data is not None:
                with open(out_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False)
                downloaded += 1
                print(f'  [OK] {surah}/114')
            else:
                failed += 1
                print(f'  [X]  {surah}/114')
            time.sleep(0.15)
    print(f'\n{"="*50}')
    print(f'Downloaded: {downloaded}')
    print(f'Skipped   : {skipped}')
    print(f'Failed    : {failed}')
    print(f'{"="*50}')

if __name__ == '__main__':
    main()