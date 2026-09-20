```python
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path
import json

WEB = "https://www.cdesteponafans.com/"
ARCHIVO_MEMORIA = Path("noticias_procesadas.txt")
ARCHIVO_NUEVAS = Path("noticias_nuevas.json")


def obtener_soup(url):
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30
    )

    response.raise_for_status()

    return BeautifulSoup(response.text, "html.parser")


def obtener_noticias():
    soup = obtener_soup(WEB)

    noticias = []

    for enlace in soup.find_all("a", href=True):
        href = enlace["href"]

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

        if noticia not in noticias:
            noticias.append(noticia)

    return noticias


def leer_memoria():
    if not ARCHIVO_MEMORIA.exists():
        return set()

    urls = set()

    for linea in ARCHIVO_MEMORIA.read_text(
        encoding="utf-8"
    ).splitlines():

        linea = linea.strip()

        if linea:
            urls.add(linea)

    return urls


def guardar_nuevas(noticias):
    ARCHIVO_NUEVAS.write_text(
        json.dumps(
            noticias,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )


# --------------------------------------------------
# BUSCAR NOTICIAS
# --------------------------------------------------

noticias = obtener_noticias()

if not noticias:
    print("No se han encontrado noticias.")
    guardar_nuevas([])
    exit()


print(f"Noticias encontradas: {len(noticias)}")


# --------------------------------------------------
# LEER MEMORIA
# --------------------------------------------------

memoria_existe = ARCHIVO_MEMORIA.exists()
procesadas = leer_memoria()


# --------------------------------------------------
# PRIMERA EJECUCIÓN
# --------------------------------------------------

if not memoria_existe:

    print("\nPrimera ejecución.")

    print(
        "Se guardarán las noticias actuales como "
        "ya procesadas para evitar publicaciones antiguas."
    )

    ARCHIVO_MEMORIA.write_text(
        "\n".join(
            noticia["url"]
            for noticia in noticias
        ),
        encoding="utf-8"
    )

    guardar_nuevas([])

    print(
        f"Se han guardado {len(noticias)} noticias "
        "como referencia inicial."
    )

    exit()


# --------------------------------------------------
# DETECTAR TODAS LAS NOTICIAS NUEVAS
# --------------------------------------------------

nuevas = [
    noticia
    for noticia in noticias
    if noticia["url"] not in procesadas
]


# --------------------------------------------------
# ORDENAR DE LA MÁS ANTIGUA A LA MÁS NUEVA
# --------------------------------------------------

nuevas.reverse()


if not nuevas:

    print("\nNo hay noticias nuevas.")

    guardar_nuevas([])

    exit()


# --------------------------------------------------
# GUARDAR PENDIENTES
# --------------------------------------------------

guardar_nuevas(nuevas)


# --------------------------------------------------
# MOSTRAR RESULTADO
# --------------------------------------------------

print(
    f"\n🆕 Se han detectado {len(nuevas)} "
    "noticia(s) nueva(s):"
)

for numero, noticia in enumerate(nuevas, start=1):

    print(f"\n{numero}. {noticia['titulo']}")
    print(noticia["url"])
```
