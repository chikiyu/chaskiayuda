# Stage B — Dataset SFT

**Entrada:** `data/raw/` (output de todos los integrantes de Stage A)
**Salida:** `data/sft/sft_dataset.jsonl` + subido a HuggingFace
**Meta:** 2,000–3,000 pares instrucción→respuesta de calidad

## Proceso

```
1. generate_sft_pairs.py   → LLM genera pares desde los textos crudos
2. Revisión en Google Sheets (filtrar calidad 1/2/3)
3. upload_to_hf.py         → subir dataset limpio a HuggingFace
```

## Criterios de calidad para la revisión

- **3 — Incluir:** respuesta da pasos concretos + recursos peruanos reales
- **2 — Editar:** información correcta pero vaga o muy corta → mejorar y incluir
- **1 — Descartar:** burocrático, incorrecto, no aplica a Perú

## Cómo correr

```bash
# Necesita ANTHROPIC_API_KEY en .env
python stage_b_sft/generate_sft_pairs.py

# Subir a HuggingFace (necesita HF_TOKEN en .env)
python stage_b_sft/upload_to_hf.py
```
