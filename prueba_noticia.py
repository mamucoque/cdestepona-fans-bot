import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL = "https://www.cdesteponafans.com/es/noticias/a-la-tercera-va-la-vencida-el-cd-estepona-se-impone-0-2-al-salerm-puente-genil"

response = requests.get(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=30
)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")


# TÍTULO
titulo = None

if soup.find("h1"):
    titulo = soup.find("h1").get_text(" ", strip=True)

if not titulo and soup.title:
    titulo = soup.title.get_text(" ", strip=True)


# DESCRIPCIÓN
descripcion = None

meta_description = soup.find(
    "meta",
    attrs={"name": "description"}
)

if meta_description:
    descripcion = meta_description.get(
        "content",
        ""
    ).strip()


# IMAGEN
imagen = None

meta_imagen = soup.find(
    "meta",
    attrs={"property": "og:image"}
)

if meta_imagen:
    imagen = meta_imagen.get("content")

    if imagen:
        imagen = urljoin(URL, imagen)


print("--- RESULTADO ---")

print("\nTÍTULO:")
print(titulo)

print("\nDESCRIPCIÓN:")
print(descripcion)

print("\nIMAGEN:")
print(imagen)

print("\nURL:")
print(URL)
