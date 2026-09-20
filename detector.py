import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path

WEB = "https://www.cdesteponafans.com/"
ARCHIVO_MEMORIA = Path("ultima_noticia.txt")


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


def leer_ultima_noticia():
    if not ARCHIVO_MEMORIA.exists():
        return None

    return ARCHIVO_MEMORIA.read_text(
        encoding="utf-8"
    ).strip()


def guardar_ultima_noticia(url):
    ARCHIVO_MEMORIA.write_text(
        url,
        encoding="utf-8"
    )


def extraer_datos_noticia(url):
    soup = obtener_soup(url)

    # Título
    titulo = None

    if soup.find("h1"):
        titulo = soup.find("h1").get_text(" ", strip=True)

    if not titulo and soup.title:
        titulo = soup.title.get_text(" ", strip=True)

    # Descripción
    descripcion = None

    meta_description = soup.find(
        "meta",
        attrs={"name": "description"}
    )

    if meta_description:
        descripcion = meta_description.get("content", "").strip()

    # Imagen principal
    imagen = None

    meta_imagen = soup.find(
        "meta",
        attrs={"property": "og:image"}
    )

    if meta_imagen:
        imagen = meta_imagen.get("content")

        if imagen:
            imagen = urljoin(url, imagen)

    return {
        "titulo": titulo,
        "descripcion": descripcion,
        "imagen": imagen,
        "url": url
    }


# --------------------------------------------------
# PROGRAMA PRINCIPAL
# --------------------------------------------------

noticias = obtener_noticias()

if not noticias:
    print("No se han encontrado noticias.")
    exit()

ultima_noticia = noticias[0]
url_guardada = leer_ultima_noticia()

print("Última noticia encontrada:")
print(ultima_noticia["titulo"])
print(ultima_noticia["url"])


if url_guardada is None:

    print("\nPrimera ejecución.")
    print("Guardando la noticia actual como referencia.")

    guardar_ultima_noticia(
        ultima_noticia["url"]
    )


elif ultima_noticia["url"] == url_guardada:

    print("\nNo hay noticias nuevas.")


else:

    print("\n🆕 ¡HAY UNA NOTICIA NUEVA!")

    datos = extraer_datos_noticia(
        ultima_noticia["url"]
    )

    print("\n--- DATOS DE LA NOTICIA ---")

    print("\nTítulo:")
    print(datos["titulo"])

    print("\nDescripción:")
    print(datos["descripcion"])

    print("\nImagen:")
    print(datos["imagen"])

    print("\nURL:")
    print(datos["url"])

    guardar_ultima_noticia(
        ultima_noticia["url"]
    )
