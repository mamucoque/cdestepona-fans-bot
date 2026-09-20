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


def extraer_datos_noticia(url):
    soup = obtener_soup(url)

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
            imagen = urljoin(url, imagen)

    return {
        "titulo": titulo,
        "descripcion": descripcion,
        "imagen": imagen,
        "url": url
    }


# --------------------------------------------------
# BUSCAR LA NOTICIA MÁS RECIENTE
# --------------------------------------------------

noticias = obtener_noticias()

if not noticias:
    print("No se han encontrado noticias.")
    exit()

ultima_noticia = noticias[0]

url_guardada = None

if ARCHIVO_MEMORIA.exists():
    url_guardada = ARCHIVO_MEMORIA.read_text(
        encoding="utf-8"
    ).strip()


# --------------------------------------------------
# COMPROBAR SI ES NUEVA
# --------------------------------------------------

if ultima_noticia["url"] == url_guardada:

    print("No hay noticias nuevas.")
    exit()


# --------------------------------------------------
# EXTRAER DATOS
# --------------------------------------------------

datos = extraer_datos_noticia(
    ultima_noticia["url"]
)


# --------------------------------------------------
# RESUMEN
# --------------------------------------------------

descripcion = datos["descripcion"] or ""

# Limitar el resumen para que sea cómodo
# de leer en WhatsApp.
if len(descripcion) > 300:
    descripcion = descripcion[:300].rsplit(" ", 1)[0] + "..."


# --------------------------------------------------
# MENSAJE PARA WHATSAPP
# --------------------------------------------------

mensaje = f"""🔴🔵 *NUEVA NOTICIA*

📰 *{datos["titulo"]}*

{descripcion}

🔗 Leer la noticia completa:
{datos["url"]}

*CD Estepona Fans | La Voz de la Afición*"""


# --------------------------------------------------
# ARCHIVO ÚNICO PARA PUBLICAR
# --------------------------------------------------

contenido = f"""IMAGEN:
{datos["imagen"]}

━━━━━━━━━━━━━━━━━━━━

MENSAJE:

{mensaje}
"""


Path("PUBLICAR_EN_WHATSAPP.txt").write_text(
    contenido,
    encoding="utf-8"
)


# --------------------------------------------------
# MOSTRAR RESULTADO
# --------------------------------------------------

print("--- PUBLICACIÓN GENERADA ---")
print(contenido)
