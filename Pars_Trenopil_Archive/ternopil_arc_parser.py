import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote
import re

BASE_URL = "https://archives.te.gov.ua/"
active_links = [
    "https://archives.te.gov.ua/ocifrovanni-spravi/f37-kremeneckij-miskij-magistrat-opis-2/#l-f37-kremeneckij-miskij-magistrat-opis-2",
    "https://archives.te.gov.ua/ocifrovanni-spravi/f484-yevrejska-sinagoga-kremeneckogo-povitu-volins/#l-f484-yevrejska-sinagoga-kremeneckogo-povitu-volins",
    "https://archives.te.gov.ua/ocifrovanni-spravi/f-487-opis-1-greko-katolicki-povitovi-upravlinnya/#l-f-487-opis-1-greko-katolicki-povitovi-upravlinnya",
    "https://archives.te.gov.ua/f-258-duhovnij-sobor-pochayivskoyi-uspenskoyi-lavr/f-258-opis-1/#l-f-258-opis-1",
    "https://archives.te.gov.ua/f-258-duhovnij-sobor-pochayivskoyi-uspenskoyi-lavr/f-258-opis-2/#l-f-258-opis-2",
    "https://archives.te.gov.ua/f-258-duhovnij-sobor-pochayivskoyi-uspenskoyi-lavr/f-258-opis-3/#l-f-258-opis-3",
]


def get_decoded_links():
    already_links = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    for ac_link in active_links:
        print(f"Парсимо: {ac_link}")
        try:
            response = requests.get(ac_link, headers=headers)
            soup = BeautifulSoup(response.text, "lxml")
            for l in soup.find_all("a"):
                s = l.get("href")
                if s and s.startswith(".."):
                    raw_url = urljoin(BASE_URL, s.strip("../../../../.."))
                    decoded_url = unquote(raw_url)
                    already_links.append(decoded_url)
                elif s and s.startswith("https://drive"):
                    already_links.append(s)
        except Exception as e:
            print(f"Помилка {ac_link}: {e}")

    return list(set(already_links))


decoded_links = get_decoded_links()

with open('decoded_links.txt', 'w', encoding='utf-8') as f:
    for link in decoded_links:
        fond_match = re.search(r'fond(\d+)|f-?(\d+)', link)
        fond = (fond_match.group(1) or fond_match.group(2) or 'unknown') if fond_match else 'unknown'
        filename = unquote(link.split('/')[-1])
        f.write(f"{link} | fond_{fond} | {filename}\n")

print(f"Створено decoded_links.txt з {len(decoded_links)} лінками")
