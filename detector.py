import requests
from bs4 import BeautifulSoup

URL = "https://www.cdesteponafans.com/"

response = requests.get(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=30
)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

print("Página cargada correctamente.")

# Mostrar los enlaces encontrados
for enlace in soup.find_all("a", href=True):
    texto = enlace.get_text(" ", strip=True)
    url = enlace["href"]

    if texto:
        print(f"{texto} -> {url}")
