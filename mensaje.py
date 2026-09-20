```python
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pathlib import Path
import json


ARCHIVO_NUEVAS = Path("noticias_nuevas.json")
ARCHIVO_MEMORIA = Path("noticias_procesadas.txt")
ARCHIVO_PUBLICACION = Path("PUBLICAR_EN_WHATSAPP.txt")


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


def extraer_datos_noticia(url):
    soup = obtener_soup(url)

    # --------------------------------------------------
    # TÍTULO
    # --------------------------------------------------

    titulo = None

    if soup.find("h1"):
        titulo = soup.find("h1").get_text(
            " ",
            strip=True
        )

    if not titulo and soup.title:
        titulo = soup.title.get_text(
            " ",
            strip=True
        )

    # --------------------------------------------------
    # DESCRIPCIÓN
    # --------------------------------------------------

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

    # --------------------------------------------------
    # IMAGEN
    # --------------------------------------------------

    imagen = None

    meta_imagen = soup.find(
        "meta",
        attrs={"property": "og:image"}
    )

    if meta_imagen:
        imagen = meta_imagen.get("content")

        if imagen:
            imagen = urljoin(
                url,
                imagen
            )

    return {
        "titulo": titulo,
        "descripcion": descripcion,
        "imagen": imagen,
        "url": url
    }


# --------------------------------------------------
# LEER NOTICIAS NUEVAS
# --------------------------------------------------

if not ARCHIVO_NUEVAS.exists():

    print("No existe el archivo de noticias nuevas.")

    exit()


try:

    noticias = json.loads(
        ARCHIVO_NUEVAS.read_text(
            encoding="utf-8"
        )
    )

except Exception as error:

    print(
        f"Error leyendo noticias_nuevas.json: {error}"
    )

    exit(1)


if not noticias:

    print("No hay noticias nuevas.")

    # Evitar que quede un archivo antiguo
    if ARCHIVO_PUBLICACION.exists():
        ARCHIVO_PUBLICACION.unlink()

    exit()


# --------------------------------------------------
# GENERAR TODAS LAS PUBLICACIONES
# --------------------------------------------------

publicaciones = []
urls_procesadas = []


for numero, noticia in enumerate(
    noticias,
    start=1
):

    print(
        f"\nProcesando noticia "
        f"{numero}/{len(noticias)}..."
    )

    datos = extraer_datos_noticia(
        noticia["url"]
    )

    descripcion = datos["descripcion"] or ""

    # Limitar el resumen
    if len(descripcion) > 300:

        descripcion = (
            descripcion[:300]
            .rsplit(" ", 1)[0]
            + "..."
        )

    # --------------------------------------------------
    # MENSAJE WHATSAPP
    # --------------------------------------------------

    mensaje = f"""🔴🔵 *NUEVA NOTICIA*

📰 *{datos["titulo"]}*

{descripcion}

🔗 Leer la noticia completa:
{datos["url"]}

*CD Estepona Fans | La Voz de la Afición*"""


    # --------------------------------------------------
    # GUARDAR PUBLICACIÓN
    # --------------------------------------------------

    publicacion = f"""🆕 PUBLICACIÓN {numero}/{len(noticias)}

IMAGEN:
{datos["imagen"]}

━━━━━━━━━━━━━━━━━━━━

MENSAJE:

{mensaje}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    publicaciones.append(publicacion)

    urls_procesadas.append(
        noticia["url"]
    )


# --------------------------------------------------
# CREAR ARCHIVO FINAL
# --------------------------------------------------

contenido_final = "\n".join(
    publicaciones
)

ARCHIVO_PUBLICACION.write_text(
    contenido_final,
    encoding="utf-8"
)


# --------------------------------------------------
# ACTUALIZAR MEMORIA
# --------------------------------------------------

with ARCHIVO_MEMORIA.open(
    "a",
    encoding="utf-8"
) as archivo:

    for url in urls_procesadas:

        archivo.write(
            url + "\n"
        )


# --------------------------------------------------
# MOSTRAR RESULTADO
# --------------------------------------------------

print("\n======================================")
print("PUBLICACIONES GENERADAS")
print("======================================")

print(
    f"\nSe han preparado "
    f"{len(publicaciones)} publicación(es)."
)

print(
    f"\nArchivo generado: "
    f"{ARCHIVO_PUBLICACION}"
)
```
