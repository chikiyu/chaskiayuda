# Stage B — Dataset SFT

**Entrada:** archivos `.jsonl` de todos los integrantes de Stage A  
**Salida:** dataset de pares instrucción→respuesta subido a HuggingFace  
**Meta:** 2,000–3,000 pares de calidad  
**Responsables:** Emilio + Raven99 (+ apoyo de Maskuyruru)

## Qué hay que hacer

1. Tomar los textos crudos de Stage A
2. Usar un LLM (Claude API o GPT-4o-mini) para generar 3 pares por texto
3. Revisar y filtrar en Google Sheets (calidad 1/2/3)
4. Subir el dataset limpio a HuggingFace Hub

## Formato del dataset final

```json
{
  "messages": [
    {"role": "user",       "content": "Hubo inundaciones en Piura, ¿qué ayuda hay?"},
    {"role": "assistant",  "content": "Hay varias opciones: (1) INDECI línea 115..."}
  ]
}
```

## Script de generación

Pendiente — se agrega aquí cuando Stage A esté completo.  
Ver `pipeline-completo.md` para el prompt de generación.

## Criterios de revisión en Google Sheets

| Calidad | Criterio | Acción |
|---|---|---|
| 3 — Bueno | Da pasos concretos + recursos peruanos reales | Incluir |
| 2 — Mejorable | Correcto pero vago o corto | Editar y incluir |
| 1 — Descartar | Burocrático, incorrecto, no aplica a Perú | Eliminar |
