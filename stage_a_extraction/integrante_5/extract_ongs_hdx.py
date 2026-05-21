"""
Integrante 5 — Extracción ONGs + HDX + CENEPRED
=================================================
Scraping de Cruz Roja, Cáritas, WFP y consulta API HDX.
Output: data/raw/ongs_hdx/

Uso:
    python extract_ongs_hdx.py
    python extract_ongs_hdx.py --solo hdx
    python extract_ongs_hdx.py --solo ongs
"""

import json
import requests
import re
import argparse
from datetime import date
from pathlib import Path

try:
    from bs4 import BeautifulSoup
    BS4_OK = True
except ImportError:
    BS4_OK = False
    print("AVISO: pip install beautifulsoup4")

OUTPUT_DIR = Path(__file__).parents[2] / "data" / "raw" / "ongs_hdx"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ChasquiAyuda-Research/1.0)"}

FUENTES_ONGS = [
    {
        "id": "cruzroja-pe-home",
        "nombre": "Cruz Roja Peruana",
        "url": "https://www.cruzroja.org.pe",
        "org": "Cruz Roja Peruana",
    },
    {
        "id": "caritas-pe-home",
        "nombre": "Cáritas Perú",
        "url": "https://www.caritasperu.org.pe",
        "org": "Cáritas Perú",
    },
    {
        "id": "wfp-peru",
        "nombre": "WFP Perú",
        "url": "https://www.wfp.org/countries/peru",
        "org": "World Food Programme",
    },
    {
        "id": "care-peru",
        "nombre": "CARE Perú",
        "url": "https://www.care.org.pe",
        "org": "CARE",
    },
]


def scrapear_ong(fuente):
    if not BS4_OK:
        return None
    try:
        r = requests.get(fuente["url"], headers=HEADERS, timeout=15)
        if r.status_code != 200:
            print(f"  HTTP {r.status_code}")
            return None

        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["nav", "footer", "script", "style", "header", "aside"]):
            tag.decompose()

        texto = re.sub(r"\s+", " ", soup.get_text(separator=" ")).strip()
        if len(texto) < 300:
            return None

        return {
            "id": fuente["id"],
            "fuente": "ong_web",
            "org": fuente["org"],
            "url_fuente": fuente["url"],
            "tipo_crisis": "general",
            "region": "nacional",
            "fecha_extraccion": str(date.today()),
            "licencia": "sitio_publico",
            "texto": texto[:4000],
        }
    except Exception as e:
        print(f"  Error: {e}")
        return None


def buscar_hdx_peru():
    """Busca datasets de Perú en HDX y devuelve los que tienen CSV."""
    print("\nBuscando datasets en HDX...")
    url = "https://data.humdata.org/api/3/action/package_search"
    params = {
        "q": "Peru emergency disaster humanitarian response",
        "rows": 20,
        "sort": "score desc, metadata_modified desc",
    }

    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            print(f"  HDX HTTP {r.status_code}")
            return []

        datasets = r.json().get("result", {}).get("results", [])
        resultados = []

        for ds in datasets:
            nombre = ds.get("title", "")
            modificado = ds.get("metadata_modified", "")[:10]
            recursos = ds.get("resources", [])

            csvs = [res for res in recursos if res.get("format", "").upper() == "CSV"]
            if not csvs:
                continue

            for csv_res in csvs[:2]:  # máximo 2 CSVs por dataset
                url_csv = csv_res.get("url", "")
                # Verificar si el CSV es accesible
                try:
                    check = requests.head(url_csv, headers=HEADERS,
                                          timeout=8, allow_redirects=True)
                    accesible = check.status_code == 200
                except Exception:
                    accesible = False

                resultados.append({
                    "id": f"hdx-{ds.get('id', '')[:8]}",
                    "fuente": "hdx",
                    "titulo": nombre,
                    "url_csv": url_csv,
                    "accesible": accesible,
                    "fecha_modificacion": modificado,
                    "fecha_extraccion": str(date.today()),
                    "licencia": ds.get("license_title", ""),
                    "nota": "Descargar CSV y revisar columnas con texto descriptivo",
                })

                estado = "✅" if accesible else "⚠️ "
                print(f"  {estado} {nombre[:50]} | {modificado}")

        return resultados

    except Exception as e:
        print(f"  Error HDX: {e}")
        return []


def guardar_jsonl(registros, nombre):
    ruta = OUTPUT_DIR / nombre
    with open(ruta, "w", encoding="utf-8") as f:
        for r in registros:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Guardado: {ruta} ({len(registros)} registros)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--solo", choices=["ongs", "hdx", "ambos"], default="ambos")
    args = parser.parse_args()

    todos_ongs = []
    todos_hdx = []

    if args.solo in ("ongs", "ambos"):
        print("=== Scraping ONGs ===")
        for fuente in FUENTES_ONGS:
            print(f"  {fuente['nombre']}...")
            resultado = scrapear_ong(fuente)
            if resultado:
                todos_ongs.append(resultado)
                print(f"  ✅ {len(resultado['texto'])} chars")
            else:
                print(f"  ⚠️  Sin resultado")
        if todos_ongs:
            guardar_jsonl(todos_ongs, "ongs.jsonl")

    if args.solo in ("hdx", "ambos"):
        print("\n=== HDX Datasets ===")
        todos_hdx = buscar_hdx_peru()
        if todos_hdx:
            guardar_jsonl(todos_hdx, "hdx_datasets.jsonl")
            accesibles = sum(1 for d in todos_hdx if d.get("accesible"))
            print(f"\nCSVs encontrados: {len(todos_hdx)} | Accesibles: {accesibles}")

    print(f"\nTotal ONGs: {len(todos_ongs)} | HDX: {len(todos_hdx)}")
