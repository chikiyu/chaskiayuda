# Stage C — Dataset DPO

**Entrada:** `sphere_estandares_clave.md` del Integrante 3  
**Salida:** dataset de pares chosen/rejected subido a HuggingFace  
**Meta:** 600–800 pares revisados manualmente  
**Responsable:** Fran

## Qué hay que hacer

1. Usar el Sphere Handbook como fuente del "chosen" (qué es una buena respuesta)
2. Generar pares con LLM: prompt + chosen (respuesta correcta) + rejected (respuesta burocrática)
3. Revisar TODOS los pares manualmente — este paso no se puede saltar
4. Subir a HuggingFace Hub

## Formato del dataset final

```json
{
  "prompt":   "No tenemos agua desde las inundaciones. ¿Qué hacemos?",
  "chosen":   "El mínimo de supervivencia es 3 litros por persona por día. Opciones: (1) INDECI 115...",
  "rejected": "Debe comunicarse con las autoridades competentes de su localidad."
}
```

## La diferencia clave chosen vs rejected

| Dimensión | Chosen ✅ | Rejected ❌ |
|---|---|---|
| Accionabilidad | Pasos numerados y concretos | "Contacte a las autoridades" |
| Recursos | INDECI 115, Cruz Roja, MIDIS | "organismos competentes" |
| Tono | Empático, reconoce la situación | Frío y burocrático |
| Seguimiento | Hace pregunta para precisar ayuda | Termina la conversación |

## Script de generación

Pendiente — se agrega cuando Stage A Integrante 3 esté completo.
