# 🤖 CD Estepona Fans Bot

Bot automatizado para detectar nuevas noticias publicadas en [CD Estepona Fans](https://www.cdesteponafans.com/) y generar una publicación preparada para compartir manualmente en su canal de WhatsApp.

## ⚙️ ¿Cómo funciona?

El sistema comprueba automáticamente la web de CD Estepona Fans cada 5 minutos mediante **GitHub Actions**.

```text
🌐 CD Estepona Fans
        │
        ▼
🔎 detector.py
        │
        │ ¿Hay una noticia nueva?
        ▼
📰 Extrae la nueva noticia
        │
        ▼
📝 mensaje.py
        │
        ├── 📰 Título
        ├── 📝 Descripción
        ├── 🖼️ Imagen principal
        └── 🔗 URL
        │
        ▼
📄 PUBLICAR_EN_WHATSAPP.txt
        │
        ▼
📱 Publicación manual en WhatsApp
```

## 🚀 Características

* 🔎 Detecta automáticamente nuevas noticias.
* ⏱️ Comprueba la web aproximadamente cada 5 minutos.
* 📰 Extrae el título de la noticia.
* 📝 Extrae y acorta la descripción.
* 🖼️ Obtiene la imagen principal mediante `og:image`.
* 🔗 Obtiene automáticamente la URL de la noticia.
* 🧠 Guarda la última noticia detectada para evitar duplicados.
* ✍️ Genera un mensaje con formato compatible con WhatsApp.
* 📦 Guarda el resultado como un Artifact de GitHub Actions.
* ☁️ Funciona en la nube mediante GitHub Actions, por lo que no es necesario mantener un ordenador encendido.

## 📂 Estructura del proyecto

```text
cdestepona-fans-bot/
│
├── detector.py
│   └── Detecta la noticia más reciente y controla la memoria.
│
├── mensaje.py
│   └── Extrae los datos y genera la publicación para WhatsApp.
│
├── ultima_noticia.txt
│   └── Guarda la URL de la última noticia procesada.
│
└── .github/
    └── workflows/
        └── detector.yml
            └── Ejecuta automáticamente el bot.
```

## 🔍 Detector de noticias

`detector.py` consulta la página web y busca enlaces pertenecientes a la sección de noticias:

```text
/es/noticias/
```

El sistema toma la noticia que aparece en primer lugar como la más reciente.

Después compara su URL con la almacenada en:

```text
ultima_noticia.txt
```

Si coincide, no hace nada.

Si es diferente, se considera una noticia nueva.

## 📝 Generación de la publicación

Cuando se detecta una noticia nueva, `mensaje.py` obtiene:

* Título.
* Descripción.
* Imagen principal.
* URL.

Después genera un archivo:

```text
PUBLICAR_EN_WHATSAPP.txt
```

El archivo contiene la imagen y el mensaje preparado para copiar y pegar.

Ejemplo:

```text
IMAGEN:
https://images.cdesteponafans.com/...

━━━━━━━━━━━━━━━━━━━━

MENSAJE:

🔴🔵 *NUEVA NOTICIA*

📰 *Título de la noticia*

Resumen de la noticia...

🔗 Leer la noticia completa:
https://www.cdesteponafans.com/es/noticias/...

*CD Estepona Fans | La Voz de la Afición*
```

## ☁️ GitHub Actions

El workflow situado en:

```text
.github/workflows/detector.yml
```

ejecuta automáticamente el bot.

También puede ejecutarse manualmente desde:

**GitHub → Actions → Detector de noticias → Run workflow**

Cuando existe una noticia nueva, GitHub genera el Artifact:

```text
PUBLICAR-EN-WHATSAPP
```

Este archivo puede descargarse desde la ejecución correspondiente.

## 📱 WhatsApp

Actualmente la última parte del proceso es manual:

1. Descargar `PUBLICAR-EN-WHATSAPP`.
2. Copiar la URL de la imagen.
3. Adjuntar la imagen en el canal.
4. Copiar el mensaje generado.
5. Publicarlo.

La detección y preparación de la publicación están automatizadas, mientras que el envío al canal se realiza manualmente.

## 🛠️ Tecnologías utilizadas

* **Python**
* **Requests**
* **BeautifulSoup**
* **GitHub Actions**
* **GitHub Artifacts**

## 🔐 Seguridad

El proyecto no necesita contraseñas, cookies ni claves API para realizar la detección de noticias.

Si se añaden credenciales o secretos en el futuro, **no deben incluirse directamente en el código ni en archivos públicos del repositorio**.

## ♻️ Reutilización

El sistema puede adaptarse a otras páginas web modificando principalmente:

* La URL de la web.
* El patrón utilizado para localizar las noticias.
* Los selectores HTML si la estructura de la web es diferente.
* El formato del mensaje generado.

Por tanto, la arquitectura puede utilizarse como base para otros proyectos de automatización de noticias.

## 📌 Estado del proyecto

**🟢 Funcionando**

Actualmente el sistema detecta nuevas noticias y genera automáticamente una publicación preparada para compartir en WhatsApp.

---

### CD Estepona Fans

**La Voz de la Afición** ❤️💙

🌐 https://www.cdesteponafans.com/
