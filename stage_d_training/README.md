# Stage D — Entrenamiento

**Entrada:** datasets SFT y DPO en HuggingFace  
**Salida:** modelo fine-tuned en HuggingFace Hub  
**Responsable:** @ayayon  
**Entorno:** Google Colab Pro o créditos GPU del hackathon

## Scripts

Se agregan aquí cuando los datasets estén listos (día 4-5).

## Orden de ejecución

```
1. Verificar entorno GPU (día 1-2)
   → Cargar Qwen2.5-7B-Instruct en 4-bit y hacer una inferencia de prueba

2. SFT Training (día 4-5, cuando Stage B tenga datos)
   → QLoRA sobre Qwen2.5-7B-Instruct
   → Subir modelo SFT a HuggingFace

3. DPO Training (día 6, cuando Stage C tenga datos)
   → DPO sobre el modelo SFT
   → Subir modelo final a HuggingFace

4. Evaluación (día 7)
   → Comparar base vs SFT vs DPO con 3 preguntas de prueba
   → Generar tabla para el paper
```

## Modelo base

**Qwen2.5-7B-Instruct** — mejor español entre open-source de 7B  
https://huggingface.co/Qwen/Qwen2.5-7B-Instruct
