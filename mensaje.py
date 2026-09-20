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
# SI NO HAY NOTICIA NUEVA, TERMINAMOS
# --------------------------------------------------

if ultima_noticia["url"] == url_guardada:

    print("No hay noticias nuevas.")
    exit()


# --------------------------------------------------
# EXTRAER INFORMACIÓN DE LA NUEVA NOTICIA
# --------------------------------------------------

datos = extraer_datos_noticia(
    ultima_noticia["url"]
)


# --------------------------------------------------
# GENERAR MENSAJE
# --------------------------------------------------

mensaje = f"""🔴🔵 NUEVA NOTICIA

📰 {datos["titulo"]}

{datos["descripcion"]}

🔗 Leer la noticia completa:
{datos["url"]}

CD Estepona Fans | La Voz de la Afición
"""


# --------------------------------------------------
# MOSTRAR RESULTADO
# --------------------------------------------------

print("--- MENSAJE GENERADO ---")
print(mensaje)

print("--- IMAGEN ---")
print(datos["imagen"])


# --------------------------------------------------
# GUARDAR ARCHIVO LISTO PARA COPIAR
# --------------------------------------------------

Path("mensaje_whatsapp.txt").write_text(
    mensaje,
    encoding="utf-8"
)

Path("imagen_noticia.txt").write_text(
    datos["imagen"] or "",
    encoding="utf-8"
)

print("--- ARCHIVOS GENERADOS ---")
print("mensaje_whatsapp.txt")
print("imagen_noticia.txt")
