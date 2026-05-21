"""
Stage C — Generación de pares DPO (chosen / rejected)
======================================================
Usa el Sphere Handbook como fuente del "chosen".
Output: data/dpo/dpo_dataset.jsonl

Uso:
    python generate_dpo_pairs.py
"""

import json
import time
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

try:
    import anthropic
    LLM = "anthropic"
except ImportError:
    import openai
    LLM = "openai"

RAW_DIR = Path(__file__).parent.parent / "data" / "raw"
DPO_DIR = Path(__file__).parent.parent / "data" / "dpo"
DPO_DIR.mkdir(parents=True, exist_ok=True)

PROMPT_DPO = """Eres un experto en estándares humanitarios del Sphere Handbook.

A partir del texto, genera UN par DPO para entrenar un modelo a dar mejores respuestas humanitarias.

REGLAS:
- prompt: pregunta realista de alguien en crisis en Perú
- chosen: respuesta que cumple estándares Sphere — accionable, empática, con recursos reales peruanos
  * Da pasos concretos y numerados
  * Menciona organizaciones reales: INDECI 115, Cruz Roja, MIDIS, MINSA
  * Reconoce la situación antes de informar
  * Hace una pregunta de seguimiento para precisar la ayuda
- rejected: respuesta que un sistema burocrático daría — inútil en una emergencia real
  * Vaga, sin pasos concretos
  * Solo dice "contacte a las autoridades"
  * No menciona recursos específicos

El contraste debe ser CLARO pero el rejected debe parecer algo real (no absurdo).

Formato JSON puro:
{
  "prompt": "...",
  "chosen": "...",
  "rejected": "..."
}

Texto Sphere:
{texto}"""


def generar_par_dpo(texto):
    try:
        if LLM == "anthropic":
            client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            r = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1024,
                messages=[{"role": "user", "content": PROMPT_DPO.format(texto=texto[:2000])}]
            )
            return json.loads(r.content[0].text.strip())
        else:
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            r = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": PROMPT_DPO.format(texto=texto[:2000])}],
                max_tokens=1024,
            )
            return json.loads(r.choices[0].message.content.strip())
    except Exception as e:
        print(f"  Error: {e}")
        return None


def procesar_sphere(limite=800):
    sphere_path = list((RAW_DIR / "sphere").glob("*.jsonl"))
    if not sphere_path:
        print("ERROR: No se encontró sphere_chunks.jsonl — correr Stage A Integrante 3 primero")
        return []

    chunks = []
    with open(sphere_path[0], encoding="utf-8") as f:
        for linea in f:
            if linea.strip():
                chunks.append(json.loads(linea))

    chunks = chunks[:limite]
    print(f"Procesando {len(chunks)} chunks del Sphere Handbook...")

    pares = []
    for i, chunk in enumerate(chunks):
        texto = chunk.get("texto", "")
        if len(texto) < 150:
            continue

        par = generar_par_dpo(texto)
        if not par:
            continue

        pares.append({
            "prompt":   par["prompt"],
            "chosen":   par["chosen"],
            "rejected": par["rejected"],
            "fuente_id": chunk.get("id", ""),
            "categoria": chunk.get("categoria", "general"),
            "revisado": False,  # cambiar a True después de revisión humana
        })

        if (i + 1) % 10 == 0:
            print(f"  Progreso: {i+1}/{len(chunks)} | Pares DPO: {len(pares)}")

        time.sleep(0.3)

    return pares


def guardar_dpo(pares):
    ruta = DPO_DIR / "dpo_dataset.jsonl"
    with open(ruta, "w", encoding="utf-8") as f:
        for p in pares:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    print(f"Guardado: {ruta} ({len(pares)} pares DPO)")
    print("\n⚠️  IMPORTANTE: revisar TODOS los pares manualmente antes de entrenar")
    print("   Verificar que 'chosen' es claramente mejor que 'rejected'")
    print("   Cambiar 'revisado': true en los pares aprobados")


if __name__ == "__main__":
    if not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        print("ERROR: Configura ANTHROPIC_API_KEY en .env")
        exit(1)

    pares = procesar_sphere(limite=800)
    if pares:
        guardar_dpo(pares)
    print(f"\nTotal pares DPO generados: {len(pares)}")
