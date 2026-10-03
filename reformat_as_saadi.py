# -*- coding: utf-8 -*-
import os, json

FOLDER = r'D:\nuran_tafsir_data\urdu\as_saadi'

def main():
    ok, skip, fail = 0, 0, 0
    for surah in range(1, 115):
        path = os.path.join(FOLDER, f'{surah}.json')
        if not os.path.exists(path):
            fail += 1
            continue
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, dict) and 'ayahs' in data:
                skip += 1
                continue
            if isinstance(data, list):
                ayahs = []
                for i, item in enumerate(data, start=1):
                    if isinstance(item, dict):
                        text = item.get('text', '')
                    elif isinstance(item, str):
                        text = item
                    else:
                        continue
                    if text:
                        ayahs.append({'ayah': i, 'text': text})
                new_data = {'ayahs': ayahs}
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(new_data, f, ensure_ascii=False)
                ok += 1
            else:
                fail += 1
        except Exception:
            fail += 1
    print(f'Reformatted: {ok}')
    print(f'Skipped    : {skip}')
    print(f'Failed     : {fail}')

if __name__ == '__main__':
    main()