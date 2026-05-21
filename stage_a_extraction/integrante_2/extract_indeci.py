"""
Integrante 2 — Extracción INDECI
==================================
Extrae texto de PDFs de INDECI y datos del portal de datos abiertos.
Output: data/raw/indeci/

Uso:
    python extract_indeci.py --modo pdf      # solo PDFs
    python extract_indeci.py --modo api      # solo API datos abiertos
    python extract_indeci.py --modo ambos    # ambos (default)
"""

import json
import requests
import argparse
from datetime import date
from pathlib import Path

try:
    import pdfplumber
    PDF_DISPONIBLE = True
except ImportError:
    PDF_DISPONIBLE = False
    print("AVISO: pdfplumber no instalado. Instalar con: pip install pdfplumber")

OUTPUT_DIR = Path(__file__).parents[2] / "data" / "raw" / "indeci"
PDF_DIR = OUTPUT_DIR / "pdfs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PDF_DIR.mkdir(exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ChasquiAyuda/1.0)"}


def extraer_pdf(ruta_pdf):
    """Extrae texto de un PDF de INDECI por páginas."""
    if not PDF_DISPONIBLE:
        print("  ❌ pdfplumber no disponible")
        return []

    nombre = ruta_pdf.stem
    chunks = []

    try:
        with pdfplumber.open(ruta_pdf) as pdf:
            total_paginas = len(pdf.pages)
            paginas_utiles = 0

            for i, pagina in enumerate(pdf.pages):
                texto = pagina.extract_text()
                if not texto or len(texto.strip()) < 150:
                    continue

                chunks.append({
                    "id": f"indeci-{nombre}-p{i+1}",
                    "fuente": "indeci_pdf",
                    "documento": nombre,
                    "pagina": i + 1,
                    "total_paginas": total_paginas,
                    "fecha_extraccion": str(date.today()),
                    "tipo_crisis": "general",
                    "region": "nacional",
                    "texto": texto.strip(),
                    "licencia": "dominio_publico_peru",
                })
                paginas_utiles += 1

        print(f"  {nombre}: {paginas_utiles}/{total_paginas} páginas con texto extraído")
    except Exception as e:
        print(f"  Error en {ruta_pdf.name}: {e}")

    return chunks


def extraer_todos_pdfs():
    """Procesa todos los PDFs en la carpeta pdfs/."""
    pdfs = list(PDF_DIR.glob("*.pdf")) + list(PDF_DIR.glob("*.PDF"))

    if not pdfs:
        print(f"No se encontraron PDFs en {PDF_DIR}")
        print("Descargar PDFs manualmente y colocarlos en esa carpeta (ver README.md)")
        return []

    todos = []
    for pdf_path in pdfs:
        print(f"Procesando: {pdf_path.name}")
        chunks = extraer_pdf(pdf_path)
        todos.extend(chunks)

    return todos


def extraer_datos_abiertos():
    """Consulta la API de datosabiertos.gob.pe para datasets de INDECI."""
    print("\nConsultando API datos abiertos del gobierno...")

    url = "https://www.datosabiertos.gob.pe/api/3/action/package_search"
    terminos = ["emergencias INDECI", "desastres", "inundaciones Peru"]
    todos = []

    for termino in terminos:
        try:
            r = requests.get(
                url,
                params={"q": termino, "rows": 10},
                headers=HEADERS,
                timeout=15
            )
            if r.status_code != 200:
                print(f"  HTTP {r.status_code} para '{termino}'")
                continue

            datasets = r.json().get("result", {}).get("results", [])
            for ds in datasets:
                titulo = ds.get("title", "")
                recursos = ds.get("resources", [])

                for res in recursos:
                    if res.get("format", "").upper() in ("CSV", "XLSX"):
                        todos.append({
                            "id": f"indeci-ckan-{ds.get('id', '')[:8]}",
                            "fuente": "indeci_datos_abiertos",
                            "titulo_dataset": titulo,
                            "url_descarga": res.get("url", ""),
                            "formato": res.get("format", ""),
                            "fecha_extraccion": str(date.today()),
                            "licencia": "dominio_publico_peru",
                            "nota": "Descargar CSV y revisar columnas con texto descriptivo",
                        })

            print(f"  '{termino}': {len(datasets)} datasets encontrados")
        except Exception as e:
            print(f"  Error en '{termino}': {e}")

    return todos


def guardar_jsonl(registros, nombre):
    ruta = OUTPUT_DIR / nombre
    with open(ruta, "w", encoding="utf-8") as f:
        for r in registros:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Guardado: {ruta} ({len(registros)} registros)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--modo", choices=["pdf", "api", "ambos"], default="ambos")
    args = parser.parse_args()

    if args.modo in ("pdf", "ambos"):
        print("=== Extracción PDFs INDECI ===")
        chunks_pdf = extraer_todos_pdfs()
        if chunks_pdf:
            guardar_jsonl(chunks_pdf, "indeci_pdfs.jsonl")
        print(f"Total chunks PDF: {len(chunks_pdf)}")

    if args.modo in ("api", "ambos"):
        print("\n=== Datos abiertos INDECI ===")
        datasets = extraer_datos_abiertos()
        if datasets:
            guardar_jsonl(datasets, "indeci_datasets.jsonl")
        print(f"Total datasets encontrados: {len(datasets)}")
