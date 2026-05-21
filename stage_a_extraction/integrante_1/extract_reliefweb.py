"""
Integrante 1 — Extracción ReliefWeb API
========================================
Descarga reportes humanitarios sobre Perú en español.
Output: data/raw/reliefweb/reliefweb.jsonl

Uso:
    python extract_reliefweb.py
    python extract_reliefweb.py --limite 500 --desde 2020-01-01
"""

import requests
import json
import time
import argparse
from datetime import date
from pathlib import Path

OUTPUT_DIR = Path(__file__).parents[2] / "data" / "raw" / "reliefweb"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

APPNAME = "chasquiayuda-somosnlp-2026"

TEMAS_CRISIS = {
    "Floods":           "inundacion",
    "Earthquake":       "terremoto",
    "Landslide":        "deslizamiento",
    "Drought":          "sequia",
    "Epidemic":         "epidemia",
    "Food Insecurity":  "inseguridad_alimentaria",
    "Shelter":          "albergue",
    "Health":           "salud",
}


def clasificar_crisis(temas_lista):
    for tema in temas_lista:
        nombre = tema.get("name", "")
        for key, valor in TEMAS_CRISIS.items():
            if key.lower() in nombre.lower():
                return valor
    return "general"


def limpiar_texto(texto):
    import re
    texto = re.sub(r"<[^>]+>", " ", texto)   # eliminar HTML
    texto = re.sub(r"\s+", " ", texto)         # normalizar espacios
    return texto.strip()


def extraer_reliefweb(limite=1000, desde="2015-01-01"):
    print(f"Iniciando extracción ReliefWeb — meta: {limite} reportes desde {desde}")

    url = "https://api.reliefweb.int/v2/reports"
    params = {"appname": APPNAME}
    todos = []
    offset = 0
    batch = 50

    while len(todos) < limite:
        payload = {
            "filter": {
                "operator": "AND",
                "conditions": [
                    {"field": "country.iso3",  "value": "PER"},
                    {"field": "language.code", "value": "spa"},
                    {"field": "date.created",  "from": desde},
                ],
            },
            "fields": {
                "include": ["title", "date", "source", "body", "theme", "url"]
            },
            "limit": batch,
            "offset": offset,
            "sort": ["date:desc"],
        }

        r = requests.post(url, params=params, json=payload, timeout=15)

        if r.status_code != 200:
            print(f"  Error {r.status_code} en offset {offset}: {r.text[:200]}")
            break

        data = r.json()
        items = data.get("data", [])
        total_api = data.get("totalCount", 0)

        if not items:
            print(f"  Sin más resultados. Total en API: {total_api}")
            break

        nuevos = 0
        for item in items:
            f = item.get("fields", {})
            body = f.get("body", "")
            if not body or len(body) < 200:
                continue

            registro = {
                "id": f"rw-{item['id']}",
                "fuente": "reliefweb",
                "org": f.get("source", [{}])[0].get("name", "") if f.get("source") else "",
                "fecha": f.get("date", {}).get("created", "")[:10],
                "fecha_extraccion": str(date.today()),
                "tipo_crisis": clasificar_crisis(f.get("theme", [])),
                "region": "Peru",
                "titulo": f.get("title", ""),
                "texto": limpiar_texto(body),
                "url_fuente": f.get("url", ""),
                "licencia": "cc_by",
            }
            todos.append(registro)
            nuevos += 1

        print(f"  Offset {offset}: +{nuevos} registros válidos | Total: {len(todos)}/{limite}")
        offset += batch
        time.sleep(0.5)

        if offset >= total_api:
            break

    return todos


def guardar_jsonl(registros, nombre_archivo):
    ruta = OUTPUT_DIR / nombre_archivo
    with open(ruta, "w", encoding="utf-8") as f:
        for r in registros:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"\nGuardado: {ruta} ({len(registros)} registros)")
    return ruta


def reporte_distribucion(registros):
    from collections import Counter
    tipos = Counter(r["tipo_crisis"] for r in registros)
    print("\n--- Distribución por tipo de crisis ---")
    for tipo, n in tipos.most_common():
        barra = "█" * (n * 30 // max(tipos.values()))
        print(f"  {tipo:<25} {n:>4}  {barra}")
    print(f"\nTotal registros: {len(registros)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--limite", type=int, default=1000)
    parser.add_argument("--desde", type=str, default="2015-01-01")
    args = parser.parse_args()

    registros = extraer_reliefweb(limite=args.limite, desde=args.desde)
    guardar_jsonl(registros, "reliefweb.jsonl")
    reporte_distribucion(registros)
