"""
Stage B — Generación de pares SFT con LLM
==========================================
Lee los textos crudos de Stage A y genera pares instrucción→respuesta
usando Claude Haiku (barato: ~$2 para todo el proyecto).

Uso:
    python generate_sft_pairs.py
    python generate_sft_pairs.py --fuente reliefweb --limite 200
"""

import json
import time
import argparse
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

try:
    import anthropic
    LLM = "anthropic"
except ImportError:
    try:
        import openai
        LLM = "openai"
    except ImportError:
        print("ERROR: pip install anthropic  (o pip install openai)")
        exit(1)

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
SFT_DIR = Path(__file__).parent.parent / "data" / "sft"
SFT_DIR.mkdir(parents=True, exist_ok=True)

PROMPT_GENERACION = """Eres un experto en respuesta humanitaria para Perú.

A partir del texto fuente, genera EXACTAMENTE 3 pares pregunta-respuesta.

REGLAS:
- Las preguntas deben sonar como alguien afectado por un desastre en Perú (primera persona, lenguaje coloquial)
- Las respuestas deben ser ACCIONABLES: pasos concretos, números de teléfono reales, organizaciones peruanas
- Mencionar cuando aplique: INDECI 115, Cruz Roja Perú, MIDIS, MINSA, Línea 100
- Tono: empático, claro, directo — sin burocracia
- Si el texto no permite generar preguntas relevantes sobre crisis en Perú, responde solo: SKIP

Formato de salida (JSON puro, sin markdown):
[
  {"pregunta": "...", "respuesta": "..."},
  {"pregunta": "...", "respuesta": "..."},
  {"pregunta": "...", "respuesta": "..."}
]

Texto fuente:
{texto}"""


def generar_con_anthropic(texto):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    r = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": PROMPT_GENERACION.format(texto=texto)}]
    )
    respuesta = r.content[0].text.strip()
    if respuesta == "SKIP":
        return None
    return json.loads(respuesta)


def generar_con_openai(texto):
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": PROMPT_GENERACION.format(texto=texto)}],
        max_tokens=1024,
    )
    respuesta = r.choices[0].message.content.strip()
    if respuesta == "SKIP":
        return None
    return json.loads(respuesta)


def generar_pares(texto):
    try:
        if LLM == "anthropic":
            return generar_con_anthropic(texto[:2000])
        else:
            return generar_con_openai(texto[:2000])
    except json.JSONDecodeError:
        return None
    except Exception as e:
        print(f"    Error LLM: {e}")
        return None


def procesar_fuente(nombre_jsonl, limite=None):
    ruta = RAW_DIR / nombre_jsonl
    if not ruta.exists():
        # Buscar en subdirectorios
        encontrados = list(RAW_DIR.rglob(nombre_jsonl))
        if not encontrados:
            print(f"  No encontrado: {nombre_jsonl}")
            return []
        ruta = encontrados[0]

    registros_raw = []
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                registros_raw.append(json.loads(linea))

    if limite:
        registros_raw = registros_raw[:limite]

    pares_generados = []
    print(f"  Procesando {len(registros_raw)} textos de {nombre_jsonl}...")

    for i, registro in enumerate(registros_raw):
        texto = registro.get("texto", "")
        if not texto or len(texto) < 200:
            continue

        pares = generar_pares(texto)
        if not pares:
            continue

        for par in pares:
            pares_generados.append({
                "messages": [
                    {"role": "user",      "content": par["pregunta"]},
                    {"role": "assistant", "content": par["respuesta"]},
                ],
                "fuente_id": registro.get("id", ""),
                "fuente_nombre": registro.get("fuente", ""),
                "tipo_crisis": registro.get("tipo_crisis", "general"),
                "calidad": None,  # se llena en la revisión humana
            })

        if (i + 1) % 10 == 0:
            print(f"    Progreso: {i+1}/{len(registros_raw)} | Pares: {len(pares_generados)}")

        time.sleep(0.3)  # rate limit

    return pares_generados


def guardar_para_revision(pares, nombre):
    """Guarda en formato que facilita la revisión en Google Sheets."""
    ruta_jsonl = SFT_DIR / f"{nombre}.jsonl"
    ruta_tsv   = SFT_DIR / f"{nombre}_revision.tsv"

    with open(ruta_jsonl, "w", encoding="utf-8") as f:
        for p in pares:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")

    # TSV para copiar a Google Sheets
    with open(ruta_tsv, "w", encoding="utf-8") as f:
        f.write("pregunta\trespuesta\ttipo_crisis\tfuente\tcalidad(1-3)\tcomentario\n")
        for p in pares:
            pregunta  = p["messages"][0]["content"].replace("\t", " ").replace("\n", " ")
            respuesta = p["messages"][1]["content"].replace("\t", " ").replace("\n", " ")
            f.write(f"{pregunta}\t{respuesta}\t{p['tipo_crisis']}\t{p['fuente_nombre']}\t\t\n")

    print(f"Guardado: {ruta_jsonl} ({len(pares)} pares)")
    print(f"TSV para revisión: {ruta_tsv}")
    print("→ Abrir el TSV en Google Sheets y revisar columna 'calidad(1-3)'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fuente", default="reliefweb",
                        help="Nombre del archivo JSONL en data/raw/ (sin extensión)")
    parser.add_argument("--limite", type=int, default=None,
                        help="Máximo número de textos a procesar")
    args = parser.parse_args()

    if not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        print("ERROR: Configura ANTHROPIC_API_KEY u OPENAI_API_KEY en el archivo .env")
        exit(1)

    print(f"Generando pares SFT desde: {args.fuente}")
    print(f"LLM: {LLM}")

    pares = procesar_fuente(f"{args.fuente}.jsonl", limite=args.limite)
    if pares:
        guardar_para_revision(pares, f"sft_{args.fuente}")
    print(f"\nTotal pares generados: {len(pares)}")
