# Stage C — Dataset DPO

**Entrada:** `data/raw/sphere/sphere_chunks.jsonl` (del Integrante 3)
**Salida:** `data/dpo/dpo_dataset.jsonl` + subido a HuggingFace
**Meta:** 600–800 pares chosen/rejected revisados manualmente

## Proceso

```
1. generate_dpo_pairs.py  → LLM genera pares desde Sphere Handbook
2. Revisión manual TODOS los pares (crítico — no saltar este paso)
3. upload_to_hf.py        → subir a HuggingFace
```

## Por qué la revisión es obligatoria aquí

En Stage B (SFT) la revisión puede ser rápida. En Stage C (DPO) el contraste
chosen/rejected debe ser **real y justificable** — si el modelo detecta que
el rejected es solo peor por razones triviales, no aprende nada útil.

Criterios de revisión:
- ¿El `chosen` da información que realmente ayuda a alguien en crisis?
- ¿El `rejected` es algo que un sistema real podría decir (no una respuesta absurda)?
- ¿El contraste es claro pero no exagerado?

## Cómo correr

```bash
python stage_c_dpo/generate_dpo_pairs.py
```
