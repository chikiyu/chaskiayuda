# ChasquiAyuda 🏔️
### Asistente humanitario post-entrenado para Perú

Post-entrenamiento de Qwen2.5-7B-Instruct con DPO + QLoRA para respuesta
a emergencias y desastres naturales en español, adaptado al contexto peruano.

**SomosNLP Hackathon 2026** · ODS 11 · ODS 13

---

## El problema

Cuando ocurre un desastre en Perú, las personas afectadas no saben a qué
ayuda tienen derecho ni cómo acceder a ella. Los modelos genéricos responden
con lenguaje burocrático sin recursos concretos.

**ChasquiAyuda** responde con empatía, pasos accionables y recursos reales:
INDECI (115), Cruz Roja Peruana, SAMU (106), MIDIS, Línea 100.

## Ejemplo

**Entrada:** *"Hubo inundaciones en Piura, perdimos todo. ¿Qué hacemos?"*

**ChasquiAyuda:** *"Entendemos que están viviendo una situación muy difícil.
Hay varias rutas simultáneas: (1) INDECI línea 115 — gratuita 24h, te
informan de puntos de distribución activos. (2) Cruz Roja Peruana
(01-266-6978) — busca sus carpas de registro los primeros días.
(3) MIDIS — Programa Contigo se activa automáticamente en emergencias
declaradas, el registro es siempre gratuito..."*

---

## Resultados

| Métrica | Modelo base | ChasquiAyuda DPO |
|---------|-------------|------------------|
| Reward Accuracy | 50.0% | **96.8%** |
| Mean Reward Margin | — | 0.4212 |
| Entrenamiento | — | 1 época · T4 · 2h 42min |

## Dataset

620 pares DPO construidos desde 8 fuentes:

| Fuente | Pares |
|--------|-------|
| Sphere Handbook 2018 | 180 |
| INDECI (manuales oficiales) | 140 |
| Programas gobierno peruano | 110 |
| ReliefWeb / OCHA | 90 |
| ONGs (Cruz Roja, Cáritas, CARE) | 40 |
| Fenómeno El Niño 2026 | 42 |
| HDX / IDMC | 30 |
| CHS 2024 | 30 |

## Estructura del repositorio

```
chaskiayuda/
├── data                        # Dataset y  dataCARD
├── notebooks                   # Notebook de postentrenamiento
├── model                       # Modelo postentrenado 
└── demo                        # Demo Gradio (HF Space) y Colab demo
 
```

## Uso

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
import torch

bnb = BitsAndBytesConfig(load_in_4bit=True,
                          bnb_4bit_compute_dtype=torch.bfloat16)
base = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-7B-Instruct",
                                             quantization_config=bnb,
                                             device_map="auto")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-7B-Instruct")
model = PeftModel.from_pretrained(base,
                                   "somosnlp-hackathon-2026/chaskiayuda-model")
```

## Recursos

- 📊 **Dataset:** [somosnlp-hackathon-2026/chaskiayuda-dataset-dpo](https://huggingface.co/datasets/somosnlp-hackathon-2026/chaskiayuda-dataset-dpo)
- 🤖 **Modelo:** [somosnlp-hackathon-2026/chaskiayuda-model](https://huggingface.co/somosnlp-hackathon-2026/chaskiayuda-model)
- 🚀 **Demo:** [somosnlp-hackathon-2026/chaskiayuda](https://huggingface.co/spaces/somosnlp-hackathon-2026/chaskiayuda)

## Licencias

- Modelo: Apache 2.0 (hereda de Qwen2.5)
- Dataset: CC-BY-4.0 (fuentes Sphere, OCHA, INDECI)