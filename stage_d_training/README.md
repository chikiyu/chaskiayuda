# Stage D — Entrenamiento

**Entrada:** datasets SFT y DPO en HuggingFace Hub
**Salida:** modelo fine-tuned en HuggingFace Hub
**Entorno:** Google Colab Pro o créditos GPU del hackathon (A10G / A100)
**Responsable:** 1 persona (perfil ML)

## Scripts

| Script | Qué hace |
|---|---|
| `train_sft.py` | Fine-tuning SFT con QLoRA sobre Qwen2.5-7B-Instruct |
| `train_dpo.py` | DPO sobre el modelo SFT |
| `evaluate.py` | Comparativa base vs SFT vs DPO |

## Orden de ejecución

```bash
# 1. Verificar que el entorno funciona (ANTES de que lleguen los datos)
python stage_d_training/train_sft.py --test

# 2. SFT (cuando Stage B tenga datos)
python stage_d_training/train_sft.py

# 3. DPO (cuando Stage C tenga datos)
python stage_d_training/train_dpo.py

# 4. Evaluación
python stage_d_training/evaluate.py
```

## Requisitos de entorno

```
GPU: mínimo 16GB VRAM (A10G preferido)
RAM: 32GB
Disco: 50GB libres
Python: 3.10+
```

## Checkpoints

Los checkpoints se guardan automáticamente en `./outputs/`.
Si Colab se cae, reanudar desde el último checkpoint:
```python
trainer.train(resume_from_checkpoint=True)
```
