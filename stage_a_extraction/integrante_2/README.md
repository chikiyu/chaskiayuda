# Integrante 2 — INDECI

**Fuente:** Instituto Nacional de Defensa Civil + datosabiertos.gob.pe
**Método:** Descarga manual de PDFs + extracción con pdfplumber + API CKAN
**Output:** `data/raw/indeci/`
**Meta:** 10–20 documentos procesados + datos CSV de emergencias

## PDFs a descargar (manualmente)

Ir a cada URL, descargar el PDF, y copiarlo a `data/raw/indeci/pdfs/`:

| Archivo a guardar como | URL | Verificar texto extraíble |
|---|---|---|
| `manual_edan.pdf` | https://www.indeci.gob.pe (buscar "Manual EDAN") | ✅ / ❌ |
| `plan_nacional_grd.pdf` | https://www.indeci.gob.pe (buscar "Plan Nacional GRD") | ✅ / ❌ |
| `guia_albergues.pdf` | https://www.indeci.gob.pe (buscar "Guía albergues") | ✅ / ❌ |
| `protocolo_evacuacion.pdf` | https://www.indeci.gob.pe (buscar "evacuación") | ✅ / ❌ |

**Verificar si el texto es extraíble:**
1. Abrir el PDF
2. Ctrl+A → Ctrl+C en cualquier página con texto
3. Pegar en un editor: si aparece texto legible → ✅ extraíble

Si el PDF está escaneado (❌): anotar en la tabla y pasar al siguiente.

## Datos abiertos (automatizado)

```bash
python stage_a_extraction/integrante_2/extract_indeci.py
```

## Output esperado

```
data/raw/indeci/
├── pdfs/               ← PDFs descargados (en .gitignore)
├── indeci_pdfs.jsonl   ← texto extraído de los PDFs
└── indeci_csv.jsonl    ← datos de la API de datos abiertos
```

## Checklist

- [ ] Al menos 5 PDFs descargados y verificados como extraíbles
- [ ] Script de extracción PDF corrido sin errores
- [ ] Datos CSV de la API descargados
- [ ] Reportar cuántos PDFs estaban escaneados (no extraíbles)
