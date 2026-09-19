import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

WEB = "https://www.cdesteponafans.com/"

response = requests.get(
    WEB,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=30
)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

noticias = []

for enlace in soup.find_all("a", href=True):
    href = enlace["href"]

    # Solo queremos enlaces de noticias
    if "/es/noticias/" not in href:
        continue

    titulo = enlace.get_text(" ", strip=True)

    if not titulo:
        continue

    url = urljoin(WEB, href)

    noticia = {
        "titulo": titulo,
        "url": url
    }

    # Evitar duplicados
    if noticia not in noticias:
        noticias.append(noticia)


print(f"Se han encontrado {len(noticias)} noticias.")

print("\n--- NOTICIAS DETECTADAS ---\n")

for numero, noticia in enumerate(noticias, start=1):
    print(f"{numero}. {noticia['titulo']}")
    print(f"   {noticia['url']}")
    print()
