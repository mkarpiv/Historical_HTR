import requests
import os
import re
from urllib.parse import unquote
from tqdm import tqdm

INPUT_FILE = 'decoded_links.txt'
BASE_DIR = 'Архів'

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})


def parse_link_info(line):
    parts = line.strip().split(' | ')
    if len(parts) >= 3:
        url, fond_str, filename = parts[0], parts[1], parts[2]
        fond_num = re.search(r'fond_(\d+)', fond_str)
        return url, fond_num.group(1) if fond_num else 'unknown', filename
    return None, None, None


def download_file(url, fond, filename):
    fond_dir = os.path.join(BASE_DIR, f'Fond_{fond}')
    os.makedirs(fond_dir, exist_ok=True)

    clean_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    if not clean_filename.lower().endswith('.pdf'):
        clean_filename += '.pdf'

    filepath = os.path.join(fond_dir, clean_filename)

    if os.path.exists(filepath):
        print(f"✓ Пропуск: Fond_{fond}/{clean_filename}")
        return True

    try:
        resp = session.get(url, stream=True, timeout=60)
        resp.raise_for_status()

        total_size = int(resp.headers.get('content-length', 0))
        with open(filepath, 'wb') as f, tqdm(
                total=total_size, unit='B', unit_scale=True,
                desc=f'Fond_{fond}/{os.path.basename(clean_filename)[:50]}'  # Тільки в прогресі
        ) as pbar:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
                pbar.update(len(chunk))

        print(f"✓ Завантажено: Fond_{fond}/{clean_filename}")
        return True
    except Exception as e:
        print(f"✗ Помилка Fond_{fond}/{filename}: {e}")
        return False


if not os.path.exists(INPUT_FILE):
    print(f"Створіть {INPUT_FILE}!")
    exit()

os.makedirs(BASE_DIR, exist_ok=True)
total_downloaded = 0

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    for line in tqdm(f.readlines(), desc="Завантаження"):
        url, fond, filename = parse_link_info(line)
        if url and fond:
            if download_file(url, fond, filename):
                total_downloaded += 1

print(f"\nЗавершено! {total_downloaded} файлів у Архів/Fond_XXX/")
