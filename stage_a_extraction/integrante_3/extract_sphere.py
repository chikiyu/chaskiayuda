"""
Integrante 3 — Extracción Sphere Handbook
==========================================
Extrae texto del Sphere Handbook por capítulo y genera
un resumen de los estándares clave para el dataset DPO.
Output: data/raw/sphere/

Uso:
    python extract_sphere.py
    python extract_sphere.py --pdf ruta/al/sphere.pdf
"""

import json
import argparse
import re
from datetime import date
from pathlib import Path

try:
    import pdfplumber
except ImportError:
    print("ERROR: pip install pdfplumber")
    exit(1)

OUTPUT_DIR = Path(__file__).parents[2] / "data" / "raw" / "sphere"
PDF_DIR = OUTPUT_DIR / "pdfs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PDF_DIR.mkdir(exist_ok=True)

# Palabras clave para identificar capítulos en el índice
CAPITULOS_CLAVE = {
    "agua": "wash_agua_saneamiento",
    "saneamiento": "wash_agua_saneamiento",
    "wash": "wash_agua_saneamiento",
    "alimentari": "seguridad_alimentaria",
    "nutrici": "seguridad_alimentaria",
    "albergue": "albergue_asentamiento",
    "refugio": "albergue_asentamiento",
    "salud": "salud",
    "médic": "salud",
    "protecci": "proteccion_transversal",
    "género": "proteccion_transversal",
}

# Estándares clave para extraer manualmente como referencia DPO
ESTANDARES_CLAVE = [
    {
        "id": "sphere-wash-01",
        "capitulo": "Agua y Saneamiento",
        "estandar": "Cantidad mínima de agua",
        "valor": "15 litros por persona por día en situación de no emergencia aguda; 3 litros en supervivencia inmediata",
        "aplicacion_dpo": "Cuando alguien pregunta sobre agua en emergencia, la respuesta chosen debe mencionar estos números"
    },
    {
        "id": "sphere-wash-02",
        "capitulo": "Agua y Saneamiento",
        "estandar": "Distancia máxima a punto de agua",
        "valor": "500 metros como máximo desde el albergue al punto de distribución de agua",
        "aplicacion_dpo": "Si alguien dice que el punto de agua está lejos, el chosen debe mencionar este estándar"
    },
    {
        "id": "sphere-albergue-01",
        "capitulo": "Albergue",
        "estandar": "Espacio mínimo por persona",
        "valor": "3.5 m² por persona en albergue de emergencia",
        "aplicacion_dpo": "Respuesta chosen menciona el derecho a espacio mínimo en albergues"
    },
    {
        "id": "sphere-salud-01",
        "capitulo": "Salud",
        "estandar": "Atención de salud de emergencia",
        "valor": "Acceso a atención de salud esencial, sin discriminación, en las primeras 72 horas",
        "aplicacion_dpo": "El chosen menciona el derecho a atención inmediata sin pago en emergencias"
    },
    {
        "id": "sphere-alimentacion-01",
        "capitulo": "Seguridad Alimentaria",
        "estandar": "Calorías mínimas por persona",
        "valor": "2,100 kcal por persona por día como mínimo en emergencias",
        "aplicacion_dpo": "Cuando alguien pregunta sobre alimentación de emergencia"
    },
]


def clasificar_pagina(texto):
    texto_lower = texto.lower()
    for keyword, categoria in CAPITULOS_CLAVE.items():
        if keyword in texto_lower:
            return categoria
    return "general"


def extraer_sphere(ruta_pdf):
    print(f"Procesando: {ruta_pdf.name}")
    chunks = []

    with pdfplumber.open(ruta_pdf) as pdf:
        total = len(pdf.pages)
        utiles = 0

        for i, pagina in enumerate(pdf.pages):
            texto = pagina.extract_text()
            if not texto or len(texto.strip()) < 100:
                continue

            texto_limpio = re.sub(r"\s+", " ", texto).strip()
            categoria = clasificar_pagina(texto_limpio)

            chunks.append({
                "id": f"sphere-p{i+1}",
                "fuente": "sphere_handbook_2018",
                "pagina": i + 1,
                "total_paginas": total,
                "categoria": categoria,
                "fecha_extraccion": str(date.today()),
                "licencia": "cc_by",
                "region": "internacional",
                "tipo_uso": "dpo_chosen",
                "texto": texto_limpio,
            })
            utiles += 1

        print(f"  Páginas útiles: {utiles}/{total}")
    return chunks


def guardar_jsonl(registros, nombre):
    ruta = OUTPUT_DIR / nombre
    with open(ruta, "w", encoding="utf-8") as f:
        for r in registros:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Guardado: {ruta} ({len(registros)} chunks)")


def guardar_estandares_clave():
    """Guarda los estándares clave como referencia para el equipo de Stage C (DPO)."""
    ruta = OUTPUT_DIR / "sphere_estandares_clave.json"
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(ESTANDARES_CLAVE, f, ensure_ascii=False, indent=2)
    print(f"Guardado: {ruta} ({len(ESTANDARES_CLAVE)} estándares clave para DPO)")


def reporte_distribucion(chunks):
    from collections import Counter
    categorias = Counter(c["categoria"] for c in chunks)
    print("\n--- Distribución por categoría ---")
    for cat, n in categorias.most_common():
        print(f"  {cat:<30} {n:>4} páginas")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", type=str, default=None,
                        help="Ruta al PDF del Sphere Handbook")
    args = parser.parse_args()

    if args.pdf:
        pdf_path = Path(args.pdf)
    else:
        pdfs = list(PDF_DIR.glob("*.pdf")) + list(PDF_DIR.glob("*.PDF"))
        if not pdfs:
            print(f"No se encontró PDF en {PDF_DIR}")
            print("Descargar de https://spherestandards.org/handbook/ y colocar en esa carpeta")
            exit(1)
        pdf_path = pdfs[0]
        print(f"Usando: {pdf_path.name}")

    chunks = extraer_sphere(pdf_path)
    guardar_jsonl(chunks, "sphere_chunks.jsonl")
    guardar_estandares_clave()
    reporte_distribucion(chunks)
