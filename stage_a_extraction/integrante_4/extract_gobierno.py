"""
Integrante 4 — Extracción programas de gobierno peruano
=========================================================
Scraping de páginas web de programas sociales y de emergencia.
Output: data/raw/gobierno/

Uso:
    python extract_gobierno.py
"""

import json
import requests
import re
from datetime import date
from pathlib import Path

try:
    from bs4 import BeautifulSoup
    BS4_OK = True
except ImportError:
    BS4_OK = False
    print("AVISO: pip install beautifulsoup4")

OUTPUT_DIR = Path(__file__).parents[2] / "data" / "raw" / "gobierno"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ChasquiAyuda-Research/1.0)"
}

# Páginas a scrapear
FUENTES_WEB = [
    {
        "id": "midis-contigo",
        "nombre": "MIDIS - Programa Contigo",
        "url": "https://www.midis.gob.pe/index.php/es/programa-contigo",
        "tipo_crisis": "general",
        "programa": "Contigo",
    },
    {
        "id": "minsa-emergencias",
        "nombre": "MINSA - Emergencias y Desastres",
        "url": "https://www.minsa.gob.pe/emergencias/",
        "tipo_crisis": "salud",
        "programa": "MINSA Emergencias",
    },
    {
        "id": "indeci-lineas",
        "nombre": "INDECI - Líneas de emergencia",
        "url": "https://www.indeci.gob.pe/atencion-al-ciudadano/",
        "tipo_crisis": "general",
        "programa": "INDECI",
    },
]

# Fichas manuales (completar con información real de las páginas web)
# Formato: llenar después de visitar cada URL
FICHAS_MANUALES = [
    {
        "id": "ficha-contigo-001",
        "fuente": "gobierno_peruano",
        "programa": "Programa Contigo (MIDIS)",
        "tipo_crisis": "general",
        "quien_califica": "Personas con discapacidad severa en situación de pobreza; se activa también en emergencias declaradas",
        "como_acceder": "Registro gratuito en el MIDIS más cercano o en el módulo de atención durante emergencias",
        "que_reciben": "Transferencia monetaria de S/300 bimestral; en emergencias puede activarse transferencia adicional",
        "contacto": "Línea 101 (gratuita), web: midis.gob.pe",
        "activacion_emergencia": "MIDIS activa protocolos especiales en zonas con emergencia declarada por el gobierno",
        "texto": "El Programa Contigo del MIDIS otorga transferencias monetarias a personas con discapacidad severa en pobreza. En situaciones de emergencia declarada, MIDIS puede activar transferencias especiales. Para acceder: acudir al módulo MIDIS más cercano o llamar al 101. El registro siempre es gratuito.",
        "fecha_extraccion": str(date.today()),
        "licencia": "dominio_publico_peru",
        "region": "nacional",
    },
    {
        "id": "ficha-indeci-001",
        "fuente": "gobierno_peruano",
        "programa": "INDECI - Respuesta a emergencias",
        "tipo_crisis": "general",
        "quien_califica": "Cualquier persona afectada por desastre natural o emergencia declarada",
        "como_acceder": "Llamar a la línea 115 (gratuita, 24 horas) o acudir al Centro de Operaciones de Emergencia más cercano",
        "que_reciben": "Información sobre puntos de distribución de ayuda, albergues habilitados, organizaciones activas en la zona",
        "contacto": "Línea 115 (gratuita, 24h), web: indeci.gob.pe",
        "activacion_emergencia": "INDECI coordina la respuesta nacional ante toda emergencia declarada",
        "texto": "En caso de emergencia, INDECI coordina la respuesta humanitaria en Perú. Línea de emergencia: 115 (gratuita, disponible las 24 horas). INDECI informa sobre albergues habilitados, puntos de distribución de víveres y organizaciones activas en cada zona.",
        "fecha_extraccion": str(date.today()),
        "licencia": "dominio_publico_peru",
        "region": "nacional",
    },
    # COMPLETAR con más fichas según las URLs visitadas
    # Copiar el formato de arriba para cada programa
]


def limpiar_texto(texto):
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def scrapear_pagina(fuente):
    if not BS4_OK:
        return None
    try:
        r = requests.get(fuente["url"], headers=HEADERS, timeout=15)
        if r.status_code != 200:
            print(f"  HTTP {r.status_code}: {fuente['url']}")
            return None

        soup = BeautifulSoup(r.text, "html.parser")
        # Eliminar nav, footer, scripts
        for tag in soup(["nav", "footer", "script", "style", "header"]):
            tag.decompose()

        texto = limpiar_texto(soup.get_text(separator=" "))
        if len(texto) < 200:
            return None

        return {
            "id": fuente["id"],
            "fuente": "gobierno_web",
            "programa": fuente["nombre"],
            "url_fuente": fuente["url"],
            "tipo_crisis": fuente["tipo_crisis"],
            "region": "nacional",
            "fecha_extraccion": str(date.today()),
            "licencia": "dominio_publico_peru",
            "texto": texto[:3000],  # máximo 3000 chars del scraping
        }
    except Exception as e:
        print(f"  Error scrapeando {fuente['url']}: {e}")
        return None


def guardar_jsonl(registros, nombre):
    ruta = OUTPUT_DIR / nombre
    with open(ruta, "w", encoding="utf-8") as f:
        for r in registros:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Guardado: {ruta} ({len(registros)} registros)")


if __name__ == "__main__":
    todos = []

    # Fichas manuales (siempre incluir)
    print(f"Fichas manuales: {len(FICHAS_MANUALES)}")
    todos.extend(FICHAS_MANUALES)

    # Scraping web
    print("\nScrapeando páginas web...")
    for fuente in FUENTES_WEB:
        print(f"  {fuente['nombre']}...")
        resultado = scrapear_pagina(fuente)
        if resultado:
            todos.append(resultado)
            print(f"  ✅ {len(resultado['texto'])} chars extraídos")
        else:
            print(f"  ⚠️  Sin resultado")

    guardar_jsonl(todos, "gobierno.jsonl")
    print(f"\nTotal registros: {len(todos)}")
    print("\n📌 RECORDATORIO: completar FICHAS_MANUALES con información real de cada programa")
