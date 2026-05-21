"""
Funciones compartidas para formateo y limpieza de datos.
Usadas por todos los stages.
"""

import re
import json
from pathlib import Path


def limpiar_texto(texto: str) -> str:
    """Elimina HTML, normaliza espacios."""
    texto = re.sub(r"<[^>]+>", " ", texto)
    texto = re.sub(r"\s+", " ", texto)
    return texto.strip()


def cargar_jsonl(ruta: str) -> list:
    """Carga un archivo JSONL como lista de dicts."""
    registros = []
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if linea:
                registros.append(json.loads(linea))
    return registros


def guardar_jsonl(registros: list, ruta: str):
    """Guarda una lista de dicts como JSONL."""
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8") as f:
        for r in registros:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"Guardado: {ruta} ({len(registros)} registros)")


def contar_tokens_aprox(texto: str) -> int:
    """Estimación rápida de tokens (1 token ≈ 4 caracteres en español)."""
    return len(texto) // 4


def truncar_texto(texto: str, max_tokens: int = 1500) -> str:
    """Trunca el texto para no superar el límite de tokens del LLM."""
    max_chars = max_tokens * 4
    if len(texto) <= max_chars:
        return texto
    return texto[:max_chars] + "..."


TIPOS_CRISIS = {
    "inundacion":         ["inundación", "inundaciones", "desborde", "lluvias intensas", "El Niño", "huaico"],
    "terremoto":          ["sismo", "terremoto", "movimiento sísmico", "réplica", "epicentro"],
    "deslizamiento":      ["deslizamiento", "huayco", "derrumbe", "alud", "lahar"],
    "sequia_helada":      ["sequía", "déficit hídrico", "helada", "friaje", "nevada"],
    "epidemia":           ["brote", "epidemia", "pandemia", "dengue", "COVID", "cólera"],
    "incendio":           ["incendio", "quema", "fuego"],
    "general":            ["emergencia", "desastre", "crisis", "damnificado", "afectado"],
}


def clasificar_tipo_crisis(texto: str) -> str:
    texto_lower = texto.lower()
    for tipo, keywords in TIPOS_CRISIS.items():
        if any(kw.lower() in texto_lower for kw in keywords):
            return tipo
    return "general"
